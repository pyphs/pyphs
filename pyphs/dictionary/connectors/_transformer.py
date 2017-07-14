# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 19:13:35 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

from ..edges.connectors import Connector


class Transformer(Connector):
    """
    Transformer
    ============

    Parameters
    -----------

    label : str,
        Transformer label.

    nodes: tuple of nodes labels
        Ordering is ('A1', 'A2', 'B1', 'B2')

    kwargs: dic with following "keys:values"
        * 'alpha' : transformer value or symbol label or tuple (label, value).
    """
    def __init__(self, label, nodes, **kwargs):
        kwargs.update({'connector_type': 'transformer'})
        Connector.__init__(self, label, nodes, **kwargs)

    @staticmethod
    def metadata():
        return {'nodes': ('A1', 'A2', 'B1', 'B2'),
                'arguments': {'alpha': ('alpha', 2.)}}
