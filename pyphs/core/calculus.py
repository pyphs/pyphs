# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 01:36:55 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function
from pyphs.core.symbs_tools import simplify, _assert_expr, _assert_vec
import sympy


def gradient(scalar_func, vars_, dosimplify=True):
    """
    Symbolic computation here. Return the gradient of scalar function H
    w.r.t. vector variable x.

    Parameters
    -----------

    scalar_func : sympy.Expr

        Scalar function.

    vars_ : list or sympy.Matrix

        array of sympy symbols for variables

    dosimplify : bool

        Apply simplification

    Output
    -------

    grad : list

        gradient of H with grad[i] = H.diff(x[i])
    """
    vars_ = _assert_vec(vars_)
    _assert_expr(scalar_func)
    nvars = len(vars_)
    grad = [0, ]*nvars
    for i in range(nvars):
        grad[i] = scalar_func.diff(vars_[i]).doit()
    if dosimplify:
        grad = simplify(grad)
    return grad


def hessian(scalar_func, vars_, dosimplify=True):
    """
    Symbolic computation here. Return the hessian matrix of scalar function H
    w.r.t. vector variable x.

    Parameters
    -----------

    scalar_func : sympy.Expr

        Scalar function.

    vars_ : list or sympy.Matrix

        array of sympy symbols for variables

    dosimplify : bool

        Apply simplification

    Output
    -------

    hess : sympy.Matrix

        gradient of H with hess = Jac(Grad(H))
    """
    grad = gradient(scalar_func, vars_, dosimplify)
    hess = jacobian(grad, vars_, dosimplify)
    return hess


def jacobian(func, vars_, dosimplify=True):
    """
    Symbolic computation here. Return the jacobian matrix of vector function f
    w.r.t. vector variable x.

    Parameters
    -----------

    func : list of sympy.Expr

        Vector function.

    vars_ : list or sympy.Matrix

        List of sympy symbols for variables

    dosimplify : bool

        Apply simplification

    Output
    -------

    Jac : sympy.Matrix

        Jacobian of f with Jac[i, j] = f[i].diff(x[j])
    """
    vars_ = _assert_vec(vars_)
    func = _assert_vec(func)
    nv, nf = len(vars_), len(func)
    Jac = sympy.zeros(nf, nv)
    for i in range(nf):
        for j in range(nv):
            Jac[i, j] = func[i].diff(vars_[j]).doit()
    if dosimplify:
        Jac = simplify(Jac)
    return Jac
