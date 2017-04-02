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
import matplotlib.pyplot as plt  # plot tools

# retrieve the pyphs.PHSCore of a nonlinear RLC from the tutorial on PHSCore
from pyphs.tutorials.phscore import core as nlcore

from pyphs.examples.rlc.rlc import core as rlc
from pyphs import PHSSimulation, signalgenerator


def simulation_rlc_with_split():
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

    simu = PHSSimulation(rlc, config=config)

    dur = 0.01
    u = signalgenerator(which='sin', f0=800., tsig=dur, fs=simu.fs)

    def sequ():
        for el in u():
            yield (el, )

    simu.init(sequ=sequ(), nt=int(dur*simu.fs))
    simu.process()

    return True


def simulation_rlc_without_split():
    # Define the simulation parameters
    config = {'fs': 48e3,               # Sample rate
              'gradient': 'discret',    # in {'discret', 'theta', 'trapez'}
              'theta': 0.5,             # theta-scheme for the structure
              'split': False,           # apply core.split_linear() beforehand
              'maxit': 10,              # Max iteration for NL solvers
              'numtol': 1e-16,          # Global numerical tolerance
              'path': None,             # Path to the results folder
              'progressbar': True,      # Display a progress bar
              'timer': True,           # Display minimal timing infos
              'language': 'python',     # in {'python', 'c++'}
              'cpp_build_and_run_script': None,  # compile and exec binary
              'eigen_path': None,       # path to Eigen library
              }

    simu = PHSSimulation(rlc, config=config)

    dur = 0.01
    u = signalgenerator(which='sin', f0=800., tsig=dur, fs=simu.fs)

    def sequ():
        for el in u():
            yield (el, )

    simu.init(sequ=sequ(), nt=int(dur*simu.fs))

    simu.process()

    return True


def simulation_rlc_plot():
    # Define the simulation parameters
    config = {'fs': 48e3,               # Sample rate
              'gradient': 'discret',    # in {'discret', 'theta', 'trapez'}
              'theta': 0.5,             # theta-scheme for the structure
              'split': False,           # apply core.split_linear() beforehand
              'maxit': 10,              # Max iteration for NL solvers
              'numtol': 1e-16,          # Global numerical tolerance
              'path': None,             # Path to the results folder
              'progressbar': True,      # Display a progress bar
              'timer': True,           # Display minimal timing infos
              'language': 'python',     # in {'python', 'c++'}
              'cpp_build_and_run_script': None,  # compile and exec binary
              'eigen_path': None,       # path to Eigen library
              }

    simu = PHSSimulation(rlc, config=config)

    dur = 0.01
    u = signalgenerator(which='sin', f0=800., tsig=dur, fs=simu.fs)

    def sequ():
        for el in u():
            yield (el, )

    simu.init(sequ=sequ(), nt=int(dur*simu.fs))

    simu.process()
    simu.data.plot_powerbal(mode='multi')

    return True


def simulation_nlcore_full():

    # Define the simulation parameters
    config = {'fs': 48e3,               # Sample rate
              'gradient': 'discret',    # in {'discret', 'theta', 'trapez'}
              'theta': 0.5,             # theta-scheme for the structure
              'split': False,           # apply core.split_linear() beforehand
              'maxit': 10,              # Max number of iterations for NL solvers
              'numtol': 1e-16,          # Global numerical tolerance
              'path': None,             # Path to the folder to save the results
              'progressbar': False,     # Display a progress bar
              'timer': False,           # Display minimal timing infos
              'language': 'python',     # in {'python', 'c++'}
              'cpp_build_and_run_script': None,  # call to compiler and exec binary
              'eigen_path': None,    # path to Eigen C++ linear algebra library
              }

    # Instantiate a pyphs.PHSSimulation object associated with a given core PHS
    simu = PHSSimulation(nlcore, config=config)

    # def simulation time
    tmax = 0.02
    nmax = int(tmax*simu.fs)
    t = [n/simu.fs for n in range(nmax)]
    nt = len(t)


    # def input signal
    def sig(tn, mode='impact'):
        freq = 1000.
        amp = 1000.
        if mode == 'sin':
            pi = numpy.pi
            sin = numpy.sin
            out = amp * sin(2*pi*freq*tn)
        elif mode == 'impact':
            dur = 0.5*1e-3  # duration: 0.5ms
            start = 0.001   # start at 1ms
            out = amp if start <= tn < start + dur else 0.
        elif mode == 'const':
            out = 1.
        return out


    # def generator for sequence of inputs to feed in the PHSSimulation object
    def sequ():
        """
        generator of input sequence for PHSSimulation
        """
        for tn in t:
            u1 = sig(tn)

            # !!! must be array with shape (core.dims.u(), )
            yield numpy.array([u1, ])  # numpy.array([u1, u2, ...])

    # state initialization
    # !!! must be array with shape (core.dims.x(), )
    x0 = (0., 0.)

    # Initialize the simulation
    simu.init(sequ=sequ(), x0=x0, nt=nt)

    # Proceed
    simu.process()

    # The simulation results are stored on disk, and read with the simu.data object
    t = simu.data.t()       # a generator of time value at each time step
    x = simu.data.x()       # a generator of value for vector x at each time step
    x1 = simu.data.x(0)     # a generator of value for scalar x component 1

    # recover data as lists
    t_list = list(t)
    x_list = list(x)
    x1_list = list(x1)

    return True
