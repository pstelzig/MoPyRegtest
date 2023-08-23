# Usage
This file guides you through the examples on how to use the `mopyregtest` module to perform simple and quick regression 
testing on Modelica models. 


## Quick start

### Manual test case definition
Really quick introduction (read the in-depth explanation below to know what you are doing!): 
* Install MoPyRegtest locally (!) from the same folder where its [setup.py](/setup.py) is found with pip, e.g. like `pip3 install --user .`
* Go to [test_Modelica_Electrical_Analog_Examples](/examples/test_Modelica_Electrical_Analog_Examples)
* Copy and modify the file [test_modelica_electrical_analog_examples.py](/examples/test_Modelica_Electrical_Analog_Examples/test_modelica_electrical_analog_examples.py) according to your needs
* Execute the modified file like `python3 test_modelica_electrical_analog_examples.py`
  (or whatever you named the file now) to run regression tests on your own Modelica package and models

A more in-depth explanation of how the provided example works, what happens and how the example was created 
can be found in the following section.

### Automatic test case generation
* Go to [generate_tests](/examples/generate_tests)
* Copy and modify the file [gentests_modelica_blocks_sources.py](/examples/generate_tests/gentests_modelica_blocks_sources.py) according to your needs
* Execute the modified file like `python3 gentests_modelica_blocks_sources.py` (or whatever you named the file now) 
  to create the regression tests defined in that file
* This will produce MoPyRegtest test case definitions in test_blocksuserdef.py (or how you adapted it) and copy all
  the reference files into a subfolder `references`. The test cases can then be executed 
  like `python3 test_blocksuserdef.py`

## Manual test definition example
In the example (see the folder [test_Modelica_Electrical_Analog_Examples](/examples/test_Modelica_Electrical_Analog_Examples)) `MoPyRegtest` is used to perform 
regression testing on three examples from the Modelica standard library, namely
* `Modelica.Electrical.Analog.Examples.HeatingRectifier`
* `Modelica.Electrical.Analog.Examples.CharacteristicIdealDiodes` (twice, using different comparison metrics)

The whole test definition and the explanation of what follows is contained in the file 
[test_modelica_electrical_analog_examples.py](/examples/test_Modelica_Electrical_Analog_Examples/test_modelica_electrical_analog_examples.py). 
**Here we show how the example has been set up.** 

The regression tests shall be done as a single test case. For instance, in this fashion all examples in 
`Modelica.Electrical.Analog.Examples` could be handled in the same test case. 

### Step 1: Folder to hold test case
Have a look at the folder [examples/test_Modelica_Electrical_Analog_Examples](/examples/test_Modelica_Electrical_Analog_Examples). 
This is where the test definition and the intermediate test results go. 

To help `unittest` identify this as a test, the folder name starts with `test_`. 

It is strongly recommended to avoid the `.` character in folder names since Python interprets anything following the `.` 
in the folder name as a reference to a Python package. 

### Step 2: Reference results
Look at the folder `examples/test_Modelica_Electrical_Analog_Examples/references`. 
This is where the reference results for the models 
`Modelica.Electrical.Analog.Examples.HeatingRectifier` and `Modelica.Electrical.Analog.Examples.CharacteristicIdealDiodes` 
are located. Note the `.csv` format. 

### Step 3: Test definition
Look at the file `examples/test_Modelica_Electrical_Analog_Examples/test_modelica_electrical_analog_examples.py`. 
The file name is not important, other than having it start with `test_` and end with `.py`. 
This file contains the entire test definition. 

Make sure to have the `mopyregtest` module installed by running `pip3 install --user .` from the 
[`mopyregtest` root directory](/). Now `mopyregtest` can be imported as a module into the test case definition file. 

The following section in the file defines variables that hold the location of the Modelica package containing the models
we want to test. For other test scenarios this would be the path to a user developed Modelica package.
* The `package_folder` variable holds the path to the actual package the model to be tested is situated in. 
  More precisely, we look for the file `<package_folder>/package.mo`. 
* The `result_folder` is where the intermediate results generated in translating, building and executing the actual 
  model will be stored. 
* The `reference_folder` is where the reference simulation result files in `.csv` format are to be found. 

```python
# Setup the test data #########################################################
# Example here for an Ubuntu environment with OpenModelica
# installed like in https://openmodelica.org/download/download-linux
# and using the default OpenModelica package manager

# Path to Modelica library or model to be tested. Here Modelica.Electrial
if platform.system() == 'Windows':
    package_folder = pathlib.Path.home() / "AppData/Roaming/.openmodelica/libraries/Modelica 4.0.0+maint.om"
else:
    package_folder = pathlib.Path.home() / ".openmodelica/libraries/Modelica 4.0.0+maint.om/Electrical"

# Where to put results from this test
this_folder = pathlib.Path(__file__).absolute().parent
result_folder = this_folder

# Where to find reference results for this test
reference_folder = this_folder / "references"
```

The next section defines the actual test, which is the class `TestElectricalAnalogExamples`. 
It derives from `unittest.TestCase` and thus makes it manageable by the `unittest` module. 
The naming is important, the class (like in the [`PEP8` style guide for Python](https://www.python.org/dev/peps/pep-0008/)) 
shall be camelcase and start with `Test`, and all of its methods start with a lower case `test_`. 
See the [`unittest` documentation](https://docs.python.org/3/library/unittest.html) for details. Note that one child class of `unittest.TestCase` defines a test case. 
If you want to split into multiple test cases, create multiple classes. 
Inside each `test_` method, the `mopyregtest.RegressionTest` object `tester` test is instantiated. It performs the
actual regression. The constructor of `mopyregtest.RegressionTest` gets the 
* package folder of the Modelica model to be tested in `package_folder=`
* the actual Modelica model name in this package in `model_in_package=`
* the result folder where the simulation output goes in `result_folder=`. 

* The execution and comparison with the reference result is done in `tester.compare_result`, which gets the path to
the reference result as an argument in `reference_result=`. 

Finally, if `test.cleanup()` is called, the intermediate results are deleted automatically provided their containing 
folder has been created in the process. 

**Leave this out if you feel uncomfortable with auto-deletion. Use it only after you verified yourself that the respective code does no harm.**
Otherwise, clean up manually. Note that **result folders for failed tests will not be deleted** in order to trace back any issues. 

By default, `test.cleanup()` will ask for user confirmation before cleaning up, i.e. asking user input in the command line. 
In case this is not wanted (e.g. for automated testing), just replace `test.cleanup()` with `tester.cleanup(ask_confirmation=False)`.
**Caution: Use cleanup only if you have made sure that it does not do any harm!**

```python
class TestElectricalAnalogExamples(unittest.TestCase):

    # Testing Modelica.Electrical.Analog.Examples.HeatingRectifier
    def test_HeatingRectifier(self):
        tester = mopyregtest.RegressionTest(package_folder=package_folder,
                                            model_in_package="Modelica.Electrical.Analog.Examples.HeatingRectifier",
                                            result_folder=result_folder / "Modelica.Electrical.Analog.Examples.HeatingRectifier",
                                            modelica_version="4.0.0",
                                            dependencies=None)
        tester.compare_result(reference_result=str(reference_folder / "Modelica.Electrical.Analog.Examples.HeatingRectifier_res.csv"), tol=1e-3)

        # Deletes result_folder after it has been created. Leave out if you feel uncomfortable with auto-deletion!
        #tester.cleanup()

        return
```

If you want to use other metrics for result comparison than the default one, you can add the parameter `metric`
to `tester.compare_result`. E.g. `metric=mopyregtest.metrics.Lp_dist` for the predefined metric with the Lebesgue space norm
in L^2, or `metric=lambda r_ref, r_act: np.linalg.norm(r_ref[:, 1] - r_act[:, 1], ord=1)` as an example for a 
user-defined metric. See the methods in 
[test_modelica_electrical_analog_examples.py](/examples/test_Modelica_Electrical_Analog_Examples/test_modelica_electrical_analog_examples.py),
or the dedicated example [test_user_defined_metrics.py](/examples/test_user_defined_metrics/test_user_defined_metrics.py)

This last part is to make the file 
[test_modelica_electrical_analog_examples.py](/examples/test_Modelica_Electrical_Analog_Examples/test_modelica_electrical_analog_examples.py) 
itself an executable test case. 

```python
if __name__ == '__main__':
    unittest.main()
```

The test case can now be run from a command line in the folder 
[examples/test_Modelica_Electrical_Analog_Examples](/examples/test_Modelica_Electrical_Analog_Examples) by typing

```bash
$ python3 test_modelica_electrical_analog_examples.py
```

### Step 4: Turn into Python module for test discovery
If you want that the tests from 
[test_modelica_electrical_analog_examples.py](/examples/test_Modelica_Electrical_Analog_Examples/test_modelica_electrical_analog_examples.py) 
can be found automatically by 
Python `unittest`, you need to turn the containing folder 
[test_Modelica_Electrical_Analog_Examples](/examples/test_Modelica_Electrical_Analog_Examples) 
into a Python module. 
This is simply done by adding the (empty) file 
[__init__.py](/examples/test_Modelica_Electrical_Analog_Examples/__init__.py) to the folder 
[test_Modelica_Electrical_Analog_Examples](/examples/test_Modelica_Electrical_Analog_Examples)
Also see the [documentation of `unittest` on test discovery](https://docs.python.org/3/library/unittest.html#test-discovery). 

To verify, open a terminal, change to the folder `examples` and run

```bash
python3 -m unittest
```

which should trigger the same tests as when running `python3 test_modelica_electrical_analog_examples.py` and 
potentially many more tests in the examples folder

