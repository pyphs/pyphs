#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 00:05:25 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

from ..edges import DissipativeLinear


class Resistor(DissipativeLinear):
    """
    Linear resistor (unconstrained control)

    Parameters
    -----------

    label : str, port label.

    nodes: tuple of nodes labels

        Edge is "nodes[0] -> nodes[1]".

    kwargs: dic with following "keys:values"

        * 'R' : Resistance value or symbol label or tuple (label, value).
    """
    def __init__(self, label, nodes, **kwargs):
        if kwargs['R'] is None:
            coeff = 0
        else:
            coeff = kwargs['R']
        DissipativeLinear.__init__(self, label, nodes, coeff=coeff)

    @staticmethod
    def metadata():
        return {'nodes': ('N1', 'N2'),
                'arguments': {'R': ('Rsymbol', 1e3)}}
