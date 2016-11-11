# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 19:50:15 2016

@author: Falaize
"""
from pyphs import PortHamiltonianObject
from pyphs.dictionary.tools import mappars


class NonLinearStorage(PortHamiltonianObject):
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
        PortHamiltonianObject.__init__(self, label)
        # build correspondance between labels in subs and pars (dicpars)...
        # ... and build the correspondance between symbols and subs (subs)
        dicpars, subs = mappars(self, **kwargs)
        # update dict of subs in phs
        self.symbs.subs.update(subs)
        # replace parameters in H by correspondances in 'dicpars'
        H = H.subs(dicpars)
        # add dissipative component
        self.add_storages(x, H)
        # update phs.Graph with edges
        self.graph.add_edges_from(edges)


#        edge_data_dic = {'label': x,
#                         'type': 'storage',
#                         'ctrl': kwargs['ctrl'],
#                         'link': None}
#        edge = (nodes[0], nodes[1], edge_data_dic)
#        self.graph.add_edges_from([edge])
#        self.symbs.subs.update(subs)
