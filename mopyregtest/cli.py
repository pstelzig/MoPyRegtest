"""
MoPyRegtest: A Python enabled simple regression testing framework for Modelica models.

Copyright (c) Dr. Philipp Emanuel Stelzig, 2019--2023.

MIT License. See the project's LICENSE file.
"""

import argparse
import pathlib
from mopyregtest import metrics
from mopyregtest import Generator


def generate(args):
    test_name = args.test_name
    test_folder = pathlib.Path(args.test_folder)
    result_folder = "results"
    package_folder = args.package_folder
    models_in_package = args.models_in_package.split(",")

    if args.references is not None:
        references = {r.split(":")[0] : r.split(":")[1] for r in args.references.split(",")}
    else:
        references = None

    metric = metrics.norm_infty_dist
    if args.metric is not None:
        if args.metric == "norm_p_dist":
            metric = metrics.norm_p_dist
        elif args.metric == "norm_infty_dist":
            metric = metrics.norm_infty_dist
        elif args.metric == "Lp_dist":
            metric = metrics.Lp_dist
        elif args.metric == "Linfty_dist":
            metric = metrics.Linfty_dist
        else:
            raise ValueError("Invalid value for metric")

    gen = Generator(package_folder=package_folder, models_in_package=models_in_package, metric=metric)
    gen.generate_tests(test_folder, test_name, result_folder, references)

    return


def main():
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
    generate_parser.add_argument("--metric", type=str, help="Metric to be used. Choose here from predefined values. "
                                                            "For user-defined metrics please consider creating the tests with a dedicated script.",
                                 choices=["norm_p_dist", "norm_infty_dist", "Lp_dist", "Linfty_dist"], default="norm_infty_dist")
    generate_parser.add_argument("--references", type=str,
                                 help="Comma separated list like <model name1>:</path/to/ref1.csv>,<model name2>:</path/to/ref2.csv>. "
                                      "Missing references for models here will be generated.")
    generate_parser.set_defaults(func=generate)

    args = main_parser.parse_args()
    args.func(args)
