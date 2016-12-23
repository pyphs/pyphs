# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 19:03:49 2016

@author: Falaize
"""
from pyphs import PHSGraph
from pyphs.dictionary.tools import parsub, nice_var_label


class LinearDissipationFreeCtrl(PHSGraph):
    """
    Linear dissipative component (indeterminate control)
    """
    def __init__(self, label, nodes, **kwargs):
        PHSGraph.__init__(self, label=label)
        par, subs = parsub(self, kwargs['coeff'], 'p'+label)
        w_label = nice_var_label("w", label)
        w = self.Core.symbols(w_label)
        z_f_ctrl = par*w
        z_e_ctrl = w/par
        self.Core.add_dissipations([w], [z_f_ctrl])
        edge_data_dic = {'label': w,
                         'type': 'dissipative',
                         'ctrl': '?',
                         'z': {'e_ctrl': z_e_ctrl, 'f_ctrl': z_f_ctrl},
                         'link': None}
        edge = (nodes[0], nodes[1], edge_data_dic)
        self.add_edges_from([edge])
        self.Core.subs.update(subs)


class LinearDissipationEffortCtrl(PHSGraph):
    """
    Linear dissipative component (effort control)
    """
    def __init__(self, label, nodes, **kwargs):
        PHSGraph.__init__(self, label=label)
        par, subs = parsub(self, kwargs['coeff'], 'p'+label)
        w_label = nice_var_label("w", label)
        w = self.Core.symbols(w_label)
        z_f_ctrl = par*w
        z_e_ctrl = w/par
        self.Core.add_dissipations([w], [z_f_ctrl])
        edge_data_dic = {'label': w,
                         'type': 'dissipative',
                         'ctrl': 'e',
                         'z': {'e_ctrl': z_e_ctrl, 'f_ctrl': z_f_ctrl},
                         'link': None}
        edge = (nodes[0], nodes[1], edge_data_dic)
        self.add_edges_from([edge])
        self.Core.subs.update(subs)

        
class LinearDissipationFluxCtrl(PHSGraph):
    """
    Linear dissipative component (flux control)
    """
    def __init__(self, label, nodes, **kwargs):
        PHSGraph.__init__(self, label=label)
        par, subs = parsub(self, kwargs['coeff'], 'p'+label)
        w_label = nice_var_label("w", label)
        w = self.Core.symbols(w_label)
        z_f_ctrl = par*w
        z_e_ctrl = w/par
        self.Core.add_dissipations([w], [z_f_ctrl])
        edge_data_dic = {'label': w,
                         'type': 'dissipative',
                         'ctrl': 'f',
                         'z': {'e_ctrl': z_e_ctrl, 'f_ctrl': z_f_ctrl},
                         'link': None}
        edge = (nodes[0], nodes[1], edge_data_dic)
        self.add_edges_from([edge])
        self.Core.subs.update(subs)
