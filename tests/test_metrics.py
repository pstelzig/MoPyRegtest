import unittest
import numpy as np
import mopyregtest

class TestMetrics(unittest.TestCase):
    def test_Lp_norm(self):
        f = np.array([[0, 1],
                      [1, 2],
                      [3, -3],
                      [10, -5]])

        p = 2
        self.assertAlmostEqual(mopyregtest.metrics.Lp_norm(f), ((1-0) * 1**p + (3-1) * 2**p + (10-3) * 3**p)**(1/p))

        p = 3
        self.assertAlmostEqual(mopyregtest.metrics.Lp_norm(f, p), ((1-0) * 1**p + (3-1) * 2**p + (10-3) * 3**p)**(1/p))

        p = 1
        self.assertAlmostEqual(mopyregtest.metrics.Lp_norm(f, p), ((1-0) * 1**p + (3-1) * 2**p + (10-3) * 3**p)**(1/p))

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

        p = 2
        self.assertAlmostEqual(mopyregtest.metrics.Lp_dist(f1, f2), ((1-0) * 6**p + (3-1) * 4**p + (10-3) * 8**p)**(1/p))

        p = 3
        self.assertAlmostEqual(mopyregtest.metrics.Lp_dist(f1, f2, p), ((1-0) * 6**p + (3-1) * 4**p + (10-3) * 8**p)**(1/p))

        p = 2
        self.assertRaises(ValueError, mopyregtest.metrics.Lp_dist, f1=f1, f2=f3, p=p)

        p = 2
        self.assertRaises(ValueError, mopyregtest.metrics.Lp_dist, f1=f1, f2=f4, p=p)

    def test_Linfty_norm(self):
        f = np.array([[0, 1],
                      [1, 2],
                      [3, -3],
                      [10, -5]])

        self.assertAlmostEqual(mopyregtest.metrics.Linfty_norm(f), 5)

    def test_Linfty_dist(self):
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

        self.assertAlmostEqual(mopyregtest.metrics.Linfty_dist(f1, f2), 8)

        self.assertRaises(ValueError, mopyregtest.metrics.Linfty_dist, f1=f1, f2=f3)

        self.assertRaises(ValueError, mopyregtest.metrics.Linfty_dist, f1=f1, f2=f4)

    def test_norm_p_dist(self):
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

        p = 2
        self.assertAlmostEqual(mopyregtest.metrics.norm_p_dist(f1, f2),
                               (6 ** p + 4 ** p + 8 ** p + 7 ** p)**(1/p))

        p = 3
        self.assertAlmostEqual(mopyregtest.metrics.norm_p_dist(f1, f2, p),
                               (6 ** p + 4 ** p + 8 ** p + 7 ** p)**(1/p))

        p = 2
        self.assertRaises(ValueError, mopyregtest.metrics.norm_p_dist, f1=f1, f2=f3, p=p)

        p = 2
        self.assertRaises(ValueError, mopyregtest.metrics.norm_p_dist, f1=f1, f2=f4, p=p)

    def test_norm_infty_dist(self):
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

        self.assertAlmostEqual(mopyregtest.metrics.norm_infty_dist(f1, f2), 8)

        self.assertRaises(ValueError, mopyregtest.metrics.norm_infty_dist, f1=f1, f2=f3)

        self.assertRaises(ValueError, mopyregtest.metrics.norm_infty_dist, f1=f1, f2=f4)

    def test_funnel_dist_matching(self):
        """Test FunnelDist with identical signals returns all-zero errors."""
        f1 = np.array([[0.0, 1.0],
                       [1.0, 2.0],
                       [2.0, 3.0],
                       [3.0, 4.0]])

        metric = mopyregtest.metrics.FunnelDist(atoly=0.1)
        result = metric(f1, f1)

        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.shape[1], 2)
        self.assertTrue(np.all(result[:, 1] == 0.0))

    def test_funnel_dist_diverging(self):
        """Test FunnelDist with diverging signals returns non-zero errors."""
        f1 = np.array([[0.0, 0.0],
                       [1.0, 1.0],
                       [2.0, 0.0],
                       [3.0, 1.0]])

        f2 = np.array([[0.0, 0.0],
                       [1.0, 2.0],
                       [2.0, 0.0],
                       [3.0, 1.0]])

        metric = mopyregtest.metrics.FunnelDist(atoly=0.1)
        result = metric(f1, f2)

        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.shape[1], 2)
        # Point at x=1 has y difference of 1.0, funnel tolerance is 0.1 → error > 0
        self.assertTrue(np.any(result[:, 1] > 0))

    def test_funnel_dist_large_tolerance(self):
        """Test FunnelDist with large tolerance passes for small deviations."""
        f1 = np.array([[0.0, 0.0],
                       [1.0, 1.0],
                       [2.0, 0.0],
                       [3.0, 1.0]])

        f2 = np.array([[0.0, 0.0],
                       [1.0, 1.05],
                       [2.0, 0.0],
                       [3.0, 1.0]])

        metric = mopyregtest.metrics.FunnelDist(atoly=0.1)
        result = metric(f1, f2)

        self.assertIsInstance(result, np.ndarray)
        # Deviation of 0.05 is within atoly=0.1 → all errors should be 0
        self.assertTrue(np.all(result[:, 1] == 0.0))

    def test_funnel_dist_output_dir(self):
        """Test FunnelDist writes output to specified directory."""
        import tempfile
        import os

        f1 = np.array([[0.0, 0.0],
                       [1.0, 1.0],
                       [2.0, 0.0]])
        f2 = np.array([[0.0, 0.0],
                       [1.0, 1.5],
                       [2.0, 0.0]])

        out_dir = tempfile.mkdtemp(prefix="mopyregtest_test_funnel_")
        try:
            metric = mopyregtest.metrics.FunnelDist(atoly=0.1)
            metric.output_dir = out_dir
            metric(f1, f2)

            # Output should be in a col_1 subdirectory
            col_dir = os.path.join(out_dir, "col_1")
            self.assertTrue(os.path.isdir(col_dir))
            self.assertTrue(os.path.isfile(os.path.join(col_dir, "errors.csv")))
        finally:
            import shutil
            shutil.rmtree(out_dir)


if __name__ == '__main__':
    unittest.main()
