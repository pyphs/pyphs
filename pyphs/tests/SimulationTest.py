#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 05:40:20 2017

@author: Falaize
"""

# Support for Python 2.x and Python 3.x
from __future__ import division

# import of external packages
import numpy                     # numerical tools
import sympy

# retrieve the pyphs.Core of a nonlinear RLC from the tutorial on Core
from pyphs.tutorials.core import core as nlcore

from pyphs.examples.rlc.rlc import core

from pyphs import Simulation, signalgenerator

from pyphs.numerics.cpp.simu2cpp import simu2cpp
import os
import shutil


here = os.path.realpath(__file__)[:os.path.realpath(__file__).rfind(os.sep)]
path = os.path.join(here, 'simu')


def simulation_rlc_with_split():
    rlc = core.__copy__()
    config = {'fs': 48e3,           # Sample rate
              'grad': 'discret',    # in {'discret', 'theta', 'trapez'}
              'theta': 0.5,         # theta-scheme for the structure
              'split': True,        # apply core.split_linear() beforehand
              'maxit': 10,          # Max iteration for NL solvers
              'eps': 1e-16,         # Global numerical tolerance
              'path': path,         # Path to the results folder
              'pbar': True,         # Display a progress bar
              'timer': True,        # Display minimal timing infos
              'lang': 'python',     # in {'python', 'c++'}
              }

    simu = Simulation(rlc.to_method(), config=config)

    dur = 0.01
    u = signalgenerator(which='sin', f0=800.,
                        tsig=dur, fs=simu.config['fs'])

    sequ = u[:, numpy.newaxis]

    simu.init(u=sequ, nt=int(dur*simu.config['fs']))

    simu.process()

    simu.data.wavwrite('y', 0)

    if not os.name.lower().startswith('nt'):
        shutil.rmtree(path)
    return True


def simulation_rlc_cpp():
    rlc = core.__copy__()
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
              'lang': 'c++',     # in {'python', 'c++'}
              }

    simu = Simulation(rlc.to_method(), config=config)

    dur = 0.01
    u = signalgenerator(which='sin', f0=800., tsig=dur, fs=simu.config['fs'])

    sequ = u[:, numpy.newaxis]

    simu.init(u=sequ, nt=int(dur*simu.config['fs']))
    simu2cpp(simu)

    if not os.name.lower().startswith('nt'):
        shutil.rmtree(path)
    return True



def simulation_rlc_without_split():
    rlc = core.__copy__()
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

    simu = Simulation(rlc.to_method(), config=config)

    dur = 0.01
    u = signalgenerator(which='sin', f0=800., tsig=dur, fs=simu.config['fs'])

    sequ = u[:, numpy.newaxis]

    simu.init(u=sequ, nt=int(dur*simu.config['fs']))

    simu.process()

    if not os.name.lower().startswith('nt'):
        shutil.rmtree(path)
    return True


def simulation_rlc_without_split_trapez():
    rlc = core.__copy__()
    # Define the simulation parameters
    config = {'fs': 48e3,               # Sample rate
              'grad': 'trapez',    # in {'discret', 'theta', 'trapez'}
              'theta': 0.5,             # theta-scheme for the structure
              'split': False,           # apply core.split_linear() beforehand
              'maxit': 10,              # Max iteration for NL solvers
              'eps': 1e-16,          # Global numerical tolerance
              'path': path,             # Path to the results folder
              'pbar': False,      # Display a progress bar
              'timer': True,            # Display minimal timing infos
              'lang': 'python',     # in {'python', 'c++'}
              }

    simu = Simulation(rlc.to_method(), config=config)

    dur = 0.01
    u = signalgenerator(which='sin', f0=800., tsig=dur, fs=simu.config['fs'])

    sequ = u[:, numpy.newaxis]

    simu.init(u=sequ, nt=int(dur*simu.config['fs']))

    simu.process()

    if not os.name.lower().startswith('nt'):
        shutil.rmtree(path)
    return True


def simulation_rlc_without_split_theta():
    rlc = core.__copy__()
    # Define the simulation parameters
    config = {'fs': 48e3,               # Sample rate
              'grad': 'theta',    # in {'discret', 'theta', 'trapez'}
              'theta': 0.5,             # theta-scheme for the structure
              'split': False,           # apply core.split_linear() beforehand
              'maxit': 10,              # Max iteration for NL solvers
              'eps': 1e-16,          # Global numerical tolerance
              'path': path,             # Path to the results folder
              'pbar': False,      # Display a progress bar
              'timer': True,            # Display minimal timing infos
              'lang': 'python',     # in {'python', 'c++'}
              }

    simu = Simulation(rlc.to_method(), config=config)

    dur = 0.01
    u = signalgenerator(which='sin', f0=800., tsig=dur, fs=simu.config['fs'])

    sequ = u[:, numpy.newaxis]

    simu.init(u=sequ, nt=int(dur*simu.config['fs']))

    simu.process()

    if not os.name.lower().startswith('nt'):
        shutil.rmtree(path)
    return True


def simulation_rlc_plot():
    rlc = core.__copy__()
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

    simu = Simulation(rlc.to_method(), config=config)

    dur = 0.01
    u = signalgenerator(which='sin', f0=800., tsig=dur, fs=simu.config['fs'])

    sequ = u[:, numpy.newaxis]

    simu.init(u=sequ)

    simu.process()
    simu.data.plot_powerbal(mode='multi')

    if not os.name.lower().startswith('nt'):
        shutil.rmtree(path)
    return True


def simulation_nlcore_full():

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

    # state initialization
    # !!! must be array with shape (core.dims.x(), )
    x0 = list(map(sympy.sympify, (0., 0., 0.)))

    # Instantiate a pyphs.Simulation object associated with a given core
    simu = Simulation(nlcore.to_method(), config=config, inits={'x': x0})

    # def simulation time
    tmax = 0.02
    nmax = int(tmax*simu.config['fs'])
    t = numpy.array([n/simu.config['fs'] for n in range(nmax)])

    # def input signal

    freq = 1000.
    amp = 1000.
    sig = amp * numpy.sin(2*numpy.pi*freq*t)

    # def inputs to feed in the Simulation object
    sequ = sig[:, numpy.newaxis]

    # Initialize the simulation
    simu.init(u=sequ)

    # Proceed
    simu.process()

    if not os.name.lower().startswith('nt'):
        shutil.rmtree(path)
    return True
