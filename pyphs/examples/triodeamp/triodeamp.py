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


label = 'triodeamp'

path = os.path.realpath(__file__)[:os.path.realpath(__file__).rfind(os.sep)]

netlist_filename = path + os.sep + label + '.net'

netlist = Netlist(netlist_filename)

graph = Graph(netlist=netlist)

core = graph.to_core(verbose=False)
core.linear_nonlinear()
core.subsinverse()

#core.reduce_z()

#if __name__ == '__main__':
#
#    from pyphs import signalgenerator
#
#    config = {'fs': 96e3,
#              'split': True,
#              'pbar': True,
#              'maxit': 100,
#              'eps': 1e-9,
#              'lang': 'python'
#              }
#
#    method = core.to_method()
#    simu = method.to_simulation(config=config)
#
#    dur = 0.3
#
#    u = signalgenerator(which='const', attack_ratio=0.1, f0=800.,
#                        tsig=dur, fs=simu.config['fs'], inits={'p':[0.5]})
#
#    def sequ():
#        for el in u():
#            yield (0., 0., 200.*el)
#
#    simu.init(u=sequ(), nt=int(dur*simu.config['fs']))
#
#    simu.process()
#
##    simu.data.plot_powerbal(mode='multi')
#    x0 = list(simu.data.x())[-1]
#    w0 = list(simu.data.w())[-1]
#
## %%
#
#    config = {'fs': 96e3,
#              'split': True,
#              'eps': 1e-9,
#              'lang': 'c++'
#              }
#
#    simucpp = method.to_simulation(config=config, inits={'p':[0.5],
#                                                         'x': x0,
#                                                         'w': w0})
#
#    dur = 0.01
#
#    u = signalgenerator(which='sin', attack_ratio=1., f0=800.,
#                        tsig=dur, fs=simu.config['fs'])
#
#    def sequ():
#        for el in u():
#            yield (0., 5*el, 200.)
#
#    simucpp.init(u=sequ(), nt=int(dur*simu.config['fs']))
#
#    simucpp.process()
#
#    simucpp.data.plot(('u', 'y'))
