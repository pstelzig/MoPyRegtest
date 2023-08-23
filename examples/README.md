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
can be found in 
[test_Modelica_Electrical_Analog_Examples/README.md](/examples/test_Modelica_Electrical_Analog_Examples/README.md).

### Automatic test case generation
* Go to [generate_tests](/examples/generate_tests)
* Copy and modify the file [gentests_modelica_blocks_sources.py](/examples/generate_tests/gentests_modelica_blocks_sources.py) according to your needs
* Execute the modified file like `python3 gentests_modelica_blocks_sources.py` (or whatever you named the file now) 
  to create the regression tests defined in that file
* This will produce MoPyRegtest test case definitions in test_blocksuserdef.py (or how you adapted it) and copy all
  the reference files into a subfolder `references`. The test cases can then be executed 
  like `python3 test_blocksuserdef.py`

For a more in-depth explanation turn to
[generate_tests/README.md](/examples/generate_tests/README.md).
