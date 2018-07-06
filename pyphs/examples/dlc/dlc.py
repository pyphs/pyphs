#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 11:50:23 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import os
from pyphs import Netlist

# netlist is "{label}.net"
label = 'dlc'

# get folder path
path = os.path.realpath(__file__)[:os.path.realpath(__file__).rfind(os.sep)]

# def filename
netlist_filename = os.path.join(path, '{0}.net'.format(label))

# read in Netlist object
netlist = Netlist(netlist_filename)

# Build Graph object
graph = netlist.to_graph()

# Build Core object
core = graph.to_core()


#if __name__ == '__main__':
#
#    from pyphs import Simulation, signalgenerator
#    import numpy as np
#
#    tsig = 0.01
#    fs = 48000.
#
#    config = {'fs': 48e3,
#              'progressbar': True,
#              }
#    simu = Simulation(core.to_method(), config)
#
#    sig = signalgenerator(which='sin', f0=500., A=200., tsig=tsig, fs=fs)
#
#    def sequ():
#        for u in sig():
#            yield np.array([u, ])
#
#    nt = int(fs*tsig)
#    simu.init(u=sequ(), nt=nt)
#
#    simu.process()
#
#    simu.data.plot_powerbal()
#    pass
