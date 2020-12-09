from typing import Optional, List

from hstest.check_result import CheckResult, correct
from hstest.common.file_utils import create_files, delete_files
from hstest.dynamic.output.output_handler import OutputHandler
from hstest.exception.outcomes import ExceptionWithFeedback
from hstest.exceptions import TestPassed
from hstest.test_case import TestCase
from hstest.testing.runner.test_runner import TestRunner
from hstest.testing.tested_program import TestedProgram


class TestRun:
    def __init__(self, test_num: int, test_count: int, test_case: TestCase, test_rummer: TestRunner):
        self._test_num: int = test_num
        self._test_count: int = test_count
        self._test_case: TestCase = test_case
        self._test_runner: TestRunner = test_rummer

        self._input_used: bool = False
        self._error_in_test: Optional[BaseException] = None
        self._tested_programs: List[TestedProgram] = []

    @property
    def test_num(self) -> int:
        return self._test_num

    @property
    def test_count(self) -> int:
        return self._test_count

    @property
    def test_case(self) -> TestCase:
        return self._test_case

    @property
    def input_used(self) -> bool:
        return self._input_used

    @property
    def error_in_test(self) -> Optional[BaseException]:
        return self._error_in_test

    def set_error_in_test(self, err: Optional[BaseException]):
        if self._error_in_test is None or err is None:
            self._error_in_test = err

    def set_input_used(self):
        self._input_used = True

    def add_tested_program(self, tested_program: TestedProgram):
        self._tested_programs += [tested_program]

    def stop_tested_programs(self):
        for tested_program in self._tested_programs:
            tested_program.stop()

    def test(self) -> CheckResult:
        create_files(self._test_case.files)
        # startThreads(testCase.getProcesses())

        OutputHandler.reset_output()
        result = self._test_runner.test(self)

        # stopThreads(testCase.getProcesses(), pool)
        delete_files(self._test_case.files)

        if result is None:
            self._check_errors()

        if isinstance(self._error_in_test, TestPassed):
            return correct()

        return result

    def _check_errors(self):
        error_in_test = self._error_in_test
        test_case = self._test_case

        if error_in_test is None:
            return

        if isinstance(error_in_test, TestPassed):
            return

        if isinstance(error_in_test, ExceptionWithFeedback):
            user_exception = error_in_test.real_exception

            for exception, feedback in test_case.feedback_on_exception.items():
                ex_type = type(user_exception)
                if ex_type is not None and issubclass(ex_type, exception):
                    raise ExceptionWithFeedback(feedback, user_exception)

        raise error_in_test
