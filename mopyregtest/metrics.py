"""
MoPyRegtest: A Python enabled simple regression testing framework for Modelica models.

Copyright (c) Dr. Philipp Emanuel Stelzig, 2019--2023.

MIT License. See the project's LICENSE file.
"""

import numpy as np


def Lp_norm(f, p: float=2.0):
    """
    Computes the :math:`L^p` norm (:math:`1 \leq p < \infty`) of a piecewise constant function :math:`f: [0,T] \mapsto \mathbb{R}`
    """

    x = f[:, 0]
    y = f[:, 1]

    if len(x) != len(y):
        raise ValueError(f"The shapes of x=f[:,0] and y=f[:,1] must match but is len(x)={len(x)} and len(y)={len(y)}.")

    if len(x) < 2:
        raise ValueError("The piecewise constant function definition of f of must have at least two abscissae, i.e. len(f[:,0]) >= 2.")

    if not np.array_equal(x, sorted(x)):
        raise ValueError("The piecewise constant function definition of f requires the abscissae f[:,0] are sorted in ascending order.")

    r = 0.0
    for i in range(1, len(x)):
        r += (x[i] - x[i-1]) * abs(y[i])**p

    return r


def Lp_dist(f1, f2, p: float=2.0):
    if not f1.shape == f2.shape:
        raise ValueError(f"Shapes of f1 and f2 must match, but is f1.shape={f1.shape} and f2.shape={f2.shape}")

    return Lp_norm(np.vstack((f1[:, 0], f2[:, 1] - f1[:, 1])).transpose())
