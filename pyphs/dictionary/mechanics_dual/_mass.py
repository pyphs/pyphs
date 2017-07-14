#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 23:49:05 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function
from ..edges import StorageLinear


class Mass(StorageLinear):
    """
    Mass moving in 1D space

    Parameters
    -----------

    label : str, port label.

    nodes: tuple of nodes labels

        Edge is "nodes[0] -> nodes[1]".

    kwargs: dic with following "keys:values"

        * 'M' : Mass value or symbol label or tuple (label, value).
    """
    def __init__(self, label, nodes, **kwargs):
        par_name = 'M'
        par_val = kwargs[par_name]
        kwargs = {'name': par_name,
                  'value': par_val,
                  'inv_coeff': True,
                  'ctrl': 'e'}
        StorageLinear.__init__(self, label, (nodes[0], nodes[1]), **kwargs)

    @staticmethod
    def metadata():
        return {'nodes': ('N1', 'N2'),
                'arguments': {'M': ('M', 1e-2)}}
