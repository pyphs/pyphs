#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 20:35:18 2018

@author: afalaize
"""

from __future__ import absolute_import, division, print_function

import os
from pyphs import Netlist
import matplotlib.pyplot as plt
plt.close('all')

# netlist is "{label}.net"
label = 'sp_circuit'

# get folder path
path = os.path.realpath(__file__)[:os.path.realpath(__file__).rfind(os.sep)]

# def filename
netlist_filename = os.path.join(path, '{0}.net'.format(label))

# read in Netlist object
netlist = Netlist(netlist_filename)

# Build Graph object
graph = netlist.to_graph()

graph.sp_split()

# Build Core object
core = graph.to_core(merge_all=True)
