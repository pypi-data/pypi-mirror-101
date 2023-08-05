import logging
import time
from decimal import ROUND_DOWN, Decimal
from pathlib import Path

import pytest
from exgrex.graders import createFileLogger

SEPARATOR = '=' * 70

# https://stackoverflow.com/questions/53249304/how-to-list-all-existing-loggers-using-python-logging-module
loggers = logging.root.manager.loggerDict.keys()

# for the case when tests are run from the command line without using exgrex
if not 'scoreLogger' in loggers and not 'feedbackLogger' in loggers:
    scoreLogFile = Path(Path.cwd(), 'score.log')
    feedbackLogFile = Path(Path.cwd(), 'feedback.log')

    if scoreLogFile.exists():
        scoreLogFile.write_text('')

    if feedbackLogFile.exists():
        feedbackLogFile.write_text('')

    scoreLogger = createFileLogger(
        'scoreLogger', scoreLogFile, '%(message)s'
    )
    feedbackLogger = createFileLogger(
        'feedbackLogger', feedbackLogFile, '%(message)s'
    )


def pytest_addoption(parser):
    group = parser.getgroup(
        'grader',
        'Creates a report for an external mook course grader and saves it to a file.'
    )
    group._addoption(
        '--grader-mode', dest='grader_mode', metavar='grader-mode',
        action="store",
        choices=['no', 'line', 'short', 'long'],
        type="choice",
        help='sets one and preset reporting modes for external mook courses grader')

    group._addoption(
        '--taskname', dest='taskname', metavar='taskname',
        action="store",
        type=str,
        default='An unnamed task.',
        help='sets taskname')

    group._addoption(
        '--passrate', dest='passrate', metavar='passrate',
        action="store",
        type=Decimal,
        default=Decimal('1.0'),
        help='sets passrate')

    group._addoption(
        '--limit', dest='limit', metavar='limit',
        action="store",
        type=int,
        help='sets limit')


@pytest.hookimpl()
def pytest_sessionstart(session):
    if session.config.getoption('grader_mode'):
        taskname = session.config.getoption('taskname').strip('\'"')
        feedbackLogger.error(SEPARATOR)
        feedbackLogger.error(f'Test result of the task: "{taskname}"')
        feedbackLogger.error(SEPARATOR)


@pytest.hookimpl()
def pytest_configure(config):
    if config.getoption('grader_mode'):
        setattr(config, 'grader_errors', [])
        setattr(config, 'grader_failed', [])
        setattr(config, 'grader_start_time', time.time())


@pytest.hookimpl(trylast=True)
def pytest_collectreport(report):
    if report.outcome == 'failed':
        loggers = logging.root.manager.loggerDict.keys()

        if 'scoreLogger' in loggers and 'feedbackLogger' in loggers:
            scoreLogger.error(0)

            feedbackLogger.error(
                f'The grader crashed. Check for syntax errors in your solution and '
                f'the ability\nto import it as a module. If the error reappears, please '
                f'contact the support\nadministrator.\n\n{report.longrepr}'
            )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()

    if item.config.getoption('grader_mode'):
        if result.when in ('setup', 'teardown') and result.outcome == 'failed':
            item.config.grader_errors.append(
                f'The grader crashed. Check for syntax errors in your solution and '
                f'the ability\nto import it as a module. If the error reappears, please '
                f'contact the support\nadministrator.\n\n{result.longrepr}'
            )

        elif result.when == 'call' and result.outcome == 'failed':
            _, _, testname = result.location

            message = '[Failed] {}.\n{}'

            if item.config.getoption('grader_mode') == 'line':
                message = '[Failed] {}.'.format(testname, '')
            elif item.config.getoption('grader_mode') == 'short':
                message = message.format(testname, result.longrepr.reprcrash.message)
            elif item.config.getoption('grader_mode') == 'long':
                message = message.format(testname, result.longrepr.reprtraceback)
            else:
                message = message.format(testname, result.longrepr.reprtraceback)

            item.config.grader_failed.append(message)


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    if session.config.getoption('grader_mode'):

        if Path(scoreLogger.handlers[0].baseFilename).read_text().strip() == '0':
            feedbackLogger.error(SEPARATOR)
            feedbackLogger.error('Not passed. Try again.')
        else:
            passrate = session.config.getoption('passrate')
            maxfail = session.config.getoption('maxfail')
            limit = session.config.getoption('limit')
            mode = session.config.getoption('grader_mode')

            statistics = f'Total tests: {session.testscollected}. '

            if maxfail != 1:
                statistics += f'Tests failed: {session.testsfailed}. '

            duration = round(time.time() - session.config.grader_start_time, 4)

            statistics += f'Total testing time: {duration}.'

            feedbackLogger.error(statistics)

            if session.config.grader_errors:
                feedback = (session.config.grader_errors[0],)
            elif session.config.grader_failed:
                if session.config.getoption('grader_mode') == 'no':
                    feedback = ('Incorrect answer.',)
                else:
                    feedback = session.config.grader_failed
            else:
                feedback = tuple()

            if limit != 0:
                feedback = feedback[:limit]

            for testReport in feedback:
                feedbackLogger.error(SEPARATOR)
                feedbackLogger.error(testReport)

            if passrate == 1 or maxfail == 1 or session.config.grader_errors:
                score = abs(int(exitstatus) - 1)
            else:
                success = (session.testscollected -
                           session.testsfailed) / session.testscollected
                score = Decimal(success).quantize(Decimal('.01'), rounding=ROUND_DOWN)

            if score == 1:
                feedbackLogger.error('All tests passed.')

            elif passrate == 1 and score < passrate:
                feedbackLogger.error(SEPARATOR)
                feedbackLogger.error('Not passed. Try again.')

            elif score < passrate:
                feedbackLogger.error(SEPARATOR)
                if maxfail == 1 or mode == 'no':
                    feedbackLogger.error('Not passed. Try again.')
                else:
                    feedbackLogger.error(
                        f'Not passed. Score: {int(score * 100)} points out of 100.\n'
                        f'To pass the test, you need to score {int(passrate * 100)} '
                        f'points.\nTry again.'
                    )
            elif passrate <= score < 1:
                feedbackLogger.error(SEPARATOR)
                feedbackLogger.error(
                    f'Passed. Score: {int(score * 100)} points out of 100. \n'
                    f'You have scored the required number of points to pass the test.\n'
                    f'If you want, you can try to take the test again and get a '
                    f'higher grade.'
                )
                score = 1
            else:
                feedbackLogger.error(
                    'Grader error. Invalid test score received. Please report to '
                    'course staff.'
                )

            scoreLogger.error(score)
