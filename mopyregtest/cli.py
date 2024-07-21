"""
MoPyRegtest: A Python enabled simple regression testing framework for Modelica models.

Copyright (c) Dr. Philipp Emanuel Stelzig, 2019--2023.

MIT License. See the project's LICENSE file.
"""

import argparse
import pathlib
import sys
from mopyregtest import metrics
from mopyregtest import Generator, RegressionTest


def metric_str_to_func(m: str):
    if m == "norm_p_dist":
        return metrics.norm_p_dist
    elif m == "norm_infty_dist":
        return metrics.norm_infty_dist
    elif m == "Lp_dist":
        return metrics.Lp_dist
    elif m == "Linfty_dist":
        return metrics.Linfty_dist
    elif m == "abs_dist_ptwise":
        return metrics.abs_dist_ptwise
    else:
        raise ValueError("Invalid value for metric")


def generate(args):
    test_name = args.test_name
    test_folder = pathlib.Path(args.test_folder)
    result_folder = "results"
    package_folder = args.package_folder
    models_in_package = args.models_in_package.split(",")

    if args.references is not None:
        ref_pairs = args.references.split(",")
        references = {}
        for i in range(0, len(ref_pairs)):
            sep_idx = ref_pairs[i].find(":")
            if sep_idx == -1 or sep_idx == len(ref_pairs[i])-1:
                raise ValueError(f"The argument {args.references} has no valid reference string format. " 
                                 "Must be like <model name1>:</path/to/ref1.csv>,<model name2>:</path/to/ref2.csv>")

            k = ref_pairs[i][0:sep_idx]
            v = ref_pairs[i][sep_idx+1:]
            references[k] = v
    else:
        references = None

    metric = metrics.norm_infty_dist
    if args.metric is not None:
        metric = metric_str_to_func(args.metric)

    gen = Generator(package_folder=package_folder, models_in_package=models_in_package, metric=metric, tol=args.tol)
    gen.generate_tests(test_folder, test_name, result_folder, references)

    return


def compare(args):
    ref_result = pathlib.Path(args.ref_csv_file).absolute()
    act_result = pathlib.Path(args.act_csv_file).absolute()

    if args.validated_cols is not None:
        validated_cols = args.validated_cols.split(",")
    else:
        validated_cols = []

    metric = metrics.norm_infty_dist
    if args.metric is not None:
        metric = metric_str_to_func(args.metric)

    RegressionTest.compare_csv_files(ref_result, act_result,
                                     args.tol, validated_cols, metric, True, args.fill_in_method)

    return


def parse_args(cmd_args):
    # Main parser
    main_parser = argparse.ArgumentParser(
        prog="mopyregtest",
        epilog="Command line interface for MoPyRegtest, the CI friendly regression testing tool for Modelica models. "
               "This command line interface is a simplified version to interact with MoPyRegtest. "
               "If you want to use all options, please consider creating a dedicated Python script.")
    subparsers = main_parser.add_subparsers(title="subcommands", help="mopyregtest CLI command overview")

    # mopyregtest generate
    generate_parser = subparsers.add_parser("generate", help="Generate test case definitions")

    # mopyregtest generate [--metric {norm_p_dist,norm_infty_dist,Lp_dist,Linfty_dist}] [--references REFERENCES]  test_folder test_name package_folder models_in_package
    generate_parser.add_argument("test_folder", type=str, help="Path where test shall be generated. Advice: Should not exist yet")
    generate_parser.add_argument("test_name", type=str, help="Name of the test. Do not use special characters")
    generate_parser.add_argument("package_folder", type=str,
                                 help="Path to Modelica package from which models shall be tested. Relative paths are possible")
    generate_parser.add_argument("models_in_package", type=str,
                                 help="Comma separated list of model names like <model name1>,<model name2> "
                                      "to be turned into regression tests")
    generate_parser.add_argument("--metric", type=str,
                                 help="Metric to be used. Choose here from predefined values. "
                                      "For user-defined metrics please consider creating the tests with a dedicated script. "
                                      "If omitted, the default is norm_infty_dist",
                                 choices=["norm_p_dist", "norm_infty_dist", "Lp_dist", "Linfty_dist", "abs_dist_ptwise"],
                                 default="norm_infty_dist")
    generate_parser.add_argument("--tol", type=float,
                                 help="Absolute tolerance up to which deviation in the comparison metric is accepted",
                                 default=1e-7)
    generate_parser.add_argument("--references", type=str,
                                 help="Comma separated list like <model name1>:</path/to/ref1.csv>,<model name2>:</path/to/ref2.csv>. "
                                      "Missing references for models here will be generated.")
    generate_parser.set_defaults(func=generate)

    # mopyregtest compare
    compare_parser = subparsers.add_parser("compare", help="Compare CSV result files")

    # mopyregtest compare [--metric {norm_p_dist,norm_infty_dist,Lp_dist,Linfty_dist}] [--validated-cols VALIDATED_COLS] ref_csv_file act_csv_file
    compare_parser.add_argument("ref_csv_file", type=str, help="Path of the reference CSV result file to compare")
    compare_parser.add_argument("act_csv_file", type=str, help="Path of the actual CSV result file to compare")
    compare_parser.add_argument("--metric", type=str,
                                help="Metric to be used. Choose here from predefined values. "
                                     "For user-defined metrics please consider creating the tests with a dedicated script.",
                                choices=["norm_p_dist", "norm_infty_dist", "Lp_dist", "Linfty_dist", "abs_dist_ptwise"],
                                default="norm_infty_dist")
    compare_parser.add_argument("--validated-cols", type=str,
                                help="Comma separated list like <var name 1>,<var name 2>. "
                                     "If omitted, then all common column names from both CSV files will be used.")
    compare_parser.add_argument("--tol", type=float,
                                help="Absolute tolerance up to which deviation in the comparison metric is accepted",
                                default=1e-7)
    compare_parser.add_argument("--fill-in-method", type=str,
                                help="Defines the method used to fill in data when calling RegressionTest._unify_timestamps",
                                choices=["ffill", "bfill", "interpolate"], default="ffill")
    compare_parser.set_defaults(func=compare)

    args = main_parser.parse_args(cmd_args)
    args.func(args)


def main():
    if len(sys.argv) <= 1:
        parse_args(["--help"])
    else:
        parse_args(sys.argv[1:])
