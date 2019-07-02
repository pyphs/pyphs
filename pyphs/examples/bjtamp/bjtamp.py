#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 11:50:23 2017

Here, we build the  core asssociated with the

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import os
from pyphs import Netlist


# def netlist file name
label = 'bjtamp'
here = os.path.realpath(__file__)[:os.path.realpath(__file__).rfind(os.sep)]
netlist_filename = here + os.sep + label + '.net'

# read netlist
netlist = Netlist(netlist_filename)

# build core
core = netlist.to_core()

# reduce linear dissipative part
core.reduce_z()

# %% ------------------------------ SIMULATION ------------------------------ #

# UNCOMMENT BELOW FOR SIMULATION AND PLOTS

# if __name__ == '__main__':
#
#    from pyphs import signalgenerator, Simulation
#    import numpy
#
#    config = {'fs': 48e3,
#              'lang': 'python'}
#
#    simu = Simulation(core.to_method(), config=config)
#
#    dur = 0.01
#
#    A = 1e-3
#    Vcc = 9.
#    uIN = signalgenerator(which='sin', A=A, f0=800., tsig=dur, fs=simu.fs)
#    uVCC = signalgenerator(which='const', A=Vcc, tsig=dur, fs=simu.fs)
#    uOUT = signalgenerator(which='zero', tsig=dur, fs=simu.fs)
#
#    u = numpy.vstack((uOUT, uIN, uVCC)).T
#    simu.init(u=u)
#
#    simu.process()
#
#    simu.data.plot_powerbal(mode='multi')
