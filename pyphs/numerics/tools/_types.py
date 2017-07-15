#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 17 23:15:00 2017

@author: Falaize
"""

import numpy as np
from pyphs.config import DTYPE
# ============================ MATRICES ===================================== #

matrix_types = (np.ndarray, )


class MatrixTypeError(Exception):
    pass


def matrix_test(obj, metadata=(None, None)):
    """
    Test if obj is of matrix_types. metadata is (func_name, arg_name) for error
    information display.
    """
    if not isinstance(obj, matrix_types):
        message = 'In func{0}, name {1}: \nexpected {2}, \
            \ngot {3}'.format(metadata[0], metadata[1],
                              matrix_types, type(obj))
        raise MatrixTypeError(message, obj)
    elif not len(obj.shape) == 2:
        message = 'In {0}, name {1}: matrix must be 2D (i, j), \
            got shape {2}.'.format(metadata[0], metadata[1], obj.shape)
        raise MatrixTypeError(message, obj)
    elif not obj.dtype.type == DTYPE:
        message = 'In {0}, name {1}: Data type must be {2}, \
            got {3}.'.format(metadata[0], metadata[1], DTYPE, obj.dtype)
        raise MatrixTypeError(message, obj)


# ============================== VECTORS ==================================== #

vector_types = (np.ndarray, )


class VectorTypeError(Exception):
    pass


def vector_test(obj, metadata=(None, None)):
    """
    Test if obj is of vector_types. metadata is (func_name, arg_name) for error
    information display.
    """
    if not isinstance(obj, vector_types):
        message = 'In func{}, name {}: \nexpected {}, \
            \ngot {}'.format(metadata[0], metadata[1], vector_types, type(obj))
        raise VectorTypeError(message, obj)
    elif not len(obj.shape) == 1:
        message = 'In {}, name {}: \nvectors must be 1D (i, ), \
            \ngot shape {}.'.format(metadata[0], metadata[1], obj.shape)
        raise VectorTypeError(message, obj)
    elif not obj.dtype.type == DTYPE:
        message = 'In {}, name {}: Data type must be {}, \
            got {}.'.format(metadata[0], metadata[1], DTYPE, obj.dtype)
        raise VectorTypeError(message, obj)


# =============================== SCALARS =================================== #

scalar_types = (np.ndarray, )


class ScalarTypeError(Exception):
    pass


def scalar_test(obj, metadata=(None, None)):
    """
    Test if obj is of matrix_types. metadata is (func_name, arg_name) for error
    information display.
    """
    if not isinstance(obj, scalar_types):
        message = 'In func{}, name {}: \nexpected {}, \
            \ngot {}'.format(metadata[0], metadata[1], vector_types, type(obj))
        raise ScalarTypeError(message, obj)
    elif not len(obj.shape) == 0:
        message = 'In {}, name {}: \nscalar must be 0D (, ), \
            \ngot shape {}.'.format(metadata[0], metadata[1], obj.shape)
        raise ScalarTypeError(message, obj)
    elif not obj.dtype.type == DTYPE:
        message = 'In {}, name {}: Data type must be {}, \
            got {}.'.format(metadata[0], metadata[1], DTYPE, obj.dtype)
        raise ScalarTypeError(message, obj)
