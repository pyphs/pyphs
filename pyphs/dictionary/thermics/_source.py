#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 12:14:22 2017

@author: Falaize
"""

from ..edges import Port
from ..tools import symbols
from pyphs.graphs import datum

class Source(Port):
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
        if not label == nodes[0]:
            text = "The node label associated with a heat source must be the\
 same as the component label:\n{}\nis not \n{}".format(label, nodes[0])
            raise NameError(text)
        assert type_ in ('temperature', 'entropyvariation')
        if type_ == 'entropyvariation':
            ctrl = 'e'
            obs = {}
        elif type_ == 'temperature':
            ctrl = 'f'
            obs = {symbols('gx'+label): symbols('u'+label)}

        kwargs.update({'ctrl': ctrl})
        Port.__init__(self, label,
                         (datum, nodes[0]), **kwargs)
        self.core.observers.update(obs)

    @staticmethod
    def metadata():
        return {'nodes': ('T', ),
                'arguments': {'type': 'temperature'}}
