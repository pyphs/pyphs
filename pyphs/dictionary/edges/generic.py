#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 20:18:13 2017

@author: Falaize
"""

from pyphs import Graph
from pyphs.dictionary.tools import Argument, mappars


class Generic(Graph):
    """
Generic component class.

Parameters
-----------

label : str

    component label

edges : list of networkx edges

    networkx edges are tuples edge = (node_start, node_end, data), where data
    is a dictionary with the following 'key': value
        * ‘label': sympy.Symbol, edge label.
        * 'ctrl': in ['e', 'f', '?'] control type.
        * '': dic {'e':ze, 'f':zf} where ze and zf are the dissipation
        functions (sympy.Exprs) in the effort-controlled case and the flux
        controlled.
    case, respectively.
        * 'link': not implemented for dssipative components.

x : list of sp.Symbol

    list of state variables symbols.

H : sp.Expr

    Scalar storage function expression with symbols in 'x' and in keys of the
    kwargs arguments.

kwargs: dictionary of component parameters

    """
    def __init__(self, label, edges, **kwargs):
        # init PortHamiltonianObject
        Graph.__init__(self, label=label)
        # build correspondance between labels in subs and pars (dicpars)...
        # ... and build the correspondance between symbols and subs (subs)
        dicpars, subs = mappars(self, **kwargs)
        # update dict of subs in phs
        self.core.subs.update(subs)
        # update phs.Graph with edges
        self.add_edges_from(edges)
