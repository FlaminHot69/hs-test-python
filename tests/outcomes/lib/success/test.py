import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.common.reflection_utils import get_main
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class SuccessTest(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin='2\n4', attach='6\n'),
            TestCase(stdin='1\n3', attach='4\n'),
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(reply == attach, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = SuccessTest(get_main()).run_tests()
        self.assertEqual(status, 0)
        self.assertEqual(feedback, 'test OK')
