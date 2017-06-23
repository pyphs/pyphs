#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 15 15:53:09 2017

@author: Falaize
"""

from . import types


def free_symbols(expr):
    """
Return a set of the free symbols in expression.
expr can be a sympy.Expr, a sympy.SparseMatrix or a list of sympy.Expr
    """
    if isinstance(expr, types.matrix_types):
        symbs = free_symbols_mat(expr)
    elif isinstance(expr, types.vector_types):
        symbs = free_symbols_vec(expr)
    elif isinstance(expr, types.scalar_types):
        symbs = free_symbols_expr(expr)
    elif isinstance(expr, dict):
        symbs = free_symbols_dict(expr)
    elif expr is None:
        symbs = set()
    else:
        b = '\n'*2+'*'*50 + '\n'*2
        raise TypeError("{0}{1}{0}Unkown type {2}".format(b, expr, type(expr)))
    return symbs


def free_symbols_dict(expr):
    """
Return a set of the free symbols in expression.
expr must be a sympy.Expr
    """
    symbs = set()
    for k in expr.keys():
        symbs = symbs.union(free_symbols_expr(expr[k]))
    return symbs


def free_symbols_expr(expr):
    """
Return a set of the free symbols in expression.
expr must be a sympy.Expr
    """
    types.scalar_test(expr)
    if isinstance(expr, types.sympy.Expr):
        symbs = expr.free_symbols
    else:
        symbs = set()
    return symbs


def free_symbols_vec(vec):
    """
Return a set of the free symbols in expression.
expr must be a list of sympy.Expr
    """
    types.vector_test(vec)
    symbs = set()
    for el in vec:
        symbs = symbs.union(free_symbols_expr(el))
    return symbs


def free_symbols_mat(mat):
    """
Return a set of the free symbols in expression.
expr must be a sympy.SparseMatrix
    """
    types.matrix_test(mat)
    m, n = mat.shape
    symbs = free_symbols_vec([e for (_, _, e) in mat.row_list()])
    return symbs
