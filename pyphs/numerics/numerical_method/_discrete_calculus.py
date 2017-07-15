# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 01:46:04 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function
import sympy
from pyphs.config import EPS
from pyphs.core.tools import types
from pyphs.core.maths import gradient


def discrete_gradient(H, x, dx, numtol=EPS):
    """
    Symbolic computation here. Return the discrete gradient of scalar function\
 H between x and x+dx, with H separable with respect to x: H = sum_i[H_i(x_i)].

    Parameters
    -----------

    H : sympy.expression

        Scalar function of x.

    x : list or sympy.SparseMatrix

        1 dimensional array of sympy symbols.

    dx : list or sympy.SparseMatrix

        1 dimensional array of sympy symbols.

    Output
    -------

    gradd : list

        discrete gradient of H with
        'gradd[i] = H.diff(x) if norm(dx[i]) < numtol else \
(H(x+dx[i])-H(x))/dx[i]'
    """
    types.vector_test(x)
    types.vector_test(dx)
    types.scalar_test(H)
    nx = len(x)
    assert len(dx) == nx, \
        'dim(dx)={0!s} is not equal to dim(x)={1!s}'.format(len(dx), nx)
    dxHd = []
    for i in range(nx):
        Hpost = H.subs(x[i], x[i] + dx[i])
        dxh = (Hpost - H)/dx[i]
        dxh0 = H.diff(x[i]).doit()
        dxhi = sympy.Piecewise((dxh, dx[i] < -(numtol**2)),
                               (dxh0, dx[i] < numtol**2),
                               (dxh, True))
        dxHd.append(dxhi)
    return dxHd


def gradient_theta(H, x, dx, theta=0.):
    """
    Symbolic computation here. Return the evaluation of the gradient of scalar\
     function H at x+theta*dx.

    Parameters
    -----------

    H : sympy.expression

        Scalar function of x.

    x : list or sympy.SparseMatrix

        1 dimensional array of sympy symbols.

    dx : list or sympy.SparseMatrix

        1 dimensional array of sympy symbols.

    Output
    -------

    gradd : list

        discrete gradient of H with
        'gradd[i] = [H.diff(x).subs(x, x+theta*dx)]_i'
    """
    types.vector_test(x)
    types.vector_test(dx)
    types.scalar_test(H)
    nx = len(x)
    assert len(dx) == nx, \
        'dim(dx)={0!s} is not equal to dim(x)={1!s}'.format(len(dx), nx)
    dxHd = gradient(H, x)
    subs = {}
    for i, (xi, dxi) in enumerate(zip(x, dx)):
        subs[xi] = xi+theta*dxi
    for i, dxh in enumerate(dxHd):
        dxHd[i] = dxh.subs(subs)
    return dxHd


def gradient_trapez(H, x, dx):
    """
    Symbolic computation here. Return the mean of the evaluation of the \
    gradient of scalar function H at x and at x+dx.

    Parameters
    -----------

    H : sympy.expression

        Scalar function of x.

    x : list or sympy.SparseMatrix

        1 dimensional array of sympy symbols.

    dx : list or sympy.SparseMatrix

        1 dimensional array of sympy symbols.

    Output
    -------

    gradd : list

        discrete gradient of H with
        'gradd[i] = 0.5* ([H.diff(x)]_i+[H.diff(x).subs(x, x+dx)]_i)'
    """
    types.vector_test(x)
    types.vector_test(dx)
    types.scalar_test(H)
    nx = len(x)
    assert len(dx) == nx, \
        'dim(dx)={0!s} is not equal to dim(x)={1!s}'.format(len(dx), nx)
    dxHd = gradient(H, x)
    subs = {}
    for i, (xi, dxi) in enumerate(zip(x, dx)):
        subs[xi] = xi+dxi
    for i, dxh in enumerate(dxHd):
        dxHd[i] = 0.5*(dxh + dxh.subs(subs))
    return dxHd
