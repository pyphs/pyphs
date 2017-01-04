# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 04:32:46 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import networkx as nx
from .analysis import GraphAnalysis
from .build import buildCore
from pyphs.core.core import PHSCore
from pyphs.plots.graphs import plot
from .tools import serial_edges, getedges, parallel_edges

class PHSGraph(nx.MultiDiGraph):
    """
    Class that stores and manipulates graph representation of \
port-Hamiltonian systems.
    """
    def __init__(self, label=None, netlist=None):

        nx.MultiDiGraph.__init__(self)
        self.core = PHSCore()
        if label is not None:
            self.label = label
        if netlist is not None:
            self.Netlist = netlist
            self.build_from_netlist()

    def __add__(graph1, graph2):
        if hasattr(graph1, 'Netlist') and hasattr(graph2, 'Netlist'):
            graph1.Netlist += graph2.Netlist
        graph1.core += graph2.core
        graph1.add_edges_from(graph2.edges(data=True))
        return graph1

    def buildCore(self, verbose=False, plot=False):
        self.Analysis = GraphAnalysis(self, verbose=verbose, plot=plot)
        self.Analysis.perform()
        buildCore(self)
        core = self.core.__deepcopy__()
        core.apply_connectors()
        core.build_exprs()
        return core

    def build_from_netlist(self):
        """
        build the graph of the system from the netlist structure (see \
    'netlists' module).
        """
        from importlib import import_module
        for line in self.Netlist:
            dic_name = 'pyphs.dictionary.' + line['dictionary']
            dic = import_module(dic_name)
            name = line['component'].lower()
            klass = name[0].upper() + name[1:]
            component = getattr(dic, klass)
            component_graph = component(line['label'],
                                        line['nodes'],
                                        **line['arguments'])
            self += component_graph

    def plot(self, filename=None, ax=None):
        """
        Plot the graph (networkx.plot method).
        """
        plot(self, filename=filename, ax=ax)

    def split_serial(self):
        se = serial_edges(self)
        for edges in se:
            sg = PHSGraph()
            sg.add_edges_from(edges)
            for e in edges:
                self.remove_edges_from([(e[0], e[1], None) for e in edges])
            self.add_edge(edges[0][0], edges[-1][1],
                          attr_dict={'type': 'graph',
                                     'label': 'serial',
                                     'graph': sg})

    def split_parallel(self):
        pe = parallel_edges(self)
        for edges in pe:
            n1, n2 = edges[0][:2]
            self.remove_edges_from([(n1, n2, k) for k in self[n1][n2]])
            self.remove_edges_from([(n2, n1, k) for k in self[n2][n1]])
            pg = PHSGraph()
            pg.add_edges_from(edges)
            self.add_edge(n1, n2,
                          attr_dict={'type': 'graph',
                                     'label': 'parallel',
                                     'graph': pg})
