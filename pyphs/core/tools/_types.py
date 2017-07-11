#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 15 16:25:05 2017

@author: Falaize
"""
import sympy
from pyphs.config import DTYPE


def is_known_test(obj):
    """
    Test if type(obj) is known in the pyphs.core sub-package.
    """
    checks = [scalar_test, vector_test, matrix_test]
    found = False
    raised = 0
    while not found and checks:
        try:
            checks.pop()(obj)
            found = True
        except (ScalarExprTypeError, VectorExprTypeError, MatrixExprTypeError):
            raised += 1

    if raised == 3:
        message = 'Expression type not understood, got {}'.format(type(obj))
        raise TypeError(message)


# =============================== SCALARS =================================== #

scalar_types = (sympy.Expr, sympy.Symbol,
                sympy.Float, sympy.Integer,
                float, int, DTYPE)


class ScalarExprTypeError(Exception):
    pass


def scalar_test(obj, metadata=(None, None)):
    """
    Test if obj is of expr_types. metadata is (func_name, arg_name) for error
    information display.
    """
    if not isinstance(obj, scalar_types):
        message = 'In func{}, name {}: \nexpected {}, \
            \ngot {}'.format(metadata[0], metadata[1], vector_types, type(obj))
        raise ScalarExprTypeError(message, obj)


# ============================== VECTORS ==================================== #

vector_types = (list, tuple)


class VectorExprTypeError(Exception):
    pass


def vector_test(obj, metadata=(None, None)):
    """
    Test if obj is of vector_types. metadata is (func_name, arg_name) for error
    information display.
    """
    if not isinstance(obj, vector_types):
        message = 'In func{}, name {}: \nexpected {}, \
            \ngot {}'.format(metadata[0], metadata[1], vector_types, type(obj))
        raise VectorExprTypeError(message)
    else:
        try:
            map(lambda el: scalar_test(el, metadata), obj)
        except ScalarExprTypeError as e:
            raise VectorExprTypeError(e.message)


# ============================ MATRICES ===================================== #

matrix_types = (sympy.SparseMatrix, )


class MatrixExprTypeError(Exception):
    pass


def matrix_test(obj, metadata=(None, None)):
    """
    Test if obj is of matrix_types. metadata is (func_name, arg_name) for error
    information display.
    """
    if not isinstance(obj, matrix_types):
        message = 'In func{}, name {}: \nexpected {}, \
            \ngot {}'.format(metadata[0], metadata[1], matrix_types, type(obj))
        raise MatrixExprTypeError(message, obj)
    elif not len(obj.shape) == 2:
        message = 'In {}, name {}: matrix must be 2D (i, j), \
            got shape {}.'.format(metadata[0], metadata[1], obj.shape)
        raise MatrixExprTypeError(message, obj)
