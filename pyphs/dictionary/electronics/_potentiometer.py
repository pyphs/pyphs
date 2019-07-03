#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 00:06:10 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

from ..tools import symbols
from ..edges import DissipativeNonLinear
from ..tools import componentDoc, parametersDefault
from ..electronics import metadata as dicmetadata


class Potentiometer(DissipativeNonLinear):

    def __init__(self, label, nodes, **kwargs):
        parameters = parametersDefault(self.metadata['parameters'])
        parameters.update(kwargs)
        # parameters
        pars = ['R', 'A', 'E']
        for par in pars:
            assert par in parameters.keys()
        R, A, E = symbols(pars)
        # dissipation variable
        w = symbols(["w"+label+str(i) for i in (1, 2)])
        # dissipation funcion
        R1 = 1 + R*A**E
        R2 = 1 + R*(1-A**E)
        z = [R1*w[0], R2*w[1]]

        N1, N2, N3 = nodes
        # edges
        data_1 = {'label': w[0],
                  'type': 'dissipative',
                  'z': {'e_ctrl': w[0]/R1,
                        'f_ctrl': R1*w[0]},
                  'ctrl': '?',
                  'link': None}
        edge_1 = (N1, N2, data_1)

        # edges
        data_2 = {'label': w[1],
                  'type': 'dissipative',
                  'z': {'e_ctrl': w[1]/R2,
                        'f_ctrl': R2*w[1]},
                  'ctrl': '?',
                  'link': None}
        edge_2 = (N2, N3, data_2)

        # init component
        DissipativeNonLinear.__init__(self, label,
                                         [edge_1, edge_2],
                                         w, z, **parameters)

    metadata = {'title': 'Potentiometer',
                'component': 'Potentiometer',
                'label': 'pot',
                'dico': 'electronics',
                'desc': 'Potentiometer, i.e. two connected resistors with inverse varying resistance.',
                'nodesdesc': "Resitances are: :math:`R_{12}=1 + R\,A^E` and :math:`R_{23}=1 + R\,(1-A^E)`.",
                'nodes': ('N1', 'N2', 'N3'),
                'parameters': [['R', 'Total resistance', 'Ohms', 1e5],
                               ['A', 'Label for parameter', 'string', 'alpha'],
                               ['E', 'Exponent', 'd.u.', 1.]],
                'refs': {},
                'nnodes': 3,
                'nedges': 2,
                'flux': dicmetadata['flux'],
                'effort': dicmetadata['effort'],
                }

    # Write documentation
    __doc__ = componentDoc(metadata)
