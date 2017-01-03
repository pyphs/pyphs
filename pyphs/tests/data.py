#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 18:25:04 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import os
from pyphs import PHSNetlist


def NetlistThieleSmallNL(label='TSnl', clear=True,
                         R=1e3, L=5e-2, Bl=50, M=0.1, K=5e3, A=1):
    """
    Write the netlist for a nonlinear version of the thieleSmall modeling of \
    loudspeakers.
    """

    netlist = PHSNetlist(os.getcwd() + os.sep + label + '.net', clear=clear)

    datum = netlist.datum

    # input voltage
    source = {'dictionary': 'electronics',
              'component': 'source',
              'label': 'IN',
              'nodes': ('A', datum),
              'arguments': {'type': "voltage"}}
    netlist.add_line(source)

    # resistor 1
    resistance = {'dictionary': 'electronics',
                  'component': 'resistor',
                  'label': 'R',
                  'nodes': ('A', 'B'),
                  'arguments': {'R': ('R', R)}}
    netlist.add_line(resistance)

    # inductor
    inductor = {'dictionary': 'electronics',
                'component': 'inductor',
                'label': 'L',
                'nodes': ('B', 'C'),
                'arguments': {'L': ('L', L)}}
    netlist.add_line(inductor)

    # gyrator
    gyrator = {'dictionary': 'connectors',
               'component': 'gyrator',
               'label': 'G',
               'nodes': ('C', datum, 'D', datum),
               'arguments': {'alpha': ('Bl', Bl)}}
    netlist.add_line(gyrator)

    # masse
    mass = {'dictionary': 'mechanics',
            'component': 'mass',
            'label': 'M',
            'nodes': ('D', 'E'),
            'arguments': {'M': ('M', M)}}
    netlist.add_line(mass)

    # ressort cubic
    stifness = {'dictionary': 'mechanics',
                'component': 'springcubic',
                'label': 'K',
                'nodes': ('E', 'F'),
                'arguments': {'K0': ('K0', K),
                              'K2': ('K2', 1e20)}
                }
    netlist.add_line(stifness)

    # amortissement
    damper = {'dictionary': 'mechanics',
              'component': 'damper',
              'label': 'A',
              'nodes': ('F', datum),
              'arguments': {'A': ('A', A)}}
    netlist.add_line(damper)

    return netlist
