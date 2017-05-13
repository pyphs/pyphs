#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 11:50:23 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import os
import numpy
import matplotlib.pyplot as plt
from pyphs import PHSSimulation, PHSNetlist, PHSGraph


# ---------------------------  NETLIST  ------------------------------------- #
label = 'rhodes'
this_script = os.path.realpath(__file__)
here = this_script[:this_script.rfind(os.sep)]
netlist_filename = here + os.sep + label + '.net'
netlist = PHSNetlist(netlist_filename)

# ---------------------------  GRAPH  --------------------------------------- #
graph = PHSGraph(netlist=netlist)

# ---------------------------  CORE  ---------------------------------------- #
core = graph.buildCore()

# ---------------------------  SIMULATION  ---------------------------------- #
if __name__ == '__main__':

    core.build_R()

    # Define the simulation parameters
    config = {'fs': 48e3,           # Sample rate (Hz)
              'grad': 'discret',    # In {'discret', 'theta', 'trapez'}
              'theta': 0.,          # Theta-scheme for the structure
              'split': True,       # split implicit from explicit part
              'maxit': 10,          # Max number of iterations for NL solvers
              'eps': 1e-16,         # Global numerical tolerance
              'path': None,         # Path to the results folder
              'pbar': True,         # Display a progress bar
              'timer': False,       # Display minimal timing infos
              'lang': 'c++',        # Language in {'python', 'c++'}
              'script': None,       # Call to C++ compiler and exec binary
              'eigen': None,        # Path to Eigen C++ library
              # Options for the data reader. The data are read from index imin
              # to index imax, rendering one element out of the number decim
              'load': {'imin': None,
                       'imax': None,
                       'decim': None}
              }

    # Instanciate PHSSimulation class
    simu = PHSSimulation(core, config=config)

    # def simulation time
    tmax = .5
    nmax = int(tmax*simu.fs)
    t = [n/simu.fs for n in range(nmax)]
    nt = len(t)

    # def input signal (impulse force)
    def sig_impulse(tn):
        # onset time
        start = 10./config['fs']
        # duration
        dur = 1e-2
        # amplitude
        amp = 100.
        return amp if start <= tn < start + dur else 0.

    # def generator for sequence of inputs to feed in the PHSSimulation object
    def sequ():
        """
        generator of input sequence for PHSSimulation
        """
        for tn in t:
            u1 = sig_impulse(tn)

            # !!! must be array with shape (core.dims.u(), )
            yield numpy.array([u1, ])  # numpy.array([u1, u2, ...])

    # state initialization
    # !!! must be array with shape (core.dims.x(), )
    x0 = numpy.array([0., ]*core.dims.x())
    core_simu = simu.nums.method.core
    x0[core_simu.x.index(core.symbols('qfelt'))] = -0.05

    # Initialize the simulation
    simu.init(sequ=sequ(), x0=x0, nt=nt)

    # Proceed
    simu.process()

    plt.figure()
    x_symbs = core.symbols(['qfelt'])
    plots = ([('u', 0), ] +
             [('y', 0)] +
             [('x', e) for e in map(core.x.index, x_symbs)])
    load = {'imin': 0, 'imax': 1500, 'decim': 1}
    simu.data.plot(plots, load=load)

    plt.figure()
    simu.data.plot([('x', i) for i in range(core.dims.x())])

    plt.figure()
    simu.data.plot_powerbal()
