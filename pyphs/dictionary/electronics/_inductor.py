#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 23:56:00 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

from ..edges import StorageLinear


class Inductor(StorageLinear):
    """
    Linear inductor

    Parameters
    -----------

    label : str, port label.

    nodes: tuple of nodes labels

        Edge is "nodes[0] -> nodes[1]".

    kwargs: dic with following "keys:values"

        * 'L' : inductance value or symbol label or tuple (label, value).
    """
    def __init__(self, label, nodes, **kwargs):
        par_name = 'L'
        par_val = kwargs[par_name]
        kwargs = {'name': par_name,
                  'value': par_val,
                  'inv_coeff': True,
                  'ctrl': 'e'}
        StorageLinear.__init__(self, label, nodes, **kwargs)

    @staticmethod
    def metadata():
        return {'nodes': ('N1', 'N2'),
                'arguments': {'L': ('Lsymbol', 1e-3)}}
