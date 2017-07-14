# -*- coding: utf-8 -*-
"""
Created on Sat May 21 16:29:43 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function
from ..edges import StorageNonLinear
from pyphs.dictionary.tools import symbols
import sympy as sp


class Springsat(StorageNonLinear):
    """
    Spring with saturating nonlinearity F(q)=K0*(q + Ksat*c(q)) with
    sat(q) = (4/(4-pi))*(tan(pi*q/(2*qsat))-(pi*q/(2*qsat)))

    Usage
    -----

    mechanics.springsat label nodes: **kwargs

    Parameters:
    -----------

    nodes : (N1, N2)
        tuple of nodes labels (int or string). The edge (ie. the velocity \
'v') is directed from N1 to N2.

    kwargs : dictionary with following "key: value"

         * 'K0': Stiffness (N/m)
         * 'Ksat': Nonlinear contribution (dimensionless unit)
         * 'xsat': Saturating position (m)
    """
    def __init__(self, label, nodes, **kwargs):
        # parameters
        pars = ['K0', 'Ksat', 'xsat']
        for par in pars:
            assert par in kwargs.keys()
        K0, Ksat, xsat = symbols(pars)
        # state  variable
        x = symbols("x"+label)
        # storage funcion
        Hlin = x**2/2
        t1 = sp.pi*x/(2*xsat)
        c1 = (8*xsat/(sp.pi*(4-sp.pi)))
        Hsat = c1 * (sp.log(sp.cos(t1)) + (t1**2)/2.)
        H = K0*(Hlin - Ksat*Hsat)
        N1, N2 = nodes

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
        return {'nodes': ('N1', 'N2'),
                'arguments': {'K0': ('K0', 1e3),
                              'Ksat': ('Ksat', 1e3),
                              'xsat': ('xsat', 1e-2)}}
