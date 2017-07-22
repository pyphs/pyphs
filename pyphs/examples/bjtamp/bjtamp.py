#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 11:50:23 2017

Here, we build the  core asssociated with the

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import os
from pyphs import Netlist, Graph


label = 'bjtamp'

path = os.path.realpath(__file__)[:os.path.realpath(__file__).rfind(os.sep)]

netlist_filename = path + os.sep + label + '.net'

netlist = Netlist(netlist_filename)

graph = Graph(netlist=netlist)

core = graph.to_core()

core.reduce_z()

#if __name__ == '__main__':
#
#    from pyphs import signalgenerator, Simulation
#    config = {'fs': 48e3,
#              'split': True,
#              'progressbar': True,
#              'timer': True,
#              }
#
#    simu = Simulation(core.to_method(), config=config)
#
#    dur = 0.01
#
#    u = signalgenerator(which='sin', f0=800., tsig=dur, fs=simu.config['fs'])
#
#    def sequ():
#        for el in u():
#            yield (0, 1e-3*el, 9.)
#
#    simu.init(u=sequ(), nt=int(dur*simu.config['fs']))
#
#    simu.process()
#
#    simu.data.plot_powerbal(mode='multi')
#    pass
