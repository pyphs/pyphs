#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 11:50:23 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import os
import sys
from pyphs import netlist2core, PHSSimulation, signalgenerator


label = 'rlc'

try:
    os.chdir(os.path.dirname(sys.argv[0]))
    path = os.getcwd() + os.sep
except OSError:
    path = r''

netlist_filename = path + label + '.net'
core = netlist2core(netlist_filename)

simu = PHSSimulation(core)

dur = 0.01
u = signalgenerator(which='sin', f0=800., tsig=dur, fs=simu.fs)


def sequ():
    for el in u():
        yield (el, )

simu.init(sequ=sequ(), nt=int(dur*simu.fs))
simu.process()

simu.data.plot_powerbal()