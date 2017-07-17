#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 18 21:39:29 2017

@author: Falaize
"""
from ..tools import types, free_symbols
from ..tools import simplify as simplify_func
from pyphs.misc.tools import geteval
import sympy


# =========================================================================

def substitute_scalar(expr, subs=None):
    """
    Apply substitution method to scalar expression expr.

    Parameters
    ----------

    expr : pyphs scalar expression.
        Expression wich parameters are to be substitute.

    subs : dic
        Substitution dictionary '{symb : sub}'.

    Return
    ------

    expr_subs : pyphs scalar expression
        The resulting expression.
    """
    try:
        expr = expr.subs(subs)
    except AttributeError:
        expr = sympy.sympify(expr)
    return expr


def substitute_vector(expr, subs=None):
    """
    Apply substitution method to vector expression expr.

    Parameters
    ----------

    expr : pyphs vector expression.
        Expression wich parameters are to be substitute.

    subs : dic
        Substitution dictionary '{symb : sub}'.

    Return
    ------

    expr_subs : pyphs vector expression
        The resulting expression.
    """
    # recast as list
    if not isinstance(expr, types.vector_types[0]):
        expr = types.vector_types[0](expr)

    # iterate over list elements
    for i, e in enumerate(expr):
        expr[i] = substitute_scalar(e, subs)
    return expr


def substitute_matrix(expr, subs=None):
    """
    Apply substitution method to matrix expression expr.

    Parameters
    ----------

    expr : pyphs matrix expression.
        Expression wich parameters are to be substitute.

    subs : dic
        Substitution dictionary '{symb : sub}'.

    Return
    ------

    expr_subs : pyphs matrix expression
        The resulting expression.
    """
    # iterate over matrix elements
    return expr.subs(subs)


def substitute_dict(expr, subs):
    """
    Select and apply appropriate substitution method based on expr type.

    Parameters
    ----------

    expr : dict.
        Expressions wich parameters are to be substitute.

    subs : dic
        Substitution dictionary '{symb : sub}'.

    Return
    ------

    expr_subs : same type as expr
        The resulting expression. The substitution applies on the keys and the
        values of the dictionary.
    """
    for k in expr.keys():
        try:
            expr[k] = expr[k].subs(subs)
        except AttributeError:
            pass
    return expr


# =========================================================================

def substitute(expr, subs):
    """
    Select and apply appropriate substitution method based on expr type.

    Parameters
    ----------

    expr : pyphs scalar, vector or matrix expression, or dic.
        Expression wich parameters are to be substitute.

    subs : dic
        Substitution dictionary '{symb : sub}'.

    Return
    ------

    expr_subs : same type as expr
        The resulting expression.
    """
    if isinstance(expr, types.matrix_types):
        expr = substitute_matrix(expr, subs)
    elif isinstance(expr, types.vector_types):
        expr = substitute_vector(expr, subs)
    elif isinstance(expr, types.scalar_types):
        expr = substitute_scalar(expr, subs)
    elif isinstance(expr, dict):
        expr = substitute_dict(expr, subs)
    else:
        text = 'Type {} is not a pyphs expression.'.format(type(expr))
        raise TypeError(text)
    return expr


# =========================================================================

def substitute_core(core, subs=None, selfall=False, selfexprs=False,
                    simplify=False):
    """
    substitute_core
    ***************

    Apply substitutions to every expressions of a Core.

    Parameters
    -----------
    subs : dictionary or None
        A dictionary with entries in the format :code:`{s: v}` with
        :code:`s` the sympy symbol to substitute by value :code:`v`, which
        value can be a numerical value (:code:`float, int`), a new sympy symbol
        or a sympy expression. Default is None.

    selfall : bool
        If True, every substitutions in the dictionary :code:`Core.subs`
         are applied and the dictionary is reinitialized to :code:`{}`. Default
         is False.

    selfexprs : bool
        If True, only substitutions in the dictionary :code:`Core.subs`
        that are not numerical values are applied to the core's expressions.

    simplify : bool
        If True, every expressions are simplified after substitution (default).

    """

    # init substitution dic
    if subs is None:
        subs = {}

    # append self subs dic
    if selfall:
        substitute_core(core, selfexprs=True)
        subs.update(core.subs)
    # append only exprs in core subs dic
    elif selfexprs:
        for k in core.subs.keys():
            if not isinstance(core.subs[k], (int, float)):
                subs[k] = core.subs[k]

    # substitutions in core's own subsitution dictionary
    core.subs = substitute_dict(core.subs, subs)

    # substitutions in core's list of expressions and symbols
    attrs_to_sub = set(list(core.exprs_names) +
                       list(core.symbs_names) +
                       ['M', '_dxH', 'observers'])
    for name in attrs_to_sub:
        expr = geteval(core, name)
        keys = free_symbols(expr).intersection(set(subs.keys()))
        # recast the elements of the substitution dictionary as sympy objects
        subs_e = dict(map(lambda k, v: (k, v),
                          keys, [subs[k] for k in keys]))
        if expr is None or callable(expr):
            pass
        else:
            setattr(core, name, substitute(expr, subs_e))
            if simplify:
                expr = simplify_func(expr)

    # remove entries in core.subs
    for k in subs.keys():
        try:
            core.subs.pop(k)
        except KeyError:
            pass
