from typing import List, Any

from hstest import CheckResult
from hstest.test_case import TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


class TestOutputWithStderrAndWithStdout(UserErrorTest):
    contain = """
    Wrong answer in test #1

    Please find below the output of your program during this failed test.
    
    ---
    
    User stdout output!
    User stdout output!
    User stdout output!
    """

    def generate(self) -> List[TestCase]:
        return [
            TestCase()
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult.wrong('')
