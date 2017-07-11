#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 00:12:30 2017

@author: Falaize
"""

import sympy as sp
import numpy as np


def pwl_func(X_lst, Y_lst, symbol=sp.symbols('x'),
             integ=False, y0=0., intconst=0.):
    """
Returns a piecewise linear interpolation of the set (X_lst, Y_lst), based on
the following explicit form a + b.x + sum(c_i*abs(x - X_i)), where i denote the
ith component of the list and a, b and c are defined in [Chua and Ying, eq (2)].
[Chua and Ying, eq (2)] : Chua, L., & Ying, R. (1983). Canonical \
piecewise-linear analysis. IEEE Transactions on Circuits and Systems, \
30(3), 125-140.
    """

    # Numerical values
    assert len(X_lst) == len(Y_lst), "X and Y must have the same length"
    X = np.array(X_lst)
    Y = np.array(Y_lst)

    # State sympy symbol
    x = symbol

    # in [Chua and Ying, fig. 1], indices for x and y = f(x) range from 1 to P
    P = len(X)
    # delta_x[i] = x[x+1] - x[i] for i in [1, ..., P-1]
    delta_x = np.diff(X)
    # delta_f[i] = f(x[x+1]) - f(x[i]) for i in [1, ..., P-1]
    delta_y = np.diff(Y)
    # m[i] = delta_y[i]/delta_x[i]
    m = delta_y/delta_x
    # m <= (m[0], m, m[P-2]
    m = np.concatenate((m[np.newaxis, 0], m, m[np.newaxis, -1]))
    # in [Chua and Ying, eq (2.2)]: 0.5*(m[0] + m[-1])
    b = 0.5*(m[0] + m[-1])
    # in [Chua and Ying, eq (2.3)]: c[i] = 0.5*(m[i] - m[i-1]) for i in [1, ... P]
    c = 0.5*(m[1:] - m[:P])
    # in [Chua and Ying, eq (2.3)]: a = f(0) - sum_i(c[i]*abs(x[i]))
    # here we force f(0) = y0
    a = y0 - np.sum(c*np.abs(X))

    if integ:
        # integral of a + b.x + sum(c[i]*abs(x - X[i]))
        expr = (intconst + a*x + (b/2)*x**2 +
                sum(c*0.5*abs(x - X)*(x - X)) +
                sum(c*0.5*abs(X)*X))
    else:
        expr = a + b*x + sum(c*abs(x - X))

    return expr
