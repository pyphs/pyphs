#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 14:52:26 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

from pyphs import PHSGraph
from pyphs.dictionary.tools import PHSArgument, nicevarlabel, mappars


###############################################################
# LINEAR
###############################################################

class PHSStorageLinear(PHSGraph):
    """
    Linear flux-controlled storage component
    """
    def __init__(self, label, nodes, **kwargs):
        PHSGraph.__init__(self, label=label)
        if not isinstance(kwargs['value'], PHSArgument):
            coeff = PHSArgument(label + 'coeff', kwargs['value'])
        else:
            coeff = kwargs['value']
        x = nicevarlabel("x", label)
        x = self.core.symbols(x)
        if kwargs['inv_coeff']:
            coeff.symb = coeff.symb**-1
        H = coeff.symb * x**2/2.
        self.core.add_storages([x], H)
        edge_data_dic = {'label': x,
                         'type': 'storage',
                         'ctrl': kwargs['ctrl'],
                         'link': None}
        edge = (nodes[0], nodes[1], edge_data_dic)
        self.add_edges_from([edge])
        self.core.subs.update(coeff.sub)
        if len(coeff.sub) == 0:
            self.core.p  += [coeff.symb, ]


###############################################################
# NONLINEAR
###############################################################

class PHSStorageNonLinear(PHSGraph):
    """
    nonlinear storage component class.

    Parameters
    -----------

    label : str

        component label

    edges : list of networkx edges

    networkx edges are tuples edge = (node_start, node_end, data), where data \
is a diciotnary with the following 'key':value
        * ‘label': sympy.Symbol, edge label.
        * 'ctrl': in ['e', 'f', '?'] control type.
        * '': dic {'e':ze, 'f':zf} where ze and zf are the dissipation \
functions (sympy.Exprs) in the effort-controlled case and the flux controlled \
case, respectively.
        * 'link': not implemented for dssipative components.

    x : list of sp.Symbol

        list of state variables symbols.

    H : sp.Expr

        Scalar storage function expression with symbols in 'x' and in \
keys of the kwargs arguments.

    kwargs: dictionary of component parameters

    """
    def __init__(self, label, edges, x, H, **kwargs):
        # init PortHamiltonianObject
        PHSGraph.__init__(self, label=label)
        # build correspondance between labels in subs and pars (dicpars)...
        # ... and build the correspondance between symbols and subs (subs)
        dicpars, subs = mappars(self, **kwargs)
        # update dict of subs in phs
        self.core.subs.update(subs)
        # replace parameters in H by correspondances in 'dicpars'
        H = H.subs(dicpars)
        # add dissipative component
        self.core.add_storages(x, H)
        # update phs.Graph with edges
        self.add_edges_from(edges)
