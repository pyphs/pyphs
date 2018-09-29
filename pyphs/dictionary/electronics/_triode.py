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
from ..tools import componentDoc, parametersDefault
from ..electronics import metadata as dicmetadata


class Triode(DissipativeNonLinear):

    def __init__(self, label, nodes, **kwargs):
        parameters = parametersDefault(self.metadata['parameters'])
        parameters.update(kwargs)
        # parameters
        pars = ['mu', 'Ex', 'Kg', 'Kp', 'Kvb', 'Vct', 'Va', 'Rgk']
        mu, Ex, Kg, Kp, Kvb, Vct, Va, Rgk = symbols(pars)
        # dissipation variable
        vpk, vgk = symbols([nicevarlabel("w", label+el)
                            for el in ['pk', 'gk']])
        w = [vpk, vgk]

        # dissipation funcions

        # smoothed signum function
        def sign(expr):
            return sympy.tanh(expr/GMIN)

        # hard signum function
#        def sign(expr):
#            return sympy.Piecewise((-1, expr < 0),
#                                   (0, expr == 0.),
#                                   (1, True))

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
            e1 = vgk + Vct
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
                                      w, z, **parameters)

    metadata = {'title': 'Triode',
                'component': 'Triode',
                'label': 'tri',
                'dico': 'electronics',
                'desc': 'Triode model from [1]_ which includes Norman Koren modeling of plate to cathode current Ipk and grid effect for grid to cathod current Igk.',
                'nodesdesc': "Cathode 'K', Plate 'P' and Grid 'G'",
                'nodes': ('Nk', 'Np', 'Ng'),
                'parameters': [['mu', "Norman Koren's parameters", 'd.u.', 88.],
                               ['Ex', "Norman Koren's parameters", 'd.u.', 1.4],
                               ['Kg', "Norman Koren's parameters", 'd.u.', 1060.],
                               ['Kp', "Norman Koren's parameters", 'd.u.', 600.],
                               ['Kvb', "Norman Koren's parameters", 'd.u.', 300.],
                               ['Vct', "Norman Koren's parameters", 'V', 0.5],
                               ['Va', "Voltage threshold", 'V', 0.33],
                               ['Rgk', "Grid current resistive behaviour", 'Ohms', 3000.]],
                'refs': {1: 'I. Cohen and T. Helie, Measures and parameter estimation of triodes for the real-time simulation of a multi-stage guitar preamplifier. 129th Convention of the AES, SF USA, 2009.'},
                'nnodes': 3,
                'nedges': 2,
                'flux': dicmetadata['flux'],
                'effort': dicmetadata['effort'],
                'flux': dicmetadata['flux'],
                'effort': dicmetadata['effort'],
                }

    # Write documentation
    __doc__ = componentDoc(metadata)
