#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 23:04:04 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

from ..edges.connectors import Connector


class Gyrator(Connector):
    """
    Gyrator
    ========

    Parameters
    -----------

    label : str,
        Gyrator label.

    nodes: tuple of nodes labels
        Ordering is ('A1', 'A2', 'B1', 'B2')

    kwargs: dic with following "keys:values"
        * 'alpha' : gyrator value or symbol label or tuple (label, value).
    """
    def __init__(self, label, nodes, **kwargs):
        kwargs.update({'connector_type': 'gyrator'})
        Connector.__init__(self, label, nodes, **kwargs)

    @staticmethod
    def metadata():
        return {'nodes': ('A1', 'A2', 'B1', 'B2'),
                'arguments': {'alpha': ('alpha', 2.)}}
