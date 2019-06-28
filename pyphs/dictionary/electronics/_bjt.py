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
from ..tools import componentDoc, parametersDefault
from ..electronics import metadata as dicmetadata


class Bjt(DissipativeNonLinear):

    def __init__(self, label, nodes, **kwargs):

        self.__doc__ = componentDoc(Bjt.metadata)

        parameters = parametersDefault(self.metadata['parameters'])
        parameters.update(kwargs)

        pars = ['Is', 'betaR', 'betaF', 'Vt', 'mu', 'Rb', 'Rc', 'Re']

        for par in pars:
            assert par in parameters.keys()

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
        iNb, iNc, iNe = [label + '_' + str(el) for el in (Nb, Nc, Ne)]
        edges = [(iNb, iNc, data_bc),
                 (iNb, iNe, data_be),
                 (Nb, iNb, data_rb),
                 (Nc, iNc, data_rc),
                 (Ne, iNe, data_re)]
        # init component
        DissipativeNonLinear.__init__(self, label, edges, wbjt + wR,
                                         list(zbjt) + list(zR), **parameters)

    metadata = {'title': 'Bipolar junction transistor',
                'component': 'Bjt',
                'label': 'bjt',
                'dico': 'electronics',
                'desc': 'Bipolar junction transistor of NPN type according to the Ebers-Moll model [1]_.',
                'nodesdesc': "base 'Nb', collector 'Nc', emitter 'Ne'.",
                'nodes': ('Nb', 'Nc', 'Ne'),
                'parameters': [['Is', 'Reverse saturation current', 'A', 1e-12],
                               ['betaR', 'Reverse common emitter current gain in [0, 20]', 'd.u.', 10.],
                               ['betaF', 'Forward common emitter current gain in [20, 500]', 'd.u.', 200.],
                               ['Vt', 'Thermal voltage at room temperature', 'V', 26e-3],
                               ['mu', 'Ideality factor in [1, 2]', 'd.u.', 1.],
                               ['Rb', 'Zero bias base resistance', 'Ohms', 20.],
                               ['Rc', 'Collector resistance', 'Ohms', 0.1],
                               ['Re', 'Emitter resistance', 'Ohms', 0.1]],
                'refs': {1: 'https://en.wikipedia.org/wiki/Bipolar_junction_transistor#Ebers.E2.80.93Moll_model'},
                'nnodes': 6,
                'nedges': 5,
                'flux': dicmetadata['flux'],
                'effort': dicmetadata['effort'],
                }

    # Write documentation
    __doc__ = componentDoc(metadata)
