#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 11:45:10 2017

@author: Falaize
"""

from pyphs import netlist2core
from numpy import array
# build simple PHSCores
c1 = netlist2core('phs1.net')
print('c1.M={}'.format(c1.M))

c2 = netlist2core('phs2.net')
print('c2.M={}'.format(c2.M))

# concatenate c1 and c2 into a new phscore
c = c1 + c2

# define the connection
connector = {'u': (c1.u[1], c2.u[1]),
             'y': (c1.y[1], c2.y[1]),
             'alpha': 1.}

# add the connector to the PHSCore
c.add_connector(connector)

# apply the connection
c.apply_connectors()

# target structure matrix
target = array([[0, 1], [-1, 0]])
assert all(map(lambda x: not x, array(c.M - target).flatten()))
