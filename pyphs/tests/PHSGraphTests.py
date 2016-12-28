#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 15:14:26 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

from pyphs import PHSGraph
from .data import NetlistThieleSmallNL
from pyphs.config import datum as config_datum
import numpy as np

netlist = NetlistThieleSmallNL()
graph = PHSGraph(netlist=netlist)

target_edges = [('A', config_datum,
                 {'ctrl': 'f',
                  'label': graph.Core.symbols('yIN'),
                  'link': None,
                  'type': 'port'}),
                ('A', 'B',
                 {'ctrl': '?',
                  'label': graph.Core.symbols('wR'),
                  'link': None,
                  'type': 'dissipative',
                  'z': {'e_ctrl': graph.Core.symbols('wR')/graph.Core.symbols('R'),
                        'f_ctrl': graph.Core.symbols('R')*graph.Core.symbols('wR')}}),
                ('B', 'C',
                 {'ctrl': 'e',
                 'label': graph.Core.symbols('xL'),
                 'link': None, 'type': 'storage'}),
                 ('E', 'F',
                  {'ctrl': 'f',
                  'label': graph.Core.symbols('xK'),
                  'link': None, 'type': 'storage'}),
                 ('D', config_datum,
                  {'alpha': graph.Core.symbols('G_alpha'),
                  'connector_type': 'gyrator',
                  'ctrl': '?',
                  'label': 'yG2',
                  'link': 'yG1',
                  'type': 'connector'}),
                 ('D', 'E',
                  {'ctrl':
                   'e', 'label': graph.Core.symbols('xM'),
                   'link': None, 'type': 'storage'}),
                ('F', config_datum,
                 {'ctrl': '?',
                 'label': graph.Core.symbols('wA'),
                 'link': None,
                 'type': 'dissipative',
                 'z': {'e_ctrl': graph.Core.symbols('wA')/graph.Core.symbols('A'),
                       'f_ctrl': graph.Core.symbols('A')*graph.Core.symbols('wA')}}),
                ('C', config_datum,
                 {'alpha': graph.Core.symbols('G_alpha'),
                  'connector_type': 'gyrator',
                  'ctrl': '?',
                  'label': 'yG1',
                  'link': 'yG2',
                  'type': 'connector'})]

target_M = np.array([
                    [0, -1.0*graph.Core.symbols('G_alpha'), -1.0, 0, -1.0, 0],
                    [1.0*graph.Core.symbols('G_alpha'), 0, 0, -1.0, 0, 1.0],
                    [1.0, 0, 0, 0, 0, 0],
                    [0, 1.0, 0, 0, 0, 0],
                    [1.0, 0, 0, 0, 0, 0],
                    [0, -1.0, 0, 0, 0, 0]])
