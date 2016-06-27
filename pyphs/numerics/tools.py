# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 11:26:41 2016

@author: Falaize
"""

from sympy.printing.lambdarepr import lambdarepr
import numpy
import sympy
import ast

parser_sympy2numpy = {
            'sin': numpy.sin,
            'cos': numpy.cos,
            'tan': numpy.tan,
            'asin': numpy.arcsin,
            'acos': numpy.arccos,
            'atan': numpy.arctan,
            'atan2': numpy.arctan2,
            'sinh': numpy.sinh,
            'cosh': numpy.cosh,
            'tanh': numpy.tanh,
            'asinh': numpy.arcsinh,
            'acosh': numpy.arccosh,
            'atanh': numpy.arctanh,
            'ln': numpy.log,
            'log': numpy.log,
            'exp': numpy.exp,
            'sqrt': numpy.sqrt,
            'Abs': numpy.abs,
            'conjugate': numpy.conj,
            'im': numpy.imag,
            're': numpy.real,
            'where': numpy.where,
            'complex': numpy.complex,
            'MutableDenseMatrix': numpy.array,
            'DenseMatrix': numpy.array,
            'ImmutableDenseMatrix': numpy.array,
            'ImmutableMatrix': numpy.array,
            'Matrix': numpy.array}

def lambdify(args, expr, subs=None, simplify=True):
    """
    call to lambdify with chosen options
    """
#    from sympy.printing.theanocode import theano_function
#    return theano_function(args, expr)

    if hasattr(expr, 'index'):
        expr = sympy.Matrix(expr)

    if subs is not None:
        if hasattr(expr, 'index'):
            for i, e in enumerate(expr):
                expr[i] = e.subs(subs)
        else:
            expr = expr.subs(subs)
    if simplify:
        from pyphs.symbolics.tools import simplify as simp
        expr = simp(expr)
    str_expr = lambdarepr(expr)
    str_args = ""
    for arg in args:
        str_args += str(arg) + ', '
    func = eval('lambda ' + str_args + ' : ' + str_expr,
                parser_sympy2numpy,
                {})
    return func


def find(symbs, allsymbs):
    """
    sort elements in symbs according to listargs, and return args and \
list of positions in listargs
    """
    args = []
    inds = []
    n = 0
    for symb in allsymbs:
        if symb in symbs:
            args.append(symb)
            inds.append(n)
        n += 1
    return tuple(args), tuple(inds)
