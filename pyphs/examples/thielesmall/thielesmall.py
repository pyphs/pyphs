#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 11:50:23 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import os
import sys
from pyphs import PHSNetlist, PHSGraph, PHSSimulation, signalgenerator
from pyphs.misc.signals.analysis import transferFunction
import matplotlib.pyplot as plt

label = 'thielesmall'
path = os.path.realpath(__file__)[:os.path.realpath(__file__).rfind(os.sep)]
netlist_filename = path + os.sep + label + '.net'
netlist = PHSNetlist(netlist_filename)

graph = PHSGraph(netlist=netlist)
core = graph.buildCore()

if __name__ == '__main__':

    # UNCOMMENT BELOW FOR SIMULATION and PLOT OF TRANSFER FUNCTION
    # !!! Very long simulation with numpy
    #config = {'fs': 48e3,
    #          'split': True,
    #          'progressbar': True,
    #          'timer': True,
    #          'language': 'c++'
    #          }
    #
    #simu = PHSSimulation(core, config=config)
    #
    #dur = 10.
    #u = signalgenerator(which='noise', tsig=dur, fs=simu.fs)
    #
    #
    #def sequ():
    #    for el in u():
    #        yield (el, )
    #
    #simu.init(sequ=sequ(), nt=int(dur*simu.fs))
    #
    #simu.process()
    #
    #u = list(simu.data.u(0))
    #y = list(simu.data.y(0))
    #
    #f, TF = transferFunction(y, u, fs=simu.fs, nfft=2**13, limits=(1e2, 1e4))
    #
    #plt.close('all')
    #plt.figure()
    #plt.loglog(f, TF)

    pass