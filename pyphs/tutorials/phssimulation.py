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
from pyphs.tutorials.phscore import core

core.build_R()

# Define the simulation parameters
config = {'fs': 48e3,           # Sample rate (Hz)
          'grad': 'discret',    # In {'discret', 'theta', 'trapez'}
          'theta': 0.5,         # Theta-scheme for the structure
          'split': False,       # split implicit from explicit part
          'maxit': 10,          # Max number of iterations for NL solvers
          'eps': 1e-16,         # Global numerical tolerance
          'path': None,         # Path to the results folder
          'pbar': True,         # Display a progress bar
          'timer': False,       # Display minimal timing infos
          'lang': 'python',     # Language in {'python', 'c++'}
#          'script': None,       # Call to C++ compiler and exec binary
#          'eigen': None,        # Path to Eigen C++ library
          # Options for the data reader. The data are read from index imin
          # to index imax, rendering one element out of the number decim
          'load': {'imin': 0, 'imax': None, 'decim': 1}
          }

# Instantiate a pyphs.PHSSimulation object associated with a given core PHS
simu = PHSSimulation(core, config=config)

# def simulation time
tmax = 1e-2
nmax = int(tmax*simu.fs)
t = [n/simu.fs for n in range(nmax)]
nt = len(t)

# def input signal
def sig(tn, mode='sin'):
    freq = 300.
    amp = 1000.
    if mode == 'sin':
        pi = numpy.pi
        sin = numpy.sin
        out = amp * sin(2*pi*freq*tn)
    elif mode == 'impact':
        dur = 2*1e-3  # duration
        start = 10/config['fs']   # start at 1ms
        out = -amp if start <= tn < start + dur else 0.
    elif mode == 'const':
        out = 1.
    return out


# def generator for sequence of inputs to feed in the PHSSimulation object
def sequ():
    """
    generator of input sequence for PHSSimulation
    """
    for tn in t:
        u1 = sig(tn)

        # !!! must be array with shape (core.dims.u(), )
        yield numpy.array([u1, ])  # numpy.array([u1, u2, ...])

# state initialization
# !!! must be numpy array with shape (core.dims.x(), )
x0 = numpy.array([0., ]*core.dims.x())

# Initialize the simulation
simu.init(sequ=sequ(), x0=x0, nt=nt,
          config={'load': {'imin': 0, 'imax': None, 'decim': 1}})
# Proceed
simu.process()

# The simulation results are stored on disk,
# and read with the simu.data object
t = simu.data.t()       # generator of time vector values
x = simu.data.x()       # generator of vector x values at each time step
x1 = simu.data.x(0)     # generator of value for scalar x component 1

# recover data as lists
t_list = list(t)
x_list = list(x)
x1_list = list(x1)

# plot x_L(t)
plt.figure(1)
plt.plot(t_list, x1_list)
plt.show()

# phase plot
plt.figure(2)
plt.plot([ex[0] for ex in x_list], [ex[1] for ex in x_list])
plt.show()

# plot of several signals with the simu.data object
plt.figure(3)
x_symbs = core.symbols(['xL', 'xC'])
simu.data.plot([('u', 0), ] +
               [('x', e) for e in map(core.x.index, x_symbs)] +
               [('y', 0)],
               load={'imin': None,
                     'imax': 500,
                     'decim': None})

plt.figure(4)
simu.data.plot([('u', 0), ] +
               [('x', i) for i in range(core.dims.x())])

# power balance
plt.figure(5)
simu.data.plot_powerbal()
simu.data.plot([('u', 0), ] +
               [('x', e) for e in map(core.x.index, x_symbs)])

plt.show()
