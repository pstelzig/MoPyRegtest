"""
MoPyRegtest: A Python enabled simple regression testing framework for Modelica models.

Copyright (c) Dr. Philipp Emanuel Stelzig, 2019--2023.

MIT License. See the project's LICENSE file.
"""

import numpy as np


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