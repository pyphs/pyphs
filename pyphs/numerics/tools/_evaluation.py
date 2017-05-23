#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 20:08:06 2017

@author: Falaize
"""

from pyphs.misc.tools import geteval, find
from pyphs.core.tools import free_symbols
from ._lambdify import lambdify
import numpy


class PHSNumericalEval(object):
    """
    Class that serves as a container for numerical evaluation of all
    functions from a given PHSCore.
    """
    def __init__(self, core, vectorize=True):
        print('Build numerical evaluations...')

        self.core = core
        self.build(vectorize)

    def build(self, vectorize=True):
        names = self.core.exprs_names
        names = names.union(self.core.struc_names)
        names = names.union({'dxH'})

        subs = self.core.subs.copy()
        for k in subs.keys():
            if not isinstance(subs[k], (int, float)):
                try:
                    subs[k] = subs[k].subs(subs).simplify()
                except AttributeError:
                    pass
        # for each function, subs, stores func args, args_inds and lambda func
        for name in names:
            expr = geteval(self.core, name)
            if hasattr(expr, 'index'):
                expr = list(expr)
                for i, expr_i in enumerate(expr):
                    expr[i] = expr_i.subs(subs)
            else:
                expr = expr.subs(subs)
            func, args, inds = self._expr_to_numerics(expr,
                                                      self.core.args(),
                                                      vectorize)
            setattr(self, name, func)
            setattr(self, name+'_args', args)
            setattr(self, name+'_inds', inds)

    @staticmethod
    def _expr_to_numerics(expr, allargs, vectorize):
        """
        get symbols in expr, and return lambdified evaluation, \
arguments symbols and arguments position in list of all arguments
        """
        symbs = free_symbols(expr)
        args, inds = find(symbs, allargs)  # args are symbs reorganized
        if vectorize:
            func = numpy.vectorize(lambdify(args, expr))
        else:
            func = lambdify(args, expr)
        return func, args, inds
