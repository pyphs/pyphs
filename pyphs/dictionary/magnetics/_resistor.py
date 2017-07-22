#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 23:24:06 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

from ..edges import DissipativeLinear


class Resistor(DissipativeLinear):
    """
    Linear magnetic resistor (unconstrained control).

    Parameters
    -----------

    label : str, port label.

    nodes: tuple of nodes labels

        Edge is "nodes[0] -> nodes[1]".

    kwargs: dic with following "keys:values"

        * 'R' : Mag. resistance value or symbol label or tuple (label, value);
                units is 1/Ohm.
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
                'arguments': {'R': ('Rsymbol', 1e-3)}}
