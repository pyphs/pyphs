# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 19:13:35 2016

@author: Falaize
"""
from classes.connectors.connector import Connector


class Gyrator(Connector):
    """
    gyrator
    """
    def __init__(self, label, nodes, **kwargs):
        kwargs.update({'connector_type': 'gyrator'})
        Connector.__init__(self, label, nodes, **kwargs)


class Transformer(Connector):
    """
    transformer
    """
    def __init__(self, label, nodes, **kwargs):
        kwargs.update({'connector_type': 'transformer'})
        Connector.__init__(self, label, nodes, **kwargs)
