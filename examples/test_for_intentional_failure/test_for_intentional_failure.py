"""
Example of how to use MoPyRegtest to perform regression tests that are
intended to fail.

MIT License. See the project's LICENSE file.

(c) Dr. Philipp Emanuel Stelzig, 2024.
"""

# Preparing the dependencies ##################################################
# Essential
import unittest

# For convenience in handling paths
import pathlib
import platform
import mopyregtest
import sys
import numpy as np
import functools

# Setup the test data #########################################################
# Example here for an Ubuntu environment with OpenModelica
# installed like in https://openmodelica.org/download/download-linux
# and using the default OpenModelica package manager

# Path to Modelica library or model to be tested. Here an element of the Modelica STL.
if platform.system() == 'Windows':
    package_folder = pathlib.Path.home() / "AppData/Roaming/.openmodelica/libraries/Modelica 4.0.0+maint.om"
else:
    package_folder = pathlib.Path.home() / ".openmodelica/libraries/Modelica 4.0.0+maint.om"

if not package_folder.exists():
    error_msg = f"""[ERROR] Path \"{package_folder}\" not found. Aborting.

This example is designed to work with OpenModelica installed to 
standard paths, in order to work out of the box. 

It requires the omc binary to be in the PATH variable and that the Modelica standard 
library version 4.0.0 is installed to {package_folder}. 

If this does not fit your requirements, just adapt the package_folder variable 
in this file to your needs."""
    print(error_msg)
    sys.exit(-1)

# Where to put results from this test
this_folder = pathlib.Path(__file__).absolute().parent
result_folder = this_folder

# Where to find reference results for this test
reference_folder = this_folder / "references"


# Define the test #############################################################
class TestIntentionalFailure(unittest.TestCase):

    # Example for a Modelica simulation that shall fail on comparison with a noisy reference result.
    # No comparison CSV shall be written.
    def test_comparison_fail1(self):
        tester = mopyregtest.RegressionTest(package_folder=package_folder,
                                            model_in_package="Modelica.Blocks.Sources.Sine",
                                            result_folder=result_folder / "Modelica.Blocks.Sources.Sine",
                                            modelica_version="4.0.0",
                                            dependencies=None)

        # Comparing results with default metric
        self.assertRaises(AssertionError, tester.compare_result,
                          reference_result=str(reference_folder / "SineNoisy_res.csv"),
                          validated_cols=["y"], tol=1e-5, fill_in_method="interpolate",
                          write_comparison=False)
        self.assertFalse(
            (this_folder / "Modelica.Blocks.Sources.Sine/Modelica.Blocks.Sources.Sine_res_comparison.csv").exists())

        # Deletes result_folder after it has been created. Leave out if you feel uncomfortable with auto-deletion!
        # tester.cleanup()

        return

    # Example for a Modelica simulation that shall fail on comparison with a noisy reference result.
    # Now a comparison CSV shall be written.
    def test_comparison_fail2(self):
        tester = mopyregtest.RegressionTest(package_folder=package_folder,
                                            model_in_package="Modelica.Blocks.Sources.Sine",
                                            result_folder=result_folder / "Modelica.Blocks.Sources.Sine",
                                            modelica_version="4.0.0",
                                            dependencies=None)

        # Comparing results with default metric
        self.assertRaises(AssertionError, tester.compare_result,
                          reference_result=str(reference_folder / "SineNoisy_res.csv"),
                          validated_cols=["y"], tol=1e-5, fill_in_method="interpolate")
        self.assertTrue(
            (this_folder / "Modelica.Blocks.Sources.Sine/Modelica.Blocks.Sources.Sine_res_comparison.csv").exists())

        # Deletes result_folder after it has been created. Leave out if you feel uncomfortable with auto-deletion!
        # tester.cleanup()

        return


if __name__ == '__main__':
    unittest.main()
