# MoPyRegtest: A Python enabled simple regression testing framework for Modelica models

**General**
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/pstelzig/MoPyRegtest/tree/master/LICENSE)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/pstelzig/MoPyRegtest/issues)

**Project status**
![Unit tests](https://github.com/pstelzig/mopyregtest/actions/workflows/job-unit-tests.yml/badge.svg?branch=master)
![Examples](https://github.com/pstelzig/mopyregtest/actions/workflows/job-examples.yml/badge.svg?branch=master)
![Example usage in other repo](https://github.com/pstelzig/mopyregtest/actions/workflows/job-example-for-other-repo.yml/badge.svg?branch=master)

Scope of this project is to 
* provide a simple regression testing framework for Modelica models
* support continuous integration (CI) for Modelica library development, in particular
* test for reproducibility of results from [Modelica](https://www.modelica.org/) models and to
* have it wrapped in the well-known [Python `unittest` module](https://docs.python.org/3/library/unittest.html)

## Background: 
When developing Modelica models or libraries and releases have been made, there is definitely the need for testing. E.g.
- validation of successful model translation,
- reproducibility of simulation results, or
- making sure refactorings in Modelica libraries do not alter the behavior.
 
Other testing criteria could be memory consumption, CPU time and more. 

## Why MoPyRegtest
The scope of MoPyRegtest is to have a lightweight and simple way to perform regression tests and to be able to integrate 
this with automated testing and continuous integration (CI) toolchains, like e.g. GitHub Actions. 
Without immediately requiring commercial simulation tools or creating strong dependencies from other Modelica libraries.

All that is needed to use MoPyRegtest is a Python 3 installation, an [OpenModelica](https://www.openmodelica.org/) installation, 
and a text editor. 

## Current realization
The current realization uses the [Python `unittest` module](https://docs.python.org/3/library/unittest.html) and calls the [OpenModelica compiler `omc`](https://openmodelica.org/) as an 
external executable for translation and simulation of Modelica models. Note that the implementation of MoPyRegtest is not 
specific to OpenModelica but can be replaced by any other Modelica simulation tool that comes with a suitable scripting API. 

The test execution and orchestration is done by the Python `unittest` module. In particular, Python `unittest` supports 
[test discovery](https://docs.python.org/3/library/unittest.html#test-discovery). 
Also, `unittest` is a standard module that comes with virtually all Python distributions. 

**MoPyRegtest is work in progress!**

## Usage and example
With MoPyRegtest, users can define regression tests manually in Python for one Modelica model at a time, 
or automatically for many Modelica models simultaneously.  

### Manual test case definition
The user has to
* provide Modelica models that can be translated, built and executed and produce a result `.csv` file
* provide for every Modelica model a `.csv` file with a reference result against which an actual result is compared
* create a Python file and test methods that instantiate a `mopyregtest.RegressionTest` object, 
  which needs to know which Modelica model to test and where to find the reference result. 

Examples can be found in the `examples` folder. Also see the [examples/README.md](https://github.com/pstelzig/MoPyRegtest/tree/master/examples/README.md). 

### Automatic test case generation
MoPyRegtest can generate regression test definitions for elements of a Modelica library automatically. 
Either by creating [Generator class objects](https://github.com/pstelzig/MoPyRegtest/tree/master/mopyregtest/generator.py). Or using the 
[`mopyregtest` command line tool](https://github.com/pstelzig/MoPyRegtest/blob/master/mopyregtest/cli.py).

The folder [examples/generate_tests/README.md](https://github.com/pstelzig/MoPyRegtest/tree/master/examples/generate_tests/README.md) 
has a detailed explanation on how to automatically generate tests.

## Prerequisites
To use MoPyRegtest you need to have
* a [Python 3](https://www.python.org/) distribution including the modules [`unittest`](https://docs.python.org/3/library/unittest.html), [`numpy`](https://numpy.org/) and [`pandas`](https://pandas.pydata.org/),
* a working [OpenModelica](https://www.openmodelica.org/) installation (version 1.13.0 or later, works also for latest 1.21), and 
* the OpenModelica compiler executable `omc` must be accessible via the `PATH` variable.

## Installation using pip3
It is most convenient to install MoPyRegtest using [Python's package manager `pip`](https://packaging.python.org/tutorials/installing-packages/).
MoPyRegtest *does not need any special privileges* to run.  

### Install from PyPI
You can install MoPyRegtest from the [Python Package Index](https://pypi.org/project/MoPyRegtest/) by running

```bash
pip3 install --user mopyregtest
```

To install a specific version, e.g. `v0.3.1`, run `pip3 install --user mopyregtest==0.3.1` 

### Install from source
To install from source, first clone this repository to your local `<your-mopyregtest-dir>` (adapt to your needs) with
the command `git clone https://github.com/pstelzig/MoPyRegtest.git <your-mopyregtest-dir>`

Then run

```bash
cd <your-mopyregtest-dir>
pip3 install --user .
```

to get the latest development head. To install a specific version from source, e.g. `v0.3.1`, run 

```bash
cd <your-mopyregtest-dir>
git checkout v0.3.1
pip3 install --user .
``` 

### Uninstall
To uninstall MoPyRegtest, run
```bash
pip3 uninstall mopyregtest
```

### Troubleshooting

#### Problem: CLI `mopyregtest` cannot be found
To check if MoPyRegtest's command line tool is working, run `mopyregtest --help` from a terminal. 

If an error message shows that the program `mopyregtest` cannot be found, then you have to check if your PATH variable 
knows where to find `mopyregtest` as installed by pip. To find out the location, run `pip uninstall mopyregtest` but do 
not confirm to proceed. The uninstallation will tell you which files pip would remove upon uninstalling MoPyRegtest, 
including the `mopyregtest` executable (or `mopyregtest.exe` under Windows) and its location.

```bash
Found existing installation: MoPyRegtest 0.4.0rc1
Uninstalling MoPyRegtest-0.4.0rc1:
  Would remove:
    /home/<your user name>/.local/bin/mopyregtest
    /home/<your user name>/.local/lib/python3.10/site-packages/MoPyRegtest-0.4.0rc1.dist-info/*
    /home/<your user name>/.local/lib/python3.10/site-packages/mopyregtest/*
Proceed (Y/n)?
```

Then, one could either call `mopyregtest` with its full path, or one could add its parent folder to the PATH 
variable (Be careful! First make sure that this does not cause any harm to your system). 

## Future Work
* Allow for parallel execution of regression tests
* Improve readability of in particular failed test results 
* Provide logs that help users in the analysis of failed tests
* Make definition of the tests even simpler, e.g. using a more human-readable BDD approach 

## Open source software used
MoPyRegtest is implemented in Python3 and uses the Python core modules (including `pathlib` and `unittest`) along with 
[`numpy`](https://numpy.org/) and [`pandas`](https://pandas.pydata.org/). 

# License
MoPyRegtest is open source software. MoPyRegtest is provided "as is", without warranty of any kind. 
Usage is completely at your own risk. See the file `LICENSE`. 

# How to contribute
If you want to help me extend MoPyRegtest, please drop me a message! Contributions are welcome!

# Authors
The MoPyRegtest is being developed by the following authors:
* [Dr. Philipp Emanuel Stelzig](https://github.com/pstelzig)

