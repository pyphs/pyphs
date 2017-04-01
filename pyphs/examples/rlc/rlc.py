#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 11:50:23 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import os
import sys
from pyphs import netlist2core, PHSSimulation, signalgenerator, PHSNetlist, PHSGraph



label = 'rlc'

try:
    os.chdir(os.path.dirname(sys.argv[0]))
    path = os.getcwd() + os.sep
except OSError:
    path = r''

netlist_filename = path + label + '.net'
netlist = PHSNetlist(netlist_filename)
graph = PHSGraph(netlist=netlist)
core = netlist2core(netlist_filename)

core.build_R()

# Define the simulation parameters
config = {'fs': 48e3,               # Sample rate
          'gradient': 'discret',    # in {'discret', 'theta', 'trapez'}
          'theta': 0.5,             # theta-scheme for the structure
          'split': False,           # apply core.split_linear() beforehand
          'maxit': 10,              # Max number of iterations for NL solvers
          'numtol': 1e-16,          # Global numerical tolerance
          'path': None,             # Path to the folder to save the results
          'progressbar': True,      # Display a progress bar
          'timer': False,           # Display minimal timing infos
          'language': 'python',     # in {'python', 'c++'}
          'cpp_build_and_run_script': None,  # call to compiler and exec binary
          'eigen_path': None,       # path to Eigen C++ linear algebra library
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



