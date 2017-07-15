# -*- coding: utf-8 -*-
"""
Created on Sat May 21 16:24:12 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

import sympy as sp
from ..edges import StorageNonLinear
from pyphs.dictionary.tools import symbols


class Capacitorsat(StorageNonLinear):
    """
    Magnetic capacitor with saturating nonlinearity
    F(phi)=C0*(phi + Csat*c(phi)) with
    sat(phi) = (4/(4-phi))*(tan(pi*phi/(2*phisat))-(pi*phi/(2*phisat)))

    Usage
    -----

    magnetics.capacitorsat label nodes: **kwargs

    Parameters:
    -----------

    nodes : (N1, N2)
        tuple of nodes labels (int or string). The edge (ie. the flux \
'phi') is directed from N1 to N2.

    kwargs : dictionary with following "key: value"

         * 'C0': Magnetic capacity (H)
         * 'Csat': Nonlinear contribution (dimensionless unit)
         * 'phisat': Saturating flux (Wb)
    """
    def __init__(self, label, nodes, **kwargs):
        # parameters
        pars = ['C0', 'Csat', 'phisat']
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
                'arguments': {'C0': ('C0', 1e3),
                              'Csat': ('Csat', 1e3),
                              'phisat': ('phisat', 1e-2)}}
