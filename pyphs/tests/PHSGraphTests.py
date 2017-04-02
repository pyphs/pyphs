#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 15:14:26 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

from pyphs import PHSGraph
from pyphs.tests.data import NetlistThieleSmallNL
from pyphs.config import datum as config_datum
import numpy as np

netlist = NetlistThieleSmallNL()
graph = PHSGraph(netlist=netlist)

symbols = graph.core.symbols


target_edges = [('A', config_datum,
                 {'ctrl': 'f',
                  'label': graph.core.symbols('yIN'),
                  'link': None,
                  'type': 'port'}),
                ('A', 'B',
                 {'ctrl': '?',
                  'label': graph.core.symbols('wR'),
                  'link': None,
                  'type': 'dissipative',
                  'z': {'e_ctrl': symbols('wR')/symbols('R'),
                        'f_ctrl': symbols('R')*symbols('wR')}}),
                ('B', 'C',
                 {'ctrl': 'e',
                  'label': symbols('xL'),
                  'link': None, 'type': 'storage'}),
                ('E', 'F',
                 {'ctrl': 'f',
                  'label': symbols('xK'),
                  'link': None, 'type': 'storage'}),
                ('D', config_datum,
                 {'alpha': None,
                  'connector_type': 'gyrator',
                  'ctrl': '?',
                  'label': symbols('yG2'),
                  'link': symbols('yG1'),
                  'type': 'connector'}),
                ('D', 'E',
                 {'ctrl':
                  'e', 'label': symbols('xM'),
                  'link': None, 'type': 'storage'}),
                ('F', config_datum,
                 {'ctrl': '?',
                  'label': symbols('wA'),
                  'link': None,
                  'type': 'dissipative',
                  'z': {'e_ctrl': symbols('wA')/symbols('A'),
                        'f_ctrl': symbols('A')*symbols('wA')}}),
                ('C', config_datum,
                 {'alpha': symbols('Bl'),
                  'connector_type': 'gyrator',
                  'ctrl': '?',
                  'label': symbols('yG1'),
                  'link': symbols('yG2'),
                  'type': 'connector'})]
target_edges.sort()

target_M = np.array([
                    [0, +1.0*symbols('Bl'), -1.0, 0, -1.0, 0],
                    [-1.0*symbols('Bl'), 0, 0, -1.0, 0, 1.0],
                    [1.0, 0, 0, 0, 0, 0],
                    [0, 1.0, 0, 0, 0, 0],
                    [1.0, 0, 0, 0, 0, 0],
                    [0, -1.0, 0, 0, 0, 0]])


def split_sp():
    netlist = NetlistThieleSmallNL()
    graph = PHSGraph(netlist=netlist)
    graph.split_sp()
    return True
