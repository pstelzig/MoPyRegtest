"""
(c) Dr. Philipp Emanuel Stelzig, 2019. 

MIT License. See the project's LICENSE file.
"""

import os
import platform
import pathlib
import shutil
import numpy as np
import pandas as pd


class RegressionTest:
    """
    Class to perform regression testing on a particular Modelica model inside a larger Modelica package.
    Creates OpenModelica-compatible .mos scripts to import and simulate the model with .csv output.
    The .csv output is then compared against a reference result, possibly only on a subset of columns.
    """
    def __init__(self, package_folder, model_in_package, result_folder, tool="omc"):
        """
        Constructor of the RegresssionTest class.

        Parameters
        ----------
        package_folder : str
            Path of the folder the Modelica package containing the model to be tested
        model_in_package : str
            Name of the model to be tested
        result_folder :
            Path of the folder where the output of the model testing shall be written to
        tool:
            Simulator used to translate, compile and execute Modelica model. Valid options are omc,
            and dymola. If no argument is specified, RegressionTest will search the PATH variable
            for both omc and dymola and will execute the tests for all of the two that is found. 
        """

        self.template_folder_path = pathlib.Path(__file__).parent.absolute() / "templates"
        self.package_folder_path = pathlib.Path(package_folder).absolute()
        self.model_in_package = model_in_package
        self.result_folder_path = pathlib.Path(result_folder).absolute()

        if tool != None:
            self.tools = [tool]
        else:
            self.tools = [tl for tl in ["omc", "dymola"] if shutil.which(tl) != None]

        self.result_folder_created = False

    @staticmethod
    def replace_in_file(filename, repl_dict):
        fhandle = open(str(filename), 'r')
        contents = fhandle.read()
        fhandle.close()

        for k, v in repl_dict.items():
            contents = contents.replace(k, v)

        fhandle = open(str(filename), 'w')
        fhandle.truncate()
        fhandle.write(contents)
        fhandle.close()

        return

    def import_and_simulate(self):
        print("Simulating model {} using the simulation tools: {}" .format(self.model_in_package, ", ".join(self.tools)))

        # Create folder where output of the simulation shall be stored
        if not self.result_folder_path.exists():
            pathlib.Path.mkdir(self.result_folder_path)
            self.result_folder_created = True

        pathlib.os.chdir(self.result_folder_path)

        # Run the scripts for import and simulation
        self._run_model()

        return

    def compare_result(self, reference_result, precision=7, validated_cols=[]):
        """
        Executes simulation and then compares the obtained result and the reference result along the
        validated columns. Throws an exception (AssertionError) if the deviation is larger or equal to
        10**(-precision).

        Parameters
        ----------
        reference_result : str
            Path to a reference .csv file containing the expected results of the model
        validated_cols : list
            List of variable names (from the file header) in the reference .csv file that are used in the regression test
        precision : int
            Decimal precision up to which equality is tested

        Returns
        -------
        out : None
        """
        print("\nTesting model {}".format(self.model_in_package))

        self.import_and_simulate()
        simulation_result = str(self.result_folder_path / self.model_in_package) + "_res.csv"

        print("Comparing simulation result {} and reference {}".format(simulation_result, reference_result))

        ref_data = pd.read_csv(filepath_or_buffer=reference_result, delimiter=',')
        result_data = pd.read_csv(filepath_or_buffer=simulation_result, delimiter=',')

        # Determine common columns by comparing column headers
        common_cols = set(ref_data.columns).intersection(set(result_data.columns))

        if not validated_cols:
            validated_cols = common_cols

        for c in validated_cols:
            print("Comparing column \"{}\"".format(c))
            np.testing.assert_almost_equal(result_data[c].as_matrix(), ref_data[c].as_matrix(), precision)

        return

    def cleanup(self):
        # Only cleanup folders created here
        if self.result_folder_created:
            shutil.rmtree(self.result_folder_path)

        return

    def _run_model(self):

        for tool in self.tools:
            tool_executable = tool
            if platform.system() == 'Windows':
                tool_executable += ".exe"

            print("Using simulation tool {}".format(tool_executable))

            model_import_template = tool + "/model_import.mos.template"
            model_simulate_template = tool + "/model_simulate.mos.template"
            model_import_mos = "model_import.mos"
            model_simulate_mos = "model_simulate.mos"
            tool_output = tool + "_output.txt"

            if tool == "omc":
                # Copy mos templates to result folder
                shutil.copy(self.template_folder_path / model_import_template, self.result_folder_path / model_import_mos)
                shutil.copy(self.template_folder_path / model_simulate_template, self.result_folder_path / model_simulate_mos)

                # Modify the import template
                repl_dict = {}
                repl_dict["PACKAGE_FOLDER"] = str(self.package_folder_path.as_posix())
                repl_dict["RESULT_FOLDER"] = str(self.result_folder_path.as_posix())
                repl_dict["MODEL_IN_PACKAGE"] = self.model_in_package

                RegressionTest.replace_in_file(self.result_folder_path / model_import_mos, repl_dict)

                # Run the import script and write the output of the OpenModelica Compiler (omc) to omc_output
                os.system(tool_executable + " {} > {}".format(model_import_mos, tool_output))

                # Read simulation options from the simulation_options_file
                model_import_output_file = open(tool_output, 'r')
                omc_messages = model_import_output_file.readlines()
                model_import_output_file.close()

                (start_time, stop_time, tolerance, num_intervals, interval) = omc_messages[-1].lstrip('(').rstrip(')').split(',')

                # Modify the simulation template
                if platform.system() == 'Windows':
                    repl_dict["SIMULATION_BINARY"] = "{}.exe".format(self.model_in_package)
                elif platform.system() == 'Linux':
                    repl_dict["SIMULATION_BINARY"] = "./{}".format(self.model_in_package)
                repl_dict["START_TIME"] = start_time
                repl_dict["STOP_TIME"] = stop_time
                repl_dict["TOLERANCE"] = tolerance
                repl_dict["NUM_INTERVALS"] = num_intervals

                RegressionTest.replace_in_file(self.result_folder_path / model_simulate_mos, repl_dict)

                # Run the simulation script and append the output of the OpenModelica Compiler (omc) to omc_output
                os.system(tool_executable + " {} >> {}".format(model_simulate_mos, tool_output))

            if tool == "dymola":
                # Copy mos templates to result folder
                shutil.copy(self.template_folder_path / model_simulate_template, self.result_folder_path / model_simulate_mos)

                # Modify the simulation template
                repl_dict = {}
                repl_dict["PACKAGE_FOLDER"] = str(self.package_folder_path.as_posix())
                repl_dict["RESULT_FOLDER"] = str(self.result_folder_path.as_posix())
                repl_dict["MODEL_IN_PACKAGE"] = self.model_in_package

                RegressionTest.replace_in_file(self.result_folder_path / model_simulate_mos, repl_dict)

                # Run the simulation script
                os.system(tool_executable + " {} /nowindow >> {}".format(model_simulate_mos, tool_output))

        return
