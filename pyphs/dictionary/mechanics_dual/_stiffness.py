#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 23:48:29 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function
from ..edges import StorageLinear
from ..tools import componentDoc, parametersDefault
from ..mechanics_dual import metadata as dicmetadata
from pyphs.misc.rst import equation


class Stiffness(StorageLinear):

    def __init__(self, label, nodes, **kwargs):
        par_name = 'K'
        par_val = kwargs[par_name]
        kwargs = {'name': par_name,
                  'value': par_val,
                  'inv_coeff': False,
                  'ctrl': 'f'}
        StorageLinear.__init__(self, label, nodes, **kwargs)

    metadata = {'title': 'Stiffness',
                'component': 'Stiffness',
                'label': 'stiff',
                'dico': 'mechanics_dual',
                'desc': r'Linear stiffness between two points in a 1D space. In Laplace domain with :math:`s\in\mathbb C`:' + equation(r'e(s) = \frac{K\,f(s)}{s}.'),
                'nodesdesc': "Nodes associated with the component terminals with positive flux N1->N2.",
                'nodes': ('N1', 'N2'),
                'parametersdesc': 'Component parameter.',
                'parameters': [['K', "Mechanical stiffness", 'N/m', 1e3]],
                'refs': {},
                'nnodes': 2,
                'nedges': 1,
                'flux': dicmetadata['flux'],
                'effort': dicmetadata['effort'],
                }

    __doc__ = componentDoc(metadata)
