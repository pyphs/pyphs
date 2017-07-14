#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 23:55:44 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

from ..edges import Port


class Source(Port):
    """
    Voltage or current source

    Usage
    ------
        electronics.source label ('node1', 'node2'): type='type'

        where 'type' is the source type in ('voltage', 'current').


    Parameters
    -----------

    label : str, port label.

    nodes: tuple of nodes labels

        if a single label in nodes, port edge is "datum -> node"; \
else, the edge corresponds to "nodes[0] -> nodes[1]".

    kwargs: dic with following "keys:values"

        * 'type' : source type in ('voltage', 'current').

    Not implemented:
    ----------------

        * 'const': if not None, the input will be replaced by the value (subs).
    """
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

    @staticmethod
    def metadata():
        return {'nodes': ('N1', 'N2'),
                'arguments': {'type': 'voltage'}}
