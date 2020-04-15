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

class PHSVector(sympy.Tuple):

    def __new__(cls, *args, **kwargs):
        obj = sympy.Tuple.__new__(cls, *args)
        return obj

    @property
    def has_subarray(self):
        all_types = set()
        for elt in self:
            all_types.append(map(type, elt.free_symbols))
        return PHSSubArray in all_types

    @property
    def dim(self):
        return len(self)

    def remove(self, symb):
        out = tuple()
        for elt in self:
            if elt != symb:
                out += (elt, )
        self._args = out

    def __add__(self, other):
        return PHSVector(*super(PHSVector, self).__add__(other))

    def __iadd__(self, other):
        return PHSVector(*super(PHSVector, self).__add__(other))

    def __getitem__(self, key):
        item = super(PHSVector, self).__getitem__(key)
        if hasattr(item, "__iter__"):
            return PHSVector(*item)
        else:
            return item

    def append(self, obj):
        self._args = self._args + (obj,)

    def pop(self, i):
        args = list(self._args)
        arg = args.pop(i)
        self._args = tuple(args)
        return arg


vector_types = (PHSVector, )


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

class PHSMatrix(sympy.SparseMatrix):

    def get_ith_col(self, i):
        for elt in self.row_list():
            if elt[1] == i:
                yield elt

    def get_ith_row(self, i):
        for elt in self.col_list():
            if elt[0] == i:
                yield elt


class PHSSubArray(sympy.Symbol):

    is_scalar = False

    def __new__(self, name, *args, **kwargs):
        attrs = dict()
        for attr in ['shape', 'array']:
            kwargs.setdefault(attr, None)
            attrs[attr] = kwargs.pop(attr)

        kwargs['commutative'] = False

        obj = super(PHSSubArray, self).__new__(self, name, *args, **kwargs)

        if attrs['shape'] is not None:
            obj._phs_array = None
            obj._shape = attrs['shape']
        elif attrs['array'] is not None:
            if isinstance(attrs['array'], (list, tuple)):
                a = sympy.Array(attrs['array'])
                if len(a.shape) == 1:
                    obj._phs_array = PHSVector(*attrs['array'])
                elif len(a.shape) == 2:
                    obj._phs_array = PHSMatrix(attrs['array'])
                else:
                    raise AttributeError('`array` in SubArray must be 1 dimensional (vector) or 2 dimensional (Matrix), got {}.'.format(a))
            obj._shape = None
        else:
            raise AttributeError('Either `shape` or `array` argument must be specified to SubArray.')
        return obj

    @property
    def array(self):
        return self._phs_array

    @property
    def shape(self):
        if self.array is not None:
            return self.array.shape
        else:
            return self._shape

    def __getitem__(self, i):
        return self.array[i]


matrix_types = (PHSMatrix, )


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
