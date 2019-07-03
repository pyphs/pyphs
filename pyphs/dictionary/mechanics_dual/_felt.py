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
from ..mechanics_dual import metadata as dicmetadata
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
        N3 = label+'_N3'
        xnl = symbols('q'+label)
        hnl = sp.Piecewise((0., xnl <= 0.), ((L*F/(B+1))*(xnl/L)**(B+1), True))
        hnl = hnl.subs(dicpars)
        # edge data
        data = {'label': xnl,
                'type': 'storage',
                'ctrl': 'f',
                'link': None}
        self.add_edges_from([(N1, N3, data), ])
        self.core.add_storages(xnl, hnl)

        r = sp.Piecewise((0., xnl <= 0.), ((A * L/B)*(xnl/L)**(B-1), True))
        r = r.subs(dicpars)
        wnl = symbols('dtq'+label)
        # edge data
        data = {'label': wnl,
                'type': 'dissipative',
                'ctrl': 'f',
                'z': {'f_ctrl': r*wnl, 'e_ctrl': sp.sympify(0)},
                'link': None}
        self.add_edges_from([(N3, N2, data), ])
        self.core.add_dissipations(wnl, r*wnl)

        self.core.subs.update(subs)

    metadata = {'title': 'Felt material',
                'component': 'Felt',
                'label': 'felt',
                'dico': 'mechanics_dual',
                'desc': (r'Nonlinear felt material used in piano-hammer. The model is that found in [1]_ eq. (11). It includes a nonlinear restoring force and a nonlinear damper as follows:' +
                         equation(r'e_{total}\left(c, \dot c\right) = e_{elastic}(c) + e_{damper}\left(c, \dot c\right),') +
                         'with' +
                         equation(r'e_{elastic}(c)  = F \,c ^B,') +
                         'and' +
                         equation(r'e_{damper}\left(c, \dot c\right) = \frac{A \, L}{B} c^{B-1} \,\dot c,') +
                         'where :math:`c = \\frac{\\max (q, 0)}{L}` is the crush of the hammer with contraction :math:`q\\in\\mathbb R`.'),
                'nodesdesc': "Nodes associated with the component terminals with positive flux N1->N2.",
                'nodes': ('N1', 'N2'),
                'parametersdesc': 'Component parameters.',
                'parameters': [['L', "Height at rest", 'm', 1e-2],
                               ['F', "Elastic characteristic force", 'N', 10.],
                               ['A', "Damping coefficient", 'N.s/m', 1e2],
                               ['B', "Hysteresis coefficient", 'd.u.', 2.5]],
                'refs': {1: 'Antoine Falaize and Thomas Helie. Passive simulation of the nonlinear port-hamiltonian modeling of a rhodes piano. Journal of Sound and Vibration, 2016.'},
                'nnodes': 3,
                'nedges': 2,
                'flux': dicmetadata['flux'],
                'effort': dicmetadata['effort'],
                }

    __doc__ = componentDoc(metadata)
