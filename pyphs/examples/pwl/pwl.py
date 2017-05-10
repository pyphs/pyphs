# -*- coding: utf-8 -*-
"""
Created on Wed May 10 23:48:24 2017

@author: Falaize

Use data_generator.py to generate a valid data.txt;
Uncomment below to regenerate the netlist.

"""


from pyphs import PHSNetlist, PHSGraph
from pyphs.graphs import datum
import os
import sympy as sp

label = 'PWL'
netlist_path = os.path.join(os.getcwd(), 'pwl.net')

#netlist = PHSNetlist(netlist_path, clear=True)
#
#data_name = 'data'
#data_path = os.path.join(os.getcwd(), data_name + '.txt')
#
#netlist_line = {'dictionary': 'pwl',
#                'component': 'storage',
#                'label': label + '_stor',
#                'arguments': {'file': repr(data_path),
#                              'ctrl': 'e',
#                              'integ': True},
#                'nodes': ('N1', 'N2')}
#netlist.add_line(netlist_line)
#
#netlist_line = {'dictionary': 'pwl',
#                'component': 'dissipative',
#                'label': label + '_diss',
#                'arguments': {'file': repr(data_path),
#                              'ctrl': 'f'},
#                'nodes': (datum, 'N1')}
#netlist.add_line(netlist_line)
#netlist.write()

graph = PHSGraph(netlist=netlist_path, label=label)
sp.plot(graph.core.H, (graph.core.x[0], -10, 10))
sp.plot(graph.core.z[0], (graph.core.w[0], -10, 10))
