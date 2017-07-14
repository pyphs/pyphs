#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 23:49:58 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function
from ..edges import DissipativeLinear


class Damper(DissipativeLinear):
    """
    Linear damper (unconstrained control)

    Parameters
    -----------

    label : str, port label.

    nodes: tuple of nodes labels

        Edge is "nodes[0] -> nodes[1]".

    kwargs: dic with following "keys:values"

        * 'A' : Damping coefficient or symbol label (string) or tuple \
(label, value).
    """
    def __init__(self, label, nodes, **kwargs):
        if kwargs['A'] is None:
            coeff = 0.
        else:
            coeff = kwargs['A']
        DissipativeLinear.__init__(self, label, nodes, coeff=coeff,
                                      inv_coeff=False)

    @staticmethod
    def metadata():
        return {'nodes': ('N1', 'N2'),
                'arguments': {'A': ('A', 1.)}}
