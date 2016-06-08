# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 11:26:41 2016

@author: Falaize
"""

import numpy

EPS = numpy.finfo(float).eps


def geteval(obj, attr):
    """
    if attr is function, return attr evaluation with no arguments, else attr.
    """
    elt = getattr(obj, attr)
    if hasattr(elt, '__call__'):
        return elt()
    else:
        return elt


def lambdify(args, expr):
    """
    call to lambdify with chosen options
    """
    import sympy
    import numpy
    return sympy.lambdify(args, expr,
                          dummify=False,
                          modules=[{'MutableDenseMatrix': numpy.matrix,
                                    'ImmutableMatrix': numpy.matrix},
                                    'numpy'])


def find(symbs, listargs):
    """
    sort elements in syms according to listargs, and return args and \
list of positions in listargs
    """
    args = []
    inds = []
    n = 0
    for arg in listargs:
        if arg in symbs:
            args.append(arg)
            inds.append(n)
        n += 1
    return tuple(args), tuple(inds)


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

