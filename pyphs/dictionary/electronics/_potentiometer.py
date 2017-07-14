#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 00:06:10 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

from ..tools import symbols
from ..edges import DissipativeNonLinear


class Potentiometer(DissipativeNonLinear):
    """
    Electronic nonlinear dissipative component: diode PN

    Usage
    -----

    electronics.diodepn label nodes: **kwargs

    Parameters:
    -----------

    nodes : (N1, N2)
        tuple of nodes labels (int or string). The edge (ie. the current 'i') \
is directed from N1 to N2, with 'i(v))=Is*(exp(v/v0)-1)'.

    kwargs : dictionary with following "key: value"

         * 'Is': saturation current (A)
         * 'v0': quality factor (V)
         * 'R': connectors resistance (Ohms)
    """
    def __init__(self, label, nodes, **kwargs):
        # parameters
        pars = ['R', 'alpha', 'expo']
        for par in pars:
            assert par in kwargs.keys()
        R, alpha, expo = symbols(pars)
        # dissipation variable
        w = symbols(["w"+label+str(i) for i in (1, 2)])
        # dissipation funcion
        R1 = 1 + R*alpha**expo
        R2 = 1 + R*(1-alpha**expo)
        z = [R1*w[0], R2*w[1]]

        N1, N2, N3 = nodes
        # edges
        data_1 = {'label': w[0],
                  'type': 'dissipative',
                  'z': {'e_ctrl': w[0]/R1,
                        'f_ctrl': R1*w[0]},
                  'ctrl': '?',
                  'link': None}
        edge_1 = (N1, N2, data_1)

        # edges
        data_2 = {'label': w[1],
                  'type': 'dissipative',
                  'z': {'e_ctrl': w[1]/R2,
                        'f_ctrl': R2*w[1]},
                  'ctrl': '?',
                  'link': None}
        edge_2 = (N2, N3, data_2)

        # init component
        DissipativeNonLinear.__init__(self, label,
                                         [edge_1, edge_2],
                                         w, z, **kwargs)

    @staticmethod
    def metadata():
        return {'nodes': ('N1', 'N2', 'N3'),
                'arguments': {'R': ('R', 1e-9),
                              'alpha': 'alpha',
                              'expo': ('expo', 1)}}
