#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 15 15:53:53 2017

@author: Falaize
"""

import sympy
import stopit
from pyphs.config import TIMEOUT, SIMPLIFY
from . import types
from pyphs.misc.tools import geteval


def sympify(expr):
    if isinstance(expr, types.scalar_types):
        expr = sympy.sympify(expr)
    elif isinstance(expr, types.vector_types):
        expr = types.vector_types[0](map(sympy.sympify, expr))
    elif isinstance(expr, types.matrix_types):
        expr = expr.applyfunc(sympy.sympify)
    elif isinstance(expr, dict):
        for k in expr.keys():
            expr[k] = sympy.sympify(expr[k])
    return expr


def simplify(expr, **kwargs):
    """
========
simplify
========

Simplify a scalar, vector or matrix expression during timeout with method \
from sympy module. If not succeed, returns 'not finished'.

Parameters
----------

expr: sympy.SparseMatrix or list of sympy.Expr or sympy.Expr
    Expression(s) to simplify.

method: str in sympy simplify methods
    Indicate the method to use, e.g. :code:`'simplify'`. Default is \
:code:`pyphs.config.SIMPLIFY`.

timeout: positive float
    Trial time before abording. Default is :code:`pyphs.config.TIMEOUT`.

Output
------
expr_simp: same type as expr
    Simplified expression if succeed, else returns 'not finished'
    """
    if isinstance(expr, types.matrix_types):
        return simplify_matrix(expr, **kwargs)
    elif isinstance(expr, types.vector_types):
        return simplify_vector(expr, **kwargs)
    elif isinstance(expr, dict):
        return simplify_dict(expr, **kwargs)
    elif isinstance(expr, types.scalar_types):
        return simplify_scalar(expr, **kwargs)
    else:
        raise TypeError('Unknown type {}'.format(type(expr)))


def timeout_simplify(expr, method=SIMPLIFY, timeout=TIMEOUT):
    """
Try to simplify an expr during timeout with method from sympy module. If not \
succeed, returns 'not finished'.

Parameters
----------

expr: sympy.Expr
    Expression to simplify.

method: str in sympy simplify methods
    Indicate the method to use, e.g. :code:`'simplify'`. Default is \
:code:`pyphs.config.SIMPLIFY`.

timeout: positive float
    Trial time before abording. Default is :code:`pyphs.config.TIMEOUT`.

Output
------
expr_simp: sympy.Expr or str
    Simplified expression if succeed, else returns 'not finished'
    """
    @stopit.threading_timeoutable(default=expr)
    def func():
        return getattr(sympy, method)(expr) if method is not None else expr
    return func(timeout=timeout)


def simplify_scalar(expr, **kwargs):
    """
Try to simplify scalar expression during timeout with method from sympy module.
If not succeed, returns 'not finished'.

Parameters
----------

expr: sympy.Expr
    Expression to simplify.

method: str in sympy simplify methods
    Indicate the method to use, e.g. :code:`'simplify'`. Default is \
:code:`pyphs.config.SIMPLIFY`.

timeout: positive float
    Trial time before abording. Default is :code:`pyphs.config.TIMEOUT`.

Output
------
expr_simp: sympy.Expr or str
    Simplified expression if succeed, else returns 'not finished'
    """
    types.scalar_test(expr)
    return timeout_simplify(expr, **kwargs)


def simplify_vector(vec, **kwargs):
    """
Try to simplify vector expression during timeout with method from sympy module.
If not succeed, returns 'not finished'.

Parameters
----------

vec: list of sympy.Expr
    Vector (list) of expressions to simplify.

method: str in sympy simplify methods
    Indicate the method to use, e.g. :code:`'simplify'`. Default is \
:code:`pyphs.config.SIMPLIFY`.

timeout: positive float
    Trial time before abording. Default is :code:`pyphs.config.TIMEOUT`.

Output
------
vec_simp: same type as vec or str
    Simplified expressions if succeed, else returns 'not finished'
    """
    types.vector_test(vec)
    for i, e in enumerate(vec):
        vec[i] = simplify_scalar(e, **kwargs)
    return 'not finished' if 'not finished' in vec else vec


def simplify_matrix(mat, **kwargs):
    """
Try to simplify vector expression during timeout with method from sympy module.
If not succeed, returns 'not finished'.

Parameters
----------

vec: list or tuple of sympy.Expr
    Vector (list) of expressions to simplify.

method: str in sympy simplify methods
    Indicate the method to use, e.g. :code:`'simplify'`. Default is \
:code:`pyphs.config.SIMPLIFY`.

timeout: positive float
    Trial time before abording. Default is :code:`pyphs.config.TIMEOUT`.

Output
------
vec_simp: same type as vec or str
    Simplified expressions if succeed, else returns 'not finished'
    """
    types.matrix_test(mat)
    dim1, dim2 = mat.shape
    not_finished = False
    for i, j, expr in mat.row_list():
        simplified_expr = simplify_scalar(expr, **kwargs)
        if simplified_expr == 'not finished':
            not_finished = True
            break
        else:
            mat[i, j] = simplified_expr
    return 'not finished' if not_finished else mat


def simplify_dict(expr, **kwargs):
    """
Try to simplify dict expression during timeout with method from sympy module.
If not succeed, returns 'not finished'.

Parameters
----------

expr: dict {sympy.Symbol : sympy.Expr}
    Expressions to simplify.

method: str in sympy simplify methods
    Indicate the method to use, e.g. :code:`'simplify'`. Default is \
:code:`pyphs.config.SIMPLIFY`.

timeout: positive float
    Trial time before abording. Default is :code:`pyphs.config.TIMEOUT`.

Output
------
expr_simp: dict
    Simplified expression if succeed, else returns 'not finished'
    """
    finished = True
    for k in expr.keys():
        new_k = timeout_simplify(k, **kwargs)
        new_v = timeout_simplify(expr[k], **kwargs)
        finished = not(new_k == 'not finished' or new_v == 'not finished')
        if finished:
            expr[new_k] = new_v
    return expr if finished else 'not finished'

# =========================================================================


def simplify_core(core):
    """
    substitute_core
    ***************

    Apply simplifications to every expressions of a Core.

    """

    # substitutions in core's list of expressions and symbols
    attrs_to_sub = set(list(core.exprs_names) +
                       list(core.symbs_names) +
                       ['M', '_dxH', 'observers'])
    for name in attrs_to_sub:
        expr = geteval(core, name)
        if expr is not None:
            setattr(core, name, simplify(expr))
