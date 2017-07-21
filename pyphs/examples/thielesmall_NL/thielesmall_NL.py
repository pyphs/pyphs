#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 11:50:23 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import os
from pyphs import Netlist, Graph

label = 'thielesmall_NL'
path = os.path.realpath(__file__)[:os.path.realpath(__file__).rfind(os.sep)]
netlist_filename = path + os.sep + label + '.net'
netlist = Netlist(netlist_filename)

graph = Graph(netlist=netlist)
core = graph.to_core()

#    # UNCOMMENT BELOW FOR SIMULATION and PLOT OF TRANSFER FUNCTION
#if __name__ == '__main__':
#
#    from pyphs import Simulation, signalgenerator
#    from pyphs.misc.signals.analysis import transferFunction
#    import matplotlib.pyplot as plt
#
#    # !!! Very long simulation with numpy
#    config = {'fs': 48e3,
#              'split': True,
#              'pbar': True,
#              'timer': True,
#              'lang': 'c++'
#              }
#    core.subsinverse()
#    simu = Simulation(core.to_method(), config=config)
#
#    dur = 10.
#    u = signalgenerator(which='noise', tsig=dur, fs=config['fs'])
#
#    def sequ():
#        for el in u():
#            yield (el, )
#
#    simu.init(u=sequ(), nt=int(dur*config['fs']))
#
#    simu.process()
#
#    u = list(simu.data.u(0))
#    y = list(simu.data.y(0))
#
#    f, TF = transferFunction(y, u, fs=config['fs'],
#                             nfft=2**15, limits=(1e1, 5e3))
#
#    plt.close('all')
#    plt.figure()
#    plt.semilogx(f, TF)
#
#    pass
