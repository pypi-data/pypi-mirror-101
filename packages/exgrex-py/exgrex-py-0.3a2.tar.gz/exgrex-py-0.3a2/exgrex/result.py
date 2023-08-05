"""
Вывод
заголовок - имя теста

1. shortDescription - выводится первая строка docstring теста
todo сделать возможным многострочный вывод docstring
2. отключение трейсбек - вариант 1: в тестовом классе установить атрибут класса
longMessage = False, вариант 2: в декораторе RunUnittestTests передать traceback=True
3. параметр failfast - остановить выполнение тестов на первом упавшем или с ошибкой,
если True, то значение pass_rate игнорируется (необходимо чтобы все тесты были зеленые)
4. нет поддержки частичной оценки, score может принимать значения 0 или 1
5 verbosity=0, выводится название теста + shortDescription только
для упавшего теста
verbosity=1, выводится название теста + shortDescription + сообщение об ошибке только
для упавшего теста (message из assert + трейсбек, если включен)
verbosity=2, для каждого запущенного теста выводится название теста + shortDescription
+ сообщение об ошибке (message из assert + трейсбек, если включен)

"""
from decimal import ROUND_DOWN, Decimal
from unittest.result import TestResult, failfast


def _isAlreadyFailOrError(result, test):
    testId = test.id()

    for id_ in [test[0].id() for test in result.failures]:
        if id_.startswith(testId + ' '):
            return True

    for id_ in [test[0].id() for test in result.errors]:
        if id_.startswith(testId + ' '):
            return True

    return False


def _getTestResultData(test, err, verbosity):
    error, value, tr = err

    testId = test.id()
    description = test.shortDescription()

    if description is None:
        description = ''
    else:
        if verbosity != 0:
            description += '\n'

    if verbosity == 0:
        typeError = message = ''
    else:
        typeError = error.__name__ + '\n'
        message = value.args[0]

    return testId, description, typeError, message


class LogTestResult(TestResult):
    separator = '=' * 70

    def __init__(self, feedback_logger, score_logger, verbosity=1, failfast=True,
                 total_tests=None, pass_rate=None, **kwargs):
        # TODO: сделать total_tests обязательным параметром
        # created vshagur@gmail.com, 2020-12-18
        super().__init__(**kwargs)
        self.feedbackLogger = feedback_logger
        self.scoreLogger = score_logger
        self.verbosity = verbosity
        self.failfast = failfast
        self.totalTests = total_tests
        self.passRate = pass_rate

    @failfast
    def addError(self, test, err):

        """Called when an error has occurred. 'err' is a tuple of values as
        returned by sys.exc_info()."""
        super().addError(test, err)
        data = _getTestResultData(test, err, self.verbosity)
        message = '[ERROR] {}. {}{}{}'.format(*data)
        self.feedbackLogger.error(self.separator)
        self.feedbackLogger.error(message)

    @failfast
    def addFailure(self, test, err):
        """Called when an error has occurred. 'err' is a tuple of values as
        returned by sys.exc_info()."""
        super().addFailure(test, err)
        data = _getTestResultData(test, err, self.verbosity)
        message = '[FAILED] {}. {}{}{}'.format(*data)
        self.feedbackLogger.error(self.separator)
        self.feedbackLogger.error(message)

    def addSubTest(self, test, subtest, err):
        """Called at the end of a subtest.
        'err' is None if the subtest ended successfully, otherwise it's a
        tuple of values as returned by sys.exc_info().
        """
        # By default, we don't do anything with successful subtests, but
        # more sophisticated test results might want to record them.

        alreadyFailOrError = _isAlreadyFailOrError(self, test)

        if err is not None and not alreadyFailOrError:
            data = _getTestResultData(subtest, err, self.verbosity)

            if issubclass(err[0], test.failureException):
                message = '[FAILED] {}. {}{}{}'.format(*data)
            else:
                message = '[ERROR] {}. {}{}{}'.format(*data)

            self.feedbackLogger.error(self.separator)
            self.feedbackLogger.error(message)

        if not alreadyFailOrError:
            super().addSubTest(test, subtest, err)

    def addSuccess(self, test):
        "Called when a test has completed successfully"

        super().addSuccess(test)
        if self.verbosity == 2:
            message = f'[PASSED] {test.id()}. {test.shortDescription()}'
            self.feedbackLogger.error(self.separator)
            self.feedbackLogger.error(message)

    def wasSuccessful(self):
        """Tells whether or not this result was a success."""
        # The hasattr check is for test_result's OldResult test.  That
        # way this method works on objects that lack the attribute.
        # (where would such result intances come from? old stored pickles?)

        if self.failfast:
            if len(self.failures) + len(self.errors) == 0:
                self.feedbackLogger.error('Congratulations! All tests passed!')
                self.scoreLogger.error(1.00)
                return True
            else:
                self.feedbackLogger.error(f'Not passed. Try again.')
                self.scoreLogger.error(0)
                return False

        incorrect = len(self.failures) + len(self.errors)
        success = (self.totalTests - incorrect) / self.totalTests
        score = Decimal(success).quantize(Decimal('.01'), rounding=ROUND_DOWN)
        self.feedbackLogger.error(self.separator)

        if score == 1:
            self.feedbackLogger.error('Congratulations! All tests passed!')
            self.scoreLogger.error(1.00)
            return True
        elif score < self.passRate:
            self.feedbackLogger.error(
                f'Not passed. Score: {int(score * 100)} points out of 100.\n'
                f'To pass the test, you need to score {int(self.passRate * 100)} points.\n'
                f'Try again.'
            )
            self.scoreLogger.error(score)
            return False
        elif self.passRate <= score < 1:
            self.feedbackLogger.error(
                f'Passed. Score: {int(score * 100)} points out of 100. \n'
                f'You have scored the required number of points to pass the test.\n'
                f'If you want, you can try to take the test again and get a higher grade.'
            )
            # для совместимости с платформами, которые не поддерживают оценку с проходным
            # баллом, score устанавливается в 1.00 (некоторые платформы имеют систему
            # оценки - 1:задание пройдено, <1 не пройдено)
            self.scoreLogger.error(1.00)
            return False
        else:
            self.feedbackLogger.error(
                'Grader error. Invalid test score received. Please report to '
                'course staff.'
            )
            self.scoreLogger.error(0.00)

# TODO: добавить статистику - время исполнения, количество тестов пройденных, заваленых, всего
# TODO: добавить предустановленные режимы вывода
# TODO: добавить многострочный вывод shortDescription
