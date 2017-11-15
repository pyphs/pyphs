# -*- coding: utf-8 -*-
"""
Created on Sat May 21 16:29:43 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function
from ..tools import symbols, mappars
from pyphs import Graph
import sympy as sp


class Felt(Graph):
    """
    Piano hammer felt
    ==================


    Usage
    -----

    mechanics.felt label nodes: **kwargs

    Parameters:
    -----------

    label : str
        Felt label.

    nodes : (N1, N2)
        tuple of nodes labels (int or string). The edge (ie. the velocity 'v')
        is directed from N1 to N2.

    kwargs : dictionary with following "key: value"

        * 'L': [m] Height of the felt at rest (1.5cm),
        * 'F': [N] Elastic characteristic force (13.8),
        * 'A': [N.s/m] Felt damping coefficient (1e2),
        * 'B': [d.u] Hysteresis coefficient for the felt (2.5),

    """
    def __init__(self, label, nodes, **kwargs):
        Graph.__init__(self, label=label)
        dic = {'A': 1e2,  # [N.s/m] Felt damping coefficient
               'B': 2.5,  # [#] Hysteresis coefficient for the felt
               'F': 13.8,  # [N/m] Elastic characteristic force
               'L': 1.5*1e-2,  # [m] Height of the felt at rest
               }
        dic.update(kwargs)
        dicpars, subs = mappars(self, **dic)
        # parameters
        pars = ['L', 'F', 'A', 'B']
        L, F, A, B = symbols(pars)

        N1, N2 = nodes
        xnl = symbols('q'+label)
        hnl = sp.Piecewise((0., xnl <= 0.), ((L*F/(B+1))*(xnl/L)**(B+1), True))
        hnl = hnl.subs(dicpars)
        # edge data
        data = {'label': xnl,
                'type': 'storage',
                'ctrl': 'e',
                'link': None}
        self.add_edges_from([(N1, N2, data), ])
        self.core.add_storages(xnl, hnl)

        r = sp.Piecewise((0., xnl <= 0.), ((A * L/B)*(xnl/L)**(B-1), True))
        r = r.subs(dicpars)
        wnl = symbols('dtq'+label)
        # edge data
        data = {'label': wnl,
                'type': 'dissipative',
                'ctrl': 'e',
                'z': {'e_ctrl': r*wnl, 'f_ctrl': sp.sympify(0)},
                'link': None}
        self.add_edges_from([(N1, N2, data), ])
        self.core.add_dissipations(wnl, r*wnl)

        self.core.subs.update(subs)

    @staticmethod
    def metadata():
        return {'nodes': ('N1', 'N2'),
                'arguments': {'L': ('L', 1.5e-2),
                              'K': ('K', 5e5),
                              'A': ('A', 1e2),
                              'B': ('B', 2.5)}}
