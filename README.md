# MoPyRegtest: A Python enabled simple regression testing framework for Modelica models

Scope of this project is to 
* provide a intentionally simple and quick to use unit testing framework to 
* test for reproduceability of results from [Modelica](https://www.modelica.org/) models and to
* have it wrapped in the well-known [Python `unittest` module](https://docs.python.org/3/library/unittest.html)


## Background: 
When developing Modelica models or libraries and a certain maturity or complexity level has been reached or releases have been made, there is definitely the need to test for reproduceability of successful model translation, simulation results, memory consumption, CPU time and more. Testing of Modelica models appears to have been a topic from the early beginnings of Modelica and has many faces and realizations up to this day. 


## Why MoPyRegtest
The scope of `MoPyRegtest` is first and foremost to have a transparent, quick, lightweight and simple way to perform regression tests. Without immediately requiring commercial simulation tools or creating strong dependencies from other Modelica libraries. This is why MoPyRegtest consists of just one source file. 

All that is needed to use `MoPyRegtest` is a Python 3 installation, an [OpenModelica](https://www.openmodelica.org/) installation and a text editor -- things that very likely most (Open)Modelica users do have anyway. All that is needed to deploy `MoPyRegtest` is to write a Python file, just like in the `examples` folder of this project. 


## Current realization
The current realization uses the [Python `unittest` module](https://docs.python.org/3/library/unittest.html) and calls the [OpenModelica compiler `omc`](https://openmodelica.org/?id=51:open-modelica-compiler-omc&catid=10:main-category) as an external executable for translation and simulation of Modelica models. Note that the implementation `MoPyRegtest` is not specific to OpenModelica but can be replaced by any other Modelica simulation tool that comes with a suitable scripting API. 

The test execution and orchestration is done by the Python `unittest` module. In particular, Python `unittest` supports [test discovery](https://docs.python.org/3/library/unittest.html#test-discovery). That is, when the aforementioned Python files that the user has to create for regression testing are suitably placed, Python can discover and execute them automatically, thus making test orchestration and execution a lot easier. Also, `unittest` is a standard module that comes with virtually all Python distributions. 

**MoPyRegtest is work in progress!**


## Usage and example
The user has to
* provide Modelica models that can be translated, built and executed and produce a result `.csv` file
* provide for every Modelica model a `.csv` file with reference results against which (or a subset of columns of which) results are compared
* create a Python file containing a child class of `unittest.TestCase` and test methods that instantiate a `mopyregtest.RegressionTest` object, which just needs to be told which Modelica model to test and where to find the reference result. 

Examples of how such a file would look like can be found in the `examples` folder. Also see the [examples/README.md](/examples/README.md). 


## Prerequisites
To use `MoPyRegtest` you need to have
* a [Python 3](https://www.python.org/) distribution including the modules [`unittest`](https://docs.python.org/3/library/unittest.html) and [`Numpy`](https://numpy.org/)
* a working [OpenModelica](https://www.openmodelica.org/) installation (version 1.13.0 or later) and 
* the OpenModelica compiler executable `omc` has to be found via the `PATH` variable.

To test for the latter, open a command line terminal (`cmd` in Windows), type `omc` and press `Enter`. If `omc` is in the `PATH` variable, you should get a long list of options and links to the documentation of OpenModelica, otherwise an error message.


## Installation using pip3
If you want to install `MoPyRegtest` using [Python's package manager `pip`](https://packaging.python.org/tutorials/installing-packages/), just clone this repo

```bash
$ cd <your-mopyregtest-dir>
$ git clone https://gitlab.com/pstelzig/mopyregtest.git
```

to your local `<your-mopyregtest-dir>` (adapt to your needs) and then

```
pip3 install --user <your-mopyregtest-dir>/mopyregtest
```

To uninstall, run
```bash
pip3 uninstall mopyregtest
```


## Future Work
* Support other simulators like e.g. Dymola
* Make definition of the tests even simpler, e.g. using a more human-readable BDD approach with [Behave. BDD, Python style](https://github.com/behave/behave)
* Allow for parallel execution of regression tests


## Open source software used
MoPyRegtest is implemented in Python3 and uses the Python core modules (including `pathlib` and `unittest`) along with [Numpy](https://numpy.org/) and [pandas](https://pandas.pydata.org/). 


# License
MoPyRegtest is open source software. MoPyRegtest is provided "as is", without warranty of any kind. Usage is completely at your own risk. See the file `LICENSE`. 


# How to contribute
If you want to help me extend MoPyRegtest, please drop me a message! Contributions are welcome!


# Authors
The MoPyRegtest is being developed by the following authors:
* [Dr. Philipp Emanuel Stelzig](mailto:software@philippstelzig.de)

