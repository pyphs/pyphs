#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 11:50:23 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import os
from pyphs import (netlist2core, PHSSimulation, signalgenerator)
import shutil

label = 'rlc'

here = os.path.realpath(__file__)[:os.path.realpath(__file__).rfind(os.sep)]

netlist_filename = os.path.join(here, label + '.net')
core = netlist2core(netlist_filename)
simu = PHSSimulation(core)

if  __name__ == '__main__':
    # Define the simulation parameters
    core.build_R()

    config = {'fs': 48e3,               # Sample rate
              'grad': 'discret',    # in {'discret', 'theta', 'trapez'}
              'theta': .5,             # theta-scheme for the structure
              'split': True,           # apply core.split_linear() beforehand
              'maxit': 10,              # Max iteration for NL solvers
              'eps': 1e-16,          # Global numerical tolerance
              'path': None,             # Path to the results folder
              'pbar': False,      # Display a progress bar
              'timer': False,           # Display minimal timing infos
              'lang': 'c++',     # in {'python', 'c++'}
#              'script': None,  # compile and exec binary
#              'eigen': None,       # path to Eigen library
              }

    simu = PHSSimulation(core, config=config)

    dur = 0.01
    u = signalgenerator(which='sin', f0=800., tsig=dur, fs=simu.config['fs'])

    def sequ():
        for el in u():
            yield (el, )

    simu.init(sequ=sequ(), nt=int(dur*simu.config['fs']))

    simu.process()

    simu.data.plot_powerbal(mode='multi')

    # clean: delete folders 'data' and 'figures'
    shutil.rmtree(os.path.join(here, 'data'))
    shutil.rmtree(os.path.join(here, 'figures'))
    pass
