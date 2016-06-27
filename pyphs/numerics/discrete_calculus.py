# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 01:46:04 2016

@author: Falaize
"""
import sympy
from config import EPS
from pyphs.symbolics.tools import _assert_expr, _assert_vec, simplify


def discrete_gradient(H, x, dx, numtol=EPS):
    """
    Symbolic computation here. Return the discrete gradient of scalar function\
 H between x and x+dx, with H separable with respect to x: H = sum_i[H_i(x_i)].

    Parameters
    -----------

    H : sympy.expression

        Scalar function of x.

    x : list or sympy.Matrix

        1 dimensional array of sympy symbols.

    dx : list or sympy.Matrix

        1 dimensional array of sympy symbols.

    Output
    -------

    gradd : list

        discrete gradient of H with
        'gradd[i] = H.diff(x) if norm(dx[i]) < numtol else \
(H(x+dx[i])-H(x))/dx[i]'
    """
    x = _assert_vec(x)
    dx = _assert_vec(dx)
    _assert_expr(H)
    nx = len(x)
    assert len(dx) == nx, \
        'dim(dx)={0!s} is not equal to dim(x)={1!s}'.format(len(dx), nx)
    dxHd = []
    for i in range(nx):
        Hpost = H.subs(x[i], x[i] + dx[i])
        dxh = simplify((Hpost - H)/dx[i])
        dxh0 = simplify(H.diff(x[i]).doit())
        dxhi = sympy.Piecewise((dxh, dx[i] < -numtol),
                               (dxh0, dx[i] < numtol),
                               (dxh, True))
        dxHd.append(dxhi)
    return dxHd
