# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 19:13:35 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

from ..edges.connectors import Connector
from ..tools import componentDoc, parametersDefault
from ..connectors import metadata as dicmetadata


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
                'desc': 'Quadripole connector of gyrator type.',
                'nodesdesc': "Connected edges are A1->A2 and B1->B2.",
                'nodes': ('A1', 'A2', 'B1', 'B2'),
                'parametersdesc': '',
                'parameters': [['alpha', 'Gyrator ratio', 'd.u.', 1.]],
                'refs': {},
                'nedges': 2,
                'nnodes': 4,
                'flux': dicmetadata['flux'],
                'effort': dicmetadata['effort'],
                }

Transformer.__doc__ = componentDoc(Transformer.metadata)
