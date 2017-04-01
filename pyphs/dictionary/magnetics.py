# -*- coding: utf-8 -*-
"""
Created on Sat May 21 16:24:12 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

import sympy as sp
from .edges import (PHSPort,
                    PHSDissipativeLinear, PHSStorageLinear,
                    PHSStorageNonLinear)
from pyphs.core.core import symbols

__all__ = ['Source', 'Capacitor', 'Resistor', 'Capacitorsat']


class Source(PHSPort):
    """
    Source of variation of magnetic flux or magnetomotive force.

    Usage
    ------
        magnetics.source label ('node1', 'node2'): type='type'

        where 'type' is the source type in ('mmf', 'fluxvar').


    Parameters
    -----------

    label : str, port label.

    nodes: tuple of nodes labels

        if a single label in nodes, port edge is "datum -> node"; \
else, the edge corresponds to "nodes[0] -> nodes[1]".

    kwargs: dic with following "keys:values"

        * 'type' : source type in ('mmf', 'fluxvar').
            With variation of magnetic flux (fluxvar) or
            magnetomotive force (mmf).

    Not implemented:
    ----------------

        * 'const': if not None, the input will be replaced by the value (subs).
    """
    def __init__(self, label, nodes, **kwargs):
        type_ = kwargs['type']
        type_ = type_.lower()
        assert type_ in ('mmf', 'fluxvar')
        if type_ == 'mmf':
            ctrl = 'f'
        elif type_ == 'fluxvar':
            ctrl = 'e'
        kwargs.update({'ctrl': ctrl})
        PHSPort.__init__(self, label, nodes, **kwargs)

    @staticmethod
    def metadata():
        return {'nodes': ('N1', 'N2'),
                'arguments': {'type': 'mmf'}}


class Capacitor(PHSStorageLinear):
    """
    Linear capacitor

    Parameters
    -----------

    label : str, port label.

    nodes: tuple of nodes labels

        Edge is "nodes[0] -> nodes[1]".

    kwargs: dic with following "keys:values"

        * 'C' : mag. capacitance value or symbol label or tuple (label, value);
                units is H.
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


class Resistor(PHSDissipativeLinear):
    """
    Linear magnetic resistor (unconstrained control).

    Parameters
    -----------

    label : str, port label.

    nodes: tuple of nodes labels

        Edge is "nodes[0] -> nodes[1]".

    kwargs: dic with following "keys:values"

        * 'R' : Mag. resistance value or symbol label or tuple (label, value);
                units is 1/Ohm.
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
                'arguments': {'R': ('Rsymbol', 1e-3)}}


class Capacitorsat(PHSStorageNonLinear):
    """
    Magnetic capacitor with saturating nonlinearity
    F(phi)=C0*(phi + Csat*c(phi)) with
    sat(phi) = (4/(4-phi))*(tan(pi*phi/(2*phisat))-(pi*phi/(2*phisat)))

    Usage
    -----

    magnetics.capacitorsat label nodes: **kwargs

    Parameters:
    -----------

    nodes : (N1, N2)
        tuple of nodes labels (int or string). The edge (ie. the flux \
'phi') is directed from N1 to N2.

    kwargs : dictionary with following "key: value"

         * 'C0': Magnetic capacity (H)
         * 'Csat': Nonlinear contribution (dimensionless unit)
         * 'phisat': Saturating flux (Wb)
    """
    def __init__(self, label, nodes, **kwargs):
        # parameters
        pars = ['C0', 'Csat', 'phisat']
        for par in pars:
            assert par in kwargs.keys()
        K0, Ksat, xsat = symbols(pars)
        # state  variable
        x = symbols("x"+label)
        # storage funcion
        Hlin = x**2/2
        t1 = sp.pi*x/(2*xsat)
        c1 = (8*xsat/(sp.pi*(4-sp.pi)))
        Hsat = c1 * (sp.log(sp.cos(t1)) + (t1**2)/2.)
        H = K0*(Hlin - Ksat*Hsat)
        N1, N2 = nodes

        # edge data
        data = {'label': x,
                'type': 'storage',
                'ctrl': 'f',
                'link': None}

        # edge
        edge = (N1, N2, data)

        # init component
        PHSStorageNonLinear.__init__(self, label, [edge],
                                     x, H, **kwargs)

    @staticmethod
    def metadata():
        return {'nodes': ('N1', 'N2'),
                'arguments': {'C0': ('C0', 1e3),
                              'Csat': ('Csat', 1e3),
                              'phisat': ('phisat', 1e-2)}}
