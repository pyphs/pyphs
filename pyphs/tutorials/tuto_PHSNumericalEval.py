# -*- coding: utf-8 -*-
"""
This is the tutorial 0 for pyphs.

Details can be found at: https://afalaize.github.io/pyphs/posts/phscore/

author: afalaize
date: 01. February 2017
"""

# Support for Python 2.x and Python 3.x
from __future__ import division, print_function, absolute_import

# retrieve the pyphs.PHSCore of a simple RLC from previous tutorial
from tuto_PHSCore import core

# load the pyphs.PHSNumericalEval class in the current namespace
from pyphs import PHSNumericalEval

# instantiate a pyphs.PHSNumericalEval object associated with a pyphs.PHSCore
evals = PHSNumericalEval(core)

# values for arguments
x = [5e-4, 2e-2]
dx = [5e-3, 2e-1]
w = [5e-3, ]
u = [1.5, ]

# collect all arguments
args = x + dx + w + u

# numerical evaluations
args_H = [args[i] for i in evals.H_inds]
H = evals.H(*args_H)
print('{}{}={}'.format('H', evals.H_args, H))

for name in ('dxH', 'dxHd', 'z', 'Jxx', 'Rxx'):
    func = getattr(evals, name)
    func_args = getattr(evals, name + '_args')
    func_inds = getattr(evals, name + '_inds')
    func_args_vals = [args[i] for i in func_inds]
    func_eval = func(*func_args_vals)
    print('\n{}{}=\n'.format(name, func_args), func_eval)
