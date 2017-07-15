#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 12:14:04 2017

@author: Falaize
"""

from ..edges import StorageNonLinear
from ..tools import symbols
from pyphs.graphs import datum
import sympy as sp


class Capacitor(StorageNonLinear):
    """
    Thermal capacitor (mass) with exponential law
    * The state is the entropy x=s
    * The Parameters are the thermal capacity C and the initial temperature t0.
    * The Storage function is H(s) = C*t0*exp(s/C)
    * The Derivative of Storage function is dH/ds(s) = t0*exp(s/C)

    Usage
    -----

    thermics.capacitor label nodes: **kwargs

    Parameters:
    -----------

    nodes: (str, )
        Edge is `datum -> nodes[0]`.

    kwargs : dictionary with following "key: value"

         * 'C': Heat capacity (J/K)
         * 'T0': Reference temperature (K)
    """
    def __init__(self, label, nodes, **kwargs):
        # parameters
        if not label == nodes[0]:
            text = "The node label associated with a heat capacitor must be the\
 same as the component label:\n{}\nis not \n{}".format(label, nodes[0])
            raise NameError(text)
        pars = ['C', 'T0']
        base_kwargs = {'C': ('C', 1e2), 'T0': ('T0', 273.16)}
        for k in base_kwargs.keys():
            if k not in kwargs:
                kwargs[k] = base_kwargs[k]
        for par in pars:
            assert par in kwargs.keys()
        C, T0 = symbols(pars)
        # state  variable
        x = symbols("x"+label)
        # storage funcion
        H = C*T0*sp.exp(x/C)
        N1, N2 = datum, nodes[0]

        # edge data
        data = {'label': x,
                'type': 'storage',
                'ctrl': 'f',
                'link': None}

        # edge
        edge = (N1, N2, data)

        # init component
        StorageNonLinear.__init__(self, label, [edge],
                                     x, H, **kwargs)

    @staticmethod
    def metadata():
        return {'nodes': ('T', ),
                'arguments': {'C': ('C', 1e2),
                              'T0': ('T0', 273.16)}}
