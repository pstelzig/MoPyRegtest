import unittest
import mopyregtest

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
