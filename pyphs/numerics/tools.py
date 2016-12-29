# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 11:26:41 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

from pyphs.core.symbs_tools import simplify as simp
import numpy
import sympy
import copy

NumericalOperationParser = {'add': numpy.add,
                            'addarray': lambda v1, v2: numpy.add(v1.flatten(),
                                                                 v2.flatten()),
                            'dot': numpy.dot,
                            'inv': numpy.linalg.inv,
                            'norm': lambda x: numpy.sqrt(float(numpy.dot(x,
                                                                         x))),
                            }


def lambdify_NumericalOperation(nums, operation):
    eval_args = []
    for arg in operation.args:
        if isinstance(arg, PHSNumericalOperation):
            eval_args.append(lambdify_NumericalOperation(nums, arg))
        elif isinstance(arg, (float, int)):
            f = copy.copy(arg)
            eval_args.append(lambda: f)
        else:
            assert isinstance(arg, str)
            eval_args.append(getattr(nums, arg))
    func = NumericalOperationParser[operation.operation]

    def eval_func():
        return numpy.asarray(func(*[arg() for arg in eval_args]))
    return eval_func


def lambdify_SymbolicExpression(nums, name):
    expr = getattr(nums.method, name + '_expr')
    args = getattr(nums.method, name + '_args')
    inds = getattr(nums.method, name + '_inds')
    func = lambdify(args, expr,
                    subs=nums.method.subs)
    if len(inds) > 0:
        inds = numpy.array(inds)
    else:
        inds = list()

    def eval_func():
        return numpy.asarray(func(*numpy.array(nums.args[inds])))
    return eval_func


# generator of evaluation functions
def eval_generator(nums, name):
    expr = getattr(nums.method, name + '_expr')
    if isinstance(expr, PHSNumericalOperation):
        func = lambdify_NumericalOperation(nums, expr)
    elif isinstance(expr, str):
        attr = getattr(nums, expr)
        def func():
            return numpy.asarray(attr())
    else:
        func = lambdify_SymbolicExpression(nums, name)
    return func


def getarg_generator(nums, inds):
    """
    generators of 'get'
    """
    if len(inds) > 0:
        inds = numpy.array(inds)
    else:
        inds = list()

    def get_func():
        return nums.args[inds]

    return get_func


def setarg_generator(nums, inds):
    """
    generators of 'set'
    """
    if len(inds) > 0:
        inds = numpy.array(inds)
    else:
        inds = list()

    def set_func(array):
        nums.args[inds] = array.flatten()

    return set_func

def getfunc_generator(nums, name):
    """
    generators of 'get'
    """

    def get_func():
        return getattr(nums, '_' + name)

    return get_func


def setfunc_generator(nums, name):
    """
    generators of 'set'
    """

    def set_func(array):
        setattr(nums, '_' + name, array)

    return set_func


class PHSNumericalOperation:

    def __init__(self, operation, args):
        self.operation = operation
        self.args = args
        self.freesymbols = set()
        func = NumericalOperationParser[self.operation]
        self.call = [func, [None, ]*len(args)]
        for i, arg in enumerate(args):
            if isinstance(arg, PHSNumericalOperation):
                symbs = arg.freesymbols
                arg = arg.call
            elif isinstance(arg, str):
                symbs = set([arg, ])
            else:
                assert isinstance(arg, (int, float))
                symbs = set()
            self.call[1][i] = arg
            self.freesymbols = self.freesymbols.union(symbs)

    def __call__(self, *args):
        return self.func(*args)


def lambdify(args, expr, subs=None, simplify=True):
    """
    call to lambdify with chosen options
    """
    vector_expr = hasattr(expr, 'index')
    if subs is not None:
        if vector_expr:
            for i, e in enumerate(expr):
                expr[i] = e.subs(subs)
        else:
            expr = expr.subs(subs)
    if simplify:
        expr = simp(expr)
    # array2mat = [{'ImmutableMatrix': numpy.matrix}, 'numpy']
    expr_lambda = sympy.lambdify(args,
                                 expr, 
                                 dummify=False, 
                                 modules='numpy')
    return expr_lambda


def find(symbs, allsymbs):
    """
    sort elements in symbs according to listargs, and return args and \
list of positions in listargs
    """
    args = []
    inds = []
    n = 0
    for symb in allsymbs:
        if symb in symbs:
            args.append(symb)
            inds.append(n)
        n += 1
    return tuple(args), tuple(inds)


def regularize_dims(vec):
    """
    return column vector of zeros if vec has no shape along 2nd dimension
    """
    if vec.shape[1] == 0:
        vec = sympy.zeros(vec.shape[0], 1)
    return vec
