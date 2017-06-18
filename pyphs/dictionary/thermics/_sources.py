#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 12:14:22 2017

@author: Falaize
"""

from ..edges import PHSStorageNonLinear

class Source(PHSPort):
    """
    Voltage or current source

    Parameters
    -----------

    label : str, port label.

    nodes: tuple of nodes labels

        if a single label in nodes, port edge is "datum -> node"; \
else, the edge corresponds to "nodes[0] -> nodes[1]".

    kwargs: dic with following "keys:values"

        * 'type' : source type in ('force', 'velocity').
        * 'const': if not None, the input will be replaced by the value (subs).
    """
    def __init__(self, label, nodes, **kwargs):
        type_ = kwargs['type']
        type_ = type_.lower()
        assert type_ in ('force', 'velocity')
        if type_ == 'force':
            ctrl = 'e'
        elif type_ == 'velocity':
            ctrl = 'f'
        kwargs.update({'ctrl': ctrl})
        PHSPort.__init__(self, label, nodes, **kwargs)

    @staticmethod
    def metadata():
        return {'nodes': ('N1', 'N2'),
                'arguments': {'type': 'force'}}

