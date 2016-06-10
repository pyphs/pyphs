# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 19:06:45 2016

@author: Falaize
"""
from pyphs import PortHamiltonianObject, symbols
from dictionary.tools import mappars
from dictionary.config import nice_var_label


class Connector(PortHamiltonianObject):
    """
    class for gyrators and transformers
    """
    def __init__(self, label, nodes, **kwargs):
        # init PortHamiltonianObject
        PortHamiltonianObject.__init__(self, label)
        # pop connector type
        connector_type = kwargs.pop('connector_type')
        # build correspondance between labels in subs and pars (dicpars)...
        # ... and build the correspondance between symbols and subs (subs)
        dicpars, subs = mappars(self, kwargs)
        # update dict of subs in phs
        self.subs.update(subs)
        # replace parameters in alpha by correspondances in 'dicpars'
        alpha = symbols('alpha')
        alpha = alpha.subs(dicpars)
        # symbols for inputs and outputs:
        u1, u2 = symbols([nice_var_label('u', label + str(el))
                          for el in (1, 2)])
        y1, y2 = symbols([nice_var_label('y', label + str(el))
                          for el in (1, 2)])
        connector = {'u': (str(u1), str(u2)), 'y': (str(y1), str(y2)),
                     'alpha': alpha}
        # add connector component
        self.add_connector(connector)
        # update phs.Graph with edges
        edge1_data = {'type': 'connector',
                      'connector_type': connector_type,
                      'alpha': alpha,
                      'realizability': '?',
                      'label': str(y1),
                      'link': str(y2)}
        edge2_data = {'type': 'connector',
                      'connector_type': connector_type,
                      'alpha': alpha,
                      'realizability': '?',
                      'label': str(y2),
                      'link': str(y1)}
        N1, N2, N3, N4 = nodes
        edges = [(N1, N2, edge1_data), (N3, N4, edge2_data)]
        # update phs.Graph with edges
        self.graph.add_edges_from(edges)
