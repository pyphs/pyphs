#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 23:56:30 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import sympy
from ..tools import symbols
from pyphs.config import GMIN
from ..edges import DissipativeNonLinear
from ..tools import componentDoc, parametersDefault
from ..electronics import metadata as dicmetadata


class Diode(DissipativeNonLinear):

    def __init__(self, label, nodes, **kwargs):

        parameters = parametersDefault(self.metadata['parameters'])
        parameters.update(kwargs)
        parameters.update({'gmin': ('gmin', GMIN)})
        # parameters
        pars = ['Is', 'v0', 'R', 'mu']
        Is, v0, R, mu, gmin = symbols(pars+['gmin'])
        # dissipation variable
        w = symbols(["w"+label, "w"+label+"_R", "w"+label+"_gmin"])
        # dissipation funcion
        zd_ectrl = Is*(sympy.exp(w[0]/(mu*v0))-1)
        zd_fctrl = mu*v0*sympy.log(w[0]/(Is)+1)
        # dissipation funcion
        z_ectrl = w[1]/R
        z_fctrl = R*w[1]

        # dissipation funcion
        zgmin_ectrl = w[2]*gmin
        zgmin_fctrl = w[2]/gmin

        N1, N2 = nodes
        iN2 = str(N2)+label

        # edge diode data
        data_diode = {'label': w[0],
                      'z': {'e_ctrl': zd_ectrl, 'f_ctrl': zd_fctrl},
                      'type': 'dissipative',
                      'ctrl': '?',
                      'link': None}
        # edge
        edge_diode = (N1, iN2, data_diode)

        # edge resistance data
        data_resistor = {'label': w[1],
                         'z': {'e_ctrl': z_ectrl, 'f_ctrl': z_fctrl},
                         'type': 'dissipative',
                         'ctrl': '?',
                         'link': None}
        # edge
        edge_resistor = (iN2, N2, data_resistor)

        # edge gmin data
        data_gmin = {'label': w[2],
                     'z': {'e_ctrl': zgmin_ectrl, 'f_ctrl': zgmin_fctrl},
                     'type': 'dissipative',
                     'ctrl': '?',
                     'link': None}
        # edge
        edge_gmin = (N1, iN2, data_gmin)

        # init component
        DissipativeNonLinear.__init__(self, label,
                                         [edge_diode,
                                          edge_resistor,
                                          edge_gmin],
                                         w,
                                         [zd_fctrl, z_fctrl, zgmin_fctrl],
                                         **parameters)

    metadata = {'title': 'PN Diode',
                'component': 'Diode',
                'label': 'D',
                'dico': 'electronics',
                'desc': 'PN Diode governed by the Shockley diode equation [1]_.',
                'nodesdesc': "The current is directed from 'N1' to 'N2'.",
                'nodes': ('N1', 'N2'),
                'parameters': [['Is', 'Saturation current', 'A', 2e-9],
                               ['mu', 'Quality factor', 'd.u.', 1.7],
                               ['R', 'Connectors resistance', 'Ohms', 0.5],
                               ['v0', 'Thermal voltage', 'V', 26e-3]],
                'refs': {1: 'https://en.wikipedia.org/wiki/Shockley_diode_equation'},
                'nnodes': 3,
                'nedges': 3,
                'flux': dicmetadata['flux'],
                'effort': dicmetadata['effort'],
                }

    # Write documentation
    __doc__ = componentDoc(metadata)
