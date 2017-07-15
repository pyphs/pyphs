#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 11:50:23 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import os
from pyphs import Netlist, Graph


# ---------------------------  NETLIST  ------------------------------------- #
label = 'rhodes'
this_script = os.path.realpath(__file__)
here = this_script[:this_script.rfind(os.sep)]
netlist_filename = here + os.sep + label + '.net'
netlist = Netlist(netlist_filename)

# ---------------------------  GRAPH  --------------------------------------- #
graph = Graph(netlist=netlist)

# ---------------------------  CORE  ---------------------------------------- #
core = graph.buildCore()
core.reduce_z()
core.subsinverse()


# ---------------------------  SIMULATION  ---------------------------------- #
#if __name__ == '__main__':
#
#    import numpy
#    import matplotlib.pyplot as plt
#    from pyphs import Simulation
#    from pyphs.misc.signals.waves import wavwrite
#
#    # Define the simulation parameters
#    config = {'fs': 48e3,           # Sample rate (Hz)
#              'grad': 'discret',    # In {'discret', 'theta', 'trapez'}
#              'theta': 0.,          # Theta-scheme for the structure
#              'split': True,       # split implicit from explicit part
#              'maxit': 10,          # Max number of iterations for NL solvers
#              'eps': 1e-16,         # Global numerical tolerance
#              'path': None,         # Path to the results folder
#              'pbar': True,         # Display a progress bar
#              'timer': False,       # Display minimal timing infos
#              'lang': 'c++',        # Language in {'python', 'c++'}
#              # Options for the data reader. The data are read from index imin
#              # to index imax, rendering one element out of the number decim
#              'load': {'imin': None,
#                       'imax': None,
#                       'decim': None}
#              }
#
#    # Instanciate Simulation class
#    simu = Simulation(core, config=config)
#
#    def ordering(name, *args):
#        def get_index(e):
#            symb = simu.nums.method.symbols(e)
#            return getattr(simu.nums.method, name).index(symb)
#        return list(map(get_index, args))
#
#    order = ordering('y', 'yOutput', 'yPickupMagnet')
#
#    # def simulation time
#    tmax = 5
#    nmax = int(tmax*simu.config['fs'])
#    t = [n/simu.config['fs'] for n in range(nmax)]
#    nt = len(t)
#    vin_max = 2  # [m/s] Maximal initial velocity of the hammer
#    sig = list()
#
#    # ---------------------------  LOOP  --------------------------------
#
#    for v_hammer in numpy.linspace(1, 1, 1):
#
#        # def generator for sequence of inputs to feed in the Simulation
#        def sequ():
#            """
#            generator of input sequence for Simulation
#            """
#            for tn in t:
#                # numpy.array([u1, u2, ...])
#                yield numpy.array([[0., 1.][i] for i in order])
#
#        # state initialization
#        # !!! must be array with shape (core.dims.x(), )
#        x0 = numpy.array([0., ]*core.dims.x())
#
#        # shortcut to core method
#        core_simu = simu.nums.method
#
#        # Init Hammer velocity
#        # v_hammer = 1  # Hammer velocity (m/s)
#        symbol_hammer_mass = core.symbols('Mhammer')
#        m_hammer = core.subs[symbol_hammer_mass]  # Hammer mass (kg)
#        # Set mass momentum (N.s)
#        ixHammerMass = core_simu.x.index(core.symbols('xHammerMass'))
#        x0[ixHammerMass] = v_hammer * m_hammer
#
#        tinit = 2e-2  # [s] time between init of velocity and impact
#        qh0 = -v_hammer*tinit  # [m] Hammer's initial position w.r.t contact
#        iqHammerFelt = core_simu.x.index(core.symbols('qHammerFelt'))
#        x0[iqHammerFelt] = qh0  # (m)
#
#        # Initialize the simulation
#        simu.init(u=sequ(), x0=x0, nt=nt)
#
#        # Proceed
#        simu.process()
#
#        wave_path = os.path.join(here, 'PickupOut_{}={}'.format('vHammer',
#                                                                str(v_hammer)))
#        simu.data.wavwrite('y', order[1], path=wave_path)
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
