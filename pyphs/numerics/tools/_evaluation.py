#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 20:08:06 2017

@author: Falaize
"""

from pyphs.config import VERBOSE, THEANO
from pyphs.misc.tools import geteval, find
from pyphs.core.tools import free_symbols, types
from ._lambdify import lambdify
import numpy


class Evaluation(object):
    """
    Return an object with all the numerical function associated with all
    or a selected set of symbolic functions from a given pyphs.Core.

    Notice this is not a dynamical object, so it has to be rebuild if the
    original core object is changed in any way.

    Parameters
    ----------

    names : list of strings or 'all' (optional)
        List of core's arguments names associated with the functions that
        will be lambdified. If 'all', the names for every arguments,
        every functions (including all systems matrices and sub-matrices),
        and every operations are considered (processing time increase
        quickly with original core's complexity).

    vectorize : bool (optional)
        If True, every functions are vectorized with numpy.vectorize.
        The default is True.

    Output
    ------

    evaluation : pyphs.Evaluation
        An object with all the numerical function associated with all
        or a selected set of symbolic functions from a given pyphs.Core.

    """
    def __init__(self, core, names=None, vectorize=True, theano=None):
        if VERBOSE >= 1:
            print('Build numerical evaluations...')

        self.core = core.__copy__()
        self.core.o = list(self.core.observers.values())

        self.core.substitute(selfall=True)

        if names in ['all', None]:
            names = self.core.exprs_names
            names = names.union(self.core.struc_names)
            names = names.union({'dxH'})
            try:
                # Includes Method attibutes
                names = names.union(self.core.args_names)
                names = names.union(self.core.funcs_names)
                names = names.union(self.core.ops_names)
                names = names.union(self.core.update_actions)
            except AttributeError:
                pass

        self.build(vectorize=vectorize, names=names, theano=theano)

    def build(self, vectorize=True, names='all', theano=None):

        # for each function, subs, stores func args, args_inds and lambda func
        for name in names:

            func, args, inds = self.expr_to_numeric(self.core, name,
                                                    self.args(),
                                                    theano=theano)
            setattr(self, name, func)
            setattr(self, name+'_args', args)
            setattr(self, name+'_inds', inds)

    def args(self):
        return (self.core.x + self.core.dx() + self.core.w + self.core.u +
                self.core.p + list(self.core.observers.keys()))

    @staticmethod
    def expr_to_numeric(core, name, allargs, theano=None, vectorize=True):
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

        # set theano
        if theano is None:
            theano = THEANO

        # recover func from core
        expr = geteval(core, name)

        if expr is not None:

            # recover symbols from expr
            symbs = free_symbols(expr)

            # args are symbs reorganized
            args, inds = find(symbs, allargs)

            if isinstance(expr, types.vector_types):
                func = vector_expr_to_numeric(args, expr, subs=core.subs,
                                              theano=theano,
                                              vectorize=vectorize)
            else:
                func = scalar_expr_to_numeric(args, expr, subs=core.subs,
                                              theano=theano,
                                              vectorize=vectorize)

            func.__doc__ = """
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
            print('Expression {0} is None'.format(name))
            func, args, inds = None, None, None

        return func, args, inds


def scalar_expr_to_numeric(args, expr, subs=None, theano=None, vectorize=True):

        # set theano
        if theano is None:
            theano = THEANO

        if subs is None:
            subs = {}

        # lambdify func
        f = lambdify(args, expr, subs=subs, theano=theano)

        # map inputs to array (see sympy issue #11306)
        def fun(*args):
            return f(*map(numpy.array, args))

        # Cope with vector evaluation of functions with arguments
        if vectorize and len(args) > 0:
            func = numpy.vectorize(fun)

        # Cope with vector evaluation of functions with no arguments
        elif vectorize and len(args) == 0:
            def func(*args):
                if len(args) == 0:
                    return numpy.array(fun())
                elif isinstance(args[0], list):
                    return numpy.array([fun(), ]*len(args[0]))
                elif isinstance(args[0], numpy.ndarray):
                    return numpy.array([fun(), ]*args[0].shape[0])
                else:
                    return numpy.array(fun())
        # No vectorization
        else:
            func = fun

        return func


def vector_expr_to_numeric(args, expr, subs=None, theano=None, vectorize=True):

        funcs = []
        for e in expr:
            funcs.append(scalar_expr_to_numeric(args, e, subs=subs,
                                                theano=theano,
                                                vectorize=vectorize))

        def func(*args):
            return numpy.array(list(map(lambda f: f(*args), funcs))).T

        return func
