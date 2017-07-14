#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 13:13:07 2017

@author: Falaize
"""

from pyphs.graphs import datum
from ..edges import DissipativeNonLinear
from ..tools import symbols


class Transfer(DissipativeNonLinear):
    """
    Thermal transfer between two masses.
    * The dissipation variables are temperatures w1=t1, w2=t2,
    * The Parameter is the thermal transfer coefficient R,
    * The "Dissipative function" is z(w)=(R*(t1-t2)/t1,
                                          R*(t2-t1)/t2)

    Usage
    -----

    thermics.transfer label nodes: **kwargs

    Parameters:
    -----------

    nodes: (T1, T2)
        Temperature nodes.

    kwargs : dictionary with following "key: value"

         * 'R': Heat transfer coefficient (K/W)
    """
    def __init__(self, label, nodes, **kwargs):
        # parameters
        pars = ['R', ]
        for par in pars:
            assert par in kwargs.keys()
        R, = symbols(pars)

        # dissipation variable
        w = symbols('w{}_(:2)'.format(label))

        t1, t2 = symbols(['gx'+str(n) for n in nodes])

        # dissipation funcion
        zero = (w[0]-w[0]).simplify()
        z1 = R*(w[0]-w[1])/t1
        z2 = R*(w[1]-w[0])/t2

        N1, N2 = nodes
        # edge diode data
        data1 = {'label': w[0],
                 'z': {'e_ctrl': z1, 'f_ctrl': zero},
                 'type': 'dissipative',
                 'ctrl': 'e',
                 'link': None}
        # edge
        edge1 = (datum, N1, data1)

        # edge diode data
        data2 = {'label': w[1],
                 'z': {'e_ctrl': z2, 'f_ctrl': zero},
                 'type': 'dissipative',
                 'ctrl': 'e',
                 'link': None}
        # edge
        edge2 = (datum, N2, data2)

        # init component
        DissipativeNonLinear.__init__(self, label,
                                         [edge1,
                                          edge2],
                                         w, [z1, z2],
                                         **kwargs)

    @staticmethod
    def metadata():
        return {'nodes': ('T1', 'T2'),
                'arguments': {'R': ('R', 2.9)}}
