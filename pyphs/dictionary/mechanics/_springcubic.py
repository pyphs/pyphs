# -*- coding: utf-8 -*-
"""
Created on Sat May 21 16:29:43 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function
from ..edges import StorageNonLinear
from ..tools import symbols


class Springcubic(StorageNonLinear):
    """
    Spring with cubic nonlinearity F(q)=K0*(q + K2*q**3)

    Usage
    -----

    mechanics.springcubic label nodes: **kwargs

    Parameters:
    -----------

    nodes : (N1, N2)
        tuple of nodes labels (int or string). The edge (ie. the velocity \
'v') is directed from N1 to N2.

    kwargs : dictionary with following "key: value"

         * 'K0': Stiffness (N/m)
         * 'K2': Nonlinear contribution (dimensionless unit)
    """
    def __init__(self, label, nodes, **kwargs):
        # parameters
        pars = ['K0', 'K2']
        for par in pars:
            assert par in kwargs.keys()
        K0, K2 = symbols(pars)
        # state  variable
        x = symbols("x"+label)
        # storage funcion
        H = K0*x*(x + K2*x**3/2)/2
        N1, N2 = nodes

        # edge data
        data = {'label': x,
                'type': 'storage',
                'ctrl': 'e',
                'link': None}

        # edge
        edge = (N1, N2, data)

        # init component
        StorageNonLinear.__init__(self, label, [edge],
                                     x, H, **kwargs)

    @staticmethod
    def metadata():
        return {'nodes': ('N1', 'N2'),
                'arguments': {'K0': ('K0', 1e3),
                              'K2': ('K2', 1e3)}}
