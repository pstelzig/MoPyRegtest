# MoPyRegtest: A Python enabled simple regression testing framework for Modelica models

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](/LICENSE)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/pstelzig/MoPyRegtest/issues)

Scope of this project is to 
* provide a simple unit testing framework
* support continuous integration testing for modelica models (CI), in particular
* test for reproduceability of results from [Modelica](https://www.modelica.org/) models and to
* have it wrapped in [Python `unittest` module](https://docs.python.org/3/library/unittest.html)

## Background: 
When developing Modelica models or libraries and releases have been made, there is definitely the need for testing. E.g. for
- validation of successful model translation
- reproduceability of simulation results
- making sure refactorings in Modelica libraries do not alter the behavior
but also for testing memory consumption, CPU time and more. 

## Why MoPyRegtest
The scope of `MoPyRegtest` is to have a lightweight and simple way to perform regression tests and to be able to integrate 
this with automated testing and popular continuous integration (CI) toolchains, like e.g. GitHub Actions. 
Without immediately requiring commercial simulation tools or creating strong dependencies from other Modelica libraries. 

All that is needed to use `MoPyRegtest` is a Python 3 installation, an [OpenModelica](https://www.openmodelica.org/) installation and a text editor. 

## Current realization
The current realization uses the [Python `unittest` module](https://docs.python.org/3/library/unittest.html) and calls the [OpenModelica compiler `omc`](https://openmodelica.org/) as an 
external executable for translation and simulation of Modelica models. Note that the implementation `MoPyRegtest` is not 
specific to OpenModelica but can be replaced by any other Modelica simulation tool that comes with a suitable scripting API. 

The test execution and orchestration is done by the Python `unittest` module. In particular, Python `unittest` supports 
[test discovery](https://docs.python.org/3/library/unittest.html#test-discovery). Also, `unittest` is a standard module that comes with virtually all Python distributions. 

**MoPyRegtest is work in progress!**


## Usage and example

### Manual test case definition
The user has to
* provide Modelica models that can be translated, built and executed and produce a result `.csv` file
* provide for every Modelica model a `.csv` file with reference results against which or columns of which results are compared
* create a Python file and test methods that instantiate a `mopyregtest.RegressionTest` object, 
  which needs to know which Modelica model to test and where to find the reference result. 

Examples can be found in the `examples` folder. Also see the [examples/README.md](/examples/README.md). 

### Automatic test case generation
Regression test definitions for elements of a Modelica library can also be generated automatically by MoPyRegtest. 
Either by creating [Generator](/mopyregtest/generator.py) class objects. Or from the command line using the 
[testgen.py](/tools/testgen.py) script. 

The [generate_tests folder in examples](/examples/generate_tests) has a detailed example on how to automatically 
generate tests using a Python script.

## Prerequisites
To use `MoPyRegtest` you need to have
* a [Python 3](https://www.python.org/) distribution including the modules [`unittest`](https://docs.python.org/3/library/unittest.html), [`numpy`](https://numpy.org/) and [`pandas`](https://pandas.pydata.org/)
* a working [OpenModelica](https://www.openmodelica.org/) installation (version 1.13.0 or later, works also for latest 1.21) and 
* the OpenModelica compiler executable `omc` has to be found via the `PATH` variable.

To test for the latter, open a command line terminal (`cmd` in Windows), type `omc` and press `Enter`. 
If `omc` is in the `PATH` variable, you should get a long list of options and links to the documentation of OpenModelica, 
otherwise an error message.

## Installation using pip3
If you want to install `MoPyRegtest` using [Python's package manager `pip`](https://packaging.python.org/tutorials/installing-packages/), 
just clone this repo to your local `<your-mopyregtest-dir>` (adapt to your needs) and then run

```bash
cd <your-mopyregtest-dir>
pip3 install --user .
```

To uninstall, run
```bash
pip3 uninstall mopyregtest
```

## Future Work
* Support other simulators like e.g. Dymola, MapleSim, SystemModeler or others
* Make definition of the tests even simpler, e.g. using a more human-readable BDD approach
* Allow for parallel execution of regression tests

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

