#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 20:24:57 2017

@author: Falaize
"""

# Support for Python 2.x and Python 3.x
from __future__ import division

from pyphs import PHSSimulation, signalgenerator
from pyphs.misc.signals.analysis import transferFunction, spectrogram
from pyphs.misc.signals.processing import lowpass
import numpy as np


def plot_power_balance_rlc_with_split():
    # Define the simulation parameters
    config = {'fs': 48e3,               # Sample rate
              'gradient': 'discret',    # in {'discret', 'theta', 'trapez'}
              'theta': 0.5,             # theta-scheme for the structure
              'split': True,           # apply core.split_linear() beforehand
              'maxit': 10,              # Max iteration for NL solvers
              'numtol': 1e-16,          # Global numerical tolerance
              'path': None,             # Path to the results folder
              'progressbar': True,      # Display a progress bar
              'timer': True,           # Display minimal timing infos
              'language': 'python',     # in {'python', 'c++'}
              'cpp_build_and_run_script': None,  # compile and exec binary
              'eigen_path': None,       # path to Eigen library
              }

    # retrieve the pyphs.PHSCore of a linear RLC from the examples
    from pyphs.examples.rlc.rlc import core as rlc

    rlc_ = rlc.__copy__()
    rlc_.build_R()
    simu = PHSSimulation(rlc_, config=config)

    dur = 0.01
    u = signalgenerator(which='sin', f0=800., tsig=dur, fs=simu.fs)

    def sequ():
        for el in u():
            yield (el, )

    simu.init(sequ=sequ(), nt=int(dur*simu.fs))
    simu.process()

    simu.data.plot_powerbal(mode='single', show=False)
    simu.data.plot_powerbal(mode='multi', show=False)

    return True


def plot_power_balance_nlcore_with_split():
    # Define the simulation parameters
    config = {'fs': 48e3,               # Sample rate
              'gradient': 'discret',    # in {'discret', 'theta', 'trapez'}
              'theta': 0.5,             # theta-scheme for the structure
              'split': True,           # apply core.split_linear() beforehand
              'maxit': 10,              # Max iteration for NL solvers
              'numtol': 1e-16,          # Global numerical tolerance
              'path': None,             # Path to the results folder
              'progressbar': True,      # Display a progress bar
              'timer': True,           # Display minimal timing infos
              'language': 'python',     # in {'python', 'c++'}
              'cpp_build_and_run_script': None,  # compile and exec binary
              'eigen_path': None,       # path to Eigen library
              }

    # retrieve the pyphs.PHSCore of a nonlinear RLC from
    # the tutorial on PHSCore
    from pyphs.tutorials.phscore import core as nlcore
    nlcore.build_R()
    simu = PHSSimulation(nlcore, config=config)

    dur = 0.01
    u = signalgenerator(which='sin', f0=800., tsig=dur, fs=simu.fs)

    def sequ():
        for el in u():
            yield (el, )

    simu.init(sequ=sequ(), nt=int(dur*simu.fs))
    simu.process()

    simu.data.plot_powerbal(mode='single', show=False)
    simu.data.plot_powerbal(mode='multi', show=False)

    return True


def plot_rlc_with_split():
    # Define the simulation parameters
    config = {'fs': 48e3,               # Sample rate
              'gradient': 'discret',    # in {'discret', 'theta', 'trapez'}
              'theta': 0.5,             # theta-scheme for the structure
              'split': False,           # apply core.split_linear() beforehand
              'maxit': 10,              # Max iteration for NL solvers
              'numtol': 1e-16,          # Global numerical tolerance
              'path': None,             # Path to the results folder
              'progressbar': True,      # Display a progress bar
              'timer': True,            # Display minimal timing infos
              'language': 'python',     # in {'python', 'c++'}
              'cpp_build_and_run_script': None,  # compile and exec binary
              'eigen_path': None,       # path to Eigen library
              }

    # retrieve the pyphs.PHSCore of a linear RLC from the examples
    from pyphs.examples.rlc.rlc import core as rlc

    print(rlc.w)
    print(rlc.z)

    simu = PHSSimulation(rlc, config=config)

    dur = 0.01
    u = signalgenerator(which='sin', f0=800., tsig=dur, fs=simu.fs)

    def sequ():
        for el in u():
            yield (el, )

    simu.init(sequ=sequ(), nt=int(dur*simu.fs))
    simu.process()

    print(simu.nums.method.core.w)
    print(simu.nums.method.core.z)

    dims = simu.nums.method.core.dims
    # plot u, y
    simu.data.plot([('u', i) for i in range(dims.y())] +
                   [('y', i) for i in range(dims.y())], show=False)
    # plot w, z
    simu.data.plot([('w', 0), ('z', 0)], show=False)

    simu.data.plot([('dtx', i) for i in range(dims.x())] +
                   [('dxH', i) for i in range(dims.x())], show=False)

    return True
    
    
def TranferFunction():
    sig1 = np.random.rand(int(1e4))
    sig2 = lowpass(sig1, 0.1)
    f, TF = transferFunction(sig1, sig2, 100)
    spectrogram(sig1, sig2, fs=100)
    return True
    
