"""
Created on Sat May 21 16:29:43 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function
from ..edges import Port


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
        assert type_ in ('force', 'velocity')
        if type_ == 'force':
            ctrl = 'e'
        elif type_ == 'velocity':
            ctrl = 'f'
        kwargs.update({'ctrl': ctrl})
        Port.__init__(self, label, nodes, **kwargs)

    @staticmethod
    def metadata():
        return {'nodes': ('N1', 'N2'),
                'arguments': {'type': 'force'}}
