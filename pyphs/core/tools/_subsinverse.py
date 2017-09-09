#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 22:50:43 2017

@author: Falaize
"""


import sympy as sp
from . import _types as types


def subsinverse_scalar(expr, subs, symbols):
    if isinstance(expr, (sp.Symbol, sp.Float, float)):
        return expr
    if isinstance(expr, (sp.Symbol, sp.Float, float)):
        return expr
    else:
        expr = sp.simplify(expr)
        args = expr.args
        try:
            test3 = bool(args[1] < 0)
        except (TypeError, IndexError, AttributeError):
            test3 = False
        if (isinstance(expr, sp.Pow) and bool(args[0] in subs.keys()) and
                test3):
            symb, val = args
            isymb = symbols('inv'+str(symb))
            subs.update({isymb: subs[symb]**-1})
            args = (isymb, -val)
        args = list(args)
        for i, a in enumerate(args):
            if not (a in expr.atoms() or a in subs.keys()):
                args[i] = subsinverse_scalar(a, subs, symbols)
        return expr.func(*args)



def subsinverse_vector(expr, subs, symbols):
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
        expr[i] = subsinverse_scalar(e, subs, symbols)
    return expr


def subsinverse_matrix(expr, subs, symbols):
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
    # iterate over list elements
    for i, j, e in expr.row_list():
        try:
            expr[i, j] = subsinverse_scalar(e, subs, symbols)
        except (AttributeError, TypeError):
            pass
    return expr


def subsinverse_dict(expr, subs, symbols):
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
            expr[k] = subsinverse_scalar(expr[k], subs, symbols)
        except (AttributeError, TypeError):
            pass
    return expr


# =========================================================================

def subsinverse(expr, subs, symbols):
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
        expr = subsinverse_matrix(expr, subs, symbols)
    elif isinstance(expr, types.vector_types):
        expr = subsinverse_vector(expr, subs, symbols)
    elif isinstance(expr, types.scalar_types):
        expr = subsinverse_scalar(expr, subs, symbols)
    elif isinstance(expr, dict):
        expr = subsinverse_dict(expr, subs, symbols)
    else:
        text = 'Type {} is not a pyphs expression.'.format(type(expr))
        raise TypeError(text)
    return expr



# =========================================================================

def subsinverse_core(core):
    """
    subsinverse_core
    *********************

    Remove inverse of parameters in subs.

    Parameters
    -----------
    core : Core
    """

    # substitutions in core's list of expressions and symbols
    attrs_to_sub = set(list(core.exprs_names) +
                       list(core.symbs_names) +
                       ['M', '_dxH', 'observers'])
    for name in attrs_to_sub:
        expr = getattr(core, name)
        if expr is None or callable(expr):
            pass
        else:
            setattr(core, name, subsinverse(expr, core.subs,
                                                 core.symbols))
