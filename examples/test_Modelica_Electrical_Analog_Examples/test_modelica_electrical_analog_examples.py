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

# Where to find MoPyRegtest: Temporarily add mopyregtest module to Python path
this_folder = pathlib.Path(__file__).absolute().parent
import sys      
sys.path.append(str(this_folder / "../../src/"))
import mopyregtest


# Setup the test data #########################################################
# Example here for a Ubuntu environment with OpenModelica 
# installed like in https://openmodelica.org/download/download-linux

# Path to Modelica library or model to be tested. Here Modelica.Electrial
package_folder = "/usr/lib/omlibrary/Modelica 3.2.2/Electrical/"

# Where to put results from this test
result_folder = this_folder

# Where to find reference results for this test
reference_folder = this_folder / "references"


# Define the test #############################################################
class TestElectricalAnalogExamples(unittest.TestCase):

    # Testing Modelica.Electrical.Analog.Examples.HeatingResistor
    def test_HeatingResistor(self):
        tester = mopyregtest.RegressionTest(package_folder=package_folder,
                                            model_in_package="Modelica.Electrical.Analog.Examples.HeatingResistor",
                                            result_folder=result_folder / "Modelica.Electrical.Analog.Examples.HeatingResistor")
        tester.compare_result(reference_result=str(reference_folder / "Modelica.Electrical.Analog.Examples.HeatingResistor_res.csv"))

        # Deletes result_folder after it has been created. Leave out if you feel uncomfortable with auto-deletion!
        #tester.cleanup()

        return

    # Testing Modelica.Electrical.Analog.Examples.CharacteristicIdealDiodes
    def test_CharacteristicIdealDiodes(self):
        tester = mopyregtest.RegressionTest(package_folder=package_folder,
                                            model_in_package="Modelica.Electrical.Analog.Examples.CharacteristicIdealDiodes",
                                            result_folder=result_folder / "Modelica.Electrical.Analog.Examples.CharacteristicIdealDiodes")
        tester.compare_result(reference_result=str(reference_folder / "Modelica.Electrical.Analog.Examples.CharacteristicIdealDiodes_res.csv"))

        # Deletes result_folder after it has been created. Leave out if you feel uncomfortable with auto-deletion!
        #tester.cleanup()

        return


if __name__ == '__main__':
    unittest.main()
