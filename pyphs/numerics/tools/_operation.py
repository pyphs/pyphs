#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 20:07:23 2017

@author: Falaize
"""
import numpy
from ._operators import norm


class Operation:

    def __init__(self, operation, args):

        self.operation = operation
        self.args = args

        func = PARSER[self.operation]

        self.call = [func, [None, ]*len(args)]
        self.freesymbols = set()

        for i, arg in enumerate(args):
            if isinstance(arg, Operation):
                symbs = arg.freesymbols
                arg = arg.call
            elif isinstance(arg, str):
                symbs = set([arg, ])
            else:
                symbs = set()
            self.call[1][i] = arg
            self.freesymbols = self.freesymbols.union(symbs)

    def __call__(self):
        args = list()
        for el in self.args:
            if hasattr(el, '__call__'):
                args.append(el())
            else:
                args.append(el)
        return self.call[0](*args)


# =========================================================================== #

# Dictionary of numerical methods callable by Operations
PARSER = {'add': numpy.add,
          'prod': lambda a1, a2: a1*a2,
          'dot': numpy.dot,
          'inv': numpy.linalg.inv,
          'div': numpy.divide,
          'norm': norm,
          'copy': lambda x: x,
          'none': lambda: None,
          }
