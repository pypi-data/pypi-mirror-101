import importlib.util
import shutil
import unittest
import zipfile
from datetime import datetime
from functools import wraps
from pathlib import Path

from exgrex.result import LogTestResult


def _getTestSuite(grader):
    loader = unittest.TestLoader()
    suite = loader.discover(Path(grader.cwd, grader.testsDir))

    if not suite.countTestCases():
        grader.abortExecution(
            'Grader error. No tests loaded. Please report to course staff.'
        )

    return suite


def _get_content(grader, path):
    if path is None:
        return ''

    pathToFile = Path(grader.cwd, path)

    if not pathToFile.exists() or not pathToFile.is_file():
        grader.abortExecution(f'Grader error. Invalid file path passed for {path}.')

    try:
        content = pathToFile.read_text() + '\n'
        return content
    except BaseException as err:
        grader.abortExecution(
            f'Grader error. Problems getting content from a file: {path}. {err}.'
        )


class CheckFileAsModule:
    def __init__(self, path_to_module):
        self.pathToModule = Path(path_to_module)

    def __call__(self, func):
        @wraps(func)
        def wrapper(grader):
            moduleName = 'solution'
            pathToModule = Path(grader.cwd, self.pathToModule)
            spec = importlib.util.spec_from_file_location(moduleName, pathToModule)
            module = importlib.util.module_from_spec(spec)

            try:
                spec.loader.exec_module(module)
            except Exception as err:
                grader.abortExecution(
                    f'Grader Error. An attempt to import the solution file as '
                    f'a module failed. Error: {err}.'
                )

            return func(grader)

        return wrapper


class ExtractFromZip:
    def __init__(self, filenames=None, path_to=None, cleaning=True):
        self.filenames = filenames
        self.pathTo = path_to
        self.cleaning = cleaning

    def __call__(self, func):
        @wraps(func)
        def wrapper(grader):
            solutionPath = next(grader.dirSubmission.iterdir())
            archive = zipfile.ZipFile(solutionPath, 'r')

            if self.pathTo is None:
                self.pathTo = grader.testsDir

            pathTo = Path(grader.cwd, self.pathTo)

            if pathTo.exists() and self.cleaning:
                shutil.rmtree(pathTo, ignore_errors=True)

            pathTo.mkdir(parents=True, exist_ok=True)

            try:
                if self.filenames is None:
                    archive.extractall(pathTo)
                else:
                    for file_name in self.filenames:
                        archive.extract(file_name, pathTo)

            except Exception as err:
                grader.abortExecution(
                    f'Grader Error. An error occurred while processing the archive '
                    f'with the solution. {err.__class__.__name__}'
                )

            return func(grader)

        return wrapper


class CheckZipArchive:
    def __init__(self, filenames=None):
        if filenames is None:
            self.filenames = []
        else:
            self.filenames = filenames

    def __call__(self, func):
        @wraps(func)
        def wrapper(grader):
            solutionPath = next(grader.dirSubmission.iterdir())

            if not zipfile.is_zipfile(solutionPath):
                grader.abortExecution('Grader Error. Submission should be zip archive.')

            archive = zipfile.ZipFile(solutionPath, 'r')

            for filename in self.filenames:
                if filename not in archive.namelist():
                    grader.abortExecution(
                        f'Grader Error. The solution archive should contain '
                        f'the file: {filename}.'
                    )

            return func(grader)

        return wrapper


class GlueFiles:
    def __init__(self, prefix_file_path=None, postfix_file_path=None, path_to=None,
                 filename=None):
        self.prefixFilePath = prefix_file_path
        self.postfixFilePath = postfix_file_path
        self.pathTo = path_to
        self.filename = filename

    def __call__(self, func):
        @wraps(func)
        def wrapper(grader):

            if self.pathTo is None:
                self.pathTo = grader.testsDir

            if self.filename is None:
                self.filename = grader.solutionFilename

            self.pathTo = Path(grader.cwd, self.pathTo)
            self.pathTo.mkdir(parents=True, exist_ok=True)

            prefixContent = _get_content(grader, self.prefixFilePath)
            solutionPath = grader.dirSubmission.iterdir()
            solutionContent = _get_content(grader, next(solutionPath))
            postfixContent = _get_content(grader, self.postfixFilePath)

            solutionPath = Path(self.pathTo, self.filename)
            newContent = ''.join((prefixContent, solutionContent, postfixContent))
            solutionPath.write_text(newContent)

            return func(grader)

        return wrapper


class CheckSubmissionFilename:
    def __init__(self, filename):
        self.filename = filename

    def __call__(self, func):
        @wraps(func)
        def wrapper(grader):
            path = next(grader.dirSubmission.iterdir())

            if self.filename != path.name:
                grader.abortExecution(
                    f'Error. Invalid solution file name: {path.name}. The file must '
                    f'be named {self.filename}.'
                )

            return func(grader)

        return wrapper


class CopySolutionFile:
    def __init__(self, pathTo=None, filename=None):
        self.pathTo = pathTo
        self.filename = filename

    def __call__(self, func):
        @wraps(func)
        def wrapper(grader):
            if self.pathTo is None:
                self.pathTo = Path(grader.cwd, grader.testsDir)
            else:
                self.pathTo = Path(grader.cwd, self.pathTo)

            # create if not exist
            self.pathTo.mkdir(parents=True, exist_ok=True)

            if self.filename is not None:
                grader.solutionFilename = self.filename

            try:
                source = next(grader.dirSubmission.iterdir())
                destination = Path(self.pathTo, grader.solutionFilename)
                shutil.copyfile(source.absolute(), destination.absolute())
            except BaseException as err:
                grader.abortExecution(
                    f'Grader error. Error copying solution file.\n{err}'
                )
            return func(grader)

        return wrapper


class RunUnittestTests:
    def __init__(self, test_result_class=None, failfast=True, traceback=True,
                 verbosity=1, pass_rate=1):
        self.failfast = failfast
        self.testResultClass = test_result_class or LogTestResult
        self.verbosity = verbosity
        self.traceback = traceback
        self.passRate = pass_rate
        unittest.TestCase.longMessage = self.traceback

    def __call__(self, func):
        @wraps(func)
        def wrapper(grader):
            unittest.TestCase.longMessage = self.traceback
            suite = _getTestSuite(grader)

            result = self.testResultClass(
                grader.feedbackLogger,
                grader.scoreLogger,
                verbosity=self.verbosity,
                failfast=self.failfast,
                total_tests=suite.countTestCases(),
                pass_rate=self.passRate
            )
            grader.feedbackLogger.error(result.separator)
            grader.feedbackLogger.error(f'Test result of the task: "{grader.taskName}"')
            grader.feedbackLogger.error(f'Attempt at {datetime.now().ctime()}.')

            try:
                grader.testResult = suite.run(result)
            except BaseException as err:
                grader.abortExecution(
                    f'Grader error. The launch of the tests ended with the fall of '
                    f'the grader.\n{err}'
                )

            grader.testResult.wasSuccessful()
            return func(grader)

        return wrapper
