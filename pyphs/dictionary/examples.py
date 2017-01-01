#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 21:08:37 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import pyphs
import os


def rlc():
    netlist = pyphs.PHSNetlist(os.getcwd() + os.sep + 'rlc.net')

    datum = netlist.datum
    source = {'dictionary': 'electronics',
              'component': 'source',
              'label': 'out',
              'nodes': (datum, 'A'),
              'arguments': {'type': "'voltage'"}}
    netlist.add_line(source)
    # resistor
    resistance = {'dictionary': 'electronics',
                  'component': 'resistor',
                  'label': 'R',
                  'nodes': ('A', 'B'),
                  'arguments': {'R': ('R', 1e3)}}
    netlist.add_line(resistance)

    # inductor
    inductor = {'dictionary': 'electronics',
                'component': 'inductor',
                'label': 'L',
                'nodes': ('B', 'C'),
                'arguments': {'L': ('L', 5e-2)}}
    netlist.add_line(inductor)

    # capacitor
    capacitor = {'dictionary': 'electronics',
                 'component': 'capacitor',
                 'label': 'C',
                 'nodes': ('C', datum),
                 'arguments': {'C': ('C', 2e-6)}}
    netlist.add_line(capacitor)
    netlist.write()
    graph = pyphs.PHSGraph(netlist=netlist)
    return graph
