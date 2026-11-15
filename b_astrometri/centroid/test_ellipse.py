import math
import unittest

import numpy as np

from ellipse import catalog_fields, coverage_probability, error_ellipse


class EllipseTests(unittest.TestCase):
    def test_analytic_axes_and_angle(self):
        a, b, th = 0.30, 0.10, math.radians(30)
        r = np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
        cov = r @ np.diag([a * a, b * b]) @ r.T
        e = error_ellipse(cov)
        self.assertLess(abs(e["a"] - a), 1e-9)
        self.assertLess(abs(e["b"] - b), 1e-9)
        self.assertLess(abs(e["theta"] - th), 1e-9)

    def test_two_sigma_doubles(self):
        cov = [[0.04, 0.01], [0.01, 0.02]]
        e1, e2 = error_ellipse(cov, 1), error_ellipse(cov, 2)
        self.assertAlmostEqual(e2["a"], 2 * e1["a"], places=12)
        self.assertAlmostEqual(e2["b"], 2 * e1["b"], places=12)

    def test_coverage_numbers(self):
        self.assertAlmostEqual(coverage_probability(1), 0.3935, places=4)
        self.assertAlmostEqual(coverage_probability(2), 0.8647, places=4)

    def test_monte_carlo_one_sigma_inside_39_percent(self):
        rng = np.random.default_rng(1234)
        cov = np.array([[0.09, 0.03], [0.03, 0.04]])
        n = 200_000
        pts = rng.multivariate_normal([0, 0], cov, size=n)
        d2 = np.einsum("ij,jk,ik->i", pts, np.linalg.inv(cov), pts)
        frac = float(np.mean(d2 <= 1.0))
        self.assertLess(abs(frac - 0.3935), 0.005)

    def test_diagonal_theta_zero_and_fields(self):
        f = catalog_fields([[0.04, 0.0], [0.0, 0.01]])
        self.assertAlmostEqual(f["a1"], 0.2)
        self.assertAlmostEqual(f["b1"], 0.1)
        self.assertEqual(f["theta"], 0.0)
        self.assertAlmostEqual(f["a2"], 0.4)
        self.assertEqual(f["rho"], 0.0)

    def test_rejects_bad_input(self):
        for bad in ([[1, 0], [0, float("nan")]], [[1, 2], [0, 1]],
                    [[1, 2], [2, 1]], [[-1, 0], [0, 1]]):
            with self.assertRaises(ValueError):
                error_ellipse(bad)
        with self.assertRaises(ValueError):
            error_ellipse([[1, 0], [0, 1]], k=0)


if __name__ == "__main__":
    unittest.main()
