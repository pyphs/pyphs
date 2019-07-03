#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 11:50:23 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

from pyphs import Netlist

import os
import numpy as np

label = 'magnetic_circuit'

here = os.path.realpath(__file__)[:os.path.realpath(__file__).rfind(os.sep)]

netlist_filename = os.path.join(here, label + '.net')

netlist = Netlist(netlist_filename)

core = netlist.to_core()

# %% ------------------------------ SIMILATION ------------------------------ #

# UNCOMMENT BELOW FOR SIMULATION AND PLOTS

#if __name__ == '__main__':
#
#    from pyphs import Simulation, signalgenerator
#
#    # Include the linear dissipatives in the connexion structure
#    core.reduce_z()
#
#    # Define the simulation parameters
#    config = {'fs': 48e3,           # Sample rate
#              'lang': 'python',        # in {'python', 'c++'}
#              }
#
#    simu = Simulation(core.to_method(), config=config)
#
#    dur = 0.01
#    u = signalgenerator(which='sin', f0=800., tsig=dur, fs=simu.fs)
#
#    simu.init(u=u[:, np.newaxis])
#
#    # Run the simulation
#    simu.process()
#
#    # Plots
#    simu.data.plot_powerbal(mode='multi')
#    simu.data.plot(('u', 'x', 'y'))
