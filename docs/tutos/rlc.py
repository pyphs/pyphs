#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 21:08:37 2016

@author: Falaize
"""

import pyphs


def rlc():
    phs = pyphs.PortHamiltonianObject(label='rlc',
                                      path='cwd')
    
    datum = phs.graph.netlist.datum
    source = {'dictionary': 'electronics',
              'component': 'source',
              'label': 'out',
              'nodes': (datum, 'A'),
              'arguments': {'type': "'voltage'"}}
    phs.graph.netlist.add_line(source)
    # resistor
    resistance = {'dictionary': 'electronics',
                  'component': 'resistor',
                  'label': 'R',
                  'nodes': ('A', 'B'),
                  'arguments': {'R': ('R', 1e3)}}
    phs.graph.netlist.add_line(resistance)
    
    # inductor
    inductor = {'dictionary': 'electronics',
                'component': 'inductor',
                'label': 'L',
                'nodes': ('B', 'C'),
                'arguments': {'L': ('L', 5e-2)}}
    phs.graph.netlist.add_line(inductor)
    
    # capacitor
    capacitor = {'dictionary': 'electronics',
                 'component': 'capacitor',
                 'label': 'C',
                 'nodes': ('C', datum),
                 'arguments': {'C': ('C', 2e-6)}}
    phs.graph.netlist.add_line(capacitor)
    phs.graph.netlist.write('rlc.net')
    phs.build_from_netlist('rlc.net')  
    return phs
