# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 19:14:24 2016

@author: Falaize
"""

from pyphs import PHSGraph
from pyphs.config import datum
from pyphs.core.core import symbols
from pyphs.dictionary.tools import nicevarlabel


class PHSPort(PHSGraph):
    """
    Class of port edges on PHSGraph.

    Arguments
    ----------
    label: str,
        The port edge label.

    nodes: tupple,
        The port edge terminals. If a tuple with single element (n1) is
        provided, the edge is defined as PHSGraph.datum -> n1. Else, the
        tupple must have two elements (n1, n2) and the edge is n1 -> n2.

    **kwargs: dict,
            {'ctrl': {'e', 'f', '?'},
                 Type of control for the edge with
                     - 'e' for effort-controlled,
                     - 'f' for flux-controlled,
                     - '?' for indeterminate control (default).
             'const': {None, float},
                 Constant input value, default is None.
            }

    """
    def __init__(self, label, nodes, **kwargs):

        # update default parameters
        parameters = {'ctrl': '?', 'const': None}
        parameters.update(kwargs)

        PHSGraph.__init__(self, label=label)
        # set starting node to datum if not provided
        if nodes.__len__() == 1:
            node1 = datum
            node2 = nodes[0]
        elif nodes.__len__() == 2:
            node1 = nodes[0]
            node2 = nodes[1]
        # define symbols
        u, y = symbols((nicevarlabel('u', label),
                        nicevarlabel('y', label)))
        # add port to phs
        self.core.add_ports([u], [y])
        # check edge control type (dual of input control type in values[0])
        assert parameters['ctrl'] in ('e', 'f', '?')
        # define edge data
        edge_data = {'label': y,
                     'type': 'port',
                     'ctrl': parameters['ctrl'],
                     'link': None}
        # add edge to phs.Graph
        self.add_edges_from([(node1, node2, edge_data)])
        # check if constant value is provided
        if parameters['const'] is not None:
            self.core.subs.update({u: parameters['const']})
