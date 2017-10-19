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
from pyphs import signalgenerator
from pyphs.misc.juce import fx

label = 'triodeamp'

netlist_filename = label + '.net'

netlist = Netlist(netlist_filename)

graph = Graph(netlist=netlist)

core = graph.to_core(verbose=False)

core.substitute(selfall=True)

x0 = [-3.2523141568201306e-06, 4.32844950708445e-06]
w0 = [1.9024221182132122e-10,
      -8.772982340587987e-13,
      -3.252314156820131,
      -3.2522951325239204e-05,
      -8.647333958542062e-16,
      -3.2523141570103733,
      193.49539071065595]

#method = core.to_method()

# %% Find operating point (x0 and w0 used below)
# ----------------------------------------------------------------------------

#config = {'fs': 96e3,
#          'split': True,
#          'pbar': True,
#          'maxit': 100,
#          'eps': 1e-14,
#          'lang': 'python'
#          }
#
#
#simu = method.to_simulation(config=config)
#
#dur = .3
#
#u = signalgenerator(which='const', attack_ratio=0.1, f0=800.,
#                    tsig=dur, fs=simu.config['fs'], inits={'p':[0.5]})
#
#def sequ():
#    for el in u():
#        yield (0., 0., 200.*el)
#
#simu.init(u=sequ(), nt=int(dur*simu.config['fs']))
#
#simu.process()
#
##    simu.data.plot_powerbal(mode='multi')
#x0 = list(simu.data.x())[-1]
#w0 = list(simu.data.w())[-1]


# %% C++ simulation
# ----------------------------------------------------------------------------
#config = {'fs': 48e3,
#          'split': True,
#          'eps': 1e-9,
#          'lang': 'c++'
#          }
#
#simucpp = method.to_simulation(config=config, inits={'p':[0.5],
#                                                     'x': x0,
#                                                     'w': w0})
#
#dur = 0.01
#
#u = signalgenerator(which='sin', attack_ratio=1., f0=800.,
#                    tsig=dur, fs=simucpp.config['fs'])
#
#def sequ():
#    for el in u():
#        yield (0., 5*el, 200.)
#
#simucpp.init(u=sequ(), nt=int(dur*simucpp.config['fs']))
#
#simucpp.process()
#
#simucpp.data.plot(('u', 'y'))

#%% Bunch of files for Juce audio plugin
# ----------------------------------------------------------------------------

#path = os.getcwd()
#io = (['uin', ],    # inputs
#      ['yout', ])   # outputs
#inits = {'u': (0, 0, 200.),
#         'p':[0.5],
#         'x': x0,
#         'w': w0}
#fx.method2jucefx(method, path=path, io=io, inits=inits, config={'maxit':3})

