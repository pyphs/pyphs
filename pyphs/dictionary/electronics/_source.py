#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 23:55:44 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

from ..edges import Port
from ..tools import componentDoc, parametersDefault
from ..electronics import metadata as dicmetadata


class Source(Port):

    def __init__(self, label, nodes, **kwargs):
        type_ = kwargs['type']
        type_ = type_.lower()
        assert type_ in ('voltage', 'current')
        if type_ == 'voltage':
            ctrl = 'f'
        elif type_ == 'current':
            ctrl = 'e'
        kwargs.update({'ctrl': ctrl})
#        kwargs.update({'units': units})
        Port.__init__(self, label, nodes, **kwargs)

    metadata = {'title': 'Electrical source',
                'component': 'Source',
                'label': 'sourc',
                'dico': 'electronics',
                'desc': 'Controlled voltage or current source.',
                'nodesdesc': "source terminals with positive current N1->N2.",
                'nodes': ('N1', 'N2'),
                'parameters': [['type', "Source type in {'voltage', 'current'}", 'string', 'voltage']],
                'refs': {},
                'nnodes': 2,
                'nedges': 1,
                'flux': dicmetadata['flux'],
                'effort': dicmetadata['effort'],
                }

    # Write documentation
    __doc__ = componentDoc(metadata)
