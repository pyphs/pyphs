# -*- coding: utf-8 -*-
"""
Created on Sat May 21 16:24:12 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

import sympy
from .tools import symbols, nicevarlabel
from pyphs.config import GMIN
from .edges import (PHSPort,
                    PHSDissipativeLinear, PHSDissipativeNonLinear,
                    PHSStorageLinear)

__all__ = ['Source', 'Capacitor', 'Inductor', 'Resistor',
           'Potentiometer', 'Diode', 'Bjt', 'Triode']


class Source(PHSPort):
    """
    Voltage or current source

    Usage
    ------
        electronics.source label ('node1', 'node2'): type='type'

        where 'type' is the source type in ('voltage', 'current').


    Parameters
    -----------

    label : str, port label.

    nodes: tuple of nodes labels

        if a single label in nodes, port edge is "datum -> node"; \
else, the edge corresponds to "nodes[0] -> nodes[1]".

    kwargs: dic with following "keys:values"

        * 'type' : source type in ('voltage', 'current').

    Not implemented:
    ----------------

        * 'const': if not None, the input will be replaced by the value (subs).
    """
    def __init__(self, label, nodes, **kwargs):
        type_ = kwargs['type']
        type_ = type_.lower()
        assert type_ in ('voltage', 'current')
        if type_ == 'voltage':
            ctrl = 'f'
        elif type_ == 'current':
            ctrl = 'e'
        kwargs.update({'ctrl': ctrl})
        PHSPort.__init__(self, label, nodes, **kwargs)

    @staticmethod
    def metadata():
        return {'nodes': ('N1', 'N2'),
                'arguments': {'type': 'voltage'}}


class Capacitor(PHSStorageLinear):
    """
    Linear capacitor

    Parameters
    -----------

    label : str, port label.

    nodes: tuple of nodes labels

        Edge is "nodes[0] -> nodes[1]".

    kwargs: dic with following "keys:values"

        * 'C' : capacitance value or symbol label or tuple (label, value).
    """
    def __init__(self, label, nodes, **kwargs):
        par_name = 'C'
        par_val = kwargs[par_name]
        kwargs = {'name': par_name,
                  'value': par_val,
                  'inv_coeff': True,
                  'ctrl': 'f'}
        PHSStorageLinear.__init__(self, label, nodes, **kwargs)
    @staticmethod
    def metadata():
        return {'nodes': ('N1', 'N2'),
                'arguments': {'C': ('Csymbol', 1e-9)}}


class Inductor(PHSStorageLinear):
    """
    Linear inductor

    Parameters
    -----------

    label : str, port label.

    nodes: tuple of nodes labels

        Edge is "nodes[0] -> nodes[1]".

    kwargs: dic with following "keys:values"

        * 'L' : inductance value or symbol label or tuple (label, value).
    """
    def __init__(self, label, nodes, **kwargs):
        par_name = 'L'
        par_val = kwargs[par_name]
        kwargs = {'name': par_name,
                  'value': par_val,
                  'inv_coeff': True,
                  'ctrl': 'e'}
        PHSStorageLinear.__init__(self, label, nodes, **kwargs)
    @staticmethod
    def metadata():
        return {'nodes': ('N1', 'N2'),
                'arguments': {'L': ('Lsymbol', 1e-3)}}


class Resistor(PHSDissipativeLinear):
    """
    Linear resistor (unconstrained control)

    Parameters
    -----------

    label : str, port label.

    nodes: tuple of nodes labels

        Edge is "nodes[0] -> nodes[1]".

    kwargs: dic with following "keys:values"

        * 'R' : Resistance value or symbol label or tuple (label, value).
    """
    def __init__(self, label, nodes, **kwargs):
        if kwargs['R'] is None:
            coeff = 0
        else:
            coeff = kwargs['R']
        PHSDissipativeLinear.__init__(self, label, nodes, coeff=coeff)
    @staticmethod
    def metadata():
        return {'nodes': ('N1', 'N2'),
                'arguments': {'R': ('Rsymbol', 1e3)}}


class Potentiometer(PHSDissipativeNonLinear):
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
    """
    def __init__(self, label, nodes, **kwargs):
        # parameters
        pars = ['R', 'alpha', 'expo']
        for par in pars:
            assert par in kwargs.keys()
        R, alpha, expo = symbols(pars)
        # dissipation variable
        w = symbols(["w"+label+str(i) for i in (1, 2)])
        # dissipation funcion
        R1 = 1 + R*alpha**expo
        R2 = 1 + R*(1-alpha**expo)
        z = [R1*w[0], R2*w[1]]

        N1, N2, N3 = nodes
        # edges
        data_1 = {'label': w[0],
                  'type': 'dissipative',
                  'z': {'e_ctrl': w[0]/R1,
                        'f_ctrl': R1*w[0]},
                  'ctrl': '?',
                  'link': None}
        edge_1 = (N1, N2, data_1)

        # edges
        data_2 = {'label': w[1],
                  'type': 'dissipative',
                  'z': {'e_ctrl': w[1]/R2,
                        'f_ctrl': R2*w[1]},
                  'ctrl': '?',
                  'link': None}
        edge_2 = (N2, N3, data_2)

        # init component
        PHSDissipativeNonLinear.__init__(self, label,
                                         [edge_1, edge_2],
                                         w, z, **kwargs)
    @staticmethod
    def metadata():
        return {'nodes': ('N1', 'N2', 'N3'),
                'arguments': {'R': ('R', 1e-9),
                              'alpha': 'alpha',
                              'expo': ('expo', 1)}}


class Diode(PHSDissipativeNonLinear):
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
            assert par in kwargs.keys()
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
        PHSDissipativeNonLinear.__init__(self, label,
                                         [edge_diode,
                                          edge_resistor,
                                          edge_gmin],
                                         w,
                                         [zd_fctrl, z_fctrl, zgmin_fctrl],
                                         **kwargs)

    @staticmethod
    def metadata():
        return {'nodes': ('N1', 'N2'),
                'arguments': {'Is': ('Is', 2e-09),
                              'R': ('Rd', 0.5),
                              'v0': ('v0', 26e-3),
                              'mu': ('mu', 1.7)}}


class Bjt(PHSDissipativeNonLinear):
    """
    bipolar junction transistor of NPN type according to on Ebers-Moll model.

    Usage
    -----

    electronics.bjt label (Nb, Nc, Ne): **kwargs

    Parameters
    -----------

    +------------+----------------+------------------------------------------+
    | Param.     | Typical value  | Description (units)                      |
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
        coeffs = sympy.Matrix([[(betaR+1)/betaR, -1],
                               [-1, (betaF+1)/betaF]])
        funcs = [Is*(sympy.exp(wbjt[0]/(mu*Vt))-1) + GMIN*wbjt[0],
                 Is*(sympy.exp(wbjt[1]/(mu*Vt))-1) + GMIN*wbjt[1]]
        zbjt = coeffs*sympy.Matrix(funcs)
        # bjt edges data
        data_bc = {'label': wbjt[0],
                   'type': 'dissipative',
                   'ctrl': 'e',
                   'link': None}
        data_be = {'label': wbjt[1],
                   'type': 'dissipative',
                   'ctrl': 'e',
                   'link': None}
        # connector resistances dissipative functions
        wR = symbols(["w"+label+ind for ind in ['rb', 'rc', 're']])
        Rmat = sympy.diag(Rb, Rc, Re)
        zR = Rmat*sympy.Matrix(wR)
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
        PHSDissipativeNonLinear.__init__(self, label, edges, wbjt + wR,
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

class Triode(PHSDissipativeNonLinear):
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
    def __init__(self, label, nodes_labels, subs):
        # parameters
        pars = ['mu', 'Ex', 'Kg', 'Kp', 'Kvb', 'Vcp', 'Va', 'Rgk']
        mu, Ex, Kg, Kp, Kvb, Vcp, Va, Rgk = symbols(pars)
        # dissipation variable
        vpk, vgk = symbols([nicevarlabel("w", label+el)
                            for el in ['pk', 'gk']])
        w = [vpk, vgk]

        # dissipation funcions

        def igk():
            """
            dissipation function for edge 'e = (g->k)'
            """
            exprp = (vgk-Va)/Rgk
            exprm = 0.
            expr = sympy.Piecewise((exprm, vgk <= Va), (exprp, True))
            return expr

        def ipk():
            """
            dissipation function for edge 'e = (p->k)'
            """
            e1 = vgk + Vcp
            e2 = sympy.sqrt(Kvb + vpk**2)
            e3 = Kp*(mu**-1 + e1/e2)
            exprE = (vpk/Kp)*sympy.log(1 + sympy.exp(e3))
            expr = exprE**Ex * (1 + sympy.sign(exprE)) / Kg
            return expr

        z = [ipk(), igk()]

        # edges data
        edge_pk_data = {'label': w[0],
                        'type': 'dissipative',
                        'realizability': 'effort_controlled',
                        'linear': False,
                        'link': w[0]}
        edge_gk_data = {'label': w[1],
                        'type': 'dissipative',
                        'realizability': 'effort_controlled',
                        'linear': False,
                        'link': w[1]}
        # edges
        edge_pk = (nodes_labels[1], nodes_labels[0], edge_pk_data)
        edge_gk = (nodes_labels[2], nodes_labels[0], edge_gk_data)
        edges = [edge_pk, edge_gk]

        # init component
        PHSDissipativeNonLinear.__init__(self, label, nodes_labels, subs,
                                         pars, [w], [z], edges)

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
