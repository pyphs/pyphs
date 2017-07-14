#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 10 23:48:24 2017

@author: Falaize
"""

import numpy as np
import os
from pyphs import Netlist
from pyphs.graphs import datum

x = np.linspace(-4, 4, 20)
x.put(list(x<0).index(False), 0)
y = x**3

path = os.path.realpath(__file__)[:os.path.realpath(__file__).rfind(os.sep)]


netlist_name = 'pwl'
data_name = 'data'
data_path = os.path.join(path, data_name + '.pwl')


def generate_data():
    #path = os.path.join(os.getcwd(), data_path)
    
    np.savetxt(data_path, np.vstack((x, y)))

    
def generate_netlist():
    netlist_path = os.path.join(path, netlist_name + '.net')
    netlist = Netlist(netlist_path, clear=True)
    
    netlist_line = {'dictionary': 'pwl',
                    'component': 'storage',
                    'label': 'stor',
                    'arguments': {'file': repr(data_path),
                                  'ctrl': 'e',
                                  'integ': True},
                    'nodes': ('N1', 'N2')}
    netlist.add_line(netlist_line)
    
    netlist_line = {'dictionary': 'pwl',
                    'component': 'dissipative',
                    'label': 'diss',
                    'arguments': {'file': repr(data_path),
                                  'ctrl': 'f'},
                    'nodes': (datum, 'N1')}
    netlist.add_line(netlist_line)

    netlist_line = {'dictionary': 'electronics',
                    'component': 'source',
                    'label': 'IN',
                    'arguments': {'type': 'voltage',
                                  'ctrl': 'f'},
                    'nodes': (datum, 'N2')}
    netlist.add_line(netlist_line)


    netlist.write()
