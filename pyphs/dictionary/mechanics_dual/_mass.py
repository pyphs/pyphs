#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 23:49:05 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function
from ..edges import StorageLinear
from ..tools import componentDoc, parametersDefault
from ..mechanics_dual import metadata as dicmetadata
from pyphs.misc.rst import equation


class Mass(StorageLinear):

    def __init__(self, label, nodes, **kwargs):

        parameters = parametersDefault(self.metadata['parameters'])
        parameters.update(kwargs)

        par_name = 'M'
        par_val = parameters[par_name]
        kwargs = {'name': par_name,
                  'value': par_val,
                  'inv_coeff': True,
                  'ctrl': 'e'}
        StorageLinear.__init__(self, label, (nodes[0], nodes[1]), **kwargs)

    metadata = {'title': 'Mass',
                'component': 'Mass',
                'label': 'mass',
                'dico': 'mechanics_dual',
                'desc': r'Mass moving in 1D space. In Laplace domain with :math:`s\in\mathbb C`:' + equation(r'f(s) = \frac{e(s)}{M\,s}.'),
                'nodesdesc': "Nodes associated with the component terminals with positive flux N1->N2.",
                'nodes': ('N1', 'N2'),
                'parametersdesc': 'Component parameter.',
                'parameters': [['M', "Mechanical mass", 'kg', 1e-2]],
                'refs': {},
                'nnodes': 2,
                'nedges': 1,
                'flux': dicmetadata['flux'],
                'effort': dicmetadata['effort'],
                }

    __doc__ = componentDoc(metadata)
