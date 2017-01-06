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
    result = func(timeout=3.)
    if result == 'not finished':
        return expr
    else:
        return result


def _simplify_expr(expr):
    assert isinstance(expr, sympy.Expr),\
        "{0!s}\nexpr should be sp.Expr, got {1!s}".format(expr, type(expr))
    return timeout_simplify(expr)


def _simplify_list(lis):
    assert hasattr(lis, '__len__'), "{0!s}\ntype({1!s}) not a valid argument for\
'utils.calculus.simplify_list' ".format(lis, type(lis))
    return timeout_simplify(lis)


def _simplify_mat(mat):
    assert hasattr(mat, 'shape'), "{0!s}\ntype({1!s}) not a valid argument for\
'utils.calculus.simplify_mat' ".format(mat, type(mat))
    dim1, dim2 = mat.shape
    for i in range(dim1):
        row = [elt for elt in mat[i, :]]
        row = _simplify_list(row)
        for j in range(dim2):
            mat[i, j] = row[j]
    return mat


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
    nvec = vec.shape[0]
    nmat, mmat = mat.shape
    if nvec == 0:
        return sympy.zeros(nmat, 0)
    else:
        return mat*vec


###############################################################################


def free_symbols(obj):
    if hasattr(obj, '__len__'):
        symbs = set()
        for el in obj:
            _assert_expr(el)
            symbs = symbs.union(sympy.sympify(el).free_symbols)
    else:
        _assert_expr(obj)
        symbs = sympy.sympify(obj.free_symbols)
    return symbs

###############################################################################


def _assert_expr(obj):
    assert isinstance(obj, (sympy.Expr, sympy.Symbol)), "argument should be sympy.Expr, \
got {0}".format(type(obj))


def _assert_vec(obj):
    # if matrix then transpose to column vector
    if hasattr(obj, 'shape'):
        assert 1 in obj.shape, "Matrix argument should have a single \
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
        obj[n, :] = row
