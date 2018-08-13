#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 00:12:15 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import numpy as np
import sympy as sp
import os
from .. import edges
from pyphs import Graph
from ..tools import componentDoc, parametersDefault
from ..mechanics import metadata as dicmetadata
from pyphs.misc.rst import equation

from ..tools import symbols
from .tools import pwl_func, data_generator

here = os.path.realpath(__file__)[:os.path.realpath(__file__).rfind(os.sep)]


class Dissipative(Graph):

    def __init__(self, label, nodes, **kwargs):

        # instanciate a Graph object
        Graph.__init__(self, label=label)

        path = kwargs.pop('file')
        data = np.vstack(map(np.array, data_generator(path)))
        w_vals = data[0, :]
        z_vals = data[1, :]

        assert all(z_vals[np.nonzero(w_vals >= 0)] >= 0), 'All values z(w) for\
 w>=0 must be non-negative (component {})'.format(label)

        assert all(z_vals[np.nonzero(w_vals < 0)] < 0), 'All values z(w) for\
 w<0 must be negative (component {})'.format(label)

        assert all(z_vals[np.nonzero(w_vals == 0)] == 0), 'z(0) must be zero \
(component {})'.format(label)

        assert all(np.diff(z_vals) > 0), "z'(0) must be positive\
(component {})".format(label)

        ctrl = kwargs.pop('ctrl')

        # state  variable
        w = symbols("w"+label)
        # dissipative funcion
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

    metadata = {'title': 'PWL Dissipation',
                'component': 'Dissipative',
                'label': 'diss',
                'dico': 'pwl',
                'desc': r'Piecewise-linear SISO dissipative component based on the PWL interpolation proposed in [1]_, (eq (2), known as the *Chua* interpolation). The file pointed by `file` argument should contains two lines, each blank separated list of floats for (x, y) values.',
                'nodesdesc': "Positive flux N1->N2.",
                'nodes': ('N1', 'N2'),
                'parametersdesc': 'Component parameter.',
                'parameters': [['file', "Path to data file for (w, z) values", 'string', 'example.txt'],
                               ['start', "Index of first value", 'd.u.', None],
                               ['stop', "Index of last value", 'd.u.', None],
                               ['step', "step >= 1", 'd.u.', None]],
                'refs': {1 : 'Chua, L., & Ying, R. (1983). Canonical piecewise-linear analysis. IEEE Transactions on Circuits and Systems, 30(3), 125-140.'},
                'nnodes': 2,
                'nedges': 1,
                'flux': dicmetadata['flux'],
                'effort': dicmetadata['effort'],
                }

    __doc__ = componentDoc(metadata)
