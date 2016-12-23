# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 11:26:41 2016

@author: Falaize
"""

from pyphs.core.symbs_tools import simplify as simp
import numpy
import sympy


def lambdify(args, expr, subs=None, simplify=True):
    """
    call to lambdify with chosen options
    """
    vector_expr = hasattr(expr, 'index')
    if vector_expr:
        expr = sympy.Matrix(expr)

    if subs is not None:
        if vector_expr:
            for i, e in enumerate(expr):
                expr[i] = e.subs(subs)
        else:
            expr = expr.subs(subs)
    if simplify:
        expr = simp(expr)
    array2mat = [{'ImmutableMatrix': numpy.matrix}, 'numpy']
    expr_lambda = sympy.lambdify(args, expr, dummify=False, modules=array2mat)
    return expr_lambda


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
