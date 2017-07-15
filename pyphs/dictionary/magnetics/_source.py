#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 23:21:59 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

from ..edges import Port


class Source(Port):
    """
    Source of variation of magnetic flux or magnetomotive force.

    Usage
    ------
        magnetics.source label ('node1', 'node2'): type='type'

        where 'type' is the source type in ('mmf', 'fluxvar').


    Parameters
    -----------

    label : str, port label.

    nodes: tuple of nodes labels

        if a single label in nodes, port edge is "datum -> node"; \
else, the edge corresponds to "nodes[0] -> nodes[1]".

    kwargs: dic with following "keys:values"

        * 'type' : source type in ('mmf', 'fluxvar').
            With variation of magnetic flux (fluxvar) or
            magnetomotive force (mmf).

    Not implemented:
    ----------------

        * 'const': if not None, the input will be replaced by the value (subs).
    """
    def __init__(self, label, nodes, **kwargs):
        type_ = kwargs['type']
        type_ = type_.lower()
        assert type_ in ('mmf', 'fluxvar')
        if type_ == 'mmf':
            ctrl = 'f'
        elif type_ == 'fluxvar':
            ctrl = 'e'
        kwargs.update({'ctrl': ctrl})
        Port.__init__(self, label, nodes, **kwargs)

    @staticmethod
    def metadata():
        return {'nodes': ('N1', 'N2'),
                'arguments': {'type': 'mmf'}}
