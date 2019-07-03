#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 23:04:04 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

from ..edges.connectors import Connector
from ..tools import componentDoc, parametersDefault
from ..connectors import metadata as dicmetadata
from pyphs.misc.rst import equation


class Gyrator(Connector):

    def __init__(self, label, nodes, **kwargs):
        pars = parametersDefault(self.metadata['parameters'])
        pars.update(kwargs)
        pars.update({'connector_type': 'gyrator'})
        Connector.__init__(self, label, nodes, **pars)

    metadata = {'title': 'Gyrator',
                'component': 'Gyrator',
                'label': 'gyr',
                'dico': 'connectors',
                'desc': r'Quadripole connector of gyrator type with:' +
                        equation(r'\left\{\begin{array}{rcl} e_A &=& -\alpha\,f_B, \\ e_B &=& + \alpha\,f_A. \end{array}\right.'),
                'nodesdesc': "Connected edges are edge A = A1->A2 and edge B = B1->B2.",
                'nodes': ('A1', 'A2', 'B1', 'B2'),
                'parameters': [['alpha', 'Ratio', 'unknown', 1.]],
                'refs': {},
                'nedges': 2,
                'nnodes': 4,
                'flux': dicmetadata['flux'],
                'effort': dicmetadata['effort'],
                }

    # Write documentation
    __doc__ = componentDoc(metadata)
