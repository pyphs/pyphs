#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 00:12:24 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import numpy as np
from .. import edges
from pyphs import Graph
from pyphs.misc.io import data_generator
from ..tools import symbols
from .tools import pwl_func


class Storage(Graph):
    def __init__(self, label, nodes, **kwargs):

        # instanciate a Graph object
        Graph.__init__(self, label=label)

        assert 'file' in kwargs, "pwl.storage component need 'file' argument"
        path = kwargs.pop('file')
        vals = np.vstack(map(np.array, data_generator(path)))
        x_vals = vals[0, :]
        h_vals = vals[1, :]

        assert all(h_vals[np.nonzero(x_vals >= 0)] >= 0), 'All values h(x) for\
 x>=0 must be non-negative (component {})'.format(label)

        if kwargs['integ']:
            assert all(h_vals[np.nonzero(x_vals < 0)] < 0), 'All values dxh(x)\
 for x<0 must be negative (component {})'.format(label)
        else:
            assert all(h_vals[np.nonzero(x_vals < 0)] >= 0), 'All values h(x)\
 for x<0 must be non-negative (component {})'.format(label)

        assert h_vals[np.nonzero(x_vals == 0)] == 0, 'dxh(0) and h(0) must be \
zero (component {})'.format(label)

        ctrl = kwargs.pop('ctrl')

        # state  variable
        x = symbols("x"+label)
        # storage funcion
        h = pwl_func(x_vals, h_vals, x, **kwargs)

        # edge data
        data = {'label': x,
                'type': 'storage',
                'ctrl': ctrl,
                'link': None}
        N1, N2 = nodes

        # edge
        edge = (N1, N2, data)

        # init component
        self += edges.StorageNonLinear(label, [edge], x, h, **kwargs)

    @staticmethod
    def metadata():
        return {'nodes': ('N1', 'N2'),
                'arguments': {'integ': False}}
