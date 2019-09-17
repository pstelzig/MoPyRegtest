# Usage
This file guides you through the examples on how to use the `mopyregtest` module to perform simple and quick regression testing on Modelica models. 


## Example `test_Modelica_Electrical_Analog_Examples`
In the example (see the folder `examples/test_Modelica_Electrical_Analog_Examples`) `MoPyRegtest` is used to perform regression testing on two examples from the Modelica standard library, namely
* `Modelica.Electrical.Analog.Examples.HeatingResistor`
* `Modelica.Electrical.Analog.Examples.Rectifier`

The whole test definition and the explanation of what follows is contained in the file `examples/test_Modelica_Electrical_Analog_Examples/test_modelica_electrical_analog_examples.py`. **Here we show how the example has been set up.** 

Both regression tests shall be done as a single test case, so that e.g. all examples in `Modelica.Electrical.Analog.Examples` are handled in the same test case. 


### Step 1: Folder to hold test case
Create the folder `examples/test_Modelica_Electrical_Analog_Examples`. This is where the test definition and the intermediate test results go. 


To help `unittest` identify this as a test, start the folder name with `test_`. 


It is strongly recommended to avoid the `.` character in folder names since Python interprets anything following the `.` in the folder name as a reference to a Python package. 


### Step 2: Reference results
Create the folder `examples/test_Modelica_Electrical_Analog_Examples/references`. This is where the reference results for the models `Modelica.Electrical.Analog.Examples.HeatingResistor` and `Modelica.Electrical.Analog.Examples.Rectifier` shall be copied in the `.csv` format. In our case, you shall find

```
examples/test_Modelica_Electrical_Analog_Examples/references/Modelica.Electrical.Analog.Examples.HeatingResistor_res.csv
examples/test_Modelica_Electrical_Analog_Examples/references/Modelica.Electrical.Analog.Examples.Rectifier_res.csv
```


### Step 3: Test definition
Create the file `examples/test_Modelica_Electrical_Analog_Examples/test_modelica_electrical_analog_examples.py`. The file name is not important, other than having it start with `test_` and end with `.py`. This file contains the entire test definition. 


This section defines the essential imports to run the test. For other test definitions, the relative loction of the `mopyregtest` module to the test definition file might be different and has to be adapted. In this case it location relative to `test_modelica_electrical_analog_examples.py` is `../../src/`. 

```
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
```


The next section defines variables that hold the location of the package the model to be tested is situated in. The definition below is the case of an Ubuntu installation where the OpenModelica system libraries are found under `/usr/lib/omlibrary/`. Under Windows this would be something like `C:\OpenModelica1.13.264bit\lib\omlibrary`. For other test scenarios this would be the absolute path to a user developed Modelica package. The `package_folder` variable holds the path to the actual package the model to be tested is situated in. More precisely, we look for the file `<package_folder>/package.mo`. The `result_folder` is where the intermediate results generated in translating, building and executing the actual model to be tested go. The `reference_folder` is where the reference simulation result files in `.csv` format are to be found. 

```
# Setup the test data #########################################################
# Example here for a Ubuntu environment with OpenModelica 
# installed like in https://openmodelica.org/download/download-linux

# Path to Modelica library or model to be tested. Here Modelica.Electrical
package_folder = "/usr/lib/omlibrary/Modelica 3.2.2/Electrical/"

# Where to put results from this test
result_folder = this_folder

# Where to find reference results for this test
reference_folder = this_folder / "references"
```


This section defines the actual test, which is the class `TestElectricalAnalogExamples`. It derives from `unittest.TestCase` and thus makes it manageable by the `unittest` module. The naming is important, the class (like in the [`PEP8` style guide for Python](https://www.python.org/dev/peps/pep-0008/)) shall be camelcase and start with `Test`, and all of its methods start with a lower case `test_`. See the [`unittest` documentation](https://docs.python.org/3/library/unittest.html) for details. Note that one child class of `unittest.TestCase` defines a test case -- if you want to split into multiple test cases, create multiple classes. 
Inside each `test_` method, the actual `MoPyRegtest` object `tester` to perform the regression test is instantiated. The constructor of `mopyregtest.RegressionTest` gets the 
* package folder of the Modelica model to be tested in `package_folder=`
* the actual Modelica model name in this package in `model_in_package=`
* the result folder where the simulation output goes in `result_folder=`. 
The actual execution and comparison with the reference result is done in `tester.compare_result`, which gets the path to the reference result as an argument in `reference_result=`. Finally, if `test.cleanup()` is called, the intermediate results are deleted automatically provided their containing folder has been created in the process. **Leave this out if you feel uncomfortable with auto-deletion** and prefer to delete manually. Note that **result folders for failed tests will not be deleted** in order to trace back any issues. 

```
# Define the test #############################################################
class TestElectricalAnalogExamples(unittest.TestCase):

    # Testing Modelica.Electrical.Analog.Examples.HeatingResistor
    def test_HeatingResistor(self):
        tester = mopyregtest.RegressionTest(package_folder=package_folder,
                                            model_in_package="Modelica.Electrical.Analog.Examples.HeatingResistor",
                                            result_folder=result_folder / "Modelica.Electrical.Analog.Examples.HeatingResistor")
        tester.compare_result(reference_result=str(reference_folder / "Modelica.Electrical.Analog.Examples.HeatingResistor_res.csv"))

        # Deletes result_folder after it has been created. Leave out if you feel uncomfortable with auto-deletion!
        tester.cleanup()

        return

    # Testing Modelica.Electrical.Analog.Examples.Rectifier
    def test_HeatingResistor(self):
        tester = mopyregtest.RegressionTest(package_folder=package_folder,
                                            model_in_package="Modelica.Electrical.Analog.Examples.Rectifier",
                                            result_folder=result_folder / "Modelica.Electrical.Analog.Examples.Rectifier")
        tester.compare_result(reference_result=str(reference_folder / "Modelica.Electrical.Analog.Examples.Rectifier_res.csv"))

        # Deletes result_folder after it has been created. Leave out if you feel uncomfortable with auto-deletion!
        tester.cleanup()

        return
```


This last part is to make the file `test_modelica_electrical_analog_examples.py` itself an executable test case. 

```
if __name__ == '__main__':
    unittest.main()
```

The test case can now be run from a command line in the folder `examples/test_Modelica_Electrical_Analog_Examples/` by typing

```
$ python3 test_modelica_electrical_analog_examples.py
```


### Step 4: Turn into Python module for test discovery
If you want to have this test in `test_modelica_electrical_analog_examples.py` to be found automatically by Python `unittest` you need to turn the containing folder `test_Modelica_Electrical_Analog_Examples` into a Python module. This is simply done by adding the (empty) file `examples/test_Modelica_Electrical_Analog_Examples/__init__.py`. Also see the [documentation of `unittest` on test discovery](https://docs.python.org/3/library/unittest.html#test-discovery). 

To verify, open a command line terminal and change to the folder `examples` and run

```
python3 -m unittest
```

which should trigger the same tests as when running `python3 test_modelica_electrical_analog_examples.py` and potentially many more tests in the examples folder
