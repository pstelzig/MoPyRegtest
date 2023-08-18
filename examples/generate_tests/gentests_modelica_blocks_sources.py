import pathlib
import platform
import mopyregtest
import sys

# Setup the test data #########################################################
# Example here for an Ubuntu environment with OpenModelica
# installed like in https://openmodelica.org/download/download-linux
# and using the default OpenModelica package manager

# Path to Modelica library or model to be tested. Here an element of the Modelica STL.
if platform.system() == 'Windows':
    package_folder = pathlib.Path.home() / "AppData/Roaming/.openmodelica/libraries/Modelica 4.0.0+maint.om"
else:
    package_folder = pathlib.Path.home() / ".openmodelica/libraries/Modelica 4.0.0+maint.om"

if not package_folder.exists():
    error_msg = f"""[ERROR] Path \"{package_folder}\" not found. Aborting.

This example is designed to work with OpenModelica installed to 
standard paths, in order to work out of the box. 

It requires the omc binary to be in the PATH variable and that the Modelica standard 
library version 4.0.0 is installed to {package_folder}. 

If this does not fit your requirements, just adapt the package_folder variable 
in this file to your needs."""
    print(error_msg)
    sys.exit(-1)

# Where to put results from this test
this_folder = pathlib.Path(__file__).absolute().parent
result_folder = this_folder

# Where to find reference results for this test
reference_folder = this_folder / "references"

# Generating a test battery with a predefined metric ###################################################################
# Models to generate regression tests for
models_in_package = ["Modelica.Blocks.Sources.Sine", "Modelica.Blocks.Sources.ExpSine", "Modelica.Blocks.Sources.Step"]

gen = mopyregtest.Generator(package_folder=package_folder, models_in_package=models_in_package,
                            metric=mopyregtest.metrics.Lp_dist)
gen.generate_tests(test_folder=this_folder / "gen_tests", test_name="BlocksLpDist",
                   test_results_folder=this_folder / "results",
                   cleanup_ref_gen=True)

# Generating a test battery with a user defined metric #################################################################
# Models to generate regression tests for
models_in_package = ["Modelica.Blocks.Sources.Cosine", "Modelica.Blocks.Sources.Sinc", "Modelica.Blocks.Sources.Ramp"]

gen = mopyregtest.Generator(package_folder=package_folder, models_in_package=models_in_package,
                            metric="lambda r_ref, r_act: np.linalg.norm(r_ref[:, 1] - r_act[:, 1], ord=np.inf)")
gen.generate_tests(test_folder=this_folder / "gen_tests", test_name="BlocksUserDef",
                   test_results_folder=this_folder / "results",
                   cleanup_ref_gen=True)
