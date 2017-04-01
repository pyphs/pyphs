# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 01:46:04 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function
import sympy
from pyphs.config import EPS
from pyphs.core.symbs_tools import _assert_expr, _assert_vec, simplify
from pyphs.core.calculus import gradient


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
    return simplify(dxHd)


def gradient_theta(H, x, dx, theta=0.):
    """
    Symbolic computation here. Return the evaluation of the gradient of scalar\
     function H at x+theta*dx.

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
        'gradd[i] = [H.diff(x).subs(x, x+theta*dx)]_i'
    """
    x = _assert_vec(x)
    dx = _assert_vec(dx)
    _assert_expr(H)
    nx = len(x)
    assert len(dx) == nx, \
        'dim(dx)={0!s} is not equal to dim(x)={1!s}'.format(len(dx), nx)
    dxHd = gradient(H, x)
    subs = {}
    for i, (xi, dxi) in enumerate(zip(x, dx)):
        subs[xi] = xi+theta*dxi
    for i, dxh in enumerate(dxHd):
        dxHd[i] = dxh.subs(subs)
    return simplify(dxHd)


def gradient_trapez(H, x, dx):
    """
    Symbolic computation here. Return the mean of the evaluation of the \
    gradient of scalar function H at x and at x+dx.

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
        'gradd[i] = 0.5* ([H.diff(x)]_i+[H.diff(x).subs(x, x+dx)]_i)'
    """
    x = _assert_vec(x)
    dx = _assert_vec(dx)
    _assert_expr(H)
    nx = len(x)
    assert len(dx) == nx, \
        'dim(dx)={0!s} is not equal to dim(x)={1!s}'.format(len(dx), nx)
    dxHd = gradient(H, x)
    subs = {}
    for i, (xi, dxi) in enumerate(zip(x, dx)):
        subs[xi] = xi+dxi
    for i, dxh in enumerate(dxHd):
        dxHd[i] = 0.5*(dxh + dxh.subs(subs))
    return simplify(dxHd)
