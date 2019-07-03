# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 19:13:35 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

from ..edges.connectors import Connector
from ..tools import componentDoc, parametersDefault
from ..connectors import metadata as dicmetadata
from pyphs.misc.rst import equation


class Transformer(Connector):

    def __init__(self, label, nodes, **kwargs):
        pars = parametersDefault(self.metadata['parameters'])
        pars.update(kwargs)
        pars.update({'connector_type': 'transformer'})
        Connector.__init__(self, label, nodes, **pars)

    metadata = {'title': 'Transformer',
                'label': 'trans',
                'dico': 'connectors',
                'component': 'Transformer',
                'desc': r'Quadripole connector of transformer type with:' +
                        equation(r'\left\{\begin{array}{rcl} f_A &=& -\alpha\, f_B, \\ e_B &=& + \alpha\,e_A. \end{array}\right.'),
                'nodesdesc': "Connected edges are A1->A2 and B1->B2.",
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
