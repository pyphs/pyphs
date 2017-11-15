#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 23:56:24 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import sympy
from ..tools import symbols
from pyphs.config import GMIN
from pyphs.core.tools import types
from ..edges import DissipativeNonLinear


class Bjt(DissipativeNonLinear):
    """
    bipolar junction transistor of NPN type according to the Ebers-Moll model.

    Usage
    -----

    electronics.bjt label (Nb, Nc, Ne): **kwargs

    Parameters
    -----------

    +------------+----------------+------------------------------------------+
    | Parameter  | Typical value  | Description (units)                      |
    +------------+----------------+------------------------------------------+
    | Is         | 1e-15 to 1e-12 | reverse saturation current (A)           |
    +------------+----------------+------------------------------------------+
    | betaR (d.u)| 0 to 20        | reverse common emitter current gain (d.u)|
    +------------+----------------+------------------------------------------+
    | betaF (d.u)| 20 to 500      | forward common emitter current gain (d.u)|
    +------------+----------------+------------------------------------------+
    | Vt (V)     | 26e-3          |  thermal voltage at room temperature (V) |
    +------------+----------------+------------------------------------------+
    | N (d.u)    | 1 o 2          |  ideality factor (d.u)                   |
    +------------+----------------+------------------------------------------+
    | Rb         | 20             |  zero bias base resistance (Ohms)        |
    +------------+----------------+------------------------------------------+
    | Rc         | 0.1            |  collector resistance (Ohms)             |
    +------------+----------------+------------------------------------------+
    | Re         | 0.1            |  emitter resistance (Ohms)               |
    +------------+----------------+------------------------------------------+

    Reference
    ----------

    [1] https://en.wikipedia.org/wiki/Bipolar_junction_\
transistor#Ebers.E2.80.93Moll_model

    """
    def __init__(self, label, nodes, **kwargs):
        pars = ['Is', 'betaR', 'betaF', 'Vt', 'mu', 'Rb', 'Rc', 'Re']
        for par in pars:
            assert par in kwargs.keys()
        Is, betaR, betaF, Vt, mu, Rb, Rc, Re = symbols(pars)
        # dissipation variable
        wbjt = symbols(["w"+label+ind for ind in ['bc', 'be']])
        # bjt dissipation funcion
        coeffs = types.matrix_types[0]([[(betaR+1)/betaR, -1],
                               [-1, (betaF+1)/betaF]])
        funcs = [Is*(sympy.exp(wbjt[0]/(mu*Vt))-1) + GMIN*wbjt[0],
                 Is*(sympy.exp(wbjt[1]/(mu*Vt))-1) + GMIN*wbjt[1]]
        zbjt = coeffs*types.matrix_types[0](funcs)
        # bjt edges data
        data_bc = {'label': wbjt[0],
                   'type': 'dissipative',
                   'ctrl': 'e',
                   'z': {'e_ctrl': zbjt[0], 'f_ctrl': sympy.sympify(0)},
                   'link': None}
        data_be = {'label': wbjt[1],
                   'type': 'dissipative',
                   'z': {'e_ctrl': zbjt[1], 'f_ctrl': sympy.sympify(0)},
                   'ctrl': 'e',
                   'link': None}
        # connector resistances dissipative functions
        wR = symbols(["w"+label+ind for ind in ['rb', 'rc', 're']])
        Rmat = types.matrix_types[0](sympy.diag(Rb, Rc, Re))
        zR = Rmat*types.matrix_types[0](wR)
        # connector resistances edges data
        data_rb = {'label': wR[0],
                   'z': {'e_ctrl': wR[0]/Rb, 'f_ctrl': Rb*wR[0]},
                   'type': 'dissipative',
                   'ctrl': '?',
                   'link': None}
        data_rc = {'label': wR[1],
                   'z': {'e_ctrl': wR[1]/Rc, 'f_ctrl': Rc*wR[1]},
                   'type': 'dissipative',
                   'ctrl': '?',
                   'link': None}
        data_re = {'label': wR[2],
                   'z': {'e_ctrl': wR[2]/Re, 'f_ctrl': Re*wR[2]},
                   'type': 'dissipative',
                   'ctrl': '?',
                   'link': None}
        # edge
        Nb, Nc, Ne = nodes
        iNb, iNc, iNe = [str(el)+label for el in (Nb, Nc, Ne)]
        edges = [(iNb, iNc, data_bc),
                 (iNb, iNe, data_be),
                 (Nb, iNb, data_rb),
                 (Nc, iNc, data_rc),
                 (Ne, iNe, data_re)]
        # init component
        DissipativeNonLinear.__init__(self, label, edges, wbjt + wR,
                                         list(zbjt) + list(zR), **kwargs)

    @staticmethod
    def metadata():
        return {'nodes': ('Nb', 'Nc', 'Ne'),
                'arguments': {'Is': ('Is', 2.39e-14),
                              'betaR': ('betaR', 7.946),
                              'betaF': ('betaF', 294.3),
                              'mu': ('mu', 1.006),
                              'Vt': ('Vt', 26e-3),
                              'Rb': ('Rb', 1.),
                              'Rc': ('Rc', 0.85),
                              'Re': ('Re', 0.4683)}}
