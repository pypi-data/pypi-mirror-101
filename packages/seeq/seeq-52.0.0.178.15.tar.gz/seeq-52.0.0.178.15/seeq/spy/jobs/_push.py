import os

from typing import Optional

import pandas as pd

from .._common import Status
from ._schedule import schedule_df, running_in_executor, SchedulePostingError


def push(jobs_df: pd.DataFrame, spread: Optional[str] = None, datalab_notebook_url: Optional[str] = None,
         label: Optional[str] = None, user: Optional[str] = None, interactive_index: int = 0, suspend: bool = False,
         quiet: bool = False, status: Optional[Status] = None):
    """
    Schedules the automatic execution of a notebook and returns the row
    corresponding for the currently running schedule.

    When used inside a Data Lab notebook, the current notebook is scheduled
    for execution. A notebook can be scheduled also by specifying its URL, and
    the scheduling can be done on behalf of another user by a user with admin
    privileges.

    Successive calls to 'push()' for the same notebook and label but with
    different schedules will replace the previous schedule for that notebook-
    label combination.

    Removing the scheduling is accomplished via unschedule().

    Parameters
    ----------
    jobs_df : pd.DataFrame
        A DataFrame that contains the schedules in the form of schedule
        specification strings and optional parameters for each job.

        The DataFrame must have an integer index and a column named 'Schedule'
        containing the scheduling specifications. If no column named 'Schedule'
        is found, the first column is used.

        Examples of scheduling specification strings:

                  'every 15 minutes'
                  'every tuesday and friday at 6am'
                  'every fifth of the month'

        The timezone used for scheduling is the one specified in the logged-in
        user's profile.

        You can also use Quartz Cron syntax. Use the following site to
        construct it:
        https://www.freeformatter.com/cron-expression-generator-quartz.html

    spread : str, default None
        A time period over which to spread out the jobs. This should generally
        be the same value of the frequency of the jobs. For example, if you
        want the jobs to run every 6 hours, you should specify spread='6h'
        to dynamically space out the execution of the jobs throughout that
        6-hour period so that the load on Seeq services isn't concentrated
        at the same time.

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

    interactive_index : int, default 0
        Used during notebook development to control which row of jobs_df is
        returned when NOT executing as a job. Change this value if you want
        to test your notebook in the Jupyter environment with various rows
        of parameters.

        When the notebook is executed as a job, this parameter is ignored.

    suspend : bool default False
        If True, un-schedules all jobs for the specified notebook. This is used
        in scenarios where you wish to work with a notebook interactively and
        temporarily prevent job execution. Remove the argument (or change it
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
    pd.Series
        The row that corresponds to the currently executing job. If not
        executing in the context of job, then the row is returned according
        to the interactive_index parameter.

    """
    status = Status.validate(status, quiet)

    try:
        schedule_df(jobs_df=jobs_df, spread=spread, datalab_notebook_url=datalab_notebook_url, label=label, user=user,
                    suspend=suspend, status=status)
    except SchedulePostingError:
        # When the notebook is executed as a job, push will first re-schedule the notebook. If any errors will happen
        # during that reschedule, an exception forces an exit from the method, and the currently executing notebook will
        # not get the needed parameters and will have a failed execution (assuming it needs the parameters). Most of
        # the time, such transient errors are unnecessary to the running of a job. One example where a failed schedule
        # call is actually expected is when you schedule a notebook to run exactly once, with a fixed date. When the
        # notebook is executing on schedule, the date is already in the past, and that means the schedule will fail
        # because you cannot schedule something to run in the past.
        #
        # So we ignore the error here when running as a job and fall through to get_parameters(). Note that
        # schedule_df() will have filled in the status.message with an error and set it to FAILURE so that it appears in
        # red in the job result HTML.
        if not running_in_executor():
            raise

    return get_parameters(jobs_df, interactive_index, status)


def get_parameters(jobs_df, interactive_index, status):
    if running_in_executor():
        schedule_index = os.environ.get('SEEQ_SDL_SCHEDULE_INDEX')

        if schedule_index is None:
            raise RuntimeError('Job is being executed without a SEEQ_SDL_SCHEDULE_INDEX environment variable')

        status.update(status.message +
                      f'\nParameters returned are for DataFrame row index <strong>{schedule_index}</strong>.')

        return jobs_df.iloc[int(schedule_index)]
    else:
        if not isinstance(interactive_index, int):
            raise ValueError(f'Invalid interactive_index argument: "{interactive_index}"')

        status.update(status.message +
                      f'\nParameters returned are for DataFrame row index <strong>{interactive_index}</strong>. To '
                      'change the DataFrame row returned in the INTERACTIVE context, add/change the '
                      '<code>interactive_index</code> argument.')

        return jobs_df.iloc[interactive_index]
