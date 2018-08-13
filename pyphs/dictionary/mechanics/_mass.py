# -*- coding: utf-8 -*-
"""
Created on Sat May 21 16:29:43 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function
from ..edges import StorageLinear
from pyphs.graphs import datum
from ..tools import componentDoc, parametersDefault
from ..mechanics import metadata as dicmetadata
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
                  'ctrl': 'f'}
        StorageLinear.__init__(self, label, (datum, nodes[0]), **kwargs)

    metadata = {'title': 'Mass',
                'component': 'Mass',
                'label': 'mass',
                'dico': 'mechanics',
                'desc': r'Mass moving in 1D space. In Laplace domain with :math:`s\in\mathbb C`:' + equation(r'e(s) = \frac{f(s)}{M\,s}.'),
                'nodesdesc': "Mechanical point associated with the mass. The velocity is measured from a reference point with edge datum->P.",
                'nodes': ('P', ),
                'parametersdesc': 'Component parameter.',
                'parameters': [['M', "Mechanical mass", 'kg', 1e-2]],
                'refs': {},
                'nnodes': 2,
                'nedges': 1,
                'flux': dicmetadata['flux'],
                'effort': dicmetadata['effort'],
                }

    __doc__ = componentDoc(metadata)
