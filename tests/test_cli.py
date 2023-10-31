import unittest
import pathlib
from mopyregtest import cli

this_folder = pathlib.Path(__file__).absolute().parent

class TestCli(unittest.TestCase):
    def test_generate(self):
        cmd_args = ["generate",
                    "--metric=Lp_dist",
                    "--tol=1.2e-5",
                    str(this_folder / "../examples/generate_tests/gen_tests"),
                    "BlocksLpDist_from_cli",
                    "~/.openmodelica/libraries/Modelica 4.0.0+maint.om/",
                    "Modelica.Blocks.Sources.Sine,Modelica.Blocks.Sources.ExpSine,Modelica.Blocks.Sources.Step"]

        cli.parse_args(cmd_args)

        return

    def test_compare1(self):
        cmd_args = ["compare",
                     "--metric=Lp_dist",
                     "--tol=2.5e-4",
                     "--vars=sine.y,y",
                     "--fill-in-method=interpolate",
                     str(this_folder / "../examples/test_user_defined_metrics/references/SineNoisy_res.csv"),
                     str(this_folder / "../examples/test_user_defined_metrics/references/SineNoisy_res.csv")]

        cli.parse_args(cmd_args)

        return

    def test_compare2(self):
        cmd_args = ["compare",
                     "--vars=y",
                     "--fill-in-method=interpolate",
                     str(this_folder / "../examples/test_user_defined_metrics/references/SineNoisy_res.csv"),
                     str(this_folder / "../examples/test_user_defined_metrics/references/Sine_res.csv")]

        self.assertRaises(AssertionError, cli.parse_args, cmd_args=cmd_args)

        return
