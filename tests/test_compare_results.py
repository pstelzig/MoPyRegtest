import unittest
import pathlib
import os
import mopyregtest

this_folder = pathlib.Path(__file__).absolute().parent

class TestCompareResults(unittest.TestCase):
    def test_time_col_ignored(self):
        """
        Validates that time as a validated column is ignored in the result comparison
        """

        self.assertRaises(ValueError, mopyregtest.RegressionTest.compare_csv_files,
                          reference_result="../examples/test_user_defined_metrics/references/Sine_res.csv",
                          simulation_result="../examples/test_user_defined_metrics/references/Sine_res.csv",
                          validated_cols=["time"])

    def test_disjoint_cols(self):
        """
        Validate that test of two CSV result files that have no common result variable besides time fails
        """
        self.assertRaises(ValueError, mopyregtest.RegressionTest.compare_csv_files,
                          reference_result="../examples/test_Modelica_Electrical_Analog_Examples/references/Modelica.Electrical.Analog.Examples.CharacteristicIdealDiodes_res.csv",
                          simulation_result="../examples/test_user_defined_metrics/references/Sine_res.csv")
        return

    def test_validated_cols_not_contained1(self):
        """
        Validate that comparison fails if not all elements of validated cols are contained in both reference and actual
        result.
        """

        self.assertRaises(ValueError, mopyregtest.RegressionTest.compare_csv_files,
                          reference_result="../examples/test_user_defined_metrics/references/Sine_res.csv",
                          simulation_result="../examples/test_user_defined_metrics/references/SineNoisy_res.csv",
                          validated_cols=["y", "not_present_var"])
        return

    def test_validated_cols_not_contained2(self):
        """
        Validate that comparison fails if not all elements of validated cols are contained in both reference and actual
        result. Case: Column not contained in reference_result.
        """

        self.assertRaises(ValueError, mopyregtest.RegressionTest.compare_csv_files,
                          reference_result="../examples/test_user_defined_metrics/references/Sine_res.csv",
                          simulation_result="../examples/test_user_defined_metrics/references/SineNoisy_res.csv",
                          validated_cols=["y", "uniformNoise.y"])
        return

    def test_validated_cols_not_contained3(self):
        """
        Validate that comparison fails if not all elements of validated cols are contained in both reference and actual
        result. Case: Column not contained in simulation_result.
        """

        self.assertRaises(ValueError, mopyregtest.RegressionTest.compare_csv_files,
                          reference_result="../examples/test_user_defined_metrics/references/SineNoisy_res.csv",
                          simulation_result="../examples/test_user_defined_metrics/references/Sine_res.csv",
                          validated_cols=["y", "uniformNoise.y"])
        return

    def test_write_comparison_timeseries1(self):
        """
        Validate that writing a comparison timeseries on failed tests can be switched off using the write_comparison
        argument.
        """

        compare_file_path = (this_folder / "../examples/test_user_defined_metrics/references/Sine_res_comparison.csv")

        if compare_file_path.exists():
            os.remove(compare_file_path)

        self.assertRaises(AssertionError, mopyregtest.RegressionTest.compare_csv_files,
                          reference_result="../examples/test_user_defined_metrics/references/SineNoisy_res.csv",
                          simulation_result="../examples/test_user_defined_metrics/references/Sine_res.csv",
                          tol=1e-5,
                          validated_cols=["y"],
                          write_comparison=False)
        self.assertFalse(compare_file_path.exists())

        return

    def test_write_comparison_timeseries2(self):
        """
        Validate that a comparison timeseries is written on a failed test by default.
        """

        compare_file_path = (this_folder / "../examples/test_user_defined_metrics/references/Sine_res_comparison.csv")

        if compare_file_path.exists():
            os.remove(compare_file_path)

        self.assertRaises(AssertionError, mopyregtest.RegressionTest.compare_csv_files,
                          reference_result="../examples/test_user_defined_metrics/references/SineNoisy_res.csv",
                          simulation_result="../examples/test_user_defined_metrics/references/Sine_res.csv",
                          tol=1e-5,
                          validated_cols=["y"])
        self.assertTrue(compare_file_path.exists())

        return


if __name__ == '__main__':
    unittest.main()
