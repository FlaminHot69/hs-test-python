import unittest
from inspect import cleandoc
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class FeedbackOnExceptionTest2(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(feedback_on_exception={
                ZeroDivisionError: 'Do not divide by zero!',
                AttributeError: 'Attribute Error raised!'
            })
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(True, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = FeedbackOnExceptionTest2('main').run_tests()

        self.assertEqual(cleandoc('''\
            Exception in test #1
            
            Attribute Error raised!
            
            Traceback (most recent call last):
              File "main.py", line 1, in <module>
                raise AttributeError()
            AttributeError'''), feedback)

        self.assertEqual(status, -1)
