# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 15:27:55 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

from pyphs.core.symbs_tools import free_symbols
from .tools import (lambdify, find, eval_generator,
                    getarg_generator, setarg_generator,
                    getfunc_generator, setfunc_generator)
import numpy


class PHSNumericalCore:
    """
    Class that serves as a container for all numerical functions
    """
    def __init__(self, method):
        self.method = method
        self.args_names = {'vl', 'vnl',
                           'x', 'dx',
                           'xl', 'dxl',
                           'xnl', 'dxnl',
                           'w', 'wl', 'wnl',
                           'u', 'p'}
        self.build_args()
        self.build_funcs()

    def build_args(self):
        """
        define accessors and mutators of numerical values associated with
        arguments of expressions.
        """
        # init args values with 0
        setattr(self, 'args', numpy.array([0., ]*self.method.nargs))

        for name in self.args_names:
            inds = getattr(self.method, name + '_inds')
            setattr(self, name, getarg_generator(self, inds))
            setattr(self, 'set_' + name, setarg_generator(self, inds))

    def build_funcs(self):
        """
        link and lambdify all functions for python simulation
        """
        # link evaluation to internal values
        for name in self.method.exprs_names:
            if name not in self.args_names:
                setattr(self, name, eval_generator(self, name))
#                setattr(self, 'eval_' + name, eval_generator(self, name))
#                setattr(self, name, getfunc_generator(self, name))
#                setattr(self, 'set_' + name, setfunc_generator(self, name))
#                setattr(self, '_' + name, getattr(self, 'eval_' + name)())
                print(name)


class PHSNumericalEval:
    """
    Class that serves as a container for numerical evaluation of all
    functions from a given PHSCore.
    """
    def __init__(self, core):
        self.core = core.__deepcopy__()
        if not self.core._built:
            self.core.exprs_build()
        self.build()

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
