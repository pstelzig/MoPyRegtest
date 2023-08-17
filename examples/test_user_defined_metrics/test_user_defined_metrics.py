"""
Example of how to use MoPyRegtest to perform regression tests. 

MIT License. See the project's LICENSE file.

(c) Dr. Philipp Emanuel Stelzig, 2023.
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
# Example here for a Ubuntu environment with OpenModelica 
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
class TestUserDefinedMetrics(unittest.TestCase):

    # Example for a user defined metric on a Modelica simulation result against a noisy reference result
    def test_Sine(self):
        tester = mopyregtest.RegressionTest(package_folder=package_folder,
                                            model_in_package="Modelica.Blocks.Sources.Sine",
                                            result_folder=result_folder / "Modelica.Blocks.Sources.Sine",
                                            modelica_version="4.0.0",
                                            dependencies=None)

        # Comparing results by computing the L^2([T_min,T_max])-norm of the result difference (as piecewise constant functions over [T_min,T_max])
        tester.compare_result(reference_result=str(reference_folder / "SineNoisy_res.csv"),
                              metric=functools.partial(mopyregtest.metrics.Lp_dist, p=2),
                              validated_cols=["y"], tol=2e-3, fill_in_method="interpolate")

        # Deletes result_folder after it has been created. Leave out if you feel uncomfortable with auto-deletion!
        #tester.cleanup()

        return

    @staticmethod
    def metric_different_timestamps(r_ref, r_act):
        """
        Example for a L^2-norm like metric for r_ref and r_act even if dimensions or timestamps are not matching.
        Resamples timestamps with linear interpolation and then uses the trapezoidal rule to compute the integral.
        """
        # Resample both r_ref and r_act to 100 uniformly distributed timestamps using linear interpolation
        tStart = min(r_ref[0, 0], r_act[0, 0])
        tEnd = max(r_ref[-1, 0], r_act[-1, 0])
        tSamples = np.linspace(start=tStart, stop=tEnd, num=100)

        y_ref_resmpl = np.interp(tSamples, r_ref[:,0], r_ref[:,1])
        y_act_resmpl = np.interp(tSamples, r_act[:,0], r_act[:,1])

        # Compute the integral of the squared difference, then take root to get L^2([tStart, tEnd]) norm
        delta = np.transpose(np.vstack([tSamples, np.square(y_act_resmpl - y_ref_resmpl)]))
        res = np.sqrt(np.trapz(y=delta[:, 1], x=delta[:, 0]))

        return res

    # Example for a user defined metric and without applying timestamp unification
    def test_Sine_no_unification(self):
        tester = mopyregtest.RegressionTest(package_folder=package_folder,
                                            model_in_package="Modelica.Blocks.Sources.Sine",
                                            result_folder=result_folder / "Modelica.Blocks.Sources.Sine",
                                            modelica_version="4.0.0",
                                            dependencies=None)

        # Comparing results without timestamp unification, but using a self-defined metric that can still compare results
        tester.compare_result(reference_result=str(reference_folder / "SineNoisy_res.csv"),
                              metric=TestUserDefinedMetrics.metric_different_timestamps,
                              validated_cols=["y"], tol=2e-3, unify_timestamps=False)

        # Deletes result_folder after it has been created. Leave out if you feel uncomfortable with auto-deletion!
        #tester.cleanup()

        return

if __name__ == '__main__':
    unittest.main()
