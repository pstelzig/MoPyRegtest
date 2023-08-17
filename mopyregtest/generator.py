"""
MoPyRegtest: A Python enabled simple regression testing framework for Modelica models.

Copyright (c) Dr. Philipp Emanuel Stelzig, 2019--2023.

MIT License. See the project's LICENSE file.
"""

import shutil
import pathlib
import tempfile

import mopyregtest.metrics
from . import utils
from .modelicaregressiontest import RegressionTest

class Generator:
    """
    Class that allows to automatically generate MoPyRegtest regression test definitions for a given library.
    This is make it easier to retroactively turn e.g. an Examples package of an existing Modelica library into
    regression tests with minimal effort.

    One just has to specify the library and a list of elements in the library to turn into regression tests.
    It is possible to pass reference .csv result files for each specified element, or to generate missing reference
    results using a simulation tool like e.g. OpenModelica's omc.

    As a result one gets a MoPyRegtest regression test file which one can then further integrate e.g. into
    a continuous integration toolchain.
    """
    IMPORTS = \
        """
# Preparing the dependencies ##################################################
# Essential
import unittest 

# For convenience in handling paths
import pathlib
import platform
import mopyregtest
import sys
import numpy as np
        """

    CLASS = \
        """
class Test$$CLASS_NAME$$(unittest.TestCase):        
        """

    METHOD = \
        """
    def test_$$METHOD_NAME$$(self):
        tester = mopyregtest.RegressionTest(package_folder="$$PACKAGE_FOLDER$$",
                                            model_in_package="$$MODEL_IN_PACKAGE$$",
                                            result_folder="$$RESULT_FOLDER$$",
                                            modelica_version="$$MODELICA_VERSION$$",
                                            dependencies=$$DEPENDENCIES$$)
    
        # Comparing results
        tester.compare_result(reference_result="$$REFERENCE_RESULT$$",
                              metric=$$METRIC$$,
                              validated_cols=[], tol=$$TOLERANCE$$, 
                              unify_timestamps=$$UNIFY_TIMESTAMPS$$, fill_in_method="$$FILL_IN_METHOD$$")
    
        # Deletes result_folder after it has been created. Leave out if you feel uncomfortable with auto-deletion!
        $$DO_CLEANUP$$tester.cleanup()
    
        return
        """

    MAIN_STATEMENT = \
        """
if __name__ == '__main__':
    unittest.main()        
        """

    def __init__(self, package_folder, models_in_package, modelica_version="default", dependencies=None,
                 metric=mopyregtest.metrics.norm_infty_dist,
                 tol=1e-7, unify_timestamps=True, fill_in_method="ffill"):
        """

        Parameters
        ----------
        package_folder : str or PathLike
            Path to the package, from which elements shall be turned into regression tests. Relative paths to the
            file that instantiates a Generator class are possible.
        models_in_package : list[str]
            List of strings with Modelica names of elements in the library to be turned into regression tests.
        modelica_version : str
            Modelica STL version as a string. Default value is "default"
        dependencies : None or list[str]
            Optional list of strings with names of packages that the package to be tested depends on.
            Each dependency must point to the .mo file that defines the dependency. E.g. if the
            dependency is an entire package, it must be the path to the respective package's package.mo.
        metric : function or str
            Metric to be used in result comparison. Important: If the metric is given as a funtion, one must use one
            of the predefined metrics, i.e. mopyregtest.metrics.norm_p_dist, mopyregtest.metrics.norm_infty_dist,
            mopyregtest.metrics.Lp_dist or mopyregtest.metrics.Linfty_dist.

            If a user-defined metric shall be used, the code must be passed as a string!
        tol : float
            Tolerance to be used in all regression tests.
        unify_timestamps : bool
            Boolean controlling whether the timestamp unification shall be called in the RegressionTest.compare_result
            before evaluating the metric. Default=True.

            If set to False, then the function passed in the argument "metric" will be evaluated for matching columns
            of reference and actual result. In this case the definition of the metric has to
            ensure that computations are meaningful, e.g. for non-matching dimensions or different timestamps.
        fill_in_method : str
            Defines the method used to fill in data when calling RegressionTest._unify_timestamps and if results have
            different timestamps and cannot be compared pointwise.

            Valid methods are "ffill", "bfill", "interpolate" where
            ffill and bfill are the forward fill and backward fill methods from
            pandas.DataFrame.fillna and "interpol" uses linear interpolation
            as in pandas.DataFrame.interpol
        """
        self.package_folder = package_folder
        self.models_in_package = models_in_package
        self.modelica_version = modelica_version
        self.dependencies = dependencies
        self.metric = f"mopyregtest.metrics.{metric.__name__}"
        self.tol = tol
        self.unify_timestamps = unify_timestamps
        self.fill_in_method = fill_in_method

        return

    def _generate_reference(self, reference_folder, model_in_package, tool="omc", do_cleanup=False):
        """
        Generates missing reference results for a Modelica model using the specified tool. Note that this requires
        the simulation data like start, stop and timestep size to be stored in the model's annotation.

        Parameters
        ----------
        reference_folder : str or PathLike
            Folder where to store the reference result
        model_in_package : str
            Modelica model name for which to generate the reference result
        tool : str
            Simulator used to translate, compile and execute Modelica model. The only valid
            tool right now is omc (OpenModelica Compiler). If no argument is specified,
            RegressionTest will search the PATH variable for omc and will execute the simulation if found.
        do_cleanup : bool
            Whether to clean up the files generated during simulation (e.g. code and generated binaries)
        Returns
        -------
        out : str
            Complete path of the reference result generated

        """
        tmp_res_folder = tempfile.mkdtemp(prefix=model_in_package, dir=tempfile.gettempdir())

        # Simulate in temporary folder
        regtest = RegressionTest(package_folder=self.package_folder,
                                 model_in_package=model_in_package,
                                 result_folder=tmp_res_folder, tool=tool,
                                 modelica_version=self.modelica_version,
                                 dependencies=self.dependencies)
        regtest._import_and_simulate()

        # Copy reference result file from temporary folder into reference target folder
        res_file = f"{model_in_package}_res.csv"
        r_ref = str(pathlib.Path(reference_folder) / res_file)

        shutil.copyfile(pathlib.Path(tmp_res_folder) / res_file, r_ref)

        # Cleanup temporary directory with simulation data
        if do_cleanup:
            shutil.rmtree(tmp_res_folder)

        return r_ref

    def generate_tests(self, test_folder, test_name, test_results_folder,
                       references=None, generate_missing_refs=True,
                       cleanup_ref_gen=False, cleanup_in_tests=False):
        """
        Generates the test for the library elements specified in the constructor. All tests will be included in one
        single test class. For every library element an individual test method will be generated in the test class.

        Parameters
        ----------
        test_folder : str or PathLike
            Folder where the definition file for the MoPyRegtest regression tests shall be stored. This folder will be
            created if it does not exist, but an error will be raised if it exists already.
        test_name : str
            Name of the regression test collection to be created. The resulting definition file will be called like
            test_<test_name>.py and the test class like Test<test_name>. Make sure to use characters only that do not
            cause problems in the naming.
        test_results_folder : str or PathLike
            Folder where the results of the generated tests shall be stored, when the generated tests are actually run.
        references : dict
            Dictionary whose keys are names from self.models_in_package. That is, Modelica model names.
            For each Modelica model name, the value is a path to the reference result. If a Modelica model
            element from self.models_in_package has no corresponding key in references, then the missing reference
            result will be generated. But only, if generate_missing_refs is set to True.
            Otherwise, during test case execution an error will be encountered due to a missing reference result file.
        generate_missing_refs : bool
            Whether to generated reference result .csv files for models from self.models_in_package that are not
            given through the parameter references.
        cleanup_ref_gen : bool
            Whether to clean up intermediate simulation files from generating reference results.
        cleanup_in_tests : bool
            Whether result files shall be cleaned up once the generated tests are actually run.

        Returns
        -------
        out : None

        """
        # Creating the target folder where the MoPyRegtest test definition shall be created
        test_folder = pathlib.Path(test_folder)
        if not test_folder.exists():
            test_folder.mkdir(parents=True, exist_ok=False)
        if not (test_folder / "references").exists():
            (test_folder / "references").mkdir()

        # Creating the MoPyRegtest test definition
        tfile = open(pathlib.Path(test_folder) / f"test_{test_name.lower()}.py", 'w')
        tfile.truncate()
        tfile.write(Generator.IMPORTS)
        tfile.write(Generator.CLASS.replace("$$CLASS_NAME$$", test_name))

        # Creating a test method for every element in self.models_in_package
        for md in self.models_in_package:
            if (references is None or md not in references.keys()) and generate_missing_refs:
                r_ref = self._generate_reference(reference_folder=test_folder / "references",
                                                 model_in_package=md, do_cleanup=cleanup_ref_gen)
            else:
                r_ref = references[md]
                shutil.copyfile(r_ref, test_folder / "references" / f"{md}_res.csv")

            dependencies_str = "None" if self.dependencies is None else "[{}]".format(",".join(self.dependencies))
            repl_dict = {
                "$$METHOD_NAME$$": md.lower().replace(".", "_"),
                "$$PACKAGE_FOLDER$$": str(self.package_folder),
                "$$MODEL_IN_PACKAGE$$": md,
                "$$RESULT_FOLDER$$": str(test_results_folder),
                "$$MODELICA_VERSION$$": self.modelica_version,
                "$$DEPENDENCIES$$": dependencies_str,
                "$$REFERENCE_RESULT$$": r_ref,
                "$$METRIC$$": self.metric,
                "$$TOLERANCE$$": str(self.tol),
                "$$UNIFY_TIMESTAMPS$$": str(self.unify_timestamps),
                "$$FILL_IN_METHOD$$": self.fill_in_method,
                "$$DO_CLEANUP$$": "" if cleanup_in_tests else "#"
            }

            test_method = utils.replace_in_str(Generator.METHOD, repl_dict)
            tfile.write(test_method)
            tfile.flush()

        tfile.write(Generator.MAIN_STATEMENT)
        tfile.close()

        return
