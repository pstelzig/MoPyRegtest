"""
(c) Dr. Philipp Emanuel Stelzig, 2019. 

License according to this project's LICENSE.md file. 
"""

import os
import platform
import pathlib
import shutil
import numpy as np


class RegressionTest:
    """
    Class to perform regression testing on a particular Modelica model inside a larger Modelica package.
    Creates OpenModelica-compatible .mos scripts to import and simulate the model with .csv output.
    The .csv output is then compared against a reference result, possibly only on a subset of columns.
    """
    def __init__(self, package_folder, model_in_package, result_folder):
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
        """

        self.template_folder_path = pathlib.Path(__file__).parent.absolute() / "templates"
        self.package_folder_path = pathlib.Path(package_folder).absolute()
        self.model_in_package = model_in_package
        self.result_folder_path = pathlib.Path(result_folder).absolute()

        self.model_import_template = "model_import.mos.template"
        self.model_simulate_template = "model_simulate.mos.template"
        self.model_import_mos = "model_import.mos"
        self.model_simulate_mos = "model_simulate.mos"
        self.omc_output = "omc_output.txt"

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
        # Create folder where output of the simulation shall be stored

        if not self.result_folder_path.exists():
            pathlib.Path.mkdir(self.result_folder_path)
            self.result_folder_created = True

        pathlib.os.chdir(self.result_folder_path)

        # Copy mos templates to result folder
        shutil.copy(self.template_folder_path / self.model_import_template, self.result_folder_path / self.model_import_mos)
        shutil.copy(self.template_folder_path / self.model_simulate_template, self.result_folder_path / self.model_simulate_mos)

        # Modify the import template
        repl_dict = {}
        repl_dict["PACKAGE_FOLDER"] = str(self.package_folder_path.as_posix())
        repl_dict["RESULT_FOLDER"] = str(self.result_folder_path.as_posix())
        repl_dict["MODEL_IN_PACKAGE"] = self.model_in_package

        RegressionTest.replace_in_file(self.result_folder_path / self.model_import_mos, repl_dict)

        # Run the import script and write the output of the OpenModelica Compiler (omc) to omc_output
        os.system("omc {} > {}".format(self.model_import_mos, self.omc_output))

        # Read simulation options from the simulation_options_file
        model_import_output_file = open(self.omc_output, 'r')
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

        RegressionTest.replace_in_file(self.result_folder_path / self.model_simulate_mos, repl_dict)

        # Run the simulation script and append the output of the OpenModelica Compiler (omc) to omc_output
        os.system("omc {} >> {}".format(self.model_simulate_mos, self.omc_output))

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
            List of column indeces in the reference .csv file that are used in the regression test
        precision : int
            Decimal precision up to which equality is tested

        Returns
        -------
            out : None
        """
        self.import_and_simulate()

        ref_data = np.loadtxt(fname=reference_result, delimiter=',', skiprows=1)
        result_data = np.loadtxt(fname=str(self.result_folder_path / self.model_in_package) + "_res.csv",
                                 delimiter=',', skiprows=1)

        if not validated_cols:
            validated_cols = range(0, ref_data.shape[1])

        for j in validated_cols:
            np.testing.assert_almost_equal(result_data[:, j], ref_data[:, j], precision)

        return

    def cleanup(self):
        # Only cleanup folders created here
        if self.result_folder_created:
            shutil.rmtree(self.result_folder_path)

        return

