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
        tmp_res_folder = tempfile.mkdtemp(prefix=model_in_package, dir=tempfile.gettempdir())

        regtest = RegressionTest(package_folder=self.package_folder,
                                 model_in_package=model_in_package,
                                 result_folder=tmp_res_folder, tool=tool,
                                 modelica_version=self.modelica_version,
                                 dependencies=self.dependencies)
        regtest._import_and_simulate()

        res_file = f"{model_in_package}_res.csv"
        r_ref = str(pathlib.Path(reference_folder) / res_file)

        shutil.copyfile(pathlib.Path(tmp_res_folder) / res_file, r_ref)

        if do_cleanup:
            shutil.rmtree(tmp_res_folder)

        return r_ref

    def generate_tests(self, test_folder, test_name, test_results_folder,
                       references=None, generate_missing_refs=True,
                       cleanup_ref_gen=False, cleanup_in_tests=False):
        test_folder = pathlib.Path(test_folder)
        if not test_folder.exists():
            test_folder.mkdir(parents=True, exist_ok=False)
        if not (test_folder / "references").exists():
            (test_folder / "references").mkdir()

        tfile = open(pathlib.Path(test_folder) / f"test_{test_name.lower()}.py", 'w')
        tfile.truncate()
        tfile.write(Generator.IMPORTS)
        tfile.write(Generator.CLASS.replace("$$CLASS_NAME$$", test_name))

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

