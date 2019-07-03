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

# Build Core object
core = netlist.to_core()


# %% ------------------------------ SIMULATION ------------------------------ #

# UNCOMMENT BELOW FOR SIMULATION AND PLOTS

# if __name__ == '__main__':
#
#    from pyphs import signalgenerator
#    import numpy as np
#
#    tsig = 0.01
#    fs = 192000.
#
#    config = {'fs': 48e3,
#              'lang': 'python'}
#
#    simu = core.to_simulation(config=config)
#
#    sig = signalgenerator(which='sin', f0=500., A=1., tsig=tsig, fs=fs)
#    u = sig[:, np.newaxis]
#
#    nt = int(fs*tsig)
#    simu.init(u=u)
#
#    simu.process()
#
#    simu.data.plot(('u', 'y'))
