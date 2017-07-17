#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 11 11:17:07 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import os
from pyphs import Netlist, Graph

# ---------------------------  NETLIST  ------------------------------------- #
label = 'piano_hammer'
this_script = os.path.realpath(__file__)
here = this_script[:this_script.rfind(os.sep)]
netlist_filename = here + os.sep + label + '.net'
netlist = Netlist(netlist_filename)


# ---------------------------  GRAPH  --------------------------------------- #
graph = Graph(netlist=netlist)


# ---------------------------  CORE  ---------------------------------------- #
core = graph.to_core()


## ---------------------------  SIMULATION  ---------------------------------- #
#if __name__ == '__main__':
#
#    import numpy
#    import matplotlib.pyplot as plt
#    from pyphs import Simulation
#
#    core.reduce_z()
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
#    simu = Simulation(core.to_method(), config=config)
#
#    def ordering(name, *args):
#        def get_index(e):
#            symb = simu.nums.method.symbols(e)
#            return getattr(simu.nums.method, name).index(symb)
#        return list(map(get_index, args))
#
#    order = ordering('y', 'ycontact')
#
#    # def simulation time
#    tmax = 1e-1
#    nmax = int(tmax*simu.config['fs'])
#    t = [n/simu.config['fs'] for n in range(nmax)]
#    nt = len(t)
#    vin_max = 2  # [m/s] Maximal initial velocity of the hammer
#    sig = list()
#
#    # ---------------------------  LOOP  --------------------------------
#    # def generator for sequence of inputs to feed in the Simulation object
#    def sequ():
#        """
#        generator of input sequence for Simulation
#        """
#        for tn in t:
#            # numpy.array([u1, u2, ...])
#            yield numpy.array([[0., 1.][i] for i in order])
#
#    # state initialization
#    # !!! must be array with shape (core.dims.x(), )
#    x0 = numpy.array([0., ]*core.dims.x())
#
#    # shortcut to core method
#    core_simu = simu.nums.method
#
#    plt.close('all')
#
#    def velocities(vmax):
#        """
#        return a list of 5 equally spaced velocities between 0 and vmax
#        """
#        return numpy.linspace(0, vmax, 6)[1:]
#
#    vmax = 1.
#    for v_hammer in velocities(vmax):
#        # Init Hammer velocity
#        # v_hammer = 1  # Hammer velocity (m/s)
#        symbol_hammer_mass = core.symbols('Mhammer')
#        m_hammer = core.subs[symbol_hammer_mass]  # Hammer mass (kg)
#        # Set mass momentum (N.s)
#        x0[core_simu.x.index(core.symbols('xmass'))] = v_hammer * m_hammer
#
#        tinit = 2e-2  # [s] time between init of velocity and impact
#        qh0 = -v_hammer*tinit  # [m] Hammer's initial position w.r.t contact
#        iqfelt = core_simu.x.index(core.symbols('qfelt'))
#        x0[iqfelt] = qh0  # (m)
#
#        # Initialize the simulation
#        simu.init(u=sequ(), x0=x0, nt=nt)
#
#        # Proceed
#        simu.process()
#
#        q = numpy.array(list(simu.data.x(iqfelt)))
#        y = numpy.array(list(simu.data.y(0)))
#
#        indices = numpy.nonzero(q >= 0)
#        q = numpy.array(q)[indices]
#        y = numpy.array(y)[indices]
#
#        plt.plot(q, y, label=r'$v_0=%.1f$ m.s$^{-1}$' % v_hammer)
#        plt.grid('on')
#        plt.grid(which='minor')
#        plt.xlabel('Felt crush (m)')
#        plt.ylabel('Contact force (N)')
#        plt.legend(fontsize=15)
#        plt.title('Felt force-compression characteristic')
