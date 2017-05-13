#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 11:50:23 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import os
from pyphs import (netlist2core, PHSSimulation, signalgenerator,
                   PHSNetlist, PHSGraph)


label = 'rlc'

path = os.path.realpath(__file__)[:os.path.realpath(__file__).rfind(os.sep)]

netlist_filename = path + os.sep + label + '.net'
netlist = PHSNetlist(netlist_filename)
graph = PHSGraph(netlist=netlist)
core = netlist2core(netlist_filename)

if __name__ == '__main__':
    # Define the simulation parameters
    config = {'fs': 48e3,               # Sample rate
              'grad': 'discret',    # in {'discret', 'theta', 'trapez'}
              'theta': 0.5,             # theta-scheme for the structure
              'split': True,           # apply core.split_linear() beforehand
              'maxit': 10,              # Max iteration for NL solvers
              'eps': 1e-16,          # Global numerical tolerance
              'path': None,             # Path to the results folder
              'pbar': True,      # Display a progress bar
              'timer': False,           # Display minimal timing infos
              'lang': 'python',     # in {'python', 'c++'}
              'script': None,  # compile and exec binary
              'eigen': None,       # path to Eigen library
              }

    simu = PHSSimulation(core, config=config)

    dur = 0.01
    u = signalgenerator(which='sin', f0=800., tsig=dur, fs=simu.fs)

    def sequ():
        for el in u():
            yield (el, )

    simu.init(sequ=sequ(), nt=int(dur*simu.fs))

    simu.process()

    simu.data.plot_powerbal(mode='multi')
