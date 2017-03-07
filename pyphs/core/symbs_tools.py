# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 11:26:23 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

import stopit
import sympy


def timeout_simplify(expr):
    @stopit.threading_timeoutable(default='not finished')
    def func():
        return sympy.simplify(expr)
    return func(timeout=3.)


def _simplify_expr(expr):
    assert isinstance(expr, sympy.Expr),\
        "{0!s}\nexpr should be sp.Expr, got {1!s}".format(expr, type(expr))
    return timeout_simplify(expr)


def _simplify_list(lis):
    assert hasattr(lis, '__len__'), "{0!s}\ntype({1!s}) not a valid argument for\
'utils.calculus.simplify_list' ".format(lis, type(lis))
    not_finished = False
    for i, e in enumerate(lis):
        lis[i] = _simplify_expr(e)
        if lis[i] == 'not finished':
            not_finished = True
            break
    return 'not finished' if not_finished else lis


def _simplify_mat(mat):
    assert hasattr(mat, 'shape'), "{0!s}\ntype({1!s}) not a valid argument for\
'utils.calculus.simplify_mat' ".format(mat, type(mat))
    dim1, dim2 = mat.shape
    not_finished = False
    for i in range(dim1):
        row = [elt for elt in mat[i, :]]
        row = _simplify_list(row)
        if row == 'not finished':
            not_finished = True
            break
        for j in range(dim2):
            mat[i, j] = row[j]
    return 'not finished' if not_finished else mat


def simplify(obj):
    """
    simplify expression, list or matrix
    """
    if hasattr(obj, 'shape'):
        return _simplify_mat(obj)
    elif hasattr(obj, '__len__'):
        return _simplify_list(obj)
    else:
        return _simplify_expr(obj)


###############################################################################


def inverse(Mat, dosimplify=False):
    """
    same method for every matrix inversions
    """
    iMat = Mat.inv()
    if dosimplify:
        iMat = simplify(iMat)
    return iMat


###############################################################################


def matvecprod(mat, vec):
    """
    Safe dot product of a matrix whith shape (m, n) and a vector with shape (l, 1).
    """
    assert vec.shape[1] <= 1
    l = vec.shape[0]
    m, n = mat.shape
    assert l == n
    if m == 0 or l == 0:
        return sympy.zeros(m, 1)
    else:
        return mat*vec


###############################################################################

def free_symbols_expr(expr):
    _assert_expr(expr)
    symbs = sympy.sympify(expr).free_symbols
    return symbs


def free_symbols_vec(vec):
    _assert_vec(vec)
    symbs = set()
    for el in vec:
        symbs = symbs.union(free_symbols_expr(el))
    return symbs


def free_symbols_mat(mat):
    _assert_mat(mat)
    m, n = mat.shape
    symbs = set()
    for i in range(m):
        try:
            symbs = symbs.union(free_symbols_vec(mat[i, :]))
        except AssertionError:
            pass
    return symbs


def free_symbols(obj):
    if hasattr(obj, 'shape') and any(e == 0 for e in obj.shape):
        symbs = set()
    elif hasattr(obj, 'shape'):
        symbs = free_symbols_mat(obj)
    else:
        try:
            symbs = free_symbols_expr(obj)
        except AssertionError:
            symbs = free_symbols_vec(obj)
    return symbs

###############################################################################


def _assert_expr(obj):
    assert isinstance(obj, (sympy.Expr, sympy.Symbol)), "argument should be sympy.Expr, \
got {0}".format(type(obj))


def _assert_vec(obj):
    # if matrix then transpose to column vector
    if hasattr(obj, 'shape'):
        assert 1 in obj.shape, "Vector argument should have a single \
dimension, got dim(obj)={0}".format(obj.shape)
        obj = obj.T if obj.shape[0] < obj.shape[1] else obj
    else:
        assert hasattr(obj, '__len__'), "argument should be one dimensional, \
got type(obj)={0}".format(type(obj))
    obj = list(obj)
    for i, el in enumerate(obj):
        if isinstance(el, (float, int)):
            el = sympy.sympify(el)
        _assert_expr(el)
        obj[i] = el
    return obj


def _assert_mat(obj):
    assert hasattr(obj, 'shape'), "argument should be a matrix structure, \
got {0}".format(type(obj))
    obj = sympy.Matrix(obj)
    nrows = obj.shape[0]
    for n in range(nrows):
        row = obj.tolist()[n]
        row = _assert_vec(row)
