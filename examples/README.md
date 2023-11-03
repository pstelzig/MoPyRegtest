# Usage
This file guides you through the examples on how to use the `mopyregtest` module to perform simple and quick regression 
testing on Modelica models. 

## Quick start

### Manual test case definition
Really quick introduction (read the in-depth explanation below to know what you are doing!): 
* Install MoPyRegtest with pip like described in the [main README.md](/README.md), e.g. with `pip3 install --user .`
* Go to [test_Modelica_Electrical_Analog_Examples](/examples/test_Modelica_Electrical_Analog_Examples)
* Copy and modify the file [test_modelica_electrical_analog_examples.py](/examples/test_Modelica_Electrical_Analog_Examples/test_modelica_electrical_analog_examples.py) according to your needs
* Execute the modified file like `python3 test_modelica_electrical_analog_examples.py`
  (or whatever you named the file now) to run regression tests on your own Modelica package and models

A more in-depth explanation of how the provided example works, what happens and how the example was created 
can be found in 
[test_Modelica_Electrical_Analog_Examples/README.md](/examples/test_Modelica_Electrical_Analog_Examples/README.md).

### Automatic test case generation
There are two different ways to auto-generate test case definitions. 
Examples can be found in the [folder generate_tests](/examples/generate_tests)

* Generate test definitions using the [command line tool `mopyregtest`](/examples/generate_tests/README.md#from-the-command-line), or
* [Use a generator script](/examples/generate_tests/README.md#using-a-generator-script): 
  * Copy and modify the file [gentests_modelica_blocks_sources.py](/examples/generate_tests/gentests_modelica_blocks_sources.py) according to your needs
  * Execute the modified file like `python3 gentests_modelica_blocks_sources.py` (or whatever you named the file now) 
    to create the regression tests defined in that file
  * This will produce MoPyRegtest test case definitions in test_blocksuserdef_from_script.py (or how you adapted it) and copy all
    the reference files into a subfolder called references. The test cases can then be executed
    like `python3 test_blocksuserdef_from_script.py`

For a more in-depth explanation turn to
[generate_tests/README.md](/examples/generate_tests/README.md).
