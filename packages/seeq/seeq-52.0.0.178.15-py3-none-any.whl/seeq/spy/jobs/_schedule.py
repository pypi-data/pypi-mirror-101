import os
import re
import requests
import urllib

from datetime import datetime, timedelta
from typing import Optional

import pytz as tz
import pandas as pd

import cron_descriptor
from recurrent import RecurringEvent

from ._common import running_in_datalab, running_in_executor
from .._common import Status, validate_argument_types, add_properties_to_df, parse_str_time_to_timedelta, \
    format_exception
from .._config import get_data_lab_project_id
from .. import _login

from seeq.sdk import *


def schedule(schedule_spec: str, datalab_notebook_url: Optional[str] = None, label: Optional[str] = None,
             user: Optional[str] = None, suspend: bool = False, quiet: bool = False, status: Optional[Status] = None):
    """
    Schedules the automatic execution of a Seeq Data Lab notebook.

    The current notebook is scheduled for execution unless datalab_notebook_url
    is supplied. Scheduling can be done on behalf of another user by a user with
    admin privileges.

    Successive calls to 'schedule()' for the same notebook and label but with
    different schedules will replace the previous schedule for the notebook-
    label combination.

    Removing the scheduling is accomplished via unschedule().

    Parameters
    ----------
    schedule_spec : str
        A string that represents the frequency with which the notebook should
        execute.

        Examples: 'every 15 minutes'
                  'every tuesday and friday at 6am'
                  'every fifth of the month'

        The timezone used for scheduling is the one specified in the logged-in
        user's profile.

        You can also use Quartz Cron syntax. Use the following site to
        construct it:
        https://www.freeformatter.com/cron-expression-generator-quartz.html

    datalab_notebook_url : str, default None
        A datalab notebook URL. If the value is not specified the currently
        running notebook URL is used.

    label : str, default None
        A string used to enable scheduling of the Notebook by different users
        or from different Analysis Pages.  Labels may contain letters, numbers,
        spaces, and the following special characters: !@#$^&-_()[]{}

    user : str, default None
        Determines the user on whose behalf the notebook is executed. If the
        value is not specified the currently logged in user is used. The can be
        specified as username or a user's Seeq ID.

    suspend : bool, default False
        If True, unschedules all jobs for the specified notebook. This is used
        in scenarios where you wish to work with a notebook interactively and
        temporarily "pause" job execution. Remove the argument (or change it
        to False) when you are ready to resume job execution.

    quiet : bool, default False
        If True, suppresses progress output.

    status : spy.Status, optional
        If specified, the supplied Status object will be updated as the command
        progresses. It gets filled in with the same information you would see
        in Jupyter in the blue/green/red table below your code while the
        command is executed. The table itself is accessible as a DataFrame via
        the status.df property.

    Returns
    -------
    pd.DataFrame
        The jobs_df with an appended column containing a description of the
        schedule
    """
    validate_argument_types([
        (schedule_spec, 'schedule_string', str),
    ])

    status = Status.validate(status, quiet)

    try:
        return schedule_df(pd.DataFrame([{'Schedule': schedule_spec}]) if schedule_spec else None,
                           datalab_notebook_url=datalab_notebook_url, label=label, user=user, suspend=suspend,
                           status=status)
    except SchedulePostingError:
        # See _push.push() for why we swallow this error in the executor
        if not running_in_executor():
            raise


def unschedule(datalab_notebook_url: Optional[str] = None, label: Optional[str] = None,
               quiet: bool = False, status: Optional[Status] = None):
    """
    Unschedules ALL jobs for a particular notebook and label.

    The current notebook is unscheduled unless datalab_notebook_url
    is supplied. Unscheduling can be done on behalf of another user by a user
    with admin privileges.

    Parameters
    ----------
    datalab_notebook_url : str, default None
        A datalab notebook URL. If the value is not specified the currently
        running notebook URL is used.

    label : str, default None
        A string used to enable scheduling of the Notebook by different users
        or from different Analysis Pages.  Labels may contain letters, numbers,
        spaces, and the following special characters:

        !@#$^&-_()[]{}

        A value of '*' will unschedule all jobs across all labels associated
        with the supplied notebook (or the current Notebook, if no
        datalab_notebook_url is supplied).

    quiet : bool, default False
        If True, suppresses progress output.

    status : spy.Status, optional
        If specified, the supplied Status object will be updated as the command
        progresses. It gets filled in with the same information you would see
        in Jupyter in the blue/green/red table below your code while the
        command is executed. The table itself is accessible as a DataFrame via
        the status.df property.
    """
    status = Status.validate(status, quiet)
    schedule_df(jobs_df=None, datalab_notebook_url=datalab_notebook_url, label=label, status=status)


class SchedulePostingError(RuntimeError):
    pass


def schedule_df(jobs_df=None, spread=None, datalab_notebook_url=None, label=None, user=None, suspend=False,
                status=None):
    input_args = validate_argument_types([
        (jobs_df, 'jobs_df', pd.DataFrame),
        (datalab_notebook_url, 'datalab_notebook_url', str),
        (label, 'label', str),
        (user, 'user', str),
        (suspend, 'suspend', bool),
        (status, 'status', Status)
    ])

    _login.validate_login(status)

    cron_expressions = get_cron_expression_list(jobs_df) if not suspend else []
    if spread:
        cron_expressions = spread_over_period(cron_expressions, spread)
    next_trigger_map = validate_and_get_next_trigger(cron_expressions)
    project_id, file_path = retrieve_notebook_path(datalab_notebook_url)

    try:
        user_identity = _login.find_user(user) if user is not None else None
        if len(cron_expressions) == 0:
            call_unschedule_notebook_api(project_id, file_path, label)
        else:
            call_schedule_notebook_api(cron_expressions, project_id, file_path, label, user_identity)
    except BaseException as e:
        status.update(format_exception(e), Status.FAILURE)
        raise SchedulePostingError(e)

    with_label_text = f' with label <strong>{label}</strong> ' if label else ' '
    if cron_expressions:
        status.update(f'Scheduled the notebook <strong>{file_path}</strong>{with_label_text}successfully.\n'
                      f'Current context is <strong>{"JOB" if running_in_executor() else "INTERACTIVE"}</strong>.',
                      Status.SUCCESS)
    else:
        unlabeled = " " if label else " unlabeled "
        with_label_text = ' for all labels ' if label == '*' else with_label_text
        status.update(f'Unscheduled all{unlabeled}jobs for notebook <strong>{file_path}'
                      f'</strong>{with_label_text}successfully.', Status.SUCCESS)

    if cron_expressions:
        schedule_result_df = pd.concat([jobs_df, pd.Series(cron_expressions).rename('Scheduled')
                                       .map(cron_descriptor.get_description)], axis=1)
        schedule_result_df = pd.concat([schedule_result_df, pd.Series(cron_expressions).rename('Next Run')
                                       .map(lambda ce: next_trigger_map[ce])], axis=1)
    else:
        schedule_result_df = pd.DataFrame()
    schedule_df_properties = dict(
        func='spy.schedule',
        kwargs=input_args,
        status=status)
    add_properties_to_df(schedule_result_df, **schedule_df_properties)

    status.df = schedule_result_df
    status.update()
    return schedule_result_df


def validate_and_get_next_trigger(cron_expression_list):
    jobs_api = JobsApi(_login.client)
    validate_cron_input = ValidateCronListInputV1()
    validate_cron_input.timezone = _login.get_user_timezone()
    validate_cron_input.next_valid_time_after = datetime.now(tz.timezone(_login.get_user_timezone())) \
        .replace(microsecond=0)
    validate_cron_input.schedules = cron_expression_list
    validation_output = jobs_api.validate_cron(body=validate_cron_input)

    invalid_cron_expressions = []
    for cron_validation in validation_output.schedules:
        if cron_validation.error is not None:
            invalid_cron_expressions.append({'string': cron_validation.quartz_cron_expression,
                                             'error': cron_validation.error})
    if invalid_cron_expressions:
        raise RuntimeError('The following schedules are invalid: ' + str(invalid_cron_expressions))
    return dict((s.quartz_cron_expression, s.next_run_time) for s in validation_output.schedules)


def call_schedule_notebook_api(cron_expressions, project_id, file_path, label, user_identity):
    projects_api = ProjectsApi(_login.client)
    schedule_input = ScheduledNotebookInputV1()
    schedule_input.file_path = file_path
    schedule_input.schedules = list(map(lambda cs: ScheduleV1(cs), cron_expressions))
    schedule_input.timezone = _login.get_user_timezone()
    schedule_input.label = label
    if user_identity is not None:
        schedule_input.user_id = user_identity.id

    projects_api.schedule_notebook(id=project_id, body=schedule_input)


def call_unschedule_notebook_api(project_id, file_path, label):
    if label is None:
        ProjectsApi(_login.client).unschedule_notebook(id=project_id, file_path=file_path)
    else:
        ProjectsApi(_login.client).unschedule_notebook(id=project_id, file_path=file_path, label=label)


def retrieve_notebook_path(datalab_notebook_url=None):
    if datalab_notebook_url is None:
        if running_in_datalab():
            return get_data_lab_project_id(), get_notebook_path_from_running_kernel()
        if running_in_executor():
            return get_data_lab_project_id(), os.environ['SEEQ_SDL_FILE_PATH']
        else:
            raise RuntimeError('Provide a Seeq Data Lab Notebook URL for scheduling')
    return parse_project_id_and_path(datalab_notebook_url)


def parse_project_id_and_path(notebook_url):
    url_path = urllib.parse.unquote(urllib.parse.urlparse(notebook_url).path)
    matches = re.search(r'/data-lab/([0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12})/[\w]+/(.*)',
                        url_path)
    if not matches:
        raise ValueError('URL is not a valid SDL notebook')
    project_id = matches.group(1)
    file_path = matches.group(2)
    return project_id, file_path


def get_notebook_path_from_running_kernel():
    import json
    import ipykernel
    from requests.compat import urljoin
    from notebook.notebookapp import list_running_servers

    kernel_id = re.search('kernel-(.*).json', ipykernel.connect.get_connection_file()).group(1)
    servers = list_running_servers()
    for ss in servers:
        response = requests.get(urljoin(ss['url'], 'api/sessions'), params={'token': ss.get('token', '')})
        for nn in json.loads(response.text):
            if nn['kernel']['id'] == kernel_id:
                return nn['notebook']['path']


def spread_over_period(cron_expressions, over_period):
    over_period_delta = parse_str_time_to_timedelta(over_period)

    if len(cron_expressions) == 0:
        return []

    if over_period_delta.total_seconds() > (60 * 60 * 24):
        raise ValueError(f'over_period cannot be more than 24 hours')

    spacing = timedelta(seconds=(over_period_delta.total_seconds() / len(cron_expressions)))
    current_slot = timedelta()
    new_expressions = list()
    for cron_expression in cron_expressions:
        parts = re.split(r'\s+', cron_expression)
        parts[0] = re.sub(r'(.+?)(/.+)?', rf'{int(current_slot.total_seconds() % 60)}\2', parts[0])
        if over_period_delta.total_seconds() > 60:
            parts[1] = re.sub(r'(.+?)(/.+)?', rf'{int((current_slot.total_seconds() / 60) % 60)}\2', parts[1])
        if over_period_delta.total_seconds() > (60 * 60):
            parts[2] = re.sub(r'(.+?)(/.+)?', rf'{int(current_slot.total_seconds() / (60 * 60))}\2', parts[2])
        new_expressions.append(' '.join(parts))
        current_slot += spacing

    return new_expressions


def get_cron_expression_list(jobs_df):
    if jobs_df is None or jobs_df.empty:
        return []

    if 'Schedule' not in jobs_df:
        schedule_strings = jobs_df.iloc[:, 0].tolist()
    else:
        schedule_strings = jobs_df['Schedule'].tolist()

    cron_expressions = [parse_schedule_string(sch) for sch in schedule_strings]

    return cron_expressions


def parse_schedule_string(schedule_string):
    # noinspection PyBroadException
    try:
        # If cron_descriptor can parse it, then it's a valid cron schedule already
        cron_descriptor.get_description(schedule_string)
        return schedule_string
    except BaseException:
        pass

    return friendly_schedule_to_quartz_cron(schedule_string)


def friendly_schedule_to_quartz_cron(schedule_string):
    r = RecurringEvent()
    r.parse(schedule_string)

    rules = r.get_params()
    if len(rules) == 0 or 'freq' not in rules or 'interval' not in rules:
        raise ValueError(f'Could not interpret "{schedule_string}" as a schedule')
    days = {'SU': 1, 'MO': 2, 'TU': 3, 'WE': 4, 'TH': 5, 'FR': 6, 'SA': 7}
    if not r.is_recurring:
        raise ValueError(f'Could not interpret "{schedule_string}" as a recurring schedule')
    minute = rules.get('byminute', '0')
    hour = rules.get('byhour', '0')
    day_of_month = rules.get('bymonthday', '?')
    month = rules.get('bymonth', '*')
    day_of_week = ','.join([str(days[byday]) for byday in rules['byday'].split(',')]) if 'byday' in rules else '?'

    if day_of_month == '?' and day_of_week == '?':
        day_of_month = '1' if rules['freq'] in ['monthly', 'yearly'] else '*'

    interval = rules['interval']
    if rules['freq'] == 'minutely':
        hour = '*'
        minute = f'*/{interval}'
    elif rules['freq'] == 'hourly':
        hour = f'*/{interval}'
    elif rules['freq'] == 'daily':
        day_of_month += f'/{interval}'
    elif rules['freq'] == 'weekly':
        pass
    elif rules['freq'] == 'monthly':
        month += f'/{interval}'

    cron = f'0 {minute} {hour} {day_of_month} {month} {day_of_week}'

    return cron
