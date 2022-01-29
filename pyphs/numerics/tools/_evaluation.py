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


def pyphs_vectorize(func):
    """
    Control how to vectorize functions.
    """
    # return numpy.vectorize(func)
    def vec_func(*args):
        len_args = len(args[0])
        if not all(len(a) == len_args for a in args[1:]):
            raise AttributeError(
                "Can not call vectorized function {} since given arguments have not the same length.".format(
                    func.__name__
                )
            )
        for ith_args in zip(*args):
            yield func(*ith_args)

    return vec_func


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

    def __init__(self, core, names=None, vectorize=True, vslice=None, theano=None):
        if VERBOSE >= 1:
            print("Build numerical evaluations...")

        self.core = core.__copy__()
        self.core.o = list(self.core.observers.values())

        self.core.substitute(selfall=True)

        if names in ["all", None]:
            names = self.core.exprs_names
            names = names.union(self.core.struc_names)
            names = names.union({"dxH"})
            try:
                # Includes Method attibutes
                names = names.union(self.core.args_names)
                names = names.union(self.core.funcs_names)
                names = names.union(self.core.ops_names)
                names = names.union(self.core.update_actions)
            except AttributeError:
                pass

        self.build(vectorize=vectorize, names=names, theano=theano, vslice=vslice)

    def build(self, vectorize=True, names=None, theano=None, vslice=None):

        if vslice is not None and not len(names) == 1:
            raise AttributeError(
                "Can not slice Evaluation object for more than one attribute: names={}, vslice={}".format(
                    names, vslice
                )
            )

        if names is None:
            names = list()

        # for each function, subs, stores func args, args_inds and lambda func
        for name in names:

            func, args, inds = self.expr_to_numeric(
                self.core, name, self.args(), theano=theano, vslice=vslice
            )
            setattr(self, name, func)
            setattr(self, name + "_args", args)
            setattr(self, name + "_inds", inds)

    def args(self):
        return (
            self.core.x
            + self.core.dx()
            + self.core.w
            + self.core.u
            + self.core.p
            + list(self.core.observers.keys())
        )

    @staticmethod
    def expr_to_numeric(core, name, allargs, theano=None, vectorize=True, vslice=None):
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

        vslice: slice in result of function call

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
                func = vector_expr_to_numeric(
                    args,
                    expr[vslice],
                    subs=core.subs,
                    theano=theano,
                    vectorize=vectorize,
                )
            else:
                if (
                    vslice is not None
                    and not vslice.start == vslice.stop == vslice.step == None
                ):
                    raise AttributeError(
                        "Can not slice evaluation of scalar expression: expr={}, vslice={}".format(
                            expr, vslice
                        )
                    )
                func = scalar_expr_to_numeric(
                    args, expr, subs=core.subs, theano=theano, vectorize=vectorize
                )

            func.__doc__ = (
                """
    Evaluate `{0}`.

    Parameters
    ----------
    """.format(
                    name
                )
                + "".join(
                    [
                        """
    {} : float
    """.format(
                            str(a)
                        )
                        for a in args
                    ]
                )
                + """

    Return
    ------

    {0} : numpy array
        The numerical valuation of {0}{1}.
            """.format(
                    name, "" if vslice is None else "[{0}]".format(vslice)
                )
            )

        else:
            print("Expression {0} is None".format(name))
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
        func = pyphs_vectorize(fun)

    # Cope with vector evaluation of functions with no arguments
    elif vectorize and len(args) == 0:

        def func(*args):
            if len(args) == 0:
                return numpy.array(fun())
            elif isinstance(args[0], list):
                return numpy.array(
                    [
                        fun(),
                    ]
                    * len(args[0])
                )
            elif isinstance(args[0], numpy.ndarray):
                return numpy.array(
                    [
                        fun(),
                    ]
                    * args[0].shape[0]
                )
            else:
                return numpy.array(fun())

    # No vectorization
    else:
        func = fun

    return func


def vector_expr_to_numeric(args, expr, subs=None, theano=None, vectorize=True):

    funcs = []
    for e in expr:
        funcs.append(
            scalar_expr_to_numeric(
                args, e, subs=subs, theano=theano, vectorize=vectorize
            )
        )

    def func(*args):
        return numpy.array(tuple(map(lambda f: f(*args), funcs))).T

    return func
