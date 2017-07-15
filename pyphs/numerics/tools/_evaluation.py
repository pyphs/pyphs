#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 20:08:06 2017

@author: Falaize
"""

from pyphs.config import VERBOSE
from pyphs.misc.tools import geteval, find
from pyphs.core.tools import free_symbols
from ._lambdify import lambdify
import numpy

class Evaluation(object):
    """
    Class that serves as a container for numerical evaluation of all
    functions from a given Core.
    """
    def __init__(self, core, vectorize=True):
        if VERBOSE >= 1:
            print('Build numerical evaluations...')

        self.core = core.__copy__()
        self.core.substitute(selfall=True)
        self.build(vectorize)

    def build(self, vectorize=True):
        names = self.core.exprs_names
        names = names.union(self.core.struc_names)
        names = names.union({'dxH'})

        subs = self.core.subs.copy()
        for k in subs.keys():
            if not isinstance(subs[k], (int, float)):
                try:
                    subs[k] = subs[k].subs(subs)
                except AttributeError:
                    pass
        # for each function, subs, stores func args, args_inds and lambda func
        for name in names:
            func, args, inds = self.expr_to_numeric(self.core, name,
                                                    self.args())
            setattr(self, name, func)
            setattr(self, name+'_args', args)
            setattr(self, name+'_inds', inds)

    def args(self):
        return (self.core.x + self.core.dx() + self.core.w + self.core.u +
                self.core.p + self.core.o())

    @staticmethod
    def expr_to_numeric(core, name, allargs, theano=False, vectorize=True):
        """
        Return an evaluator of the function :code:`getarg(nums.method, names + '_expr')`,
        with a mapping to some of the arguments in :code:`nums.args`, using
        sympy or theano lambdification.

        Parameters
        ----------

        core : Core

        name : str

        theano : bool
        
        vectorize : bool

        Return
        ------

        func : function
            Evaluator
        """
        expr = geteval(core, name)
        if expr is not None:
            symbs = free_symbols(expr)
            args, inds = find(symbs, allargs)  # args are symbs reorganized
            func = lambdify(args, expr, subs=core.subs,
                            theano=theano)
            func = numpy.vectorize(func)
            func.func_doc = """
    Evaluate `{0}`.

    Parameters
    ----------
    """.format(name) + ''.join(["""
    {} : float
    """.format(str(a)) for a in args]) + """

    Return
    ------

    {0} : numpy array
        The numerical valuation of {0}.
            """.format(name)

        else:
            func, args, inds = None, None, None

        return func, args, inds
