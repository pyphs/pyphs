# -*- coding: utf-8 -*-
"""
Created on Tue May 31 10:46:21 2016

@author: Falaize
"""
import sympy as sp
import numpy as np
from utils.calculus import mysimplify, mysymbolicinv
from utils.calculus import eps


def args_ordering():
    """
    chosen ordering for the arguments of lambdified functions
    """
    ordering = 'x dx w u p'
    return ordering.split(' ')


def lambdify(args, expr):
    """
    call to lambdify with chosen options
    """
    return sp.lambdify(args, expr,
                       dummify=False,
                       modules=[{'MutableDenseMatrix': np.matrix,
                                 'ImmutableMatrix': np.matrix,
                                 'Piecewise': float},
                                'numpy'])


def get_free_symbols(phs, attr):
    obj = getattr(phs, attr)
    if isinstance(obj, list):
        symbs = set()
        for el in obj:
            assert isinstance(el, (sp.Expr, float, int))
            symbs = symbs.union(sp.sympify(el).free_symbols)
    else:
        assert isinstance(obj, (sp.Expr, sp.Matrix, sp.immutable.MatrixExpr)),\
            'got {0!s} obj {1!s} with type(obj): {2!s}'.format(attr, obj, type(obj))
        symbs = sp.sympify(obj.free_symbols)
    symbs_sort = []
    for var in args_ordering():
        for symb in getattr(phs, var):
            if symb in symbs:
                symbs_sort.append(symb)
    return symbs_sort


def self_lambdify(numerics):
    """
    lambdify all exprs of numerics
    """
    # list of variables quantities on which the lambdified functions depend
    variables = args_ordering()
    # list all variables
    symbs = []
    for name in variables:
        symb = getattr(numerics.phs, name)
        setattr(numerics, name+'_symbs', symb)
        setattr(numerics, name+'_inds',
                (len(symbs), len(symbs)+len(symb)))
        symbs += symb
    setattr(numerics, 'all_symbs', symbs)
    setattr(numerics, 'all_vals', [0, ]*len(numerics.all_symbs))

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
    for name in variables:
        inds = getattr(numerics, name+'_inds')
        setattr(numerics, name, get_generator(inds))
        setattr(numerics, 'set_'+name, set_generator(inds))

    # list all functions to lambdify
    numerics.funcs_to_lambdify = 'H dtx dxH dxHd z y Jx Jw Jy K Gx Gw J' +\
        numerics.funcs_to_lambdify
    for name in numerics.funcs_to_lambdify.split(' '):
        func_original = getattr(numerics.phs, name)
        symbs_in_func = get_free_symbols(numerics.phs, name)
        func_num_selected_args = lambdify(symbs_in_func, func_original)
        setattr(numerics.phs, name+'_num', func_num_selected_args)
        func_num_all_args = lambdify(numerics.all_symbs, func_original)
        setattr(numerics, name, eval_generator(func_num_all_args))


class numerics:
    """
    A system object that stores the current numerical state of a given phs.

    Parameters
    -----------

    phs : pypHs.pHobj

    x0 : init values for state vector

    """

    def __init__(self, phs, x0=None, fs=None, config=None):

        # init config
        if config is None:
            config = {}
        self.config = config_numerics()
        # update with provided dic
        self.config.update(config)
        # sample rate
        if fs is not None:
            assert isinstance(fs, (int, float)), 'fs should be int or float, \
                got {0!s}'.format(type(fs))
            fs = int(fs)
        else:
            fs = sp.symbols('fs', real=True)
        self.fs = fs
        self.ts = self.fs**(-1)
        # build phs if not yet
        if not hasattr(phs, 'dxH'):
            phs.build(print_latex=False)
        # copy phs in a new pHobj to subs
        from pypHs import pHobj
        temp = pHobj()
        from utils.structure import copy
        copy(phs, temp)
        # substitue symbols by values for the 'symbols' in 'phs.subs'
        temp.applySubs()
        # store phs structure
        self.phs = temp
        # build structure
        self_structure(self)
        # set build solver functions
        self_solver(self, self.config['solver'])
        # set build all numerical functions
        self_lambdify(self)
        # init value
        if x0 is None:
            x0 = [0, ]*temp.nx()
        else:
            assert isinstance(x0, list) and len(x0) == self.phs.nx()
        self.set_x(x0)

    def data_generator(self, var, ind=None, postprocess=None):
        from utils.io import data_generator
        import os
        filename = self.phs.folders['data']+os.sep+var+'.txt'
        load_options = self.config['load_options']
        generator = data_generator(filename, ind=ind, postprocess=postprocess,
                                   **load_options)
        return generator

