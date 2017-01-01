# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 19:13:35 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

from .edges.connectors import PHSConnector


class Gyrator(PHSConnector):
    """
    gyrator
    """
    def __init__(self, label, nodes, **kwargs):
        kwargs.update({'connector_type': 'gyrator'})
        PHSConnector.__init__(self, label, nodes, **kwargs)


class Transformer(PHSConnector):
    """
    transformer
    """
    def __init__(self, label, nodes, **kwargs):
        kwargs.update({'connector_type': 'transformer'})
        PHSConnector.__init__(self, label, nodes, **kwargs)
