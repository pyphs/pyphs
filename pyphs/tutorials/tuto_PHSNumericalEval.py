# -*- coding: utf-8 -*-
"""
This is a tutorial for pyphs about the numerical evaluation
of a given core PHS structure
Details can be found at: https://afalaize.github.io/pyphs/

author: afalaize
date: 28 February 2017
"""

# Support for Python 2.x and Python 3.x
from __future__ import division, print_function, absolute_import

# retrieve the pyphs.PHSCore of a simple RLC from the previous tutorial
from pyphs.tutorials.tuto_PHSCore import core

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

# retrieve values for arguments of the Hamiltonian function
args_H = [args[i] for i in evals.H_inds]

# numerical evaluations of the Hamiltonian function
H = evals.H(*args_H)

# print "H(xL, xC) = 3947.84176069"
print('{}{} = {}'.format('H', evals.H_args, H))

# Same as above for a list of PHScore expressions and matrices
for name in ('dxH', 'z', 'Jxx', 'Rxx'):

    # retrieve the function to evaluate
    func = getattr(evals, name)

    # retrieve the ordered list of symbols for arguments
    func_args = getattr(evals, name + '_args')

    # retrieve the indices of symbols for arguments in the global args vector
    func_inds = getattr(evals, name + '_inds')

    # retrieve the values for arguments
    func_args_vals = [args[i] for i in func_inds]

    # evaluate the function with arguments values
    func_eval = func(*func_args_vals)

    # print e.g. "z() = "
    print('\n{}{} = \n'.format(name, func_args), func_eval)


# Notice function are vectorized:
x1, x2 = range(0, 3), range(4, 7)
print("\nVectorized (not parallel) evaluation:\nx1={}, x2={}".format(x1, x2))
print("H(x1, x2)={}".format(evals.H(x1, x2)))
