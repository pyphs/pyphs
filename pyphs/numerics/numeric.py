# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 15:27:55 2016

@author: Falaize
"""

from tools import geteval, lambdify, find
from pyphs.symbolics.tools import free_symbols

# names of arguments for functions evaluation
_args_names = ('x', 'dx', 'w', 'u', 'p')


class Numeric:
    """
    Class that serves as a container for all numerical functions
    """
    def __init__(self, phs):

        # names of arguments for functions evaluation
        self.args_names = _args_names
        # lists all arguments
        args = []
        for name in self.args_names:
            symbs = geteval(phs.symbs, name)
            args += list(symbs)
        # stores args as tuple
        self.args = tuple(args)
        # lists all functions
        self.funcs_names = phs.exprs._names
        # for each function, subs, stores func args, args_inds and lambda func
        for name in self.funcs_names:
            expr = getattr(phs.exprs, name)
            if hasattr(expr, 'index'):
                expr = list(expr)
                for i in range(len(expr)):
                    expr[i] = expr[i].subs(phs.symbs.subs)
            else:
                expr = expr.subs(phs.symbs.subs)
            func, args, inds = self._expr_to_numerics(expr)
            setattr(self, name, func)
            setattr(self, 'args_'+name, args)
            setattr(self, 'inds_'+name, inds)

    def _expr_to_numerics(self, expr):
        """
        get symbols in expr, and return lambdified evaluation, \
arguments symbols and arguments position in list of all arguments
        """
        symbs = free_symbols(expr)
        args, inds = find(symbs, self.args)
        func = lambdify(args, expr)
        return func, args, inds
