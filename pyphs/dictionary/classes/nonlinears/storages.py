# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 19:50:15 2016

@author: Falaize
"""
from pyphs import PHSGraph
from pyphs.dictionary.tools import mappars


class NonLinearStorage(PHSGraph):
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
        self.Core.subs.update(subs)
        # replace parameters in H by correspondances in 'dicpars'
        H = H.subs(dicpars)
        # add dissipative component
        self.Core.add_storages(x, H)
        # update phs.Graph with edges
        self.add_edges_from(edges)
