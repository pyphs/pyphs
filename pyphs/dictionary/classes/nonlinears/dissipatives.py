# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 19:50:15 2016

@author: Falaize
"""
from pyphs import PHSGraph
from pyphs.dictionary.tools import mappars


class NonLinearDissipative(PHSGraph):
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
        assert len(w) == len(z),\
            'len(z)={0!s} is not equal to len(w)={1!s}.'.format(len(z), len(w))
        # init PortHamiltonianObject
        PHSGraph.__init__(self, label=label)
        # build correspondance between labels in subs and pars (dicpars)...
        # ... and build the correspondance between symbols and subs (subs)
        dicpars, subs = mappars(self, **kwargs)
        # update dict of subs in phs
        self.Core.subs.update(subs)
        # replace parameters in z by correspondances in 'dicpars'
        for i, zz in enumerate(z):
            z[i] = zz.subs(dicpars)
        for e, edge in enumerate(edges):
            if 'z' in edge[2].keys():
                for k in ['e_ctrl', 'f_ctrl']:
                    edges[e][2]['z'][k] = edge[2]['z'][k].subs(dicpars)

        # add dissipative component
        self.Core.add_dissipations(w, z)
        # update phs.Graph with edges
        self.add_edges_from(edges)
