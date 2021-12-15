import unittest

from hstest import TestedProgram
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest.testing.plotting.drawing.drawing_library import DrawingLibrary
from tests.outcomes.plot.box.test_box_drawing import test_box_drawing


class TestMatplotlibBox(PlottingTest):
    @dynamic_test
    def test(self):
        program = TestedProgram()
        program.start()

        return test_box_drawing(self.all_figures(), 2, DrawingLibrary.matplotlib)


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestMatplotlibBox('main').run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()