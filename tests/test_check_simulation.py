import os
import unittest
import pathlib
import mopyregtest

this_folder = pathlib.Path(__file__).absolute().parent
initial_cwd = os.getcwd()

class TestCheckSimulation(unittest.TestCase):
    def test_check_simulation_success(self):
        """
        Test that check_simulation passes for a model that builds and simulates.
        DoesNotFinish builds and produces a result CSV, even though it does not reach
        the simulation end time. check_simulation should succeed because a result is produced.
        """
        os.chdir(initial_cwd)

        tester = mopyregtest.RegressionTest(package_folder=this_folder / "data/FlawedModels",
                                           model_in_package="FlawedModels.DoesNotFinish",
                                           result_folder=this_folder / "data/FlawedModels/results")

        tester.check_simulation()

        tester.cleanup(ask_confirmation=False)

        return

    def test_check_simulation_build_failure(self):
        """
        Test that check_simulation raises AssertionError for a model that does not build.
        """
        os.chdir(initial_cwd)

        tester = mopyregtest.RegressionTest(package_folder=this_folder / "data/FlawedModels",
                                           model_in_package="FlawedModels.DoesNotBuild",
                                           result_folder=this_folder / "data/FlawedModels/results")

        self.assertRaises(AssertionError, tester.check_simulation)

        tester.cleanup(ask_confirmation=False)

        return


if __name__ == '__main__':
    unittest.main()
