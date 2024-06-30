import os
import unittest
import pathlib
import mopyregtest

this_folder = pathlib.Path(__file__).absolute().parent
initial_cwd = os.getcwd()

class TestModelErrors(unittest.TestCase):
    def test_build_errors(self):
        # Exception in RegressionTest._import_and_simulate raised before RegressionTest switches back to initial_cwd
        os.chdir(initial_cwd)

        tester = mopyregtest.RegressionTest(package_folder=this_folder / "data/FlawedModels",
                                          model_in_package="FlawedModels.DoesNotBuild",
                                          result_folder=this_folder / "data/FlawedModels/results")

        self.assertRaises(AssertionError, tester._import_and_simulate)

        tester.cleanup(ask_confirmation=False)

        return

    def test_simulate_errors1(self):
        """
        This test runs a simulation model that will build and run, but the simulation will not reach the
        targeted simulation end time. An error will _not_ be thrown by _import_and_simulate. This is because
        for regression we do not care about simulation end times, but about reproducibility.
        """

        # Exception in RegressionTest._import_and_simulate raised before RegressionTest switches back to initial_cwd
        os.chdir(initial_cwd)

        tester = mopyregtest.RegressionTest(package_folder=this_folder / "data/FlawedModels",
                                          model_in_package="FlawedModels.DoesNotFinish",
                                          result_folder=this_folder / "data/FlawedModels/results")

        tester._import_and_simulate()

        tester.cleanup(ask_confirmation=False)

        return


if __name__ == '__main__':
    unittest.main()
