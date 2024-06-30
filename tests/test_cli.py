import shutil
import unittest
import pathlib
from mopyregtest import cli

this_folder = pathlib.Path(__file__).absolute().parent

class TestCli(unittest.TestCase):
    def test_generate1(self):
        """
        Testing for default arguments in CLI: mopyregtest generate
        """
        cmd_args = ["generate",
                    str(this_folder / "../examples/generate_tests/gen_tests1"),
                    "BlocksLpDist_from_cli_1",
                    "~/.openmodelica/libraries/Modelica 4.0.0+maint.om/",
                    "Modelica.Blocks.Sources.Sine,Modelica.Blocks.Sources.ExpSine,Modelica.Blocks.Sources.Step"]

        cli.parse_args(cmd_args)

        return

    def test_generate2(self):
        """
        Testing for optional arguments in CLI: mopyregtest generate
        """
        cmd_args = ["generate",
                    "--metric=Lp_dist",
                    "--tol=1.2e-5",
                    str(this_folder / "../examples/generate_tests/gen_tests2"),
                    "BlocksLpDist_from_cli_2",
                    "~/.openmodelica/libraries/Modelica 4.0.0+maint.om/",
                    "Modelica.Blocks.Sources.Sine,Modelica.Blocks.Sources.ExpSine,Modelica.Blocks.Sources.Step"]

        cli.parse_args(cmd_args)

        return

    def test_generate3(self):
        """
        Testing for optional arguments in CLI: mopyregtest generate
        """
        cmd_args = ["generate",
                    "--metric=abs_dist_ptwise",
                    "--tol=1.2e-5",
                    "--references=Modelica.Blocks.Sources.Sine:{}".format(
                        this_folder / "../examples/test_user_defined_metrics/references/SineNoisy_res.csv"),
                    str(this_folder / "../examples/generate_tests/gen_tests3"),
                    "BlocksAbsDistPtwise_from_cli",
                    "~/.openmodelica/libraries/Modelica 4.0.0+maint.om/",
                    "Modelica.Blocks.Sources.Sine"]

        cli.parse_args(cmd_args)

        return

    def test_generate4(self):
        """
        Testing for generation to fail if the simulation model for which a test is
        being generated fails to build.
        """
        cmd_args = ["generate",
                    str(this_folder / "data/gentests"),
                    "FlawedModels_DoesNotBuild",
                    str(this_folder / "data/FlawedModels"),
                    "FlawedModels.DoesNotBuild"]

        with self.assertRaises(SystemExit) as e:
            cli.parse_args(cmd_args)

        self.assertEqual(e.exception.code, 1)

        # Clean up the generated regression tests as otherwise they will confuse unittest discovery
        shutil.rmtree(this_folder / "data/gentests")

        return

    def test_generate5(self):
        """

        """
        cmd_args = ["generate",
                    str(this_folder / "data/gentests"),
                    "FlawedModels_DoesNotFinish",
                    str(this_folder / "data/FlawedModels"),
                    "FlawedModels.DoesNotFinish"]

        cli.parse_args(cmd_args)

        # Clean up the generated regression tests as otherwise they will confuse unittest discovery
        shutil.rmtree(this_folder / "data/gentests")

        return

    def test_compare1(self):
        """
        Testing for default arguments in CLI: mopyregtest compare
        """
        cmd_args = ["compare",
                    str(this_folder / "../examples/test_user_defined_metrics/references/SineNoisy_res.csv"),
                    str(this_folder / "../examples/test_user_defined_metrics/references/SineNoisy_res.csv")]

        cli.parse_args(cmd_args)

        return

    def test_compare2(self):
        """
        Testing for optional arguments in CLI: mopyregtest compare
        """
        cmd_args = ["compare",
                    "--metric=Lp_dist",
                    "--tol=2.5e-4",
                    "--validated-cols=sine.y,y",
                    "--fill-in-method=interpolate",
                    str(this_folder / "../examples/test_user_defined_metrics/references/SineNoisy_res.csv"),
                    str(this_folder / "../examples/test_user_defined_metrics/references/SineNoisy_res.csv")]

        cli.parse_args(cmd_args)

        return

    def test_compare3(self):
        """
        Testing for correctly raised error in CLI when comparing different results: mopyregtest compare
        """
        cmd_args = ["compare",
                    "--validated-cols=y",
                    "--fill-in-method=interpolate",
                    str(this_folder / "../examples/test_user_defined_metrics/references/SineNoisy_res.csv"),
                    str(this_folder / "../examples/test_user_defined_metrics/references/Sine_res.csv")]

        self.assertRaises(AssertionError, cli.parse_args, cmd_args=cmd_args)
        self.assertTrue(
            (this_folder / "../examples/test_user_defined_metrics/references/Sine_res_comparison.csv").exists())

        return

    def test_compare4(self):
        """
        Testing for tol in CLI when comparing different results with sufficiently large tol: mopyregtest compare
        """
        cmd_args = ["compare",
                    "--validated-cols=y",
                    "--tol=0.012",
                    "--fill-in-method=interpolate",
                    str(this_folder / "../examples/test_user_defined_metrics/references/SineNoisy_res.csv"),
                    str(this_folder / "../examples/test_user_defined_metrics/references/Sine_res.csv")]

        cli.parse_args(cmd_args)

        return

    def test_compare5(self):
        """
        Testing for new metric argument abs_dist_ptwise in CLI: mopyregtest compare
        """
        cmd_args = ["compare",
                    "--metric=abs_dist_ptwise",
                    "--tol=2.5e-4",
                    "--validated-cols=y",
                    "--fill-in-method=interpolate",
                    str(this_folder / "../examples/test_user_defined_metrics/references/SineNoisy_res.csv"),
                    str(this_folder / "../examples/test_user_defined_metrics/references/Sine_res.csv")]

        self.assertRaises(AssertionError, cli.parse_args, cmd_args=cmd_args)
        self.assertTrue(
            (this_folder / "../examples/test_user_defined_metrics/references/Sine_res_comparison.csv").exists())

        return


if __name__ == '__main__':
    unittest.main()
