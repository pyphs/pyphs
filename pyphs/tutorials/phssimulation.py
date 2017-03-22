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


# Define the simulation parameters
config = {'fs': 48e3,               # Sample rate
          'gradient': 'discret',    # in {'discret', 'theta', 'trapez'}
          'theta': 0.5,             # theta-scheme for the structure
          'split': False,           # apply core.split_linear() beforehand
          'maxit': 10,              # Max number of iterations for NL solvers
          'numtol': 1e-16,          # Global numerical tolerance
          'path': None,             # Path to the folder to save the results
          'progressbar': False,     # Display a progress bar
          'timer': False,           # Display minimal timing infos
          'language': 'python',     # in {'python', 'c++'}
          'cpp_build_and_run_script': None,  # call to compiler and exec binary
          'eigen_path': 'None',     # path to Eigen C++ linear algebra library
          }

# Instantiate a pyphs.PHSSimulation object associated with a given core PHS
simu = PHSSimulation(core, config=config)

# def simulation time
tmax = 0.02
nmax = int(tmax*simu.fs)
t = [n/simu.fs for n in range(nmax)]
nt = len(t)


# def input signal
def sig(t, mode='impact'):
    freq = 1000.
    amp = 1000.
    if mode == 'sin':
        pi = numpy.pi
        out = amp * numpy.sin(2*pi*freq*t)
    elif mode == 'impact':
        dur = 0.5*1e-3
        start = 0.001
        out = amp if start <= t < start + dur else 0.
    elif mode == 'zero':
        out = 0.
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
# !!! must be array with shape (core.dims.x(), )
x0 = (0., 0.)

# Initialize the simulation
simu.init(sequ=sequ(), x0=x0, nt=nt)

# Proceed
simu.process()

# The simulation results are stored on disk, and read with the simu.data object
t = simu.data.t()       # a generator of time value at each time step
x = simu.data.x()       # a generator of value for vector x at each time step
x1 = simu.data.x(0)     # a generator of value for scalar x component 1

# recover data as lists
t_list = list(t)
x_list = list(x)
x1_list = list(x1)

# plot x_L(t)
plt.figure()
plt.plot(t_list, x1_list)
plt.show()

# phase plot
plt.figure()
plt.plot([ex[0] for ex in x_list], [ex[1] for ex in x_list])
plt.show()

# plot of several signals with the simu.data object
plt.figure()
simu.data.plot([('u', 0), ('x', 0), ('x', 1), ('dtx', 0), ('y', 0)])

# power balance
simu.data.plot_powerbal()
