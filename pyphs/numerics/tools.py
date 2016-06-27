# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 11:26:41 2016

@author: Falaize
"""

from sympy.printing.lambdarepr import lambdarepr


def replace_sp2np(string):
    sympy2numpy = {
            'sin': 'sin',
            'cos': 'cos',
            'tan': 'tan',
            'asin': 'arcsin',
            'acos': 'arccos',
            'atan': 'arctan',
            'atan2': 'arctan2',
            'sinh': 'sinh',
            'cosh': 'cosh',
            'tanh': 'tanh',
            'asinh': 'arcsinh',
            'acosh': 'arccosh',
            'atanh': 'arctanh',
            'ln': 'log',
            'log': 'log',
            'exp': 'exp',
            'sqrt': 'sqrt',
            'Abs': 'abs',
            'conjugate': 'conj',
            'im': 'imag',
            're': 'real',
            'where': 'where',
            'complex': 'complex',
            'contains': 'contains',
            'MutableDenseMatrix': 'array'}
#            'DenseMatrix': 'array',
#            'ImmutableDenseMatrix': 'array',
#            'ImmutableMatrix': 'array',
#            'Matrix': 'array',

    for key in sympy2numpy:
        string = string.replace(key, 'numpy.'+sympy2numpy[key])
    return string


def lambdify(args, expr, subs=None, simplify=True):
    """
    call to lambdify with chosen options
    """
#    from sympy.printing.theanocode import theano_function
#    return theano_function(args, expr)
    if subs is not None:
        if hasattr(expr, 'index'):
            for i, e in enumerate(expr):
                expr[i] = e.subs(subs)
        else:
            expr = expr.subs(subs)
    if simplify:
        from pyphs.symbolics.tools import simplify as simp
        expr = simp(expr)
    str_expr = replace_sp2np(lambdarepr(expr))
    str_args = ""
    for arg in args:
        str_args += str(arg) + ', '
    import numpy
    func = eval('lambda ' + str_args + ' : ' + str_expr, {'numpy': numpy}, {})
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
