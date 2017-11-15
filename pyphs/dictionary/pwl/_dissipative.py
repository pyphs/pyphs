#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 00:12:15 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import numpy as np
import sympy as sp
from .. import edges
from pyphs import Graph
from pyphs.misc.io import data_generator
from ..tools import symbols
from .tools import pwl_func


class Dissipative(Graph):
    def __init__(self, label, nodes, **kwargs):

        # instanciate a Graph object
        Graph.__init__(self, label=label)

        assert 'file' in kwargs, "pwl.dissipative component need 'file' argument"
        path = kwargs.pop('file')
        data = np.vstack(map(np.array, data_generator(path)))
        w_vals = data[0, :]
        z_vals = data[1, :]

        assert all(z_vals[np.nonzero(w_vals >= 0)] >= 0), 'All values z(w) for\
 w>=0 must be non-negative (component {})'.format(label)

        assert all(z_vals[np.nonzero(w_vals >= 0)] >= 0), 'All values z(w) for\
 w<0 must be negative (component {})'.format(label)

        assert all(z_vals[np.nonzero(w_vals == 0)] == 0), 'z(0) must be zero \
(component {})'.format(label)

        ctrl = kwargs.pop('ctrl')

        # state  variable
        w = symbols("w"+label)
        # storage funcion
        z = pwl_func(w_vals, z_vals, w, **kwargs)

        if ctrl == 'e':
            not_ctrl = 'f'
        else:
            assert ctrl == 'f'
            not_ctrl = 'e'

        # edge data
        data = {'label': w,
                'type': 'dissipative',
                'ctrl': ctrl,
                'z' : {ctrl+'_ctrl': z,
                       not_ctrl+'_ctrl': sp.sympify(0)},
                'link': None}
        N1, N2 = nodes

        # edge
        edge = (N1, N2, data)

        # init component
        self += edges.DissipativeNonLinear(label, [edge, ], w, z, **kwargs)

    @staticmethod
    def metadata():
        return {'nodes': ('N1', 'N2'),
                'arguments': {}}
