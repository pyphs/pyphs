# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 11:26:23 2016

@author: Falaize
"""

import sympy
from pyphs.misc.timer import timeout

###############################################################################


def symbols(obj):
    """
    assert all symbols are real
    """
    return sympy.symbols(obj, real=True)


def _simplify_expr(expr):
    assert isinstance(expr, sympy.Expr),\
        "{0!s}\nexpr should be sp.Expr, got {1!s}".format(expr, type(expr))

    def func(expr):
        #    return sympy.simplify(expr, ratio=1)
        #    return sympy.nsimplify(expr)
        return expr
    expr, _ = timeout(func, expr, dur=10)
    return expr


def _parallel_simplify(lis):
    assert hasattr(lis, '__len__'), "{0!s}\ntype({1!s}) not a valid argument for\
'utils.calculus.simplify_list' ".format(lis, type(lis))
#    from pyphs.misc.parallelize import parallel_map
#    return parallel_map(_simplify_expr, lis)
    return map(_simplify_expr, lis)


def _simplify_mat(mat):
    assert hasattr(mat, 'shape'), "{0!s}\ntype({1!s}) not a valid argument for\
'utils.calculus.simplify_mat' ".format(mat, type(mat))
    dim1, dim2 = mat.shape
    for i in range(dim1):
        row = [elt for elt in mat[i, :]]
        row = _parallel_simplify(row)
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
        return _parallel_simplify(obj)
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
    import sympy
    nvec = vec.shape[0]
    nmat, mmat = mat.shape
    if nvec == 0:
        return sympy.zeros(nmat, 0)
    else:
        return mat*vec


###############################################################################


def free_symbols(obj):
    import sympy
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
    assert isinstance(obj, sympy.Expr), "argument should be sympy.Expr, \
got %s" % type(obj)


def _assert_vec(obj):
    # if matrix then transpose to column vector
    if hasattr(obj, 'shape'):
        assert 1 in obj.shape, "Matrix argument should have a single \
dimension, got dim(obj)=%s" % obj.shape
        obj = obj.T if obj.shape[0] < obj.shape[1] else obj
    else:
        assert hasattr(obj, '__len__'), "argument should be one dimensional, \
got type(obj)=%s" % type(obj)
    obj = list(obj)
    for i in range(len(obj)):
        el = obj[i]
        if isinstance(el, (float, int)):
            el = sympy.sympify(el)
        _assert_expr(el)
        obj[i] = el
    return obj


def _assert_mat(obj):
    assert hasattr(obj, 'shape'), "argument should be a matrix structure, \
got %s" % type(obj)
    obj = sympy.Matrix(obj)
    nrows = obj.shape[0]
    for n in range(nrows):
        row = obj.tolist()[n]
        row = _assert_vec(row)
        obj[n, :] = row
