"""
MoPyRegtest: A Python enabled simple regression testing framework for Modelica models.

Copyright (c) Dr. Philipp Emanuel Stelzig, 2019.

MIT License. See the project's LICENSE file.
"""

import os
import subprocess
import platform
import pathlib
import shutil
import math
import numpy as np
import pandas as pd
from typing import List
from . import utils
from . import metrics


class RegressionTest:
    """
    Class to perform regression testing on a particular Modelica model inside a larger Modelica package.
    Creates OpenModelica-compatible .mos scripts to import and simulate the model with .csv output.
    The .csv output is then compared against a reference result, possibly only on a subset of columns.
    """
    def __init__(self, package_folder, model_in_package, result_folder, tool="omc", modelica_version="default", dependencies=None):
        """
        Constructor of the RegresssionTest class.

        Parameters
        ----------
        package_folder : str or PathLike
            Path of the folder the Modelica package containing the model to be tested
        model_in_package : str
            Name of the model to be tested
        result_folder : str or PathLike
            Path of the folder where the output of the model testing shall be written to
        tool : str
            Simulator used to translate, compile and execute Modelica model. The only valid 
            tool right now is omc (OpenModelica Compiler). If no argument is specified, 
            RegressionTest will search the PATH variable for omc and will execute the tests if found.
        modelica_version : str
            Version of the Modelica standard library to be loaded before the test is executed.
            Default is "default", other meaningful values can be "3.2.3" or "4.0.0".
        dependencies : None or List[str]
            Optional list of strings with names of packages that the package to be tested depends on.
            Each dependency must point to the .mo file that defines the dependency. E.g. if the
            dependency is an entire package, it must be the path to the respective package's package.mo.
        """

        self.template_folder_path = pathlib.Path(__file__).parent.absolute() / "templates"
        self.package_folder_path = pathlib.Path(package_folder).absolute()
        self.model_in_package = model_in_package
        self.result_folder_path = pathlib.Path(result_folder).absolute()
        self.initial_cwd = os.getcwd()
        self.modelica_version = modelica_version
        self.dependencies = dependencies

        if tool != None:
            self.tools = [tool]
        else:
            self.tools = [tl for tl in ["omc"] if shutil.which(tl) != None]

        self.result_folder_created = False

    @staticmethod
    def _unify_timestamps(results: List[pd.DataFrame], fill_in_method="ffill"):
        """
        From a list of pandas DataFrame objects containing the results of Modelica
        simulation runs, a list of extended results is generated, each of which
        has the same timestamps. To this end, a union of all timestamps from all
        results is created.

        Missing timestamps and such which occur multiple times
        are filled in until the multiplicity amongst all results to be compared
        is identical. Then, any missing data is filled in.

        For the filling in of data, different methods can be specified with the
        fill_in_method parameter.

        Parameters
        ----------
        results : List[pd.DataFrame]
            List of pandas DataFrame objects containing the results of Modelica
            simulation runs
        fill_in_method : str
            Valid methods are "ffill", "bfill", "interpolate" where
            ffill and bfill are the forward fill and backward fill methods from
            pandas.DataFrame.fillna and "interpol" uses linear interpolation
            as in pandas.DataFrame.interpol

        Returns
        -------
        out : List[pd.DataFrame]
            List of extended pandas DataFrame objects, each of which has the
            same timestamps and missing data has been filled in
        """
        # Shortcut: If timestamps match, then simply return the results unchanged
        all_equal = True
        for i in range(1, len(results)):
            all_equal = all_equal \
                        and (results[0]["time"].values.shape == results[i]["time"].values.shape) \
                        and np.allclose(results[0]["time"].values, results[i]["time"].values, atol=1e-15, rtol=1e-15)

            if not all_equal:
                break

        if all_equal:
            return results

        # Check if start times and end times match over the various results
        start_times = np.zeros(shape=(len(results),))
        end_times = np.zeros(shape=(len(results),))
        for i in range(0, len(results)):
            start_times[i] = results[i]["time"].min()
            end_times[i] = results[i]["time"].max()

        if not math.isclose(np.min(start_times), np.max(start_times), rel_tol=1e-5, abs_tol=1e-3):
            raise ValueError("The simulation start times of the results to not match. "\
                             f"Maximum deviation is {np.max(start_times) - np.min(start_times)} " \
                             f"and stems from results with indices {np.argmax(start_times)} and {np.argmin(start_times)}")

        if not math.isclose(np.min(end_times), np.max(end_times), rel_tol=1e-5, abs_tol=1e-3):
            raise ValueError("The simulation end times of the results to not match. "\
                             f"Maximum deviation is {np.max(end_times) - np.min(end_times)} " \
                             f"and stems from results with indices {np.argmax(end_times)} and {np.argmin(end_times)}")

        # Timestamps from all results and their highest multiplicity amongst all results
        timestamps_per_result = [dict(zip(*np.unique(results[i]["time"].values, return_counts=True)))
                                 for i in range(0, len(results))]

        all_timestamps_unique = np.unique(np.hstack([results[i]["time"].values for i in range(0, len(results))]).transpose())
        timestamps = np.zeros(sum([len(results[i]["time"].values) for i in range(0, len(results))]))
        ctr = 0
        for tstamp in all_timestamps_unique:
            max_occur = max([timestamps_per_result[i][tstamp] for i in range(0, len(results))
                             if tstamp in timestamps_per_result[i].keys()])
            timestamps[ctr:ctr + max_occur] = tstamp
            ctr += max_occur

        timestamps = timestamps[0:ctr]

        unique, counts = np.unique(timestamps, return_counts=True)
        all_timestamps_occur = dict(zip(unique, counts))

        # Create the extended results
        results_ext = [pd.DataFrame(0, index=np.arange(len(timestamps)), columns=results[i].keys()) for i in range(0, len(results))]

        # Add rows with NaNs for every timestamp that is not present or does not have the right multiplicity
        for i in range(0, len(results)):
            # Allocate array
            missing_timestamps = np.zeros(len(timestamps))

            # Find out which timestamps are missing
            cur_occur = timestamps_per_result[i]

            missing_ctr = 0
            for tstamp in all_timestamps_occur:
                if tstamp in cur_occur.keys():
                    number_misses = all_timestamps_occur[tstamp] - cur_occur[tstamp]
                    if number_misses > 0:
                        missing_timestamps[missing_ctr:missing_ctr + number_misses] = tstamp
                        missing_ctr += number_misses
                else:
                    number_misses = all_timestamps_occur[tstamp]
                    missing_timestamps[missing_ctr:missing_ctr + number_misses] = tstamp
                    missing_ctr += number_misses

            missing_timestamps = missing_timestamps[0:missing_ctr]

            # Add data rows for missing timestamps
            missing_tstamp_rows = pd.DataFrame(np.nan, index=range(0, len(missing_timestamps)),
                                               columns=results[i].columns)
            missing_tstamp_rows["time"] = missing_timestamps

            results_ext[i] = pd.concat([results[i], missing_tstamp_rows], axis=0)
            results_ext[i] = results_ext[i].sort_values("time", kind="mergesort")

            new_index = range(0, len(timestamps))
            results_ext[i].index = new_index

            # Fill in values at missing timestamps
            if fill_in_method == "ffill":
                results_ext[i] = results_ext[i].ffill(axis=0)
            elif fill_in_method == "bfill":
                results_ext[i] = results_ext[i].bfill(axis=0)
            elif fill_in_method == "interpolate":
                results_ext[i] = results_ext[i].interpolate(axis=0)
            else:
                raise ValueError("Unknown filling method for NaN values")

        return results_ext

    def _import_and_simulate(self):
        """
        Imports and simulates the model from the Modelica package specified in the constructor.

        Returns
        -------
        out : None
        """
        print("Simulating model {} using the simulation tools: {}" .format(self.model_in_package, ", ".join(self.tools)))

        # Create folder where output of the simulation shall be stored
        if not self.result_folder_path.exists():
            pathlib.Path.mkdir(self.result_folder_path)
            self.result_folder_created = True

        os.chdir(self.result_folder_path)

        # Run the scripts for import and simulation
        self._run_model()

        os.chdir(self.initial_cwd)

        return

    @staticmethod
    def compare_csv_files(reference_result, simulation_result, tol=1e-7, validated_cols=[],
                          metric=metrics.norm_infty_dist,
                          unify_timestamps=True, fill_in_method="ffill", write_comparison=True):
        """
        Compares two CSV files from Modelica simulation runs, one as a reference result, the other one as the actual
        simulation result.

        The default values of this function are identical to the ones in RegressionTest.compare_result

        Parameters
        ----------
        reference_result : str
            Path to a reference .csv file
        simulation_result  : str
            Path to a simulation result .csv file
        tol : float
            See doc string of RegressionTest.compare_result
        validated_cols : list
            See doc string of RegressionTest.compare_result
        metric : Callable
            See doc string of RegressionTest.compare_result
        unify_timestamps : bool
            See doc string of RegressionTest.compare_result
        fill_in_method : str
            See doc string of RegressionTest.compare_result
        write_comparison : bool
            See doc string of RegressionTest.compare_result

        Returns
        -------
        out : None
        """
        ref_data = pd.read_csv(filepath_or_buffer=reference_result, delimiter=',')
        sim_data = pd.read_csv(filepath_or_buffer=simulation_result, delimiter=',')

        if unify_timestamps:
            data_ext = RegressionTest._unify_timestamps([ref_data, sim_data], fill_in_method)
            ref_data = data_ext[0]
            sim_data = data_ext[1]

        # Determine common columns by comparing column headers
        common_cols = set(ref_data.columns).intersection(set(sim_data.columns))

        if not validated_cols:
            validated_cols = common_cols

        # Check if validated_cols is meaningful
        validated_cols = set(validated_cols)
        if "time" in validated_cols:
            validated_cols.remove("time")  # Ignore time column

        if not validated_cols.issubset(set(ref_data.columns)):
            missing_cols = validated_cols.difference(set(ref_data.columns))
            raise ValueError(f"The reference data {reference_result} does not contain all entries of validated_cols. "
                             f"Missing: {missing_cols}")

        if not validated_cols.issubset(set(sim_data.columns)):
            missing_cols = validated_cols.difference(set(sim_data.columns))
            raise ValueError(f"The simulation data {simulation_result} does not contain all entries of validated_cols." 
                             f"Missing: {missing_cols}")

        if len(validated_cols) == 0:
            raise ValueError(f"validated_cols must contain at least one common variable in "
                             f"reference {reference_result} and simulation result {simulation_result}")

        failed_cols = {}
        for c in validated_cols:
            print("Comparing column \"{}\"".format(c))
            delta = metric(ref_data[["time", c]].values, sim_data[["time", c]].values)

            if type(delta) is np.ndarray:
                if np.any(delta[:, 1] >= tol):
                    delta_gt_tol = np.where(delta >= tol, delta, 0.0)
                    failed_cols[c] = pd.DataFrame(data=delta_gt_tol, columns=["time", "delta"])
            else:
                if np.abs(delta) >= tol:
                    failed_cols[c] = delta

        if failed_cols:
            if write_comparison:
                RegressionTest._write_csv_comparison(reference_result, simulation_result,
                                                     failed_cols, fill_in_method)

            raise AssertionError(
                f"Values of results {simulation_result} and {reference_result} are different in columns "
                f"{list(failed_cols.keys())} by more than {tol}. ")

        return

    def compare_result(self, reference_result, tol=1e-7, validated_cols=[],
                       metric=metrics.norm_infty_dist,
                       unify_timestamps=True, fill_in_method="ffill", write_comparison=True):
        """
        Executes simulation and then compares the obtained result and the reference result along the
        validated columns. Throws an exception (AssertionError) if the deviation is larger or equal to tol.

        Parameters
        ----------
        reference_result : str
            Path to a reference .csv file containing the expected results of the model
        tol : float
            Absolute tolerance up to which deviation in the comparison metric is accepted
        validated_cols : list
            List of variable names (from the file header) in the reference .csv file that are used in the regression test
            Important: All entries of validated_cols must be present in both the reference result and the actual result.
        metric : Callable
            Metric-like function that is used to compute the distance between the reference result and the actual result
            produced by the simulation.

            The return value of the metric function MUST either be

            a nonnegative scalar value (i.e. a time-wise nonlocalized deviation)

            or

            an np.ndarray of shape (N,2) containing a timeseries of localized deviations between r_ref and r_act
            (i.e. a time-wise localized metric evaluation).

            The timestamps in a returned timeseries do not need to match those of r_ref or of r_act. Timestamp
            unification will be used when plotting localized deviations.

            Default is the infinity-norm on the difference between reference result and actual result.

            :math:`\| r_\text{ref} - r_\text{act} \|_{\infty} = \max_{i \in 1,\ldots,N} |r_\text{ref}[t_i] - r_\text{act}[t_i]|`

            where :math:`r_\text{ref}, r_\text{act} \in \mathbb{R}^N` denote the reference and the actual result
            with timestamps :math:`t_i, i \in 1,\ldots,N`. Note that the timestamps of both results are unified using
            the method _unify_timestamps.

            This default function is implemented in 

                metric=metrics.norm_infty_dist

            but we could also have put an in-place definition using lambda functions like

                metric=lambda r_ref, r_act: np.linalg.norm(r_ref[:, 1] - r_act[:, 1], ord=np.inf)

            A default implementation of a metric returning a timeseries of deviations would be

                metric=mopyregtest.metrics.abs_dist_ptwise

            which is simply :math:`\Big\{ (t_i, |r_\text{ref}[t_i] - r_\text{act}[t_i]| : i \in 1,\ldots,N \Big\}`

        unify_timestamps : bool
            Boolean controlling whether the timestamp unification shall be called in compare_result before evaluating
            the metric. Default=True.

            If set to False, then the function passed in the argument "metric" will be evaluated for matching columns
            (from validated_cols) of reference and actual result. In this case the definition of the metric has to
            ensure that computations are meaningful, e.g. for non-matching dimensions or different timestamps.
        fill_in_method : str
            Defines the method used to fill in data when calling RegressionTest._unify_timestamps and if results have
            different timestamps and cannot be compared pointwise.

            Valid methods are "ffill", "bfill", "interpolate" where
            ffill and bfill are the forward fill and backward fill methods from
            pandas.DataFrame.fillna and "interpol" uses linear interpolation
            as in pandas.DataFrame.interpol

        write_comparison : bool
            If there are result comparisons that have failed, this will trigger writing a comparison csv file to the
            folder where the actual simulation result is found and be called <simulation_result_name_root>_compare.csv.
            Default=True.

        Returns
        -------
        out : None
        """
        print("\nTesting model {}".format(self.model_in_package))

        self._import_and_simulate()
        simulation_result = str(self.result_folder_path / self.model_in_package) + "_res.csv"

        print("Comparing simulation result {} and reference {}".format(simulation_result, reference_result))

        RegressionTest.compare_csv_files(reference_result, simulation_result, tol, validated_cols,
                                         metric,
                                         unify_timestamps, fill_in_method, write_comparison)

        return

    def cleanup(self, ask_confirmation=True):
        """
        USE WITH CARE

        Cleans up the intermediate result folders created by the external simulation
        tool during the execution of the simulation model created from the model and
        package to be tested as specified in the constructor.

        Parameters
        ----------
        ask_confirmation : bool
            Boolean to force asking for confirmation before deletion (default=True)

        Returns
        -------
        out : None
        """

        # Only cleanup folders created here
        if self.result_folder_created:
            if ask_confirmation:
                do_delete = utils.ask_confirmation(
                    "\nDo you want to delete the folder \n\n\t{}\n\nand all its subfolders?".format(self.result_folder_path))
                if do_delete:
                    shutil.rmtree(self.result_folder_path)
            else:
                shutil.rmtree(self.result_folder_path)
        else:
            print("\nThe result folder \n\n\t{}\n\nwas not created by this program. Will not clean up. ".format(
                self.result_folder_path))

        return

    @staticmethod
    def _check_tool_message(msg: str):
        if msg.lower().find("error") != -1:
            raise AssertionError(f"The simulation tool produced error messages: {msg}")
        if msg.lower().find("fatal") != -1:
            raise AssertionError(f"The simulation tool produced fatal messages: {msg}")

        return

    def _run_model(self):
        """
        Executes the Modelica simulation tool as an external process called on the
        model and the package to be tested, as specified in the constructor.


        Returns
        -------
        out : None

        """
        for tool in self.tools:
            tool_executable = tool

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
                repl_dict["MODELICA_VERSION"] = self.modelica_version

                if self.dependencies:
                    load_str = ""
                    for d in self.dependencies:
                        load_str += "\n + loadFile(\"{}\",\"UTF-8\",true);".format(d)

                    repl_dict["DEPENDENCIES"] = load_str
                else:
                    repl_dict["DEPENDENCIES"] = ""

                utils.replace_in_file(self.result_folder_path / model_import_mos, repl_dict)

                # Run the import script and write the output of the OpenModelica Compiler (omc) to omc_output
                proc_return = subprocess.run([tool_executable, model_import_mos], check=True, capture_output=True)
                omc_messages = proc_return.stdout.decode("utf-8").strip("\'").strip("\n")
                RegressionTest._check_tool_message(omc_messages)

                (start_time, stop_time, tolerance, num_intervals, interval) = omc_messages.split("\n")[-1].lstrip('(').rstrip(')').split(',')

                # Modify the simulation template
                if platform.system() == 'Windows':
                    repl_dict["SIMULATION_BINARY"] = "{}.exe".format(self.model_in_package)
                elif platform.system() == 'Linux':
                    repl_dict["SIMULATION_BINARY"] = "./{}".format(self.model_in_package)
                repl_dict["START_TIME"] = start_time
                repl_dict["STOP_TIME"] = stop_time
                repl_dict["TOLERANCE"] = tolerance
                repl_dict["NUM_INTERVALS"] = num_intervals

                utils.replace_in_file(self.result_folder_path / model_simulate_mos, repl_dict)

                # Run the simulation script and append the output of the OpenModelica Compiler (omc) to omc_output
                proc_return = subprocess.run([tool_executable, model_simulate_mos], capture_output=True)
                omc_messages = proc_return.stdout.decode("utf-8").strip("\'").strip("\n")
                RegressionTest._check_tool_message(omc_messages)

        return

    @staticmethod
    def _write_csv_comparison(reference_result, simulation_result, failed_cols, fill_in_method="ffill",
                              comparison_fname=""):
        """
        Writes a comparison CSV file from the result comparison of reference_result and actual simulation result,
        which includes also the results for the failed variable columns in the output. Note that to have results in
        one common CSV files, the timestamps must be identical. The output CSV file has a
        format like:

        root
            |
            + -- reference
                |
                +...
            + -- actual
                    |
                    +...
            + -- failed
                    |
                    + var_failed_0
                        |
                        + reference
                        |
                        + actual
                        |
                        + [delta_nonloc|delta_greater_tol]
                    |
                    + var_failed_1
                        |
                        + reference
                        |
                        + actual
                        |
                        + [delta_nonloc|delta_greater_tol]

        In case of the metric used in the comparison returning a scalar value, the deviation is a constant
        (because it cannot be localized), and is called delta_nonloc.

        In case of metric returning a timeseries, it contains the part of the timeseries where the error exceeds the
        tolerance, and is called delta_greater_tol.

        Parameters
        ----------
        reference_result : str
            Path to a reference .csv file
        simulation_result  : str
            Path to a simulation result .csv file
        failed_cols : dict
            A dictionary mapping the name of the column for which comparison between r_ref and r_act failed to the
            deviation delta. This delta MUST FOR ALL COLUMNS have the same type, which can either be

            a nonnegative real value

            or

            a pandas DataFrame with columns ["time", "delta"].
        fill_in_method : str
            See doc string of RegressionTest.compare_result
        comparison_fname : str
            Path to where the output shall be written. If not specified, the output filename
            is <path/to/simulation_result/simulation_result_name_root>_compare.csv

        Returns
        -------
        out : None
        """

        if not comparison_fname:
            comparison_fname = (pathlib.Path(simulation_result).absolute().parent /
                                f"{pathlib.Path(simulation_result).stem}_comparison.csv")

        ref_data = pd.read_csv(filepath_or_buffer=reference_result, delimiter=',')
        sim_data = pd.read_csv(filepath_or_buffer=simulation_result, delimiter=',')

        # Determine if the delta in failed_cols between actual and reference is a (nonlocal) scalar or a timeseries
        is_scalar = True
        for v in failed_cols.values():
            if type(v) is pd.DataFrame:
                is_scalar = False
                break

        # Timestamps must be unified to have both results side by side
        if is_scalar:  # Only unify ref_data and sim_data, make delta a constant timeseries
            data_ext = RegressionTest._unify_timestamps([ref_data, sim_data], fill_in_method)
            ref_data_ext = data_ext[0]
            sim_data_ext = data_ext[1]

            timestamps_ext = sim_data_ext["time"].values
            failed_cols_ext = {}
            for c in failed_cols.keys():
                delta_ext = failed_cols[c]*np.ones(shape=timestamps_ext.shape)
                failed_cols_ext[c] = pd.DataFrame(data=np.vstack((timestamps_ext, delta_ext)).transpose(),
                                                  columns=["time", "delta"])
        else:  # Unify ref_data, sim_data and all delta timeseries
            failed_keys = list(failed_cols.keys())
            data_ext = RegressionTest._unify_timestamps([ref_data, sim_data] + list(failed_cols.values()))
            ref_data_ext = data_ext[0]
            sim_data_ext = data_ext[1]

            failed_cols_ext = {}
            for i in range(0, len(failed_keys)):
                failed_cols_ext[failed_keys[i]] = data_ext[2+i]

        # Extract the columns for time and the failed comparisons
        time_data = sim_data_ext["time"]
        ref_data_ext.drop(columns=["time"], inplace=True)
        sim_data_ext.drop(columns=["time"], inplace=True)
        for c in failed_cols_ext.keys():
            failed_cols_ext[c].drop(columns=["time"], inplace=True)

        failed_tseries = pd.DataFrame()
        for c in failed_cols_ext.keys():
            c_ref = ref_data_ext[c]
            c_ref.name = f"failed.{c}.reference"
            c_act = sim_data_ext[c]
            c_act.name = f"failed.{c}.actual"
            c_delta = failed_cols_ext[c]["delta"]
            if is_scalar:
                c_delta.name = f"failed.{c}.delta_nonloc"
            else:
                c_delta.name = f"failed.{c}.delta_greater_tol"
            failed_tseries = pd.concat([failed_tseries, c_ref, c_act, c_delta], axis=1)

        # Concatenate results and prepend result headers
        ref_data_ext.columns = [f"reference.{c}" for c in ref_data_ext.columns]
        sim_data_ext.columns = [f"actual.{c}" for c in sim_data_ext.columns]
        comparison_csv = pd.concat([time_data, ref_data_ext, sim_data_ext, failed_tseries], axis=1)
        comparison_csv.to_csv(comparison_fname, sep=",")

        return
