# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 15:27:55 2016

@author: Falaize
"""

from tools import lambdify, find
from pyphs.symbolics.tools import free_symbols


class Numeric:
    """
    Class that serves as a container for all numerical functions
    """
    def __init__(self, phs):
        # for each function, subs, stores func args, args_inds and lambda func
        for name in phs.exprs._names:
            expr = getattr(phs.exprs, name)
            if hasattr(expr, 'index'):
                expr = list(expr)
                for i, expr_i in enumerate(expr):
                    expr[i] = expr_i.subs(phs.symbs.subs)
            else:
                expr = expr.subs(phs.symbs.subs)
            func, args, inds = self._expr_to_numerics(expr, phs.symbs.args())
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
