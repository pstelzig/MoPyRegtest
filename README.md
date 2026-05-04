# MoPyRegtest: A Python enabled simple regression testing framework for Modelica models

**Project status**  
[![Unit tests](https://github.com/pstelzig/mopyregtest/actions/workflows/job-unit-tests.yml/badge.svg?branch=master)](https://github.com/pstelzig/MoPyRegtest/actions/workflows/job-unit-tests.yml)
[![Examples](https://github.com/pstelzig/mopyregtest/actions/workflows/job-examples.yml/badge.svg?branch=master)](https://github.com/pstelzig/MoPyRegtest/actions/workflows/job-examples.yml)
[![Example usage in other repo](https://github.com/pstelzig/mopyregtest/actions/workflows/job-example-for-other-repo.yml/badge.svg?branch=master)](https://github.com/pstelzig/MoPyRegtest/actions/workflows/job-example-for-other-repo.yml)
[![Publish to PyPI](https://github.com/pstelzig/mopyregtest/actions/workflows/pythonpublish.yml/badge.svg)](https://pypi.org/project/MoPyRegtest/)

A lightweight, CI-friendly regression testing framework for [Modelica](https://www.modelica.org/) models, 
wrapped in Python's [`unittest`](https://docs.python.org/3/library/unittest.html) module. 
Uses [OpenModelica](https://www.openmodelica.org/) for model translation and simulation.

**Key features:**
- **Regression testing** — compare simulation results against reference CSV files using configurable metrics and tolerances
- **Success-only testing** — verify that models compile, build, and simulate successfully (useful for unit test models with built-in assertions)
- **Automatic test generation** — generate `unittest` test files for entire Modelica libraries via CLI or Python script
- **CSV comparison** — compare two CSV result files directly from the command line

## Prerequisites
- [Python 3](https://www.python.org/) with [`numpy`](https://numpy.org/) and [`pandas`](https://pandas.pydata.org/)
- [OpenModelica](https://www.openmodelica.org/) (>= 1.13.0) with `omc` on `PATH`

## Installation

```bash
# From PyPI
python3 -m pip install --user mopyregtest

# From source
git clone https://github.com/pstelzig/MoPyRegtest.git
cd MoPyRegtest
python3 -m pip install --user .
```

Verify the CLI: `mopyregtest --help`

> **Tip:** If `mopyregtest` is not found, check that pip's script directory is on your `PATH`.  
> Run `python3 -m pip uninstall mopyregtest` (without confirming) to see where pip installed the executable.

## Quick start

### Regression test (manual)

```python
import mopyregtest

tester = mopyregtest.RegressionTest(
    package_folder="~/.openmodelica/libraries/Modelica 4.0.0+maint.om",
    model_in_package="Modelica.Electrical.Analog.Examples.HeatingRectifier",
    result_folder="./results",
    modelica_version="4.0.0")

tester.compare_result(reference_result="references/HeatingRectifier_res.csv", tol=1e-3)
tester.cleanup(ask_confirmation=False)
```

### Success-only test (manual)

```python
tester = mopyregtest.RegressionTest(
    package_folder="~/.openmodelica/libraries/Modelica 4.0.0+maint.om",
    model_in_package="Modelica.Blocks.Examples.Filter",
    result_folder="./results")

tester.check_success()
tester.cleanup(ask_confirmation=False)
```

### Auto-generate tests (CLI)

```bash
# Regression tests
mopyregtest generate ./gen_tests MyTest ~/".openmodelica/libraries/Modelica 4.0.0+maint.om/" \
    Modelica.Blocks.Sources.Sine,Modelica.Blocks.Sources.Step

# Success-only tests
mopyregtest generate --mode=success ./gen_tests MySimTest ~/".openmodelica/libraries/Modelica 4.0.0+maint.om/" \
    Modelica.Blocks.Examples.Filter
```

### Compare CSV files (CLI)

```bash
mopyregtest compare --metric=Lp_dist --tol=0.015 --validated-cols=y reference.csv actual.csv
```

## Documentation
For detailed usage, metrics reference, and worked examples see the [documentation](doc/usage.md).  
Runnable examples are in the [examples/](examples/) folder.

## License
MIT — see [LICENSE](LICENSE).

## Contributing
Contributions are welcome! Please open an issue or pull request.

## Authors
- [Dr. Philipp Emanuel Stelzig](https://github.com/pstelzig)
