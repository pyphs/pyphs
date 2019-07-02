#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 11:50:23 2017

@author: Falaize

This script run the simulation of an Euler-Bernouilli cantilever beam.


"""

from __future__ import absolute_import, division, print_function

import os
from pyphs import Netlist

# ----------------------------  NETLIST  ------------------------------------ #
label = 'beam_cantilever'

# define absolute path to netlist
here = os.path.realpath(__file__)[:os.path.realpath(__file__).rfind(os.sep)]
netlist_filename = os.path.join(here, label + '.net')

# read netlist from file
netlist = Netlist(netlist_filename)

# ------------------------------  CORE  ------------------------------------- #
# build Core object
core = netlist.to_core()


# %% ------------------------------ SIMULATION ------------------------------ #

# UNCOMMENT BELOW FOR SIMULATION AND PLOTS

# if __name__ == "__main__":
#
#    from pyphs import Simulation, Netlist, Graph, signalgenerator
#    from pyphs.misc.tools import ordering
#    import numpy
#
#    # recover normalized hammer force from wave file
#    fs = 44e3
#    tdeb = 0.01
#    tend = 0.989
#    tsig = 0.0001
#    AmpForce = 1e-3
#    T = tdeb + tend + tsig
#
#    # Define the simulation parameters
#    config = {'fs': fs,           # Sample rate (Hz)
#              'pbar': True,         # Display a progress bar
#              'lang': 'c++',        # Language in {'python', 'c++'}
#              }
#
#    # Instanciate Simulation class
#    simu = Simulation(core.to_method(), config=config)
#
#    # get proper ordering of outputs
#    order = ordering(simu.method, 'y', ('yIN', 'yOUT'))
#
#    # def inputs to feed in the Simulation object
#    hammer_force = signalgenerator(which='const', fs=fs, A=AmpForce,
#                                   tsig=tsig, tend=tend, tdeb=tdeb)
#    zeros = signalgenerator(which='zero', fs=fs, tsig=T)
#    sequ = numpy.vstack((hammer_force, zeros)).T[:, order]
#
#    # ---------------------------  LOOP  --------------------------------
#
#    # state initialization
#    # !!! must be array with shape (core.dims.x(), )
#    x0 = [0., ]*core.dims.x()
#
#    # Initialize the simulation
#    simu.init(u=sequ, inits={'x': x0})
#
#    # Proceed
#    simu.process()
#
#    # Plot
#    simu.data.plot('x')
#
#    # write wave
#    simu.data.wavwrite('y', order[1])
