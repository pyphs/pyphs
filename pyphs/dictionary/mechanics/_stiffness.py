# -*- coding: utf-8 -*-
"""
Created on Sat May 21 16:29:43 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function
from ..edges import StorageLinear
from ..tools import componentDoc, parametersDefault
from ..mechanics import metadata as dicmetadata
from pyphs.misc.rst import equation


class Stiffness(StorageLinear):

    def __init__(self, label, nodes, **kwargs):

        parameters = parametersDefault(self.metadata['parameters'])
        parameters.update(kwargs)

        par_name = 'K'
        par_val = parameters[par_name]

        kwargs = {'name': par_name,
                  'value': par_val,
                  'inv_coeff': False,
                  'ctrl': 'e'}
        StorageLinear.__init__(self, label, nodes, **kwargs)

    metadata = {'title': 'Stiffness',
                'component': 'Stiffness',
                'label': 'stiff',
                'dico': 'mechanics',
                'desc': r'Linear stiffness between two points in a 1D space. In Laplace domain with :math:`s\in\mathbb C`:' + equation(r'f(s) = \frac{K\,e(s)}{s}.'),
                'nodesdesc': "Mechanical points associated with the stiffness endpoints with positive flux P1->P2.",
                'nodes': ('P1', 'P2'),
                'parametersdesc': 'Component parameter.',
                'parameters': [['K', "Mechanical stiffness", 'N/m', 1e3]],
                'refs': {},
                'nnodes': 2,
                'nedges': 1,
                'flux': dicmetadata['flux'],
                'effort': dicmetadata['effort'],
                }

    __doc__ = componentDoc(metadata)
