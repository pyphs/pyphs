# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 01:36:55 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function
from ..tools import types
from ..tools import simplify as simplify_func
import sympy


def gradient(scalar_func, vars_, simplify=False):
    """
    Symbolic computation here. Return the gradient of scalar function H
    w.r.t. vector variable x.

    Parameters
    -----------

    scalar_func : sympy.Expr

        Scalar function.

    vars_ : list or sympy.SparseMatrix

        array of sympy symbols for variables

    dosimplify : bool

        Apply simplification

    Output
    -------

    grad : list

        gradient of H with grad[i] = H.diff(x[i])
    """
    types.vector_test(vars_)
    types.scalar_test(scalar_func)
    nvars = len(vars_)
    grad = [0, ]*nvars
    for i in range(nvars):
        grad[i] = scalar_func.diff(vars_[i]).doit()
    if simplify:
        grad = simplify_func(grad)
    return grad


def hessian(scalar_func, vars_, simplify=False):
    """
    Symbolic computation here. Return the hessian matrix of scalar function H
    w.r.t. vector variable x.

    Parameters
    -----------

    scalar_func : sympy.Expr

        Scalar function.

    vars_ : list or sympy.SparseMatrix

        array of sympy symbols for variables

    dosimplify : bool

        Apply simplification

    Output
    -------

    hess : sympy.SparseMatrix

        gradient of H with hess = Jac(Grad(H))
    """
    types.vector_test(vars_)
    types.scalar_test(scalar_func)
    grad = gradient(scalar_func, vars_, simplify=False)
    hess = jacobian(grad, vars_, simplify)
    return hess


def jacobian(func, vars_, simplify=False):
    """
    Symbolic computation here. Return the jacobian matrix of vector function f
    w.r.t. vector variable x.

    Parameters
    -----------

    func : list of sympy.Expr

        Vector function.

    vars_ : list or sympy.SparseMatrix

        List of sympy symbols for variables

    dosimplify : bool

        Apply simplification

    Output
    -------

    Jac : sympy.SparseMatrix

        Jacobian of f with Jac[i, j] = f[i].diff(x[j])
    """
    types.vector_test(vars_)
    types.vector_test(func)
    nv, nf = len(vars_), len(func)
    Jac = types.matrix_types[0](sympy.zeros(nf, nv))
    for i in range(nf):
        for j in range(nv):
            Jac[i, j] = func[i].diff(vars_[j]).doit()
    if simplify:
        Jac = simplify_func(Jac)
    return Jac
