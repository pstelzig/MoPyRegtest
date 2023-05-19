import unittest
import numpy as np
import mopyregtest

class TestMetrics(unittest.TestCase):
    def test_Lp_norm(self):
        f = np.array([[0, 1],
                      [1, 2],
                      [3, -3],
                      [10, -5]])

        p = 2.0
        self.assertAlmostEquals(mopyregtest.metrics.Lp_norm(f), (1-0) * 1**p + (3-1) * 2**p + (10-3) * 3**p)

        p = 3.0
        self.assertAlmostEquals(mopyregtest.metrics.Lp_norm(f, p), (1-0) * 1**p + (3-1) * 2**p + (10-3) * 3**p)

        p = 1.0
        self.assertAlmostEquals(mopyregtest.metrics.Lp_norm(f, p), (1-0) * 1**p + (3-1) * 2**p + (10-3) * 3**p)

    def test_Lp_dist(self):
        f1 = np.array([[0, 1],
                       [1, 2],
                       [3, -3],
                       [10, -5]])

        f2 = np.array([[0, 7],
                       [1, -2],
                       [3, 5],
                       [10, 2]])

        f3 = np.array([[0, 1],
                       [2, 2],
                       [3, -3],
                       [10, -5]])

        f4 = np.array([[-1, 1],
                       [0, 1],
                       [2, 2],
                       [3, -3],
                       [10, -5]])

        p = 2.0
        self.assertAlmostEquals(mopyregtest.metrics.Lp_dist(f1, f2), (1-0) * 6**p + (3-1) * 4**p + (10-3) * 8**p)

        p = 3.0
        self.assertAlmostEquals(mopyregtest.metrics.Lp_dist(f1, f2, p), (1-0) * 6**p + (3-1) * 4**p + (10-3) * 8**p)

        p = 2.0
        self.assertRaises(ValueError, mopyregtest.metrics.Lp_dist, f1=f1, f2=f3, p=p)

        p = 2.0
        self.assertRaises(ValueError, mopyregtest.metrics.Lp_dist, f1=f1, f2=f4, p=p)
