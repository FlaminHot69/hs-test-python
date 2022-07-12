from typing import List

from hstest import wrong, TestCase
from hstest.testing.tested_program import TestedProgram
from hstest.testing.unittest.user_error_test import UserErrorTest


class FindModuleNoInfoAnalyzeImports(UserErrorTest):
    contain = [
        'Error in test #1',
        'Cannot find a file to execute your code in directory'
    ]

    def test1(self):
        main = TestedProgram('main')
        main.start()
        return wrong('')

    def generate(self) -> List[TestCase]:
        return [
            TestCase(dynamic_testing=self.test1)
        ]
