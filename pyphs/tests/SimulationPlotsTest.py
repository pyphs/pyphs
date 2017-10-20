#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 20:24:57 2017

@author: Falaize
"""

# Support for Python 2.x and Python 3.x
from __future__ import division

from pyphs import Simulation, signalgenerator
from pyphs.misc.signals.analysis import transferFunction, spectrogram
from pyphs.misc.signals.processing import lowpass
import numpy as np
import os
import shutil

here = os.path.realpath(__file__)[:os.path.realpath(__file__).rfind(os.sep)]
path = os.path.join(here, 'simu')


def plot_power_balance_rlc_with_split():
    # Define the simulation parameters
    config = {'fs': 48e3,               # Sample rate
              'grad': 'discret',    # in {'discret', 'theta', 'trapez'}
              'theta': 0.5,             # theta-scheme for the structure
              'split': False,           # apply core.split_linear() beforehand
              'maxit': 10,              # Max iteration for NL solvers
              'eps': 1e-16,          # Global numerical tolerance
              'path': path,             # Path to the results folder
              'pbar': False,      # Display a progress bar
              'timer': True,            # Display minimal timing infos
              'lang': 'python',     # in {'python', 'c++'}
              }

    # retrieve the pyphs.Core of a linear RLC from the examples
    from pyphs.examples.rlc.rlc import core as rlc

    rlc_ = rlc.__copy__()
    rlc_.reduce_z()
    simu = Simulation(rlc_.to_method(), config=config)

    dur = 0.01
    u = signalgenerator(which='sin', f0=800., tsig=dur, fs=simu.config['fs'])

    def sequ():
        for el in u():
            yield (el, )

    simu.init(u=sequ(), nt=int(dur*simu.config['fs']))
    simu.process()

    simu.data.plot_powerbal(mode='single', show=False)
    simu.data.plot_powerbal(mode='multi', show=False)

    if not os.name.lower().startswith('nt'):
        shutil.rmtree(path)
    return True


def plot_power_balance_nlcore_with_split():
    # Define the simulation parameters
    config = {'fs': 48e3,               # Sample rate
              'grad': 'discret',    # in {'discret', 'theta', 'trapez'}
              'theta': 0.5,             # theta-scheme for the structure
              'split': True,           # apply core.split_linear() beforehand
              'maxit': 10,              # Max iteration for NL solvers
              'eps': 1e-16,          # Global numerical tolerance
              'path': path,             # Path to the results folder
              'pbar': False,      # Display a progress bar
              'timer': True,            # Display minimal timing infos
              'lang': 'python',     # in {'python', 'c++'}
              }


    # retrieve the pyphs.Core of a nonlinear RLC from
    # the tutorial on Core
    from pyphs.tutorials.core import core as nlcore
    nlcore.reduce_z()
    simu = Simulation(nlcore.to_method(), config=config)

    dur = 0.01
    u = signalgenerator(which='sin', f0=800., tsig=dur, fs=simu.config['fs'])

    def sequ():
        for el in u():
            yield (el, )

    simu.init(u=sequ(), nt=int(dur*simu.config['fs']))
    simu.process()

    simu.data.plot_powerbal(mode='single', show=False)
    simu.data.plot_powerbal(mode='multi', show=False)

    if not os.name.lower().startswith('nt'):
        shutil.rmtree(path)
    return True


def plot_rlc_with_split():
    # Define the simulation parameters
    config = {'fs': 48e3,               # Sample rate
              'grad': 'discret',    # in {'discret', 'theta', 'trapez'}
              'theta': 0.5,             # theta-scheme for the structure
              'split': False,           # apply core.split_linear() beforehand
              'maxit': 10,              # Max iteration for NL solvers
              'eps': 1e-16,          # Global numerical tolerance
              'path': path,             # Path to the results folder
              'pbar': False,      # Display a progress bar
              'timer': True,            # Display minimal timing infos
              'lang': 'python',     # in {'python', 'c++'}
              }

    # retrieve the pyphs.Core of a linear RLC from the examples
    from pyphs.examples.rlc.rlc import core as rlc

    print(rlc.w)
    print(rlc.z)

    simu = Simulation(rlc.to_method(), config=config)

    dur = 0.01
    u = signalgenerator(which='sin', f0=800., tsig=dur, fs=simu.config['fs'])

    def sequ():
        for el in u():
            yield (el, )

    simu.init(u=sequ(), nt=int(dur*simu.config['fs']))
    simu.process()

    print(simu.nums.method.w)
    print(simu.nums.method.z)

    dims = simu.nums.method.dims
    # plot u, y
    simu.data.plot([('u', i) for i in range(dims.y())] +
                   [('y', i) for i in range(dims.y())], show=False)
    # plot w, z
    simu.data.plot([('w', 0), ('z', 0)], show=False)

    simu.data.plot([('dtx', i) for i in range(dims.x())] +
                   [('dxH', i) for i in range(dims.x())], show=False)

    if not os.name.lower().startswith('nt'):
        shutil.rmtree(path)
    return True


def TranferFunction():
    sig1 = np.random.rand(int(1e4))
    sig2 = lowpass(sig1, 0.1)
    f, TF = transferFunction(sig1, sig2, 100)
    spectrogram(sig1, sig2, fs=100)
    return True
