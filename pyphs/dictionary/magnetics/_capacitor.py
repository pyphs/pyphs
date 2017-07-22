#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 23:23:08 2017

@author: Falaize
"""


from __future__ import absolute_import, division, print_function

from ..edges import StorageLinear


class Capacitor(StorageLinear):
    """
    Linear capacitor

    Parameters
    -----------

    label : str, port label.

    nodes: tuple of nodes labels

        Edge is "nodes[0] -> nodes[1]".

    kwargs: dic with following "keys:values"

        * 'C' : mag. capacitance value or symbol label or tuple (label, value);
                units is H.
    """
    def __init__(self, label, nodes, **kwargs):
        par_name = 'C'
        par_val = kwargs[par_name]
        kwargs = {'name': par_name,
                  'value': par_val,
                  'inv_coeff': True,
                  'ctrl': 'f'}
        StorageLinear.__init__(self, label, nodes, **kwargs)

    @staticmethod
    def metadata():
        return {'nodes': ('N1', 'N2'),
                'arguments': {'C': ('Csymbol', 1e-9)}}
