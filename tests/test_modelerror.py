import unittest
import pathlib
import mopyregtest

this_folder = pathlib.Path(__file__).absolute().parent

class TestModelErrors(unittest.TestCase):
    def test_build_errors(self):
        tester = mopyregtest.RegressionTest(package_folder=this_folder / "data/FlawedModels",
                                          model_in_package="FlawedModels.DoesNotBuild",
                                          result_folder=this_folder / "data/FlawedModels")

        self.assertRaises(AssertionError, tester._import_and_simulate)

        tester.cleanup(ask_confirmation=False)

        return

    def test_simulate_errors(self):
        tester = mopyregtest.RegressionTest(package_folder=this_folder / "data/FlawedModels",
                                          model_in_package="FlawedModels.DoesNotFinish",
                                          result_folder=this_folder / "data/FlawedModels")

        self.assertRaises(AssertionError, tester._import_and_simulate)

        tester.cleanup(ask_confirmation=False)

        return