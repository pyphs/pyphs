# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 11:26:41 2016

@author: Falaize
"""


def geteval(obj, attr):
    """
    if attr is function, return attr evaluation with no arguments, else attr.
    """
    elt = getattr(obj, attr)
    if hasattr(elt, '__call__'):
        return elt()
    else:
        return elt


def lambdify(args, expr):
    """
    call to lambdify with chosen options
    """
    import sympy
    import numpy
    return sympy.lambdify(args, expr,
                          dummify=False,
                          modules=[{'MutableDenseMatrix': numpy.matrix,
                                    'ImmutableMatrix': numpy.matrix},
                                   'numpy'])


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
