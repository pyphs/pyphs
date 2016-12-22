# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 15:27:55 2016

@author: Falaize
"""

from pyphs.core.symbs_tools import free_symbols
import numpy
import sympy


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
        from pyphs.core.symbs_tools import simplify as simp
        expr = simp(expr)

    lambda_expr = sympy.lambdify(args, expr, modules='numpy', dummify=False)

    def func(*args_):
        return lambda_expr(*[numpy.array(a) for a in args_])
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


class Functions:
    """
    Class that serves as a container for all numerical functions
    """
    def __init__(self, core):
        self.core = core

    def build(self):
        # for each function, subs, stores func args, args_inds and lambda func
        for name in self.core.exprs_names:
            expr = getattr(self.core, name)
            if hasattr(expr, 'index'):
                expr = list(expr)
                for i, expr_i in enumerate(expr):
                    expr[i] = expr_i.subs(self.core.subs)
            else:
                expr = expr.subs(self.core.subs)
            func, args, inds = self._expr_to_numerics(expr,
                                                      self.core.args())
            setattr(self, name, func)
            setattr(self, name+'_args', args)
            setattr(self, name+'_inds', inds)

    def _expr_to_numerics(self, expr, allargs):
        """
        get symbols in expr, and return lambdified evaluation, \
arguments symbols and arguments position in list of all arguments
        """
        symbs = free_symbols(expr)
        args, inds = find(symbs, allargs)  # args are symbs reorganized
        func = lambdify(args, expr)
        return func, args, inds
