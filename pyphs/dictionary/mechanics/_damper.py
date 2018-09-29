# -*- coding: utf-8 -*-
"""
Created on Sat May 21 16:29:43 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function
from ..edges import DissipativeLinear
from ..tools import componentDoc, parametersDefault
from ..mechanics import metadata as dicmetadata
from pyphs.misc.rst import equation


class Damper(DissipativeLinear):

    def __init__(self, label, nodes, **kwargs):
        parameters = parametersDefault(self.metadata['parameters'])
        parameters.update(kwargs)
        if parameters['A'] is None:
            coeff = 0.
        else:
            coeff = parameters['A']
        DissipativeLinear.__init__(self, label, nodes, coeff=coeff,
                                      inv_coeff=True)

    metadata = {'title': 'Linear Damper',
                'component': 'Damper',
                'label': 'damp',
                'dico': 'mechanics',
                'desc': r'Linear mechanical damping (i.e. opposing force proportional to the velocity). In Laplace domain with :math:`s\in\mathbb C`:' + equation(r'f(s) = A \, e(s).'),
                'nodesdesc': "Mechanical points associated with the damper endpoints with positive flux N1->N2.",
                'nodes': ('P1', 'P2'),
                'parametersdesc': 'Component parameter',
                'parameters': [['A', "Damping coefficient", 'N.s/m', 1.]],
                'refs': {},
                'nnodes': 2,
                'nedges': 1,
                'flux': dicmetadata['flux'],
                'effort': dicmetadata['effort'],
                }

    # Write documentation
    __doc__ = componentDoc(metadata)
