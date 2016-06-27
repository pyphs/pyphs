# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 19:03:35 2016

@author: Falaize
"""
from pyphs import PortHamiltonianObject
from pyphs.dictionary.tools import parsub
from pyphs.dictionary.config import nice_var_label


class LinearStorage(PortHamiltonianObject):
    """
    Linear flux-controlled storage component
    """
    def __init__(self, label, nodes, **kwargs):
        par_name = kwargs['name']
        par_value = kwargs['value']
        PortHamiltonianObject.__init__(self, label)
        par, subs = parsub(self, par_value, par_name + label)
        x = nice_var_label("x", label)
        x = self.symbols(x)
        coeff = par**-1 if kwargs['inv_coeff'] else par
        H = coeff * x**2/2.
        self.add_storages([x], H)
        edge_data_dic = {'label': x,
                         'type': 'storage',
                         'ctrl': kwargs['ctrl'],
                         'link': None}
        edge = (nodes[0], nodes[1], edge_data_dic)
        self.graph.add_edges_from([edge])
        self.symbs.subs.update(subs)


class LinearStorageFluxCtrl(LinearStorage):
    """
    Linear flux-controlled storage component
    """
    def __init__(self, label, nodes, **kwargs):
        kwargs.update({'ctrl': 'f'})
        LinearStorage.__init__(self, label, nodes, **kwargs)


class LinearStorageEffortCtrl(LinearStorage):
    """
    Linear effort-controlled storage component
    """
    def __init__(self, label, nodes, **kwargs):
        kwargs.update({'ctrl': 'e'})
        LinearStorage.__init__(self, label, nodes, **kwargs)
