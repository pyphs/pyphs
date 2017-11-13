#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 13:34:26 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

from pyphs import Graph
from pyphs.dictionary.tools import Argument, nicevarlabel, mappars


###############################################################
# LINEAR
###############################################################

class DissipativeLinear(Graph):
    """
    Class of linear dissipative edges on Graph.

    Arguments
    ----------
    label: str,
        The dissipative edge label.

    nodes: (n1, n2),
        The dissipative edge terminals with edge direction n1 -> n2.

    **kwargs: dict,
            {'ctrl': {'e', 'f', '?'},
                 Type of control for the edge with
                     - 'e' for effort-controlled,
                     - 'f' for flux-controlled,
                     - '?' for indeterminate control (default).
             'coeff': Argument,
                 The dissipative relation is effort = coeff.symb * flux
            }

    """
    def __init__(self, label, nodes, **kwargs):
        Graph.__init__(self, label=label)
        if not isinstance(kwargs['coeff'], Argument):
            coeff = Argument(label + 'coeff', kwargs['coeff'])
        else:
            coeff = kwargs['coeff']
        w_label = nicevarlabel("w", label)
        w = self.core.symbols(w_label)
        z_f_ctrl = coeff.symb*w
        z_e_ctrl = w/coeff.symb
        if 'inv_coeff' in kwargs and kwargs['inv_coeff']:
            z_f_ctrl, z_e_ctrl = z_e_ctrl, z_f_ctrl
        self.core.add_dissipations([w], [z_f_ctrl])
        edge_data_dic = {'label': w,
                         'type': 'dissipative',
                         'ctrl': '?',
                         'z': {'e_ctrl': z_e_ctrl, 'f_ctrl': z_f_ctrl},
                         'link': None}
        edge = (nodes[0], nodes[1], edge_data_dic)
        self.add_edges_from([edge])
        self.core.subs.update(coeff.sub)
        if len(coeff.sub) == 0:
            self.core.p  += [coeff.symb, ]


###############################################################
# NON LINEAR
###############################################################

class DissipativeNonLinear(Graph):
    """
    nonlinear dissipative componen class.

    Parameters
    -----------

    label : str

        component label

    edges : list of networkx edges

    networkx edges are tuples edge = (node_start, node_end, data), where data \
is a diciotnary with the following 'key':value
        * ‘label': sympy.Symbol, edge label.
        * 'ctrl': in ['e', 'f', '?'] control type. if indeterminate '?' then \
a dictionary of dissipation function z must be provided.
        * 'z': dic {'e':ze, 'f':zf} where ze and zf are the dissipation \
functions (sympy.Exprs) in the effort-controlled case and the flux controlled \
case, respectively.
        * 'link': not implemented for dssipative components.

    w : list of sp.Symbol

        list of dissipation variables symbols.

    z : list of sp.Expr

        list of dissipation function expressions with symbols in 'w' and in \
keys of the kwargs arguments.

    kwargs: dictionary of component parameters

    """
    def __init__(self, label, edges, w, z, **kwargs):
        if not hasattr(w, '__len__'):
            w = [w, ]
        if not hasattr(z, '__len__'):
            z = [z, ]
        assert len(w) == len(z),\
            'len(z)={0!s} is not equal to len(w)={1!s}.'.format(len(z), len(w))
        # init PortHamiltonianObject
        Graph.__init__(self, label=label)
        # build correspondance between labels in subs and pars (dicpars)...
        # ... and build the correspondance between symbols and subs (subs)
        dicpars, subs = mappars(self, **kwargs)
        # update dict of subs in phs
        self.core.subs.update(subs)
        # replace parameters in z by correspondances in 'dicpars'
        for i, zz in enumerate(z):
            z[i] = zz.subs(dicpars)
        for e, edge in enumerate(edges):
            if 'z' in edge[2].keys():
                for k in ['e_ctrl', 'f_ctrl']:
                    edges[e][2]['z'][k] = edge[2]['z'][k].subs(dicpars)

        # add dissipative component
        self.core.add_dissipations(w, z)
        # update phs.Graph with edges
        self.add_edges_from(edges)
