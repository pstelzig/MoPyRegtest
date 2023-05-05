"""
Example of how to use MoPyRegtest to perform regression tests. 

MIT License. See the project's LICENSE file.

(c) Dr. Philipp Emanuel Stelzig, 2019. 
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

# Path to Modelica library or model to be tested. Here Modelica.Electrial
if platform.system() == 'Windows':
    package_folder = pathlib.Path.home() / "AppData/Roaming/.openmodelica/libraries/Modelica 4.0.0+maint.om"
else:
    package_folder = pathlib.Path.home() / ".openmodelica/libraries/Modelica 4.0.0+maint.om/Electrical"

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
class TestElectricalAnalogExamples(unittest.TestCase):

    # Testing Modelica.Electrical.Analog.Examples.HeatingRectifier
    def test_HeatingRectifier(self):
        tester = mopyregtest.RegressionTest(package_folder=package_folder,
                                            model_in_package="Modelica.Electrical.Analog.Examples.HeatingRectifier",
                                            result_folder=result_folder / "Modelica.Electrical.Analog.Examples.HeatingRectifier",
                                            modelica_version="4.0.0",
                                            dependencies=None)
        tester.compare_result(reference_result=str(reference_folder / "Modelica.Electrical.Analog.Examples.HeatingRectifier_res.csv"), precision=3)

        # Deletes result_folder after it has been created. Leave out if you feel uncomfortable with auto-deletion!
        #tester.cleanup()

        return

    # Testing Modelica.Electrical.Analog.Examples.CharacteristicIdealDiodes
    def test_CharacteristicIdealDiodes(self):
        tester = mopyregtest.RegressionTest(package_folder=package_folder,
                                            model_in_package="Modelica.Electrical.Analog.Examples.CharacteristicIdealDiodes",
                                            result_folder=result_folder / "Modelica.Electrical.Analog.Examples.CharacteristicIdealDiodes",
                                            modelica_version="4.0.0",
                                            dependencies=None)
        tester.compare_result(reference_result=str(reference_folder / "Modelica.Electrical.Analog.Examples.CharacteristicIdealDiodes_res.csv"), precision=3,
                              metric=lambda r_ref, r_act: np.linalg.norm(r_ref[:, 1] - r_act[:, 1], ord=1.0))

        # Deletes result_folder after it has been created. Leave out if you feel uncomfortable with auto-deletion!
        #tester.cleanup()

        return

    # Testing closeness for Modelica.Electrical.Analog.Examples.CharacteristicIdealDiodes in the L2-norm
    def test_CharacteristicIdealDiodes_L2(self):
        tester = mopyregtest.RegressionTest(package_folder=package_folder,
                                            model_in_package="Modelica.Electrical.Analog.Examples.CharacteristicIdealDiodes",
                                            result_folder=result_folder / "Modelica.Electrical.Analog.Examples.CharacteristicIdealDiodes",
                                            modelica_version="4.0.0",
                                            dependencies=None)
        tester.compare_result(reference_result=str(reference_folder / "Modelica.Electrical.Analog.Examples.CharacteristicIdealDiodes_res.csv"), precision=3,
                              metric=functools.partial(mopyregtest.metrics.Lp_dist, p=2.0))

        # Deletes result_folder after it has been created. Leave out if you feel uncomfortable with auto-deletion!
        #tester.cleanup()

        return

if __name__ == '__main__':
    unittest.main()
