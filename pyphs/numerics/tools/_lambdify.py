#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 20:06:55 2017

@author: Falaize
"""

import sympy
from sympy.printing.theanocode import theano_function

import numpy
import copy

from pyphs.core.tools import types, free_symbols, substitute
from pyphs.core.tools import simplify as simp

from ._types import DTYPE

# Test for theano installed
try:
    from theano import tensor as T
    got_theano = True
except ImportError:
    got_theano = False


def theano_lambdify(args, expr):
    """
Lambdify expression expr w.r.t arguments args using theano.
    """

    theano_opts = {'on_unused_input': 'ignore',
                   'allow_input_downcast': False}

    # detect if expression is a vector
    if isinstance(expr, types.vector_types):
        # Below converts output of 1D vector functions with length 1...
        # ... back to 1D numpy array, because the default is 0D array (scalar).
        if len(expr) == 1:
            def getslice(f):
                return numpy.asarray(f, dtype=DTYPE)[numpy.newaxis]
        else:
            def getslice(f):
                return numpy.asarray(f, dtype=DTYPE)
    else:
        expr = [expr, ]

        def getslice(f):
            return numpy.asarray(f, dtype=DTYPE)

    # theano does not accept sympy numbers as output...
    expr_lambda = theano_function(args, expr, **theano_opts)

    return lambda *args: getslice(expr_lambda(*args))


def numpy_lambdify(args, expr):
    """
Lambdify expression expr w.r.t arguments args using numpy.
    """
    if isinstance(expr, types.vector_types):
        # Below converts output of 1D vector functions with length 1...
        # ... back to 1D numpy array, because the default is 0D array (scalar).
        def getslice(f):
            return numpy.asarray(f, dtype=DTYPE)
    else:
        def getslice(f):
            return numpy.asarray(f, dtype=DTYPE)

    expr_lambda = sympy.lambdify(args,
                                 expr,
                                 dummify=False,
                                 modules='numpy')

    return lambda *args: getslice(expr_lambda(*args))


def lambdify(args, expr, subs=None, simplify=False, theano=True):
    """
lambdify
********
Returns a lambda function for numerical evaluation of symbolic expression
defined by :code:`expr` with arguments defined by :code:`args`. It basically
uses :code:`sympy.lambdify`, or :code:`theano` if available on the system.

Parameters
----------

args : list of sympy.Symbols
    Arguments symbols for the symbolic expression; defines also the number of
    arguments of the returned numeric function.

expr : sympy.Expr, list of sympy.Expr, or sympy.SparseMatrix.
    Symbolic expression to lambdify.

subs: dict (optional)
    If all the symbols in :code:`expr` are not in :code:`args`, the remaining
    numerical values for replacements must be provided in this dictionary, with
    :code:`subs={symb1: val1, ...}` with :code`symb1` a symbol and :code`val1`
    the numerical value (float or int).

simplify : bool (optional)
    If True, expression is simplified before lambdification (default is False).

theano : bool (optional)
    If True, expression is compiled with theano. Then it's a compromise between
    the time for compiling C code vs. the acceleration of numerical evaluation.
    The default is True.

Return
------

f : callable
    Fast evaluation of expr provided len(args) numerical values.
    """
    # Avoid side effects of simplifications and substitutions
    expr = copy.copy(expr)

    # Check for types
    types.is_known_test(expr)

    # Substitutions
    if subs is not None:
        expr = substitute(expr, subs)

    # Simplification
    if simplify:
        expr = simp(expr)

    # sympify expression so that floats and ints are converted to sympy.Expr
    # expr = sympify(expr)

    missing_symbols = free_symbols(expr).difference(args)
    if not len(missing_symbols) == 0:
        raise AttributeError('Missing free symbols {}'.format(missing_symbols))

    # Choose backend (theano or numpy)
    if isinstance(expr, types.matrix_types):
        expr_ = sympy.Matrix(expr)
    else:
        expr_ = expr
    if theano and got_theano:
        return theano_lambdify(args, expr_)
    else:
        return numpy_lambdify(args, expr_)
