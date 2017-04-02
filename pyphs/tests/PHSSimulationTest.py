#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 05:40:20 2017

@author: Falaize
"""

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
    