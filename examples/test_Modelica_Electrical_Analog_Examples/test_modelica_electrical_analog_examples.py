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
import mopyregtest

# Setup the test data #########################################################
# Example here for a Ubuntu environment with OpenModelica 
# installed like in https://openmodelica.org/download/download-linux
# and using the default OpenModelica package manager

# Path to Modelica library or model to be tested. Here Modelica.Electrial
package_folder = pathlib.Path(pathlib.os.environ["HOME"]) / "Modelica 4.0.0+maint.om/Electrical"

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
        tester.compare_result(reference_result=str(reference_folder / "Modelica.Electrical.Analog.Examples.HeatingRectifier_res.csv"))

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
        tester.compare_result(reference_result=str(reference_folder / "Modelica.Electrical.Analog.Examples.CharacteristicIdealDiodes_res.csv"))

        # Deletes result_folder after it has been created. Leave out if you feel uncomfortable with auto-deletion!
        #tester.cleanup()

        return


if __name__ == '__main__':
    unittest.main()
