#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 11:45:10 2017

@author: Falaize
"""

from pyphs import Netlist
from numpy import array
import os

# -----------------------------  CORES  ------------------------------------- #
this_script = os.path.realpath(__file__)
here = this_script[:this_script.rfind(os.sep)]


def netlist_path(label):
    return here + os.sep + label + '.net'


def sort_outputs(core):
    for i in range(core.dims.y()):
        if not str(core.y[i]).endswith(str(i+1)):
            core.move_port([str(y).endswith(str(i+1)) for y in core.y].index(True), i)

# build simple Cores
net1 = Netlist(netlist_path('phs1'))
c1 = net1.to_core()
sort_outputs(c1)
net2 = Netlist(netlist_path('phs2'))
c2 = net2.to_core()
sort_outputs(c2)

# concatenate c1 and c2 into a new Core
core = c1 + c2
# define the connection
core.add_connector((core.y.index(c1.y[1]), core.y.index(c2.y[1])),
                alpha=1)

# apply the connection
core.connect()

# target structure matrix
target = array([[0, -1, 1, 0],
                [1, 0, 0, -1],
                [-1, 0, 0, 0],
                [0, 1, 0, 0]])

assert all(map(lambda x: not x, array(array(core.M) - target).flatten())), '{}\n\n{}'.format(core.M, target)
