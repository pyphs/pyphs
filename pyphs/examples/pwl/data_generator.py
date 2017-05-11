#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 10 23:48:24 2017

@author: Falaize
"""

import numpy as np
import os
from pyphs import PHSNetlist
from pyphs.graphs import datum

x = np.linspace(-4, 4, 11)
y = x**3

data_name = 'data'
data_path = data_name + '.pwl'
#path = os.path.join(os.getcwd(), data_path)

np.savetxt(data_path, np.vstack((x, y)))

netlist_path = os.path.join(os.getcwd(), 'pwl.net')
netlist = PHSNetlist(netlist_path, clear=True)

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
netlist.write()
