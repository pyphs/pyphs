# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 15:27:55 2016

@author: Falaize
"""

from tools import geteval, lambdify, find
from pyphs.symbolics.tools import free_symbols

_args_names = ('x', 'dx', 'w', 'u', 'p')


class Numeric:
    """
    Class that serves as a container for all numerical functions
    """
    def __init__(self, phs):

        self.args_names = _args_names
        # lists all arguments
        args = []
        for attr in self.args_names:
            symbs = geteval(phs.symbs, attr)
            args += list(symbs)
        # stores args as tuple
        self.args = tuple(args)
        # lists all functions
        self._names = phs.exprs._names
        # for each function, subs, stores func args, args_inds and lambda func
        for name in self._names:
            expr = getattr(phs.exprs, name)
            if hasattr(expr, 'index'):
                expr = list(expr)
                for i in range(len(expr)):
                    expr[i] = expr[i].subs(phs.symbs.subs)
            else:
                expr = expr.subs(phs.symbs.subs)
            func, args, inds = _expr_to_numerics(expr, self.args)
            setattr(self, name, func)
            setattr(self, 'args_'+name, args)
            setattr(self, 'inds_'+name, inds)


def _expr_to_numerics(expr, allargs):
    symbs = free_symbols(expr)
    args, inds = find(symbs, allargs)
    func = lambdify(args, expr)
    return func, args, inds


def self_lambdify(numerics):
    """
    lambdify all exprs of numerics
    """
    # list of args for the lambdified functions
    args = numerics.args

    # generators of 'get' and 'set':
    def get_generator(inds):
        def get_func():
            start, stop = inds
            return numerics.all_vals[start: stop]
        return get_func

    def set_generator(inds):
        def set_func(lis):
            start, stop = inds
            numerics.all_vals[start: stop] = lis[0: stop-start]
        return set_func

    def eval_generator(func_num_all_args):
        def eval_func():
            return func_num_all_args(*numerics.all_vals)
        return eval_func

    # get each variable in all_vals:
    for name in args:
        inds = getattr(numerics, name+'_inds')
        setattr(numerics, name, get_generator(inds))
        setattr(numerics, 'set_'+name, set_generator(inds))

    # list all functions to lambdify
    numerics.funcs_to_lambdify = 'H dtx dxH dxHd z y Jx Jw Jy K Gx Gw J' +\
        numerics.funcs_to_lambdify
    for name in numerics.funcs_to_lambdify.split(' '):
        func = getattr(numerics.phs, name)
        symbs_in_func = free_symbols(func, args)
        func_num_selected_args = lambdify(symbs_in_func, func)
        setattr(numerics.phs, name+'_num', func_num_selected_args)
        func_num_all_args = lambdify(numerics.all_symbs, func)
        setattr(numerics, name, eval_generator(func_num_all_args))


def get_argslabels(phs):
    return lambda: phs.symbs.argslabels


def get_inds(numerics, symbs):
    inds = list()
    for symb in symbs:
        inds.append(numerics.args.index(symb))
