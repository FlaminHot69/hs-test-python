import unittest

from hstest import TestedProgram
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest.testing.plotting.drawing.drawing_library import DrawingLibrary
from tests.outcomes.plot.heatmap.test_heatmap_drawing import test_heatmap_drawing


class TestMatplotlibHeatmap(PlottingTest):
    @dynamic_test
    def test(self):
        program = TestedProgram()
        program.start()

        return test_heatmap_drawing(self.all_figures(), 1, DrawingLibrary.matplotlib)


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestMatplotlibHeatmap().run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
