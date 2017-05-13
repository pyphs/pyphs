#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 11:45:10 2017

@author: Falaize
"""

from pyphs import netlist2core
from numpy import array
import os

# -----------------------------  CORES  ------------------------------------- #
this_script = os.path.realpath(__file__)
here = this_script[:this_script.rfind(os.sep)]


def netlist_path(label):
    return here + os.sep + label + '.net'

# build simple PHSCores
c1 = netlist2core(netlist_path('phs1'))
c2 = netlist2core(netlist_path('phs2'))

# concatenate c1 and c2 into a new PHSCore
c = c1 + c2

# define the connection
c.add_connector((c.y.index(c2.y[1]), c.y.index(c1.y[1])), 
                alpha=1)

# apply the connection
c.apply_connectors()

# target structure matrix
target = array([[0, -1, 1, 0],
                [1, 0, 0, 1],
                [-1, 0, 0, 0],
                [0, -1, 0, 0]])

assert all(map(lambda x: not x, array(c.M - target).flatten()))
