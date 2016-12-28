# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 04:32:46 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import networkx as nx
from .analysis.analysis import GraphAnalysis
from .analysis.build import buildCore
from pyphs.core.core import PHSCore
from pyphs.plots.graphs import plot


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

    def buildCore(self):
        self.Analysis = GraphAnalysis(self)
        self.Analysis.perform()
        buildCore(self)
        self.core.apply_connectors()
        self.core.exprs_build()
        return self.core.__deepcopy__()

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
