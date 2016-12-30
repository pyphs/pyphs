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
                  'z': {'e_ctrl': graph.core.symbols('wR')/graph.core.symbols('R'),
                        'f_ctrl': graph.core.symbols('R')*graph.core.symbols('wR')}}),
                ('B', 'C',
                 {'ctrl': 'e',
                 'label': graph.core.symbols('xL'),
                 'link': None, 'type': 'storage'}),
                 ('E', 'F',
                  {'ctrl': 'f',
                  'label': graph.core.symbols('xK'),
                  'link': None, 'type': 'storage'}),
                 ('D', config_datum,
                  {'alpha': graph.core.symbols('Bl'),
                  'connector_type': 'gyrator',
                  'ctrl': '?',
                  'label': 'yG2',
                  'link': 'yG1',
                  'type': 'connector'}),
                 ('D', 'E',
                  {'ctrl':
                   'e', 'label': graph.core.symbols('xM'),
                   'link': None, 'type': 'storage'}),
                ('F', config_datum,
                 {'ctrl': '?',
                 'label': graph.core.symbols('wA'),
                 'link': None,
                 'type': 'dissipative',
                 'z': {'e_ctrl': graph.core.symbols('wA')/graph.core.symbols('A'),
                       'f_ctrl': graph.core.symbols('A')*graph.core.symbols('wA')}}),
                ('C', config_datum,
                 {'alpha': graph.core.symbols('Bl'),
                  'connector_type': 'gyrator',
                  'ctrl': '?',
                  'label': 'yG1',
                  'link': 'yG2',
                  'type': 'connector'})]
target_edges.sort()

target_M = np.array([
                    [0, -1.0*graph.core.symbols('Bl'), -1.0, 0, -1.0, 0],
                    [1.0*graph.core.symbols('Bl'), 0, 0, -1.0, 0, 1.0],
                    [1.0, 0, 0, 0, 0, 0],
                    [0, 1.0, 0, 0, 0, 0],
                    [1.0, 0, 0, 0, 0, 0],
                    [0, -1.0, 0, 0, 0, 0]])
