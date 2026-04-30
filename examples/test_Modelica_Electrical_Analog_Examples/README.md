# Manual regression test example

This example tests two models from the Modelica standard library:
- `Modelica.Electrical.Analog.Examples.HeatingRectifier`
- `Modelica.Electrical.Analog.Examples.CharacteristicIdealDiodes` (with two different metrics)

The complete test definition is in 
[test_modelica_electrical_analog_examples.py](test_modelica_electrical_analog_examples.py).

## Structure

```
test_Modelica_Electrical_Analog_Examples/
├── __init__.py
├── test_modelica_electrical_analog_examples.py   # Test definition
└── references/                                    # Reference CSV files
    ├── ...HeatingRectifier_res.csv
    └── ...CharacteristicIdealDiodes_res.csv
```

## How it works

1. **Setup paths**: `package_folder` points to the Modelica STL, `reference_folder` to the reference CSVs.

2. **Define tests**: Each `test_` method creates a `mopyregtest.RegressionTest` and calls `compare_result()`:

```python
class TestElectricalAnalogExamples(unittest.TestCase):
    def test_HeatingRectifier(self):
        tester = mopyregtest.RegressionTest(
            package_folder=package_folder,
            model_in_package="Modelica.Electrical.Analog.Examples.HeatingRectifier",
            result_folder=result_folder / "...",
            modelica_version="4.0.0")
        tester.compare_result(reference_result="references/..._res.csv", tol=1e-3)
```

3. **Custom metrics**: Use `metric=` to specify a different comparison metric 
   (e.g., `mopyregtest.metrics.Lp_dist` or a lambda). See the test file for examples.

4. **Cleanup**: `tester.cleanup(ask_confirmation=False)` removes intermediate simulation files.
   Omit this to inspect results manually.

## Running

```bash
python3 test_modelica_electrical_analog_examples.py
```

For the full API reference, see [doc/usage.md](/doc/usage.md).
```

The test case can now be run from a command line in the folder 
[examples/test_Modelica_Electrical_Analog_Examples](/examples/test_Modelica_Electrical_Analog_Examples) by typing

```bash
python3 test_modelica_electrical_analog_examples.py
```

## Step 4: Turn into Python module for test discovery
To make sure that the tests from 
[test_modelica_electrical_analog_examples.py](/examples/test_Modelica_Electrical_Analog_Examples/test_modelica_electrical_analog_examples.py) 
can be found automatically by 
Python `unittest`, one needs to turn the containing folder 
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

