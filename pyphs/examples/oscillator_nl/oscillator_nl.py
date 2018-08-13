#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 11:50:23 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import os
from pyphs import Netlist, Graph
import  matplotlib.pyplot as plt

label = 'oscillator_nl'
path = os.path.realpath(__file__)[:os.path.realpath(__file__).rfind(os.sep)]
netlist_filename = path + os.sep + label + '.net'
netlist = Netlist(netlist_filename)
graph = Graph(netlist=netlist)
core = graph.to_core()

# %% ------------------------------ SIMULATION ------------------------------ #

# UNCOMMENT BELOW FOR SIMULATION AND PLOTS

#if __name__ == '__main__':
#
#    from pyphs import Simulation, signalgenerator
#    import numpy as np
#
#    tsig = 0.05
#    fs = 48000.
#
#    config = {'fs': 48e3,
#              'pbar': True,
#              'lang': 'c++'
#              }
#    simu = Simulation(core.to_method(), config)
#
#    u = signalgenerator(which='sin', f0=500., A=200., tsig=tsig, fs=fs)
#
#    simu.init(u=u[:, np.newaxis], inits={'x': [1e-2, 0.]})
#
#    simu.process()
#
#    simu.data.plot_powerbal(mode='multi')
#
#    x1 = simu.data['x',: , 0]
#    x2 = simu.data['x',: , 1]
#
#    plt.figure()
#    plt.plot(x1, x2, ':o')
#    plt.xlabel(r'$x(t)$')
#    plt.ylabel(r'$\dot x(t)$')
#    plt.grid('on')
