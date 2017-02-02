# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 15:27:55 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

from pyphs.core.misc_tools import geteval
from pyphs.core.symbs_tools import free_symbols
from .tools import (lambdify, find, getarg_generator, setarg_generator,
                    getfunc_generator, setfunc_generator, evalfunc_generator,
                    evalop_generator)
from pyphs.config import standard_simulations
import numpy


class PHSNumericalCore:
    """
    Class that serves as a container for all numerical functions
    """
    def __init__(self, method, config=None):

        # init config with standard configuration options
        self.config = standard_simulations.copy()
        # update with provided config
        if config is None:
            config = {}
        self.config.update(config)

        self.method = method

        self.build_args()
        self.build_funcs()
        self.build_ops()

    def build_args(self):
        """
        define accessors and mutators of numerical values associated with
        arguments of expressions.
        """
        # init args values with 0
        setattr(self, 'args', numpy.array([0., ]*self.method.core.dims.args()))

        for name in self.method.args_names:
            inds = getattr(self.method, name + '_inds')
            setattr(self, name, getarg_generator(self, inds))
            setattr(self, 'set_' + name, setarg_generator(self, inds))

    def build_funcs(self):
        """
        link and lambdify all functions for python simulation
        """
        # link evaluation to internal values
        for name in self.method.funcs_names:
                setattr(self, name + '_eval', evalfunc_generator(self, name))
                setattr(self, name, getfunc_generator(self, name))
                setattr(self, 'set_' + name, setfunc_generator(self, name))
                setattr(self, '_' + name, getattr(self, name + '_eval')())

    def build_ops(self):
        """
        link and lambdify all functions for python simulation
        """
        # link evaluation to internal values
        for name in self.method.ops_names:
                setattr(self, name + '_eval',
                        evalop_generator(self, getattr(self.method,
                                                       name + '_op')))
                setattr(self, name, getfunc_generator(self, name))
                setattr(self, 'set_' + name, setfunc_generator(self, name))
                setattr(self, '_' + name, getattr(self, name + '_eval')())

    def update(self, u=None, p=None):

        if u is None:
            u = numpy.zeros(self.method.ny)

        if p is None:
            p = numpy.zeros(self.method.np)

        self.set_u(u)
        self.set_p(p)
        for action in self.method.update_actions:
            actiontype = action[0]
            if actiontype == 'exec':
                self.execs(action[1])
            else:
                self.iterexecs(*action[1])

    def execs(self, commands):
        for command in commands:
            if isinstance(command, str):
                getname = command
                evalname = getname
            else:
                getname = command[0]
                evalname = command[1]
            setfunc = getattr(self, 'set_'+getname)
            evalfunc = getattr(self, evalname + '_eval')
            setfunc(evalfunc())

    def iterexecs(self, commands, res_name, step_name):
        # init it counter
        it = 0
        # init step on iteration
        getattr(self, 'set_' + step_name)(1.)
        # loop while res > tol, step > tol and it < itmax
        while getattr(self, res_name)() > self.config['numtol'] \
                and getattr(self, step_name)() > self.config['numtol']\
                and it < self.config['maxit']:
            self.execs(commands)
            it += 1


class PHSNumericalEval:
    """
    Class that serves as a container for numerical evaluation of all
    functions from a given PHSCore.
    """
    def __init__(self, core):
        self.core = core.__deepcopy__()
        if not self.core._exprs_built:
            self.core.build_exprs()
        self.build()

    def build(self):
        # for each function, subs, stores func args, args_inds and lambda func
        for name in self.core.exprs_names.union(self.core.struc_names):
            expr = geteval(self.core, name)
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

    @staticmethod
    def _expr_to_numerics(expr, allargs):
        """
        get symbols in expr, and return lambdified evaluation, \
arguments symbols and arguments position in list of all arguments
        """
        symbs = free_symbols(expr)
        args, inds = find(symbs, allargs)  # args are symbs reorganized
        func = lambdify(args, expr)
        return func, args, inds
