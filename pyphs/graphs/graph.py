# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 04:32:46 2016

@author: Falaize
"""

import sympy as sp
import networkx as nx


class Graph(nx.MultiDiGraph):
    """
    Class that stores and manipulates graph representation of \
port-Hamiltonian systems.
    """
    def __init__(self):
        nx.MultiDiGraph.__init__(self)

        from netlists import Netlist
        self.netlist = Netlist()

    def __add__(graph1, graph2):
        graph = graph1
        net2 = getattr(graph2, 'netlist')
        graph.netlist += net2
        graph.add_edges_from(graph2.edges(data=True))
        return graph

    def _build_analysis(self):
        from analysis.analysis import Analysis
        self.analysis = Analysis(self)

    def _perform_analysis(self):
        if not hasattr(self, 'analysis'):
            self._build_analysis()
        self.analysis.perform()

    def build_from_netlist(self, phs):
        """
        build the graph of the system from the netlist structure (see \
    'netlists' module).
        """
        from importlib import import_module
        for l in range(self.netlist.nlines()):
            line = self.netlist[l]
            dic_name = 'pyphs.dictionary.' + line['dictionary']
            dic = import_module(dic_name)
            name = line['component'].lower()
            klass = name[0].upper() + name[1:]
            component = getattr(dic, klass)
            component_phs = component(line['label'],
                                      line['nodes'],
                                      **line['arguments'])
            phs += component_phs
