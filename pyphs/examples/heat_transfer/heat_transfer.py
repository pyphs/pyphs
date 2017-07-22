#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 11:50:23 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import os
from pyphs import Netlist, Graph

label = 'heat_transfer'
path = os.path.realpath(__file__)[:os.path.realpath(__file__).rfind(os.sep)]
netlist_filename = path + os.sep + label + '.net'
netlist = Netlist(netlist_filename)
graph = Graph(netlist=netlist)
core = graph.to_core()

core.reduce_z()
core.subsinverse()

#if __name__ == '__main__':
#
#    from pyphs import Simulation
#    from pyphs.misc.plots.singleplots import singleplot
#    import numpy as np
#
#    tsig = 500.
#    fs = 1e1
#
#    config = {'fs': fs,
#              'split': True,
#              'lang': 'python',
#              'maxit': 10,
#              'eps': 1e-9,
#              'pbar': True
#              }
#    simu = Simulation(core.to_method(), config)
#
#    nt = int(fs*tsig)
#
#    # Initial entropies (J/K)
#    x0 = (1., -5.)
#
#    def u():
#        tamb = 20.   # Impose Temperature (°C)
#        for i in range(nt):
#            yield np.array([tamb+273.16, ])  # (K)
#
#    simu.init(u=u(), nt=nt, x0=x0)
#
#    simu.process()
#
#    simu.data.plot_powerbal(mode='single')
#
#    t = np.array(list(simu.data.t()))
#    theta = np.array(list(simu.data.dxH())).T
#    sigma = np.array(list(simu.data.x())).T
#    sigmay = np.array(list(simu.data.y())).T
#
#    simu.data.plot_powerbal()
#
#    singleplot(t, theta-core.subs[core.symbols('T0')],
#               unitx='Time $t$ (s)', unity=r'Temperature $\theta$ ($^\circ$C)',
#               labels=[r'$\theta_1$', r'$\theta_2$'])
#
#    singleplot(t, np.vstack((sigma, sigmay,
#                             np.sum(sigma, axis=0)[np.newaxis, :] + sigmay)),
#               unitx='Time $t$ (s)', unity=r'Entropy $\sigma$ (J/K)',
#               labels=[r'$\sigma_1$', r'$\sigma_2$',
#                       r'$\sigma_{\mathrm{amb}}$',
#                       r'$\sigma_1+\sigma_2+\sigma_{\mathrm{amb}}$'])
#
#    pass
