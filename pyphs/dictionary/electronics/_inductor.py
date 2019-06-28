#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 23:56:00 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

from ..edges import StorageLinear
from ..tools import componentDoc, parametersDefault
from ..electronics import metadata as dicmetadata


class Inductor(StorageLinear):

    def __init__(self, label, nodes, **kwargs):

        par_name = 'L'
        par_val = kwargs[par_name]
        kwargs = {'name': par_name,
                  'value': par_val,
                  'inv_coeff': True,
                  'ctrl': 'e'}
        StorageLinear.__init__(self, label, nodes, **kwargs)

    metadata = {'title': 'Inductor',
                'component': 'Inductor',
                'label': 'induc',
                'dico': 'electronics',
                'desc': 'Linear inductor.',
                'nodesdesc': "Inductor terminals with positive current N1->N2.",
                'nodes': ('N1', 'N2'),
                'parameters': [['L', 'Inductance', 'H', '1e-3']],
                'refs': {},
                'nnodes': 2,
                'nedges': 1,
                'flux': dicmetadata['flux'],
                'effort': dicmetadata['effort'],
                }

    # Write documentation
    __doc__ = componentDoc(metadata)
