#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 21:13:41 2017

@author: Falaize
"""

# Support for Python 2.x and Python 3.x
from __future__ import division

# import of external packages
import numpy                     # numerical tools
import matplotlib.pyplot as plt  # plot tools

# load the pyphs.PHSNumericalEval class in the current namespace
from pyphs import PHSSimulation

# retrieve the pyphs.PHSCore of a nonlinear RLC from the tutorial on PHSCore
from pyphs.tutorials.tuto_PHSCore import core

# Define the simulation parameters
config = {'fs': 48e3,               # Sample rate
          'gradient': 'theta',      # in {'discret', 'theta', 'trapez'}
          'theta': .5,              # theta-scheme for the structure
          'split': False,           # apply core.split_linear() beforehand
          'maxit': 10,              # Max number of iterations for NL solvers
          'numtol': 1e-16,          # Global numerical tolerance
          'path': None,             # Path to the folder to save the results
          'files_to_save': ('x', 'dx', 'dxH',
                            'w', 'z', 'y'),     # Select output files results
          'progressbar': True,      # Display a progress bar
          'timer': False            # Display minimal timing infos
          }

# Instantiate a pyphs.PHSSimulation object associated with a given core PHS
simu = PHSSimulation(core, config=config)

# def simulation time
tmax = 0.02
nmax = int(tmax*simu.nums.fs())
t = [n/simu.nums.fs() for n in range(nmax)]


# def input signal
def sig(t, mode='sin'):
    F = 1000.
    A = 1000.
    if mode == 'sin':
        out = A*numpy.sin(2*numpy.pi*F*t)
    elif mode == 'impact':
        dur = 0.5*1e-3
        start = 0.001
        out = A if start <= t < start + dur else 0.
    elif mode == 'none':
        out = 0.
    return numpy.array([out])


# def generator for sequence of inputs to feed in the PHSSimulation object
def sequ(mode='impact'):
    for tn in t:
        yield sig(tn, mode)

# Initialize the simulation
simu.init(sequ=sequ(), x0=(0., 0.), nt=len(t))

# Proceed
simu.process()

# The simulation results are stored in the simu.data object
t = simu.data.t()       # a generator of time value at each time step
x = simu.data.x()       # a generator of value for vector x at each time step
x1 = simu.data.x(0)     # a generator of value for scalar x component 1

t_list = list(t)
x_list = list(x)
x1_list = list(x1)

plt.figure()
plt.plot(t_list, x1_list)

plt.figure()
plt.plot([ex[0] for ex in x_list], [ex[1] for ex in x_list])

plt.figure()
simu.data.plot([('u', 0), ('x', 0), ('dtx', 0), ('y', 0)])

simu.data.plot_powerbal(mode='single')
