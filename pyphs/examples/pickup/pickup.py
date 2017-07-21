#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 24 23:01:21 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import os
from pyphs import Netlist, Graph

# ---------------------------  NETLIST  ------------------------------------- #
label = 'pickup'
this_script = os.path.realpath(__file__)
here = this_script[:this_script.rfind(os.sep)]
netlist_filename = here + os.sep + label + '.net'
netlist = Netlist(netlist_filename)

# ---------------------------  GRAPH  --------------------------------------- #
graph = Graph(netlist=netlist, label=label)

# ---------------------------  CORE  ---------------------------------------- #
core = graph.to_core()

## ---------------------------  SIMULATION  ---------------------------------- #
#if __name__ == '__main__':
#
#    import numpy
#    import matplotlib.pyplot as plt
#    from pyphs import Netlist, Graph
#    from pyphs.misc.tools import interleave
#
#    core.reduce_z()
#
#    # Define the simulation parameters
#    config = {'fs': 48e3,           # Sample rate (Hz)
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
#    def ordering(name, *args):
#        def get_index(e):
#            symb = simu.nums.method.symbols(e)
#            return getattr(simu.nums.method, name).index(symb)
#        return list(map(get_index, args))
#
#    order = ordering('y', 'yPMagnet', 'yOUT', 'yIN')
#
#    # def simulation time
#    tmax = .1
#    nmax = int(tmax*simu.config['fs'])
#    t = [n/simu.config['fs'] for n in range(nmax)]
#    nt = len(t)
#
#    # def input signal (impulse force)
#    def sig_impulse(tn):
#        # onset time
#        start = 10./config['fs']
#        # duration
#        dur = 0.5e-2
#        # amplitude
#        amp = 100.
#        return amp if start <= tn < start + dur else 0.
#
#    # def generator for sequence of inputs to feed in the Simulation object
#    def sequ():
#        """
#        generator of input sequence for Simulation
#        """
#        for un in signalgenerator(which='sin', tsig=tmax, fs=simu.config['fs'],
#                                  A=10, f0=100., ramp_on=True)():
#            # !!! must be array with shape (core.dims.u(), )
#            yield numpy.array(list(map(lambda i: [1., 0., un][i], order)))  # numpy.array([u1, u2, ...])
#
#    # Initialize the simulation
#    simu.init(u=sequ(), nt=nt)
#
#    # Proceed
#    simu.process()
#
#    plt.figure()
#    x_symbs = core.x
#    plots = ([('u', order[2]), ] +
#             interleave([('x', e) for e in map(core.x.index, x_symbs)],
#                        [('dtx', e) for e in map(core.x.index, x_symbs)]) +
#             [('y', order[1])])
#    simu.data.plot(plots)
#
#    plt.figure()
#    simu.data.plot([('x', i) for i in range(core.dims.x())])
#
#    plt.figure()
#    simu.data.plot_powerbal()
#    pass
