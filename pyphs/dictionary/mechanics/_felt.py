# -*- coding: utf-8 -*-
"""
Created on Sat May 21 16:29:43 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function
from ..tools import symbols, mappars
from pyphs import Graph
import sympy as sp
from ..tools import componentDoc, parametersDefault
from ..mechanics import metadata as dicmetadata
from pyphs.misc.rst import equation


class Felt(Graph):

    def __init__(self, label, nodes, **kwargs):
        Graph.__init__(self, label=label)
        parameters = parametersDefault(self.metadata['parameters'])
        parameters.update(kwargs)

        dicpars, subs = mappars(self, **parameters)
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

    metadata = {'title': 'Felt material',
                'component': 'Felt',
                'label': 'felt',
                'dico': 'mechanics',
                'desc': (r'Nonlinear felt material used in piano-hammer. The model is that found in [1]_ eq. (11). It includes a nonlinear restoring force and a nonlinear damper as follows:' +
                         equation(r'f_{total}\left(c, \dot c\right) = f_{elastic}(c) + f_{damper}\left(c, \dot c\right),') +
                         'with' +
                         equation(r'f_{elastic}(c)  = F \,c ^B,') +
                         'and' +
                         equation(r'f_{damper}\left(c, \dot c\right) = \frac{A \, L}{B} c^{B-1} \,\dot c,') +
                         'where :math:`c = \\frac{\\max (q, 0)}{L}` is the crush of the hammer with contraction :math:`q\\in\\mathbb R`.'),
                'nodesdesc': "Mechanical points associated with the felt endpoints with positive flux N1->N2.",
                'nodes': ('P1', 'P2'),
                'parametersdesc': 'Component parameters.',
                'parameters': [['L', "Height at rest", 'm', 1e-2],
                               ['F', "Elastic characteristic force", 'N', 10.],
                               ['A', "Damping coefficient", 'N.s/m', 1e2],
                               ['B', "Hysteresis coefficient", 'd.u.', 2.5]],
                'refs': {1: 'Antoine Falaize and Thomas Helie. Passive simulation of the nonlinear port-hamiltonian modeling of a rhodes piano. Journal of Sound and Vibration, 2016.'},
                'nnodes': 2,
                'nedges': 2,
                'flux': dicmetadata['flux'],
                'effort': dicmetadata['effort'],
                }

    __doc__ = componentDoc(metadata)
