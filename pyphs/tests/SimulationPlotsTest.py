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

    sequ = u[:, np.newaxis]
    simu.init(u=sequ)
    simu.process()

    simu.data.plot_powerbal(mode='single', show=False)
    simu.data.plot_powerbal(mode='multi', show=False)

    if not os.name.lower().startswith('nt'):
        shutil.rmtree(path)

    return True


def dataH5File():
    # Define the simulation parameters
    config = {'fs': 48e3,               # Sample rate
              'grad': 'discret',    # in {'discret', 'theta', 'trapez'}
              'theta': 0.5,             # theta-scheme for the structure
              'split': True,           # apply core.split_linear() beforehand
              'maxit': 10,              # Max iteration for NL solvers
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

    sequ = u[:, np.newaxis]
    simu.init(u=sequ)
    simu.process()

    simu.data.plot_powerbal(mode='single', show=False)
    simu.data.plot_powerbal(mode='multi', show=False)

    simu2 = Simulation(nlcore.to_method(), config=config, erase=False)

    start = int(simu.data.nt/10.)
    stop = int(9*simu.data.nt/10.)
    step = 3

    simu2.data.start = start
    simu2.data.stop = stop
    simu2.data.step = step

    test = len(range(start, stop, step)) == len(simu2.data['x', :, 0])

    return test


def plot_rlc_with_split():
    # Define the simulation parameters
    config = {'fs': 48e3,               # Sample rate
              'grad': 'discret',    # in {'discret', 'theta', 'trapez'}
              'theta': 0.5,             # theta-scheme for the structure
              'split': False,           # apply core.split_linear() beforehand
              'maxit': 10,              # Max iteration for NL solvers
              'path': path,             # Path to the results folder
              'pbar': False,      # Display a progress bar
              'timer': True,            # Display minimal timing infos
              'lang': 'python',     # in {'python', 'c++'}
              }

    # retrieve the pyphs.Core of a linear RLC from the examples
    from pyphs.examples.rlc.rlc import core as rlc

    simu = Simulation(rlc.to_method(), config=config)

    dur = 0.01
    u = signalgenerator(which='sin', f0=800., tsig=dur, fs=simu.config['fs'])

    sequ = u[:, np.newaxis]
    simu.init(u=sequ)
    simu.process()

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
    f, TF = transferFunction(sig1, sig2, fs=100, nfft=2**9)
    spectrogram(sig2, fs=100)
    return True


if __name__ == '__main__':
    all_tests = [dataH5File,
                 plot_power_balance_rlc_with_split,
                 plot_rlc_with_split,
                 TranferFunction]

    for test in all_tests:
        test()
