import os
from logging import Logger
from pathlib import Path
from unittest import TestCase, mock

import pytest

from exgrex.graders import UnittestGrader

EXGREX_ENV = {
    'EXGREX_DIR_SUBMISSION': 'some_dir_SUBMISSION',
    'EXGREX_TESTS_DIR': 'some_tests_dir',
    'EXGREX_SCORE_LOGFILE': 'score_logfilename',
    'EXGREX_FEEDBACK_LOGFILE': 'feedback_logfilename',
}


@pytest.fixture()
def grader():
    return UnittestGrader()


@pytest.fixture()
def delete_logfile():
    yield
    for filename in ('EXGREX_SCORE_LOGFILE', 'EXGREX_FEEDBACK_LOGFILE'):
        path = Path(EXGREX_ENV[filename])
        if path.exists():
            os.remove(path)


@pytest.fixture(scope='module')
def mock_settings_env_vars():
    with mock.patch.dict(os.environ, EXGREX_ENV):
        yield


def test_initialization_unittestgrader_attributes(mock_settings_env_vars, delete_logfile):
    grader = UnittestGrader()

    assert grader.testsDir == Path(EXGREX_ENV['EXGREX_TESTS_DIR'])
    assert grader.dirSubmission == Path(EXGREX_ENV['EXGREX_DIR_SUBMISSION'])
    assert isinstance(grader.feedbackLogger, Logger)
    assert isinstance(grader.scoreLogger, Logger)
    assert os.path.exists(grader.scoreLogFile)
    assert os.path.exists(grader.feedbackLogFile)
    assert grader.taskName is None
    assert grader.totalTests == 0
    assert grader.testResult is None
    assert grader.cwd == Path.cwd()
    assert grader.solutionFilename == 'solution.py'


def test_unittestgrader_abortExecution_method_calls_sys_exit(grader, delete_logfile):
    with mock.patch('sys.exit') as exit_mock:
        grader.abortExecution('feedback message')
        exit_mock.assert_called()
        exit_mock.assert_called_with(0)


def test_unittestgrader_abortExecution_method_write_score_log(grader, delete_logfile):
    with mock.patch('sys.exit') as exit_mock:
        with TestCase().assertLogs('scoreLogger', level='ERROR') as cm:
            grader.abortExecution('feedback message')

    assert cm.output == ['ERROR:scoreLogger:0', ]


def test_unittestgrader_abortExecution_method_write_feedback_log(grader, delete_logfile):
    with mock.patch('sys.exit') as exit_mock:
        with TestCase().assertLogs('feedbackLogger', level='ERROR') as cm:
            grader.abortExecution('feedback message')

    assert cm.output == ['ERROR:feedbackLogger:feedback message', ]
