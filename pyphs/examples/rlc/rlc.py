#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 11:50:23 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import os
import pyphs as phs

label = 'rlc'

here = os.path.realpath(__file__)[:os.path.realpath(__file__).rfind(os.sep)]

netlist_filename = os.path.join(here, label + '.net')

netlist = phs.Netlist(netlist_filename)
core = netlist.to_core()


#if __name__ == '__main__':
#
#    from pyphs import signalgenerator
#    import shutil
#    import numpy as np
#    import sympy as sp
#
#    # Include the linear dissipatives in the connexion structure
#    core.reduce_z()
#
#    # Define the simulation parameters
#    config = {'fs': 48e3,               # Sample rate
#              'grad': 'theta',    # in {'discret', 'theta', 'trapez'}
#              'theta': 0.5,             # theta-scheme for the structure
#              'split': True,           # apply core.split_linear() beforehand
#              'maxit': 10,              # Max iteration for NL solvers
#              'eps': 1e-30,          # Global numerical tolerance
#              'path': None,             # Path to the results folder
#              'pbar': True,      # Display a progress bar
#              'timer': False,           # Display minimal timing infos
#              'lang': 'c++',     # in {'python', 'c++'}
#              'theano': False
#              }
#    # Define initialization values
#    x0 = np.zeros(core.dims.x())
#    x0[0] = 1
#    x0_expr = list(map(sp.sympify, x0))
#    inits = {'x': x0_expr}
#    simu = core.to_simulation(config=config)
#
#    dur = 0.01
#    u = signalgenerator(which='sin', f0=800., tsig=dur, fs=simu.config['fs'])
#
#    def sequ():
#        for el in u():
#            yield (el, )
#
#    simu.init(u=sequ(), nt=int(dur*simu.config['fs']))
#
#    # Run the simulation
#    simu.process()
#
#    simu.data.plot([('x', 0)])
#
#    # Plots
#    simu.data.plot_powerbal(mode='single')
#    simu.data.plot(['u', 'x', 'y'])
#
#    # clean: delete folders 'data' and 'figures'
#    shutil.rmtree(os.path.join(here, 'data'))
#    shutil.rmtree(os.path.join(here, 'figures'))
#
#    # clean: delete folder 'rlc'
#    if config['lang'] == 'c++':
#        shutil.rmtree(os.path.join(here, 'rlc'))
