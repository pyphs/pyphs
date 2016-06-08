# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 19:50:15 2016

@author: Falaize
"""
from pyphs import PortHamiltonianObject
from dictionary.tools import mappars


class NonLinearDissipative(PortHamiltonianObject):
    """
    nonlinear dissipative componen class.

    Parameters
    -----------

    label : str

        component label

    nodes_labels : list of tuples

        each tupple '(n1, n2)' is associated to an edge e with 'e=(n1 -> n2)'.

    subs : list of tuples

        each tupple is associated to a parameter in 'phs.subs'.

    pars : list of str or sp.Symbol

        list of parameters in z. Coud be str or Symbols (converted to strings).

    w : list of sp.Symbol

        list of dissipation varibales symbols

    z : list of sp.Expr

        list of dissipation function expressions with symbols in 'w' and 'pars'

    edges_data : list of dict

        edges data dictionaries. each dictionary contain the keys:
        * _label_
        * _realizability_
        * _link_

    """
    def __init__(self, label, subs, pars, w, z, edges):
        assert len(w) == len(z),\
            'len(z)={0!s} is not equal to len(w)={1!s}.'.format(len(z), len(w))
        # init PortHamiltonianObject
        PortHamiltonianObject.__init__(self, label)
        # convert pars elements to strings
        pars = map(lambda el: str(el), pars)
        # build correspondance between labels in subs and pars (dicpars)...
        # ... and build the correspondance between symbols and subs (subs)
        dicpars, subs = mappars(self, pars, subs)
        # update dict of subs in phs
        self.subs.update(subs)
        # replace parameters in z by correspondances in 'dicpars'
        for n in len(z):
            z[n] = z[n].subs(dicpars)
        # add dissipative component
        self.addDissipations(w, z)
        # update phs.Graph with edges
        self.Graph.add_edges_from(edges)
