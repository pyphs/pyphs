#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 11:50:23 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import os
from pyphs import Netlist, Graph

# ---------------------------  NETLIST  ------------------------------------- #
label = 'beam_cantilever'
this_script = os.path.realpath(__file__)
here = this_script[:this_script.rfind(os.sep)]
netlist_filename = here + os.sep + label + '.net'
netlist = Netlist(netlist_filename)

# ---------------------------  GRAPH  --------------------------------------- #
graph = Graph(netlist=netlist)

# ---------------------------  CORE  ---------------------------------------- #
core = graph.to_core()
core.reduce_z()
core.substitute(selfall=True)

#if __name__ is "__main__":
#    # ---------------------------  SIMULATION  ------------------------------#
#    from pyphs import Simulation, Netlist, Graph
#    from pyphs.misc.signals.waves import wavread
#    import matplotlib.pyplot as plt
#    import numpy
#    # recover normalized hammer force from wave file
#    fs, hammer_force = wavread(os.path.join(here, 'hammer_force.wav'))
#
#    # Define the simulation parameters
#    config = {'fs': fs,           # Sample rate (Hz)
#              'grad': 'discret',    # In {'discret', 'theta', 'trapez'}
#              'theta': 0.,          # Theta-scheme for the structure
#              'split': True,       # split implicit from explicit part
#              'maxit': 10,          # Max number of iterations for NL solvers
#              'eps': 1e-16,         # Global numerical tolerance
#              'path': None,         # Path to the results folder
#              'pbar': True,         # Display a progress bar
#              'timer': False,       # Display minimal timing infos
#              'lang': 'c++',        # Language in {'python', 'c++'}
#              # Options for the data reader. The data are read from index imin
#              # to index imax, rendering one element out of the number decim
#              'load': {'imin': None,
#                       'imax': None,
#                       'decim': None}
#              }
#
#    # Instanciate Simulation class
#    simu = Simulation(core.to_method(), config=config)
#
#    def ordering(name, *args):
#        def get_index(e):
#            symb = simu.nums.method.symbols(e)
#            return getattr(simu.nums.method, name).index(symb)
#        return list(map(get_index, args))
#
#    order = ordering('y', 'yIN', 'yOUT')
#    # def simulation time
#    nmax = len(hammer_force)
#    t = [n/simu.config['fs'] for n in range(nmax)]
#    nt = len(t)
#    sig = list()
#
#    # ---------------------------  LOOP  --------------------------------
#
#    # Custom force amplitude
#    AmpForce = 20.
#    hammer_force = numpy.array(hammer_force)*AmpForce
#
#
#    # def generator for sequence of inputs to feed in the Simulation object
#    def sequ():
#        """
#        generator of input sequence for Simulation
#        """
#        for i, tn in enumerate(t):
#            # numpy.array([u1, u2, ...])
#            yield numpy.array([(hammer_force[i], 0.)[j] for j in order])
#
#    # state initialization
#    # !!! must be array with shape (core.dims.x(), )
#    x0 = numpy.array([0., ]*core.dims.x())
#
#    # Initialize the simulation
#    simu.init(u=sequ(), x0=x0, nt=nt)
#
#    # Proceed
#    simu.process()
#
#    y = list(simu.data.y(order[1]))
#    iy = -numpy.cumsum(y)
#    plt.plot(iy)
