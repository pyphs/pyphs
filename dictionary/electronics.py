# -*- coding: utf-8 -*-
"""
Created on Sat May 21 16:24:12 2016

@author: Falaize
"""
from classes.connectors.port import Port
from classes.linears.dissipatives import LinearDissipationFreeCtrl
from classes.linears.storages import LinearStorageFluxCtrl, \
    LinearStorageEffortCtrl
from classes.nonlinears.dissipatives import NonLinearDissipative

from config import nice_var_label
from tools import symbols

import sympy


class source(Port):
    """
    Voltage or current source

    Parameters
    -----------

    label : str, port label.

    nodes: tuple of nodes labels

        if a single label in nodes, port edge is "datum -> node"; \
else, the edge corresponds to "nodes[0] -> nodes[1]".

    kwargs: dic with following "keys:values"

        * 'type' : source type in ('voltage', 'current').
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
        Port.__init__(self, label, nodes, **kwargs)


class capacitor(LinearStorageFluxCtrl):
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
                  'inv_coeff': True}
        LinearStorageFluxCtrl.__init__(self, label, nodes, **kwargs)


class inductor(LinearStorageEffortCtrl):
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
                  'inv_coeff': True}
        LinearStorageEffortCtrl.__init__(self, label, nodes, **kwargs)


class resistor(LinearDissipationFreeCtrl):
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
            coeff = 0.
        else:
            coeff = kwargs['R']
        LinearDissipationFreeCtrl.__init__(self, label, nodes, coeff=coeff)


class diodepn(NonLinearDissipative):
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
    """
    def __init__(self, label, nodes, **kwargs):
        # parameters
        pars = ['Is', 'v0']
        for par in pars:
            assert par in kwargs.keys()
        Is, v0 = symbols(pars)
        # dissipation variable
        w = symbols("w"+label)
        # dissipation funcion
        z = Is*(sympy.exp(w/v0)-1)
        # edge data
        edge_data = {'label': w,
                     'type': 'dissipative',
                     'ctrl': 'e',
                     'link': None}
        # edge
        edge = (nodes[0], nodes[1], edge_data)
        # init component
        NonLinearDissipative.__init__(self, label, [edge],
                                      [w], [z], **kwargs)


class bjtnpn:
    """
    bipolar junction transistor of NPN type according to on Ebers-Moll model.
    
    Usage
    -----

    electronics.bjtnpn label (Nb, Nc, Ne] []

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
    

class triode(NonLinearDissipative):
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
        import sympy
        # parameters
        pars = ['mu', 'Ex', 'Kg', 'Kp', 'Kvb', 'Vcp', 'Va', 'Rgk']
        mu, Ex, Kg, Kp, Kvb, Vcp, Va, Rgk = symbols(pars)
        # dissipation variable
        vpk, vgk = symbols([nice_var_label("w", label+el)
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
        NonLinearDissipative.__init__(self, label, nodes_labels, subs,
                                      pars, [w], [z], edges)
