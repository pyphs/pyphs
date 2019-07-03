# -*- coding: utf-8 -*-
"""
Created on Sat May 21 16:29:43 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function
from ..edges import StorageNonLinear
from ..tools import symbols
from ..tools import componentDoc, parametersDefault
from ..mechanics import metadata as dicmetadata
from pyphs.misc.rst import equation


class Springcubic(StorageNonLinear):

    def __init__(self, label, nodes, **kwargs):

        parameters = parametersDefault(self.metadata['parameters'])
        parameters.update(kwargs)

        # parameters
        pars = ['F1', 'F3', 'xref']
        F1, F3, xref = symbols(pars)
        # state  variable
        x = symbols("x"+label)
        # storage funcion
        H = F1*x**2/(2.*xref) + F3*x**4/(4*xref**3)
        N1, N2 = nodes

        # edge data
        data = {'label': x,
                'type': 'storage',
                'ctrl': 'e',
                'link': None}

        # edge
        edge = (N1, N2, data)

        # init component
        StorageNonLinear.__init__(self, label, [edge],
                                     x, H, **parameters)

    metadata = {'title': 'Cubic spring',
                'component': 'Springcubic',
                'label': 'spring',
                'dico': 'mechanics',
                'desc': (r'Cubic spring with state :math:`q\in \mathbb R` and parameters described below. The energy is' +
                         equation(r'H(q) = \frac{F_1\,q^2}{2\,q_{ref}} + \frac{F_3\,q^4}{4q_{ref}^3}.') +
                         'The resulting force is:' +
                         equation(r'f(q)= \frac{d \, H(q)}{d q} = F_1 \,\frac{q}{q_{ref}} + F_3 \, \frac{q^3}{q_{ref}^3}.') +
                         'so that :math:`f(q_{ref}) = F1+F3`.'),
                'nodesdesc': "Mechanical points associated with component endpoints (positive flux P1->P2).",
                'nodes': ('P1', 'P2'),
                'parametersdesc': 'Component parameters',
                'parameters': [['F1', "Linear contribution to restoring force", 'N', 1e1],
                               ['F3', "Cubic contribution to restoring force", 'N', 1e1],
                               ['xref', "Reference elongation", 'N', 1e-2]],
                'refs': {},
                'nnodes': 2,
                'nedges': 1,
                'flux': dicmetadata['flux'],
                'effort': dicmetadata['effort'],
                }

    __doc__ = componentDoc(metadata)
