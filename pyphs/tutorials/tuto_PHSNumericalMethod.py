# -*- coding: utf-8 -*-
"""
This is a tutorial for pyphs.

Details can be found at: https://afalaize.github.io/pyphs/posts/phscore/

Created on Wed Feb  1 22:39:19 2017

@author: Falaize
"""

# Support for Python 2.x and Python 3.x
from __future__ import division, print_function, absolute_import

# import of external packages
import numpy  # numerical tools
import matplotlib.pyplot as plt  # plot tools

# load the pyphs.PHSNumericalEval class in the current namespace
from pyphs import PHSCore, PHSNumericalMethod, PHSNumericalCore

# instantiate a pyphs.PHSCore object
core = PHSCore()

xL, L = core.symbols(['xL', 'L'])   # define sympy symbols
HL = xL**2/(2*L)                    # define sympy expression
core.add_storages(xL, HL)           # add storage function to the `core` object

xC, C = core.symbols(['xC', 'C'])   # define sympy symbols
HC = xC**2/(2*C)                    # define sympy expression
core.add_storages(xC, HC)           # add storage function to the `core` object

# Set the skew-symetric structure
Jxx = numpy.array([[0., -1.],
                   [1., 0.]])
core.set_Jxx(Jxx)

# Physical parameters
F0 = 100.
L_value = 5e-1     # 500mH
# f0 = (2*pi*sqrt(L*C))**-1
C_value = (2*numpy.pi*F0)**-2/L_value  # ?F

# Dictionary with core.symbols as keys and parameters value as values
subs = {L: L_value,
        C: C_value}
core.subs.update(subs)

core.split_linear()
# instantiate a pyphs.PHSNumericalEval object associated with a pyphs.PHSCore
method = PHSNumericalMethod(core)

# Explicit Euler update:
# dx = Mxx*dxH(x) + Mxy*u
# x = x + dx

# Mxx * dxH
op_MxxDotdxH = method.operation('dot', ('Mxx', 'dxH'))

# Mxy * u
op_MxyDotU = method.operation('dot', ('Mxy', 'u'))

# Mxx * dxH + Mxy * u
op_MxxDotX_add_MxyDotU = method.operation('add', (op_MxxDotdxH, op_MxyDotU))

# dx = (Mxx * dxH + Mxy * u)/fs
op_update_dx = method.operation('div', (op_MxxDotX_add_MxyDotU, 'fs'))
method.setoperation('ud_dx', op_update_dx)

# x += dx
op_update_x = method.operation('add', ('x', 'dx'))
method.setoperation('ud_x', op_update_x)

# clear standard update:
method.update_actions = list()

# Explicit Euler update:
method.set_execaction([('x', 'ud_x'),       # x = x + dx
                       'dxH',               # update dxH
                       ('dx', 'ud_dx'),     # dx = Mxx*dxH(x) + Mxy*u
                       'y',                 # update y
                       'H'                  # update H
                       ])

#%%
method.build_struc()
nums = PHSNumericalCore(method, build=False)
nums.build()


def sig(t, mode='sin'):
    F = 100.
    if mode == 'sin':
        out = numpy.sin(2*numpy.pi*F*t)
    elif mode == 'impact':
        dur = 1e-3
        start = 0.005
        out = 1. if start <= t < start + dur else 0.
    elif mode == 'none':
        out = 0.
    return numpy.array([out])

# init x = x0
x0 = numpy.array([0.1, 0])
nums.set_x(x0)

# init lists for results
results_names = ['u', 'x', 'y', 'H']


class Results:
    def __init__(self):
        self.t = list()
        self.names = list()
        for name in results_names:
            setattr(self, name, list())
            self.names.append(name)

    def liststoarrays(self):
        for name in self.names:
            l = getattr(self, name)
            setattr(self, name, numpy.array(l))

    def plot(self, name, index=0, start=None, stop=None):
        if start is None:
            start = 0
        if stop is None:
            stop = len(self.t)
        try:
            values = getattr(self, name)[start:stop, index]
        except IndexError:
            values = getattr(self, name)[start:stop]

        plt.figure()
        plt.plot(self.t[start:stop], values)
        plt.title(name)
        plt.ylabel('${}({})$'.format(name, index))
        plt.xlabel('$t$ (s)')


results = Results()

# def simulation time
tmax = 0.2
nmax = int(tmax*nums.fs())
t = [n/nums.fs() for n in range(nmax)]

# simulation
for tn in t:

    # update
    nums.update()

    # store results
    results.t.append(tn)
    for name in results_names:
        ts = getattr(results, name)
        res = getattr(nums, name)()
        ts.append(res)

# transform time series from lists to numpy arrays:
results.liststoarrays()

# %%

results.plot('x', 0)
results.plot('x', 1)
results.plot('H')
plt.figure()
plt.plot(results.x[:, 0], results.x[:, 1], ':.')
plt.plot(results.x[-1, 0], results.x[-1, 1], 'or')
plt.plot(x0[0], x0[1], 'og')