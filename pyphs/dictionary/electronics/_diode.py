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


default = {'Is': ('Is', 2e-09),
           'R': ('Rd', 0.5),
           'v0': ('v0', 26e-3),
           'mu': ('mu', 1.7)}


class Diode(DissipativeNonLinear):
    """
    Electronic nonlinear dissipative component: diode PN

    Usage
    -----

    electronics.diodepn label nodes: **kwargs

    Parameters:
    -----------

    nodes : (N1, N2)
        tuple of nodes labels (int or string). The edge (ie. the current 'i') \
is directed from N1 to N2, with 'i(v))=Is*(exp(v/v0)-1)'.

    kwargs : dictionary with following "key: value"

         * 'Is': saturation current (A)
         * 'v0': quality factor (V)
         * 'R': connectors resistance (Ohms)
         * 'mu': quality factor (d.u.)
    """
    def __init__(self, label, nodes, **kwargs):
        kwargs.update({'gmin': ('gmin', GMIN)})
        # parameters
        pars = ['Is', 'v0', 'R', 'mu']
        for par in pars:
            if par not in kwargs.keys():
                kwargs[par] = default[par]
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
                      'ctrl': 'e',
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
                                         **kwargs)

    @staticmethod
    def metadata():
        return {'nodes': ('N1', 'N2'),
                'arguments': default}
