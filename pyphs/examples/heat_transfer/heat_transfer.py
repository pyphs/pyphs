#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 11:50:23 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import os
from pyphs import Netlist

# netlist label
label = 'heat_transfer'

# define absolute netlist filename
path = os.path.realpath(__file__)[:os.path.realpath(__file__).rfind(os.sep)]
netlist_filename = path + os.sep + label + '.net'

# read netlist from file
netlist = Netlist(netlist_filename)

# build Core object
core = netlist.to_core()

# %% ------------------------------ SIMULATION ------------------------------ #

# UNCOMMENT BELOW FOR SIMULATION AND PLOTS

# if __name__ == '__main__':
#
#    from pyphs import signalgenerator, Evaluation, Simulation
#    from pyphs.misc.plots.singleplots import singleplot
#    import numpy as np
#
#    tsig = 200.
#    fs = 1e0
#
#    config = {'fs': fs,
#              'split': True,
#              'maxit': 10,
#              'eps': 1e-9,
#              'pbar': True
#              }
#
#    core.reduce_z()
#    core.subsinverse()
#
#    simu = Simulation(core.to_method(), config)
#
#    # Initial entropies (J/K)
#
#    x0 = (2., -0.1)
#    evals = Evaluation(core, names=['dxH'])
#    theta0 = evals.dxH(*x0)-273.16
#
#    # Imposed Temperature (°C)
#    tamb = 20.
#
#    u = signalgenerator(which='const', A=tamb+273.16, tsig=tsig, fs=fs)  # (K)
#
#    simu.init(u=u[:, np.newaxis], inits={'x': x0})
#
#    simu.process()
#
#    simu.data.step = max((1, int(len(u)/5e2)))
#
#    simu.data.plot_powerbal(mode='single')
#
#    t = simu.data.t()
#    theta1 = simu.data['dxH'][:, 0]
#    theta2 = simu.data['dxH'][:, 1]
#    sigma1 = simu.data['dtx'][:, 0]
#    sigma2 = simu.data['dtx'][:, 1]
#    sigmay = simu.data['y'][:, 0]
#
# #    simu.data.plot_powerbal()
#
#    fig, ax = singleplot(t, (theta1-273.16,
#                             theta2-273.16),
#                         xlabel='Time $t$ (s)',
#                         ylabel=r'Temperature $\theta$ ($^\circ$C)',
#                         labels=[r'$\theta_1$', r'$\theta_2$'])
#    ax.grid('on')
#
#    fig, ax = singleplot(t, (sigma1, sigma2, sigmay, sigma1 + sigma2 + sigmay),
#                         xlabel='Time $t$ (s)',
#                         ylabel=r'Entropy variation $\dot \sigma$ (J/K/s)',
#                         labels=[r'$\dot \sigma_1$', r'$\dot \sigma_2$',
#                                 r'$\dot \sigma_{\mathrm{amb}}$',
#                                 r'$\dot \sigma_1+\dot \sigma_2+\dot \sigma_{\mathrm{amb}}$'])
#    ax.grid('on')
