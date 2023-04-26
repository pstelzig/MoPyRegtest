import unittest
import mopyregtest
import pandas as pd

class TestCompareResults(unittest.TestCase):
    def test_unify_timestamps_ffill(self):
        res1 = pd.DataFrame(data=[[0.0, 1.0, 2.0], [0.5, 2.0, 4.0], [0.75, 3.0, 6.0], [1.0, 4.0, 8.0]],
                            columns=["time", "quant1", "quant2"])
        res2 = pd.DataFrame(data=[[0.0, 1.0, 2.0], [0.25, 1.5, 3.0], [0.5, 2.0, 4.0], [1.0, 4.0, 8.0]],
                            columns=["time", "quant1", "quant2"])

        res1_ext_expect = pd.DataFrame(data=[[0.0, 1.0, 2.0], [0.25, 1.0, 2.0], [0.5, 2.0, 4.0], [0.75, 3.0, 6.0], [1.0, 4.0, 8.0]],
                            columns=["time", "quant1", "quant2"])

        res2_ext_expect = pd.DataFrame(data=[[0.0, 1.0, 2.0], [0.25, 1.5, 3.0], [0.5, 2.0, 4.0], [0.75, 2.0, 4.0], [1.0, 4.0, 8.0]],
                            columns=["time", "quant1", "quant2"])

        results_ext = mopyregtest.RegressionTest._unify_timestamps([res1, res2])

        self.assertIsNone(pd.testing.assert_frame_equal(res1_ext_expect, results_ext[0]))
        self.assertIsNone(pd.testing.assert_frame_equal(res2_ext_expect, results_ext[1]))

    def test_unify_timestamps_bfill(self):
        res1 = pd.DataFrame(data=[[0.0, 1.0, 2.0], [0.5, 2.0, 4.0], [0.75, 3.0, 6.0], [1.0, 4.0, 8.0]],
                            columns=["time", "quant1", "quant2"])
        res2 = pd.DataFrame(data=[[0.0, 1.0, 2.0], [0.25, 1.5, 3.0], [0.5, 2.0, 4.0], [1.0, 4.0, 8.0]],
                            columns=["time", "quant1", "quant2"])

        res1_ext_expect = pd.DataFrame(data=[[0.0, 1.0, 2.0], [0.25, 2.0, 4.0], [0.5, 2.0, 4.0], [0.75, 3.0, 6.0], [1.0, 4.0, 8.0]],
                            columns=["time", "quant1", "quant2"])

        res2_ext_expect = pd.DataFrame(data=[[0.0, 1.0, 2.0], [0.25, 1.5, 3.0], [0.5, 2.0, 4.0], [0.75, 4.0, 8.0], [1.0, 4.0, 8.0]],
                            columns=["time", "quant1", "quant2"])

        results_ext = mopyregtest.RegressionTest._unify_timestamps([res1, res2], fill_in_method="bfill")

        self.assertIsNone(pd.testing.assert_frame_equal(res1_ext_expect, results_ext[0]))
        self.assertIsNone(pd.testing.assert_frame_equal(res2_ext_expect, results_ext[1]))

    def test_unify_timestamps_interpolate(self):
        res1 = pd.DataFrame(data=[[0.0, 1.0, 2.0], [0.5, 2.0, 4.0], [0.75, 3.3, 6.6], [1.0, 4.0, 8.0]],
                            columns=["time", "quant1", "quant2"])
        res2 = pd.DataFrame(data=[[0.0, 1.0, 2.0], [0.25, 1.5, 3.0], [0.5, 2.0, 4.0], [1.0, 4.0, 8.0]],
                            columns=["time", "quant1", "quant2"])

        res1_ext_expect = pd.DataFrame(data=[[0.0, 1.0, 2.0], [0.25, 1.5, 3.0], [0.5, 2.0, 4.0], [0.75, 3.3, 6.6], [1.0, 4.0, 8.0]],
                            columns=["time", "quant1", "quant2"])

        res2_ext_expect = pd.DataFrame(data=[[0.0, 1.0, 2.0], [0.25, 1.5, 3.0], [0.5, 2.0, 4.0], [0.75, 3.0, 6.0], [1.0, 4.0, 8.0]],
                            columns=["time", "quant1", "quant2"])

        results_ext = mopyregtest.RegressionTest._unify_timestamps([res1, res2], fill_in_method="interpolate")

        self.assertIsNone(pd.testing.assert_frame_equal(res1_ext_expect, results_ext[0]))
        self.assertIsNone(pd.testing.assert_frame_equal(res2_ext_expect, results_ext[1]))
