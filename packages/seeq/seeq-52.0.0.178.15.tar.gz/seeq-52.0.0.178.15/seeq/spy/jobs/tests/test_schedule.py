import pytest
import mock
import os
import pandas as pd

from seeq import spy
from .. import _schedule
from .._schedule import retrieve_notebook_path, parse_project_id_and_path, validate_and_get_next_trigger, schedule_df
from .._push import get_parameters
from ...tests import test_common
from ..._common import Status


def setup_module():
    # assume all the calls return successfully
    _schedule.call_schedule_notebook_api = mock.Mock()
    _schedule.call_unschedule_notebook_api = mock.Mock()
    _schedule.get_notebook_path_from_running_kernel = mock.Mock(return_value='notebook.ipynb')


@pytest.mark.system
def test_schedule_in_datalab():
    setup_run_in_datalab()

    test_jobs_df = pd.DataFrame({'Schedule': ['0 */2 1 * * ? *', '0 0 2 * * ? *', '0 42 03 22 1 ? 2121']})
    test_status = Status()
    schedule_result = schedule_df(jobs_df=test_jobs_df, status=test_status)
    assert test_status.message.startswith("Scheduled")
    assert 'notebook.ipynb' in test_status.message
    assert len(schedule_result.index) == 3

    # dataframe without the schedule column, but first column containing the schedules
    datalab_notebook_url = 'http://192.168.1.100:34216/data-lab/8A54CD8B-B47A-42DA-B8CC-38AD4204C865/notebooks/1.ipynb'
    test_jobs_df = pd.DataFrame({'Other Name': ['0 */2 1 * * ? *', '0 0 2 * * ? *']})
    test_status = Status()
    schedule_result = schedule_df(jobs_df=test_jobs_df, datalab_notebook_url=datalab_notebook_url, status=test_status)
    assert test_status.message.startswith("Scheduled")
    assert '1.ipynb' in test_status.message
    assert len(schedule_result.index) == 2

    # schedule with a label
    label = 'This is a label!'
    schedule_result = schedule_df(jobs_df=test_jobs_df, datalab_notebook_url=datalab_notebook_url, label=label,
                                  status=test_status)
    assert test_status.message.startswith("Scheduled")
    assert '1.ipynb' in test_status.message
    assert label in test_status.message
    assert len(schedule_result.index) == 2

    # dataframe without the schedule column
    test_jobs_df = pd.DataFrame({'Some Name': ['abc'], 'Other Name': ['abc']})
    with pytest.raises(ValueError, match='Could not interpret "abc" as a schedule'):
        schedule_df(jobs_df=test_jobs_df, status=test_status)


@pytest.mark.system
def test_schedule_in_executor():
    setup_run_in_executor()

    test_jobs_df = pd.DataFrame({'Schedule': ['0 */5 * * * ?'], 'Param': ['val1']})
    test_status = Status()
    schedule_result = schedule_df(jobs_df=test_jobs_df, status=test_status)
    assert test_status.message.startswith("Scheduled")
    assert 'test.ipynb' in test_status.message
    assert len(schedule_result.index) == 1


@pytest.mark.system
def test_schedule_outside_datalab():
    setup_run_outside_datalab()
    spy.logout()

    test_jobs_df = pd.DataFrame({'Schedule': ['0 0 2 * * ? *', '0 42 03 22 1 ? 2121']})
    test_status = Status()
    with pytest.raises(RuntimeError) as err1:
        schedule_df(jobs_df=test_jobs_df, status=test_status)
    assert "Not logged in" in str(err1.value)

    test_common.login()

    # no datalab_notebook_url provided
    with pytest.raises(RuntimeError) as err2:
        schedule_df(jobs_df=test_jobs_df, status=test_status)
    assert "Provide a Seeq Data Lab Notebook URL" in str(err2.value)

    datalab_notebook_url = 'http://192.168.1.100:34216/data-lab/8A54CD8B-B47A-42DA-B8CC-38AD4204C865/notebooks/1.ipynb'
    schedule_result = schedule_df(jobs_df=test_jobs_df, datalab_notebook_url=datalab_notebook_url, status=test_status)
    assert test_status.message.startswith("Scheduled")
    assert '1.ipynb' in test_status.message
    assert len(schedule_result.index) == 2


@pytest.mark.system
def test_unschedule_in_datalab():
    setup_run_in_datalab()

    test_status = Status()
    schedule_result = schedule_df(status=test_status)
    assert test_status.message.startswith("Unscheduled")
    assert 'notebook.ipynb' in test_status.message
    pd.testing.assert_frame_equal(schedule_result, pd.DataFrame())

    datalab_notebook_url = 'http://192.168.1.100:34216/data-lab/8A54CD8B-B47A-42DA-B8CC-38AD4204C865/notebooks/1.ipynb'
    schedule_result = schedule_df(datalab_notebook_url=datalab_notebook_url, status=test_status)
    assert test_status.message.startswith("Unscheduled")
    assert '1.ipynb' in test_status.message
    pd.testing.assert_frame_equal(schedule_result, pd.DataFrame())

    label = 'Labeled!'
    schedule_result = schedule_df(jobs_df=pd.DataFrame(), label=label, status=test_status)
    assert test_status.message.startswith("Unscheduled")
    assert 'notebook.ipynb' in test_status.message
    assert label in test_status.message
    pd.testing.assert_frame_equal(schedule_result, pd.DataFrame())

    label = '*'
    schedule_result = schedule_df(jobs_df=pd.DataFrame(), label=label, status=test_status)
    assert test_status.message.startswith("Unscheduled")
    assert 'notebook.ipynb' in test_status.message
    assert 'for all labels' in test_status.message
    pd.testing.assert_frame_equal(schedule_result, pd.DataFrame())

@pytest.mark.system
def test_unschedule_outside_datalab():
    setup_run_outside_datalab()
    spy.logout()

    test_status = Status()

    with pytest.raises(RuntimeError) as err:
        schedule_df(status=test_status)
    assert "Not logged in" in str(err.value)

    test_common.login()

    # should provide a datalab_notebook_url
    with pytest.raises(RuntimeError):
        schedule_df(status=test_status)

    datalab_notebook_url = 'http://192.168.1.100:34216/data-lab/8A54CD8B-B47A-42DA-B8CC-38AD4204C865/notebooks/1.ipynb'
    schedule_result = schedule_df(datalab_notebook_url=datalab_notebook_url, status=test_status)
    assert test_status.message.startswith("Unscheduled")
    assert '1.ipynb' in test_status.message
    pd.testing.assert_frame_equal(schedule_result, pd.DataFrame())

    schedule_result = schedule_df(jobs_df=pd.DataFrame(), datalab_notebook_url=datalab_notebook_url, status=test_status)
    assert test_status.message.startswith("Unscheduled")
    assert '1.ipynb' in test_status.message
    pd.testing.assert_frame_equal(schedule_result, pd.DataFrame())


@pytest.mark.system
def test_validate_and_get_next_trigger():
    test_common.login()
    validate_result = validate_and_get_next_trigger(['0 */5 * * * ? 2069'])
    assert '2069-01-01 00:00:00 UTC' == validate_result['0 */5 * * * ? 2069']

    with pytest.raises(RuntimeError) as err1:
        validate_and_get_next_trigger(['0 */5 * * * ? 2001', '0 */5 * * * *'])
    assert "schedules are invalid" in str(err1.value)
    assert "0 */5 * * * ? 2001" in str(err1.value)
    assert "No future trigger" in str(err1.value)

    with pytest.raises(RuntimeError) as err2:
        validate_and_get_next_trigger(['* */2 * * * '])
    assert "Unexpected end of expression" in str(err2.value)

    with pytest.raises(RuntimeError) as err3:
        validate_and_get_next_trigger(['* abc * * * ? *'])
    assert "Illegal characters for this position" in str(err3.value)


@pytest.mark.system
def test_retrieve_notebook_path_in_datalab():
    setup_run_in_datalab()
    project_id, file_path = retrieve_notebook_path()
    assert project_id == '8A54CD8B-B47A-42DA-B8CC-38AD4204C863'
    assert file_path == 'notebook.ipynb'

    datalab_notebook_url = 'http://192.168.1.100:34216/data-lab/8A54CD8B-B47A-42DA-B8CC-38AD4204C865/notebooks/1.ipynb'
    project_id, file_path = retrieve_notebook_path(datalab_notebook_url)
    assert project_id == '8A54CD8B-B47A-42DA-B8CC-38AD4204C865'
    assert file_path == '1.ipynb'


@pytest.mark.system
def test_retrieve_notebook_path_in_executor():
    setup_run_in_executor()
    project_id, file_path = retrieve_notebook_path()
    assert project_id == '8A54CD8B-B47A-42DA-B8CC-38AD4204C864'
    assert file_path == 'test.ipynb'

    datalab_notebook_url = 'http://192.168.1.100:34216/data-lab/8A54CD8B-B47A-42DA-B8CC-38AD4204C866/notebooks/2.ipynb'
    project_id, file_path = retrieve_notebook_path(datalab_notebook_url)
    assert project_id == '8A54CD8B-B47A-42DA-B8CC-38AD4204C866'
    assert file_path == '2.ipynb'


@pytest.mark.unit
def test_retrieve_notebook_path_outside_sdl():
    setup_run_outside_datalab()
    with pytest.raises(RuntimeError) as err:
        retrieve_notebook_path()
    assert "Provide a Seeq Data Lab Notebook URL" in str(err.value)

    datalab_notebook_url = 'http://192.168.1.100:34216/data-lab/8A54CD8B-B47A-42DA-B8CC-38AD4204C867/notebooks/3.ipynb'
    project_id, file_path = retrieve_notebook_path(datalab_notebook_url)
    assert project_id == '8A54CD8B-B47A-42DA-B8CC-38AD4204C867'
    assert file_path == '3.ipynb'


@pytest.mark.unit
def test_parse_project_id_and_path():
    # incorrect data-lab value
    notebook_url_bad1 = 'http://192.168.1.100:34216/data-lab1/8A54CD8B-B47A-42DA-B8CC-38AD4204C862/notebooks/SPy' \
                        '%20Documentation/SchedulingTest.ipynb'
    with pytest.raises(ValueError) as err1:
        parse_project_id_and_path(notebook_url_bad1)
    assert "not a valid SDL notebook" in str(err1.value)

    # invalid project id
    notebook_url_bad2 = 'http://192.168.1.100:34216/data-lab1/A8A54CD8B-B47A-42DA-B8CC-38AD4204C862/notebooks/SPy' \
                        '%20Documentation/SchedulingTest.ipynb'
    with pytest.raises(ValueError) as err2:
        parse_project_id_and_path(notebook_url_bad2)
    assert "not a valid SDL notebook" in str(err2.value)

    # path with whitespace
    notebook_url1 = 'http://192.168.1.100:34216/data-lab/8A54CD8B-B47A-42DA-B8CC-38AD4204C862/notebooks/SPy' \
                    '%20Documentation/SchedulingTest.ipynb'
    project_id, file_path = parse_project_id_and_path(notebook_url1)
    assert project_id == '8A54CD8B-B47A-42DA-B8CC-38AD4204C862'
    assert file_path == 'SPy Documentation/SchedulingTest.ipynb'

    # partial path without whitespace
    notebook_url2 = '/data-lab/8A54CD8B-B47A-42DA-B8CC-38AD4204C862/notebooks/SchedulingTest.ipynb'
    project_id, file_path = parse_project_id_and_path(notebook_url2)
    assert project_id == '8A54CD8B-B47A-42DA-B8CC-38AD4204C862'
    assert file_path == 'SchedulingTest.ipynb'


@pytest.mark.unit
def test_get_cron_expression_list():
    jobs_df = pd.DataFrame({'Schedule': ['0 0 0 ? * 3', 'every february at 2pm']})
    assert _schedule.get_cron_expression_list(jobs_df) == ['0 0 0 ? * 3', '0 0 14 1 2 ?']

    jobs_df = pd.DataFrame({'Schedule': ["my cat's breath smells like cat food"]})
    with pytest.raises(ValueError):
        assert _schedule.get_cron_expression_list(jobs_df)


@pytest.mark.unit
def test_parse_schedule_df():
    assert _schedule.parse_schedule_string('0 0 0 ? * 3') == '0 0 0 ? * 3'
    assert _schedule.parse_schedule_string('every february at 2pm') == '0 0 14 1 2 ?'

    with pytest.raises(ValueError):
        assert _schedule.parse_schedule_string("my cat's breath smells like cat food")

    with pytest.raises(ValueError):
        assert _schedule.parse_schedule_string("every breath you take")


@pytest.mark.unit
def test_friendly_schedule_to_cron():
    assert _schedule.friendly_schedule_to_quartz_cron('every tuesday') == '0 0 0 ? * 3'
    assert _schedule.friendly_schedule_to_quartz_cron('every february at 2pm') == '0 0 14 1 2 ?'
    assert _schedule.friendly_schedule_to_quartz_cron('every tuesday and friday at 6am') == '0 0 6 ? * 3,6'
    assert _schedule.friendly_schedule_to_quartz_cron('every january and june 1st at 17:00') == '0 0 17 1 1,6 ?'
    assert _schedule.friendly_schedule_to_quartz_cron('every fifth of the month') == '0 0 0 5 */1 ?'
    assert _schedule.friendly_schedule_to_quartz_cron('every five hours') == '0 0 */5 * * ?'
    assert _schedule.friendly_schedule_to_quartz_cron('every six minutes') == '0 */6 * * * ?'
    assert _schedule.friendly_schedule_to_quartz_cron('every thursday at 2:05am') == '0 5 2 ? * 5'

    with pytest.raises(ValueError):
        assert _schedule.friendly_schedule_to_quartz_cron('0 5 2 ? * 5')

    with pytest.raises(ValueError):
        assert _schedule.friendly_schedule_to_quartz_cron('2020-01-01T00:00:00.000Z')


@pytest.mark.unit
def test_spread():
    cron = _schedule.friendly_schedule_to_quartz_cron('every february 1')
    assert _schedule.spread_over_period([cron] * 3, '8h') == ['0 0 0 1 2 ?', '0 40 2 1 2 ?', '0 20 5 1 2 ?']

    cron = _schedule.friendly_schedule_to_quartz_cron('every 2 minutes')
    assert _schedule.spread_over_period([cron] * 4, '1min') == ['0 */2 * * * ?', '15 */2 * * * ?', '30 */2 * * * ?',
                                                                '45 */2 * * * ?']

    cron = _schedule.friendly_schedule_to_quartz_cron('every 5 minutes')
    assert _schedule.spread_over_period([cron] * 4, '3min') == ['0 0/5 * * * ?', '45 0/5 * * * ?', '30 1/5 * * * ?',
                                                                '15 2/5 * * * ?']

    cron = _schedule.friendly_schedule_to_quartz_cron('every 15 minutes')
    assert _schedule.spread_over_period([cron] * 3, '1h') == ['0 0/15 * * * ?', '0 20/15 * * * ?', '0 40/15 * * * ?']

    cron = _schedule.friendly_schedule_to_quartz_cron('every 6 hours')
    assert _schedule.spread_over_period([cron] * 3, '6h') == ['0 0 0/6 * * ?', '0 0 2/6 * * ?', '0 0 4/6 * * ?']


@pytest.mark.unit
def test_get_parameters_without_interactive_index_not_executor_raises_error():
    # assure we are not in executor
    os.environ['SEEQ_SDL_CONTAINER_IS_EXECUTOR'] = 'None'

    test_jobs_df = pd.DataFrame({'Schedule': ['0 */2 1 * * *', '0 0 2 * * *', '0 42 03 22 1 * 2021']})
    test_status = Status()
    test_status.message = 'Blah'
    with pytest.raises(ValueError):
        get_parameters(test_jobs_df, None, test_status)


@pytest.mark.unit
def test_get_parameters_with_interactive_index():
    # assure we are not in executor
    os.environ['SEEQ_SDL_CONTAINER_IS_EXECUTOR'] = 'None'

    test_status = Status()
    test_status.message = 'Blah'
    test_jobs_df = pd.DataFrame({'Schedule': ['0 */2 1 * * *', '0 0 2 * * *', '0 42 03 22 1 * 2021']})
    pd.testing.assert_series_equal(pd.Series(name=0, data={'Schedule': '0 */2 1 * * *'}), get_parameters(
        test_jobs_df, 0, test_status))
    pd.testing.assert_series_equal(pd.Series(name=2, data={'Schedule': '0 42 03 22 1 * 2021'}), get_parameters(
        test_jobs_df, 2, test_status))
    with pytest.raises(IndexError):
        get_parameters(test_jobs_df, 3, test_status)

    test_jobs_df_with_params = pd.DataFrame({'Param1': ['val1', 'val2'], 'Param2': ['val3', 'val4']})
    pd.testing.assert_series_equal(pd.Series(name=1, data={'Param1': 'val2', 'Param2': 'val4'}), get_parameters(
        test_jobs_df_with_params, 1, test_status))


@pytest.mark.unit
def test_get_parameters_with_interactive_index_in_executor_is_ignored():
    # assure we are in executor
    os.environ['SEEQ_SDL_CONTAINER_IS_EXECUTOR'] = 'true'

    test_status = Status()
    test_status.message = 'Blah'
    test_jobs_df = pd.DataFrame({'Param1': ['val1', 'val2'], 'Param2': ['val3', 'val4']})
    # don't set the true schedule index yet
    with pytest.raises(RuntimeError):
        get_parameters(test_jobs_df, 1, test_status)

    # set the schedule index which will override the interactive_index
    os.environ['SEEQ_SDL_SCHEDULE_INDEX'] = '0'
    pd.testing.assert_series_equal(pd.Series(name=0, data={'Param1': 'val1', 'Param2': 'val3'}), get_parameters(
        test_jobs_df, 1, test_status))


def setup_run_outside_datalab():
    os.environ['SEEQ_SDL_CONTAINER_IS_DATALAB'] = ''
    os.environ['SEEQ_SDL_CONTAINER_IS_EXECUTOR'] = ''
    os.environ['SEEQ_PROJECT_UUID'] = ''
    os.environ['SEEQ_SDL_FILE_PATH'] = ''


def setup_run_in_datalab():
    test_common.login()
    os.environ['SEEQ_SDL_CONTAINER_IS_DATALAB'] = 'true'
    os.environ['SEEQ_SDL_CONTAINER_IS_EXECUTOR'] = ''
    os.environ['SEEQ_PROJECT_UUID'] = '8A54CD8B-B47A-42DA-B8CC-38AD4204C863'


def setup_run_in_executor():
    test_common.login()
    os.environ['SEEQ_SDL_CONTAINER_IS_DATALAB'] = ''
    os.environ['SEEQ_SDL_CONTAINER_IS_EXECUTOR'] = 'true'
    os.environ['SEEQ_PROJECT_UUID'] = '8A54CD8B-B47A-42DA-B8CC-38AD4204C864'
    os.environ['SEEQ_SDL_FILE_PATH'] = 'test.ipynb'
