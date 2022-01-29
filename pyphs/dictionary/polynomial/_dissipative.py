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
from .. import common
from pyphs import Graph
from ..tools import componentDoc, parametersDefault
from . import metadata as dicmetadata
from pyphs.misc.rst import equation

from ..tools import symbols
from .tools import polynomial

here = os.path.realpath(__file__)[:os.path.realpath(__file__).rfind(os.sep)]


class Dissipative(Graph):

    def __init__(self, label, nodes, **kwargs):

        # instanciate a Graph object
        Graph.__init__(self, label=label)

        ctrl = kwargs.pop('ctrl')

        max_degree = 0
        for c in kwargs:
            i = int(c[1:])
            max_degree = max((max_degree, i))

        coeffs = [sp.sympify(0.0) for _ in range(max_degree+1)]
        for c in kwargs:
            i = int(c[1:])
            coeffs[i] = symbols(c)

        assert len(coeffs) > 0

        # state  variable
        w = symbols("w"+label)

        # dissipative funcion
        z = polynomial(w, coeffs)

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
        self += common.DissipativeNonLinear(label, [edge, ], w, z, **kwargs)

    metadata = {'title': 'Polynomial Dissipation',
                'component': 'Dissipative',
                'label': 'polydiss',
                'dico': 'polynomial',
                'desc': r'Polynomial SISO dissipative component.',
                'nodesdesc': "Positive flux N1->N2.",
                'nodes': ('N1', 'N2'),
                'parametersdesc': 'Component parameter.',
                'parameters': [['ctrl', "Controlled quantity in {'e', 'f'} (effort or flux).", 'string', 'e'],
                               ['c0', "Constant", 'd.u.', 2.5],
                               ['c1', "Coefficient of linear monomial", 'd.u.', 3.],
                               ['c2', "Coefficient of linear monomial", 'd.u.', 4.2]],
                'refs': {},
                'nnodes': 2,
                'nedges': 1,
                'flux': dicmetadata['flux'],
                'effort': dicmetadata['effort'],
                }

    __doc__ = componentDoc(metadata)
