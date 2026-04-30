# MoPyRegtest Documentation

## Testing modes

MoPyRegtest supports two testing modes:

| Mode | Method | Purpose |
|------|--------|---------|
| **Regression** (default) | `compare_result()` | Compare simulation output against a reference CSV |
| **Simulation-only** | `check_simulation()` | Verify that a model compiles, builds, and simulates without error |

## Manual test definition

A test is a Python `unittest.TestCase` that uses `mopyregtest.RegressionTest`:

```python
import unittest
import mopyregtest

class TestMyModels(unittest.TestCase):

    def test_heating_rectifier(self):
        tester = mopyregtest.RegressionTest(
            package_folder="~/.openmodelica/libraries/Modelica 4.0.0+maint.om",
            model_in_package="Modelica.Electrical.Analog.Examples.HeatingRectifier",
            result_folder="./results",
            modelica_version="4.0.0")

        # Regression mode: compare against reference
        tester.compare_result(
            reference_result="references/HeatingRectifier_res.csv",
            tol=1e-3)

        tester.cleanup(ask_confirmation=False)

    def test_filter_simulates(self):
        tester = mopyregtest.RegressionTest(
            package_folder="~/.openmodelica/libraries/Modelica 4.0.0+maint.om",
            model_in_package="Modelica.Blocks.Examples.Filter",
            result_folder="./results")

        # Simulation-only mode: just check it runs
        tester.check_simulation()

        tester.cleanup(ask_confirmation=False)

if __name__ == '__main__':
    unittest.main()
```

### Constructor parameters

| Parameter | Description |
|-----------|-------------|
| `package_folder` | Path to the Modelica package (directory containing `package.mo`) |
| `model_in_package` | Fully qualified Modelica model name |
| `result_folder` | Directory for simulation output (created automatically) |
| `modelica_version` | Modelica STL version (`"default"`, `"3.2.3"`, `"4.0.0"`, ...) |
| `dependencies` | Optional list of paths to dependent `.mo` files |

### `compare_result()` parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `reference_result` | — | Path to reference CSV file |
| `tol` | `1e-7` | Tolerance for the comparison metric |
| `validated_cols` | `[]` (all) | List of variable names to validate |
| `metric` | `metrics.norm_infty_dist` | Distance function (see [Metrics](#metrics)) |
| `unify_timestamps` | `True` | Align timestamps before comparison |
| `fill_in_method` | `"ffill"` | How to fill missing data: `"ffill"`, `"bfill"`, `"interpolate"` |
| `write_comparison` | `True` | Write a comparison CSV on failure |

## Automatic test generation

Generate `unittest` test files for multiple models at once.

### From the command line

```bash
# Regression tests (default)
mopyregtest generate ./gen_tests MyTest <package_folder> Model1,Model2,Model3

# With options
mopyregtest generate --metric=Lp_dist --tol=1e-5 ./gen_tests MyTest <package_folder> Model1,Model2

# Simulation-only tests
mopyregtest generate --mode=simulation ./gen_tests MySimTest <package_folder> Model1,Model2

# Supply existing references
mopyregtest generate --references Model1:/path/to/ref1.csv,Model2:/path/to/ref2.csv \
    ./gen_tests MyTest <package_folder> Model1,Model2
```

Run `mopyregtest generate --help` for the full option list.

### From a Python script

```python
import mopyregtest

# Regression tests
gen = mopyregtest.Generator(
    package_folder="~/.openmodelica/libraries/Modelica 4.0.0+maint.om",
    models_in_package=["Modelica.Blocks.Sources.Sine", "Modelica.Blocks.Sources.Step"],
    metric=mopyregtest.metrics.abs_dist_ptwise,
    tol=0.12)
gen.generate_tests(test_folder="./gen_tests", test_name="MyTest", test_results_folder="./results")

# Simulation-only tests
gen = mopyregtest.Generator(
    package_folder="~/.openmodelica/libraries/Modelica 4.0.0+maint.om",
    models_in_package=["Modelica.Blocks.Examples.Filter"],
    mode="simulation")
gen.generate_tests(test_folder="./gen_tests", test_name="MySimTest", test_results_folder="./results")
```

### Generator parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `package_folder` | — | Path to the Modelica package |
| `models_in_package` | — | List of fully qualified model names |
| `mode` | `"regression"` | `"regression"` or `"simulation"` |
| `modelica_version` | `"default"` | Modelica STL version |
| `dependencies` | `None` | List of dependent `.mo` file paths |
| `metric` | `norm_infty_dist` | Predefined metric function or string for custom metrics |
| `tol` | `1e-7` | Tolerance |
| `unify_timestamps` | `True` | Align timestamps before comparison |
| `fill_in_method` | `"ffill"` | Fill-in method for missing data |

## CSV comparison (CLI)

Compare two CSV result files directly without running a simulation:

```bash
mopyregtest compare --metric=Lp_dist --tol=0.015 --validated-cols=y \
    --fill-in-method=interpolate reference.csv actual.csv
```

## Metrics

All metrics operate on Nx2 arrays of `[time, value]` pairs.

### Scalar metrics (return a single distance value)

| Metric | Description |
|--------|-------------|
| `norm_infty_dist(f1, f2)` | $\|f_1 - f_2\|_\infty$ — **default** |
| `norm_p_dist(f1, f2, p=2)` | $\|f_1 - f_2\|_p$ |
| `Lp_dist(f1, f2, p=2)` | Lp functional norm of difference (piecewise constant approximation) |
| `Linfty_dist(f1, f2)` | $L^\infty$ functional norm of difference |

### Pointwise metrics (return an Nx2 timeseries of deviations)

| Metric | Description |
|--------|-------------|
| `abs_dist_ptwise(f1, f2)` | Pointwise absolute difference |
| `func_ptwise(f1, f2, dist)` | Apply custom function elementwise |

### Custom metrics

Pass any callable as `metric` to `compare_result()`:

```python
# Lambda
tester.compare_result(..., metric=lambda r_ref, r_act: np.linalg.norm(r_ref[:,1] - r_act[:,1], ord=1))

# functools.partial
tester.compare_result(..., metric=functools.partial(mopyregtest.metrics.Lp_dist, p=2))
```

Custom metrics must accept two Nx2 arrays and return either a scalar or an Nx2 array.

For the `Generator`, custom metrics must be passed as strings:
```python
gen = mopyregtest.Generator(..., metric="lambda r_ref, r_act: np.linalg.norm(r_ref[:,1] - r_act[:,1], ord=np.inf)")
```

## CI integration

MoPyRegtest tests are standard `unittest` tests and work with any CI system. For GitHub Actions with 
OpenModelica, see the [workflow files](/.github/workflows/) in this repository.

The key pattern is:
1. Use an OpenModelica container image
2. Install Python, numpy, pandas, and MoPyRegtest inside the container
3. Run `python3 -m unittest` or execute test scripts directly
