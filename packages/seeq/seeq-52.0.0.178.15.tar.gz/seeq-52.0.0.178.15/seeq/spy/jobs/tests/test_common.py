import pytest
import os

from .._common import running_in_datalab, running_in_executor


@pytest.mark.unit
def test_running_in_datalab():
    os.environ['SEEQ_SDL_CONTAINER_IS_DATALAB'] = ''
    assert running_in_datalab() is False

    os.environ['SEEQ_SDL_CONTAINER_IS_DATALAB'] = 'true'
    assert running_in_datalab() is True


@pytest.mark.unit
def test_running_in_executor():
    os.environ['SEEQ_SDL_CONTAINER_IS_EXECUTOR'] = ''
    assert running_in_executor() is False

    os.environ['SEEQ_SDL_CONTAINER_IS_EXECUTOR'] = 'true'
    assert running_in_executor() is True
