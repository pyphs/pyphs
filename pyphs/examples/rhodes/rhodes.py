#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 11:50:23 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import os
from pyphs import Netlist

# ---------------------------  NETLIST  ------------------------------------- #
label = 'rhodes'
this_script = os.path.realpath(__file__)
here = this_script[:this_script.rfind(os.sep)]
netlist_filename = here + os.sep + label + '.net'
netlist = Netlist(netlist_filename)

# ---------------------------  CORE  ---------------------------------------- #
core = netlist.to_core()
core.subsinverse()
core.reduce_z()

## ---------------------------  SIMULATION  ---------------------------------- #
#if __name__ == '__main__':
#
#    from pyphs.core.tools import sympify
#    import numpy
#    import matplotlib.pyplot as plt
#    from pyphs.misc.signals.waves import wavwrite
#
#    config_method = {'grad': 'discret',    # In {'discret', 'theta', 'trapez'}
#                     'theta': 0.,          # Theta-scheme for the structure
#                     'split': True,        # split implicit from explicit part
#              }
#
#    # Define the simulation parameters
#    config_simulation = {'fs': 48e3,           # Sample rate (Hz)
#                         'maxit': 10,          # Max number of iterations for NL solvers
#                         'eps': 1e-16,         # Global numerical tolerance
#                         'path': None,         # Path to the results folder
#                         'pbar': True,         # Display a progress bar
#                         'timer': False,       # Display minimal timing infos
#                         'lang': 'c++',        # Language in {'python', 'c++'}
#                         # Options for the data reader. The data are read from index imin
#                         # to index imax, rendering one element out of the number decim
#                         'load': {'imin': None,
#                                  'imax': None,
#                                  'decim': None}
#                         }
#
#    def ordering(name, *args):
#        def get_index(e):
#            symb = core.symbols(e)
#            return getattr(core, name).index(symb)
#        return list(map(get_index, args))
#
#    order = ordering('y', 'yOutput', 'yPickupMagnet')
#
#    # Instanciate Method class
#    method = core.to_method(config=config_method)
#
#    # state initialization
#    list_v_hammer = numpy.linspace(1, 10, 10)
#    # !!! must be array with shape (core.dims.x(), )
#    x0 = sympify([0, ] * method.dims.x())
#
#    # Init Hammer velocity
#    # v_hammer = 1  # Hammer velocity (m/s)
#    symbol_hammer_velocity = core.symbols('Vhammer')
#    symbol_hammer_mass = core.symbols('Mhammer')
#    m_hammer = core.subs[symbol_hammer_mass]  # Hammer mass (kg)
#    # Set mass momentum (N.s)
#    ixHammerMass = method.x.index(core.symbols('xHammerMass'))
#    x0[ixHammerMass] = symbol_hammer_velocity * symbol_hammer_mass
#    method.subs[symbol_hammer_velocity] = list_v_hammer[0]
#
#    symbol_tinit = core.symbols('tinit')
#    tinit = 2e-2  # [s] time between init of velocity and impact
#    method.subs[symbol_tinit] = tinit
#    qh0 = -symbol_hammer_velocity*symbol_tinit  # [m] Hammer's initial position w.r.t contact
#    iqHammerFelt = method.x.index(core.symbols('qHammerFelt'))
#    x0[iqHammerFelt] = qh0  # (m)
#
#    subs = method.subs.copy()
#
#    # Instanciate Simulation class
#    simu = method.to_simulation(config=config_simulation,
#                                inits={'x': x0})
#
#    # def simulation time
#    tmax = 5
#    nt = int(tmax*simu.config['fs'])
#    t = [n/simu.config['fs'] for n in range(nt)]
#
#    # def generator for sequence of inputs to feed in the Simulation
#    def sequ():
#        """
#        generator of input sequence for Simulation
#        """
#        for tn in t:
#            # numpy.array([u1, u2, ...])
#            yield numpy.array([[0., 1.][i] for i in order])
#
#    # ---------------------------  LOOP  --------------------------------
#    sig = list()
#
#    waves_path = os.path.join(here, 'waves')
#    if not os.path.exists(waves_path):
#        os.mkdir(waves_path)
#
#    for v_hammer in list_v_hammer:
#
#        subs[symbol_hammer_velocity] = v_hammer
#
#        # Initialize the simulation
#        simu.init(u=sequ(), nt=nt, subs=subs)
#
#        # Proceed
#        simu.process()
#
#        wave_name = 'PickupOut_{}={}'.format('vHammer', str(v_hammer))
#        simu.data.wavwrite('y', order[1],
#                           path=os.path.join(waves_path, wave_name))
#
#        sig += list(simu.data.y(order[1], decim=1))
#        simu.data.plot([('x', 0), ('dtx', 0), ('y', order[0])],
#                       load={'imin': 0, 'imax': 2500}, label=str(v_hammer))
#
#        pass
#
#    wavwrite(sig, simu.config['fs'],
#             os.path.join(here, 'PickupOut'),
#             normalize=True)
