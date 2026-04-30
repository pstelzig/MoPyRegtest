# Automatic test generation

MoPyRegtest can auto-generate `unittest` test files for Modelica models, either from the command line or from a Python script.
For the full API reference, see [doc/usage.md](/doc/usage.md).

## From the command line

The `mopyregtest generate` command creates a test file and (in regression mode) generates missing reference results.

```bash
# Regression test (default) — compares simulation output against reference CSV
mopyregtest generate --metric=Lp_dist --tol=1.25e-5 \
    ./gen_tests BlocksLpDist \
    ~/".openmodelica/libraries/Modelica 4.0.0+maint.om/" \
    Modelica.Blocks.Sources.Sine,Modelica.Blocks.Sources.ExpSine,Modelica.Blocks.Sources.Step

# Simulation-only test — just checks that the model simulates successfully
mopyregtest generate --mode=simulation \
    ./gen_tests BlocksSimCheck \
    ~/".openmodelica/libraries/Modelica 4.0.0+maint.om/" \
    Modelica.Blocks.Examples.Filter
```

Run the generated test:
```bash
cd gen_tests
python3 test_blockslpdist.py
```

Use `mopyregtest generate --help` for all options (metric, tolerance, pre-existing references, etc.).

## From a Python script

### Regression tests
See [gentests_modelica_blocks_sources.py](gentests_modelica_blocks_sources.py):

```python
gen = mopyregtest.Generator(
    package_folder=package_folder,
    models_in_package=["Modelica.Blocks.Sources.Sine", "Modelica.Blocks.Sources.Step"],
    metric=mopyregtest.metrics.abs_dist_ptwise,
    tol=0.12)
gen.generate_tests(test_folder="./gen_tests", test_name="MyTest", test_results_folder="./results")
```

You can supply pre-existing references via the `references` parameter and use custom metrics as strings 
(see [doc/usage.md](/doc/usage.md#custom-metrics)).

### Simulation-only tests
See [gentests_simulation_check.py](gentests_simulation_check.py):

```python
gen = mopyregtest.Generator(
    package_folder=package_folder,
    models_in_package=["Modelica.Blocks.Examples.Filter"],
    mode="simulation")
gen.generate_tests(test_folder="./gen_tests", test_name="MySimTest", test_results_folder="./results")
```

No reference results are generated or needed. The test calls `check_simulation()` instead of `compare_result()`.
