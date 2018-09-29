#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 00:05:25 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

from ..edges import DissipativeLinear
from ..tools import componentDoc, parametersDefault
from ..electronics import metadata as dicmetadata


class Resistor(DissipativeLinear):

    def __init__(self, label, nodes, **kwargs):
        if kwargs['R'] is None:
            coeff = 0
        else:
            coeff = kwargs['R']
        DissipativeLinear.__init__(self, label, nodes, coeff=coeff)

    metadata = {'title': 'Resistor',
                'component': 'Resistor',
                'label': 'resi',
                'dico': 'electronics',
                'desc': 'Linear resistor.',
                'nodesdesc': "Resistor terminals with positive current N1->N2.",
                'nodes': ('N1', 'N2'),
                'parameters': [['R', 'Resistance', 'Ohms', 1e3]],
                'refs': {},
                'nnodes': 2,
                'nedges': 1,
                'flux': dicmetadata['flux'],
                'effort': dicmetadata['effort'],
                }

    # Write documentation
    __doc__ = componentDoc(metadata)
