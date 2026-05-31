"""
MoPyRegtest: A Python enabled simple regression testing framework for Modelica models.

Copyright (c) Dr. Philipp Emanuel Stelzig, 2019--2023.

MIT License. See the project's LICENSE file.
"""

import numpy as np
import os
import tempfile


def _check_comparability(f1, f2):
    if not f1.shape == f2.shape:
        raise ValueError(f"Shapes of f1 and f2 must match, but is f1.shape={f1.shape} and f2.shape={f2.shape}")

    if not np.allclose(f1[:, 0], f2[:, 0], atol=1e-15, rtol=1e-15):
        raise ValueError(f"The abscissae of f1 and f2 must match but are f1[:,0]={f1[:, 0]} and f2[:,0]={f2[:, 0]}")


def _check_piecewise_func(f):
    x = f[:, 0]
    y = f[:, 1]

    if len(x) != len(y):
        return f"The shapes of x=f[:,0] and y=f[:,1] must match but is len(x)={len(x)} and len(y)={len(y)}."

    if len(x) < 2:
        return "The piecewise constant function definition of f of must have at least two abscissae, i.e. len(f[:,0]) >= 2."

    if not np.array_equal(x, sorted(x)):
        return "The piecewise constant function definition of f requires the abscissae f[:,0] are sorted in ascending order."

    return None


def norm_p(f, p: int = 2):
    _check_piecewise_func(f)

    return np.linalg.norm(f[:, 1], ord=p)


def norm_p_dist(f1, f2, p: int = 2):
    _check_comparability(f1, f2)

    return norm_p(np.vstack((f1[:, 0], f2[:, 1] - f1[:, 1])).transpose(), p)


def norm_infty(f):
    _check_piecewise_func(f)

    return np.linalg.norm(f[:, 1], ord=np.inf)


def norm_infty_dist(f1, f2):
    _check_comparability(f1, f2)

    return norm_infty(np.vstack((f1[:, 0], f2[:, 1] - f1[:, 1])).transpose())


def Lp_norm(f, p: int = 2):
    """
    Computes the :math:`L^p` norm (:math:`1 \leq p < \infty`) of a piecewise constant function :math:`f: [x_0,x_N) \mapsto \mathbb{R}`

    The piecewise function f must be defined as pairs :math:`[(x_0,y_0),\ldots,(x_N,y_N)]` and it is assumed that the
    function is right-continuous. I.e., at the discontinuities :math:`x_i` it is

    :math:`lim_{x\\searrow x_i} f(x) = y_i`

    Note that the value of :math:`y_N` will be ignored in the computation.
    """
    _check_piecewise_func(f)

    x = f[:, 0]
    y = f[:, 1]

    r = 0.0
    for i in range(0, len(x)-1):
        r += (x[i+1] - x[i]) * abs(y[i])**p

    r = r**(1/p)

    return r


def Lp_dist(f1, f2, p: int = 2):
    _check_comparability(f1, f2)

    return Lp_norm(np.vstack((f1[:, 0], f2[:, 1] - f1[:, 1])).transpose(), p)

def Linfty_norm(f):
    """
    Computes the :math:`L^\infty` norm of a piecewise constant function :math:`f: [x_0,x_N) \mapsto \mathbb{R}`

    The piecewise function f must be defined as pairs :math:`[(x_0,y_0),\ldots,(x_N,y_N)]` and it is assumed that the
    function is right-continuous. I.e., at the discontinuities :math:`x_i` it is

    :math:`lim_{x\\searrow x_i} f(x) = y_i`

    Note that the value of :math:`y_N` will be ignored in the computation.
    """
    _check_piecewise_func(f)

    r = norm_infty(f)

    return r


def Linfty_dist(f1, f2):
    _check_comparability(f1, f2)

    return Linfty_norm(np.vstack((f1[:, 0], f2[:, 1] - f1[:, 1])).transpose())


def func_ptwise(f1, f2, dist: callable):
    _check_comparability(f1, f2)

    delta = np.vstack((f1[:, 0], np.vectorize(dist)(f2[:, 1] - f1[:, 1]))).transpose()

    return delta


def abs_dist_ptwise(f1, f2):
    return func_ptwise(f1, f2, np.abs)


class FunnelDist:
    """
    Callable metric class using pyfunnel's funnel comparison.

    Bridges pyfunnel's compareAndReport API to MoPyRegtest's metric(f1, f2) -> ndarray(N,2) protocol.
    A tolerance funnel is built around the reference data; test points outside the funnel are reported
    as errors with positive error magnitude.

    Default atoly=1e-7 aligns with MoPyRegtest's default tol=1e-7.

    Parameters
    ----------
    atolx : float
        Absolute tolerance along x axis. Default 0.
    atoly : float
        Absolute tolerance along y axis. Default 1e-7.
    ltolx : float
        Relative tolerance along x axis (relative to local value). Default 0.
    ltoly : float
        Relative tolerance along y axis (relative to local value). Default 0.
    rtolx : float
        Relative tolerance along x axis (relative to range). Default 0.
    rtoly : float
        Relative tolerance along y axis (relative to range). Default 0.
    """

    def __init__(self, atolx=0, atoly=1e-7, ltolx=0, ltoly=0, rtolx=0, rtoly=0):
        try:
            import pyfunnel
        except ImportError:
            raise ImportError(
                "pyfunnel is required for FunnelDist. "
                "Install it with: pip install MoPyRegtest[funnel]"
            )

        self.atolx = atolx
        self.atoly = atoly
        self.ltolx = ltolx
        self.ltoly = ltoly
        self.rtolx = rtolx
        self.rtoly = rtoly
        self.output_dir = None
        self._call_count = 0

    def __call__(self, f1, f2):
        import pyfunnel
        import pandas as pd

        self._call_count += 1

        if self.output_dir is not None:
            out_dir = os.path.join(self.output_dir, f"col_{self._call_count}")
            os.makedirs(out_dir, exist_ok=True)
        else:
            out_dir = tempfile.mkdtemp(prefix="mopyregtest_funnel_")

        return self._run_and_read(f1, f2, out_dir, pyfunnel, pd)

    def _run_and_read(self, f1, f2, out_dir, pyfunnel, pd):
        tol_kwargs = {}
        tol_kwargs["atolx"] = self.atolx
        tol_kwargs["atoly"] = self.atoly
        tol_kwargs["ltolx"] = self.ltolx
        tol_kwargs["ltoly"] = self.ltoly
        tol_kwargs["rtolx"] = self.rtolx
        tol_kwargs["rtoly"] = self.rtoly

        pyfunnel.compareAndReport(
            xReference=f1[:, 0], yReference=f1[:, 1],
            xTest=f2[:, 0], yTest=f2[:, 1],
            outputDirectory=out_dir,
            **tol_kwargs,
        )

        errors_path = os.path.join(out_dir, "errors.csv")
        errors = pd.read_csv(errors_path)
        
        return errors[["x", "y"]].values