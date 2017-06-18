#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 11:50:23 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import os
from pyphs import PHSNetlist, PHSGraph, PHSSimulation
from pyphs.misc.plots.singleplots import singleplot
import numpy as np


label = 'heat_transfer'
path = os.path.realpath(__file__)[:os.path.realpath(__file__).rfind(os.sep)]
netlist_filename = path + os.sep + label + '.net'
netlist = PHSNetlist(netlist_filename)
graph = PHSGraph(netlist=netlist)
core = graph.buildCore()

core.build_R()
core.subsinverse()

if __name__ == '__main__':
    tsig = 50.
    fs = 1e1

    config = {'fs': fs,
              'split': True,
              'lang': 'python',
              'maxit': 10,
              'eps': 1e-9,
              'pbar': True
              }
    simu = PHSSimulation(core, config)

    nt = int(fs*tsig)
    x0 = (4., 0.)
    simu.init(nt=nt, x0=x0)

    simu.process()

    t = np.array(list(simu.data.t()))
    theta = np.array(list(simu.data.dxH())).T
    sigma = np.array(list(simu.data.x())).T

    singleplot(t, theta, unitx='Time $t$ (s)', unity=r'Temperature $\theta$ (K)',
               labels=[r'$\theta_1$', r'$\theta_2$'])

    singleplot(t, np.vstack((sigma, np.sum(sigma, axis=0)[np.newaxis, :])),
               unitx='Time $t$ (s)', unity=r'Entropy $\sigma$ (J/K)',
               labels=[r'$\sigma_1$', r'$\sigma_2$', r'$\sigma_1+\sigma_2$'])

    pass
