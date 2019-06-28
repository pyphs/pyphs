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
from ..tools import componentDoc, parametersDefault
from ..mechanics import metadata as dicmetadata
from pyphs.misc.rst import equation

from ..tools import symbols
from .tools import pwl_func, data_generator


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
                'file': path,
                'link': None}
        N1, N2 = nodes

        # edge
        edge = (N1, N2, data)

        # init component
        self += edges.StorageNonLinear(label, [edge], x, h, **kwargs)

    metadata = {'title': 'PWL Storage',
                'component': 'Storage',
                'label': 'stor',
                'dico': 'pwl',
                'desc': r'Piecewise-linear SISO storage component based on the PWL interpolation proposed in [1]_, (eq (2), known as the *Chua* interpolation). The file pointed by `file` argument should contains two lines, each blank separated list of floats for (x, H) or (x, dxH) values. If (x, dxH) values are provided, the resulting interpolation must be integrated to yield a (x, H) mapping  (see `integrate` parameter below).',
                'nodesdesc': "Positive flux N1->N2.",
                'nodes': ('N1', 'N2'),
                'parametersdesc': 'Component parameter.',
                'parameters': [['file', "Path to data file for (x, H) or (x, dxH) values", 'string', 'example.txt'],
                               ['integrate', "If True, data is (x, dxH) and integrate to (x, H)", 'bool', False],
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
