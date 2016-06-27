# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 19:14:24 2016

@author: Falaize
"""

from pyphs import PortHamiltonianObject
from pyphs.graphs.config import datum
from pyphs.dictionary.config import nice_var_label
from pyphs.symbolics.tools import symbols


class Port(PortHamiltonianObject):
    """
    port
    """
    def __init__(self, label, nodes, **kwargs):

        PortHamiltonianObject.__init__(self, label)
        # set starting node to datum if not provided
        if nodes.__len__() == 1:
            node1 = datum
            node2 = nodes[0]
        elif nodes.__len__() == 2:
            node1 = nodes[0]
            node2 = nodes[1]
        # define symbols
        u, y = symbols((nice_var_label('u', label),
                        nice_var_label('y', label)))
        # add port to phs
        self.add_ports([u], [y])
        # check edge control type (dual of input control type in values[0])
        assert kwargs['ctrl'] in ('e', 'f', '?')
        # define edge data
        edge_data = {'label': y,
                     'type': 'port',
                     'ctrl': kwargs['ctrl'],
                     'link': None}
        # add edge to phs.Graph
        self.graph.add_edges_from([(node1, node2, edge_data)])
        # check if constant value is provided
        if 'const' in kwargs.keys():
            self.symbs.subs.update({u: kwargs['const']})
