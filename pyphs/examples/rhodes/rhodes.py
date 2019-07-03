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
# if __name__ == '__main__':
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
#
#    # array with shape (core.dims.x(), )
#    x0 = sympify([0, ] * method.dims.x())
#
#    # ---------------------------------------------------------------------------
#    # Init Hammer velocity:
#    # The prescibed hammer velocity (m.s^-1) has to be converted to
#    # momentum (N.s) wich is the dimension of the state of the hammer mass to be
#    # initialized. For efficiency when simulating with several initial hammer
#    # velocity, this init value is not hard coded.
#
#    # Define new symbols
#    hammer_V_symb = core.symbols('Vhammer')
#    hammer_M_symb = core.symbols('Mhammer')
#
#    # `xHammerMass` is the state p associated with the hammer mass
#    # Store expression pinit = m * vinit
#    index = method.index('x', 'xHammerMass')
#    x0[index] = hammer_M_symb * hammer_V_symb
#
#    # Store a dummy substitution value to be updated
#    method.subs[hammer_V_symb] = list_v_hammer[0]
#
#    # ---------------------------------------------------------------------------
#    # Init Hammer's initial position w.r.t contact:
#    # The time between simulation start and impact of the hammer on the beam
#    # is kept constant by defining the initial position as qinit = -tinit * vinit
#
#    # Time between simulation start and impact
#    tinit = 2e-2  # [s]
#
#    # Store substitution value
#    tinit_symb = core.symbols('tinit')
#    method.subs[tinit_symb] = tinit
#
#    # Store expression qinit = -tinit * vinit
#    qh0 = -tinit_symb * hammer_V_symb  # (m)
#    iqHammerFelt = method.x.index(core.symbols('qHammerFelt'))
#    x0[iqHammerFelt] = qh0  # (m)
#
#    # ---------------------------------------------------------------------------
#    # Init SIMULATION
#
#    # define dynamic dicitonary of substitutions
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
#    # def sequence of inputs to feed in the Simulation
#    sequ = [numpy.array([[0., 1.][i] for i in order]) for _ in t]
#
#    # ---------------------------  LOOP  --------------------------------
#    # list of signals to be concatenated
#    signals = list()
#
#    # path to folder where to write .wav files
#    waves_path = os.path.join(here, 'waves')
#
#    # create folder where to write .wav files
#    if not os.path.exists(waves_path):
#        os.mkdir(waves_path)
#
#    # for each hammer load
#    for v_hammer in list_v_hammer:
#
#        # update hammer load
#        subs[hammer_V_symb] = v_hammer
#
#        # Initialize the simulation with updated hammer load
#        simu.init(u=sequ,
#                  nt=nt,
#                  subs=subs)
#
#        # Proceed
#        simu.process()
#
#        # Write signal as .wav file
#        wave_name = 'PickupOut_{}={}'.format('vHammer', str(v_hammer))
#        simu.data.wavwrite('y', order[1],
#                           path=os.path.join(waves_path, wave_name))
#
#        # append signal to concatenated signals
#        signals += list(simu.data.y(vslice=order[1]))
#
#        # Plot signal
#        # simu.data.plot([('x', 0), ('dtx', 0), ('y', order[0])],
#        #                label=str(v_hammer))
#
#    # Write concatenated signals as .wav file
#    wavwrite(signals, simu.config['fs'],
#             path=os.path.join(waves_path, 'PickupOut'),
#             normalize=True)
