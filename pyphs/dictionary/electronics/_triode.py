#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 23:56:14 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import sympy
from ..tools import symbols, nicevarlabel
from ..edges import DissipativeNonLinear
from pyphs.config import GMIN


class Triode(DissipativeNonLinear):
    """
    Usage
    -----

    electronics.triode label ['K', 'P', 'G'] [mu, Ex, Kg, Kp, Kvb, Vcp, Va, \
    Rgk]

    Description
    ------------

    Triode model from [1] which includes Norman Koren modeling of plate to \
    cathode current Ipk and grid effect for grid to cathod current Igk.

    Nodes:
        3 (cathode 'K', plate 'P' and grid 'G').

    Edges:
        2 (plate->cathode 'PK' and grid->cathode 'GK').

    Parameters
    -----------

    +------------+---------+------------+---------+------------+---------+----\
--------+---------+
    |    mu      |  Ex     |    Kg      |  Kp     |     Kvb    |    Vcp  \
|  Va        |    Rgk  |
    +------------+---------+------------+---------+------------+---------+---\
---------+---------+
    | 88         | 1.4     | 1060       | 600     | 300        | 0.5     \
| 0.33       | 3000    |
    +------------+---------+------------+---------+------------+---------+---\
---------+---------+

    Reference
    ----------

    [1] I. Cohen and T. Helie, Measures and parameter estimation of triodes \
    for the real-time simulation of a multi-stage guitar preamplifier. 129th \
    Convention of the AES, SF USA, 2009.

    """
    def __init__(self, label, nodes, **kwargs):
        # parameters
        pars = ['mu', 'Ex', 'Kg', 'Kp', 'Kvb', 'Vcp', 'Va', 'Rgk']
        mu, Ex, Kg, Kp, Kvb, Vcp, Va, Rgk = symbols(pars)
        # dissipation variable
        vpk, vgk = symbols([nicevarlabel("w", label+el)
                            for el in ['pk', 'gk']])
        w = [vpk, vgk]

        # dissipation funcions

        def sign(expr):
            return sympy.tanh(expr/GMIN)

        def indicator(expr):
            return (1. + sign(expr))/2.

        def igk():
            """
            dissipation function for edge 'e = (g->k)'
            """
            expr = indicator(vgk-Va)/Rgk
            return expr

        def ipk():
            """
            dissipation function for edge 'e = (p->k)'
            """
            e1 = vgk + Vcp
            e2 = sympy.sqrt(Kvb + vpk**2)
            e3 = Kp*(mu**-1 + e1/e2)
            exprE = (vpk/Kp)*sympy.log(1 + sympy.exp(e3))

            expr = exprE**Ex * (1 + sign(exprE)) / Kg
            return expr.evalf()

        z = [ipk()+(vpk+vgk)*GMIN, igk()+(vpk+vgk)*GMIN]

        # edges data
        edge_pk_data = {'label': w[0],
                        'type': 'dissipative',
                        'z': {'e_ctrl': z[0], 'f_ctrl': sympy.sympify(0)},
                        'ctrl': 'e',
                        'link': None}
        edge_gk_data = {'label': w[1],
                        'type': 'dissipative',
                        'z': {'e_ctrl': z[1], 'f_ctrl': sympy.sympify(0)},
                        'ctrl': 'e',
                        'link': None}
        # edges
        edge_pk = (nodes[1], nodes[0], edge_pk_data)
        edge_gk = (nodes[2], nodes[0], edge_gk_data)
        edges = [edge_pk, edge_gk]

        # init component
        DissipativeNonLinear.__init__(self, label, edges,
                                         w, z, **kwargs)

    @staticmethod
    def metadata():
        return {'nodes': ('Nk', 'Np', 'Ng'),
                'arguments': {'mu': ('mu', 88.),
                              'Ex': ('Ex', 1.4),
                              'Kg': ('Kg', 1060.),
                              'Kp': ('Kp', 600.),
                              'Kvb': ('Kvb', 300.),
                              'Vcp': ('Vcp', 0.5),
                              'Va': ('Va', 0.33),
                              'Rgk': ('Rgk', 3000.)}}
