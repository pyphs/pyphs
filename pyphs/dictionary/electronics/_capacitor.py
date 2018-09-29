#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 23:55:52 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

from ..edges import StorageLinear
from ..tools import componentDoc, parametersDefault
from ..electronics import metadata as dicmetadata


class Capacitor(StorageLinear):
    """
    Linear capacitor

    Parameters
    -----------

    label : str, port label.

    nodes: tuple of nodes labels

        Edge is "nodes[0] -> nodes[1]".

    kwargs: dic with following "keys:values"

        * 'C' : capacitance value or symbol label or tuple (label, value).
    """
    def __init__(self, label, nodes, **kwargs):

        # Write documentation
        self.__doc__ = componentDoc(Capacitor.metadata)

        parameters = parametersDefault(self.metadata['parameters'])
        parameters.update(kwargs)
        par_name = 'C'
        par_val = parameters[par_name]
        kwargs = {'name': par_name,
                  'value': par_val,
                  'inv_coeff': True,
                  'ctrl': 'f'}
        StorageLinear.__init__(self, label, nodes, **kwargs)

    metadata = {'title': 'Capacitor',
                'component': 'Capacitor',
                'label': 'capa',
                'dico': 'electronics',
                'desc': 'Linear capacitor.',
                'nodesdesc': "Capacitor terminals with positive current N1->N2.",
                'nodes': ('N1', 'N2'),
                'parameters': [['C', 'Capacitance', 'F', '1e-9']],
                'refs': {},
                'nnodes': 2,
                'nedges': 1,
                'flux': dicmetadata['flux'],
                'effort': dicmetadata['effort'],
                }

    # Write documentation
    __doc__ = componentDoc(metadata)
