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
from .tools import serial_edges, parallel_edges
from .exceptions import PHSUndefinedPotential
from pyphs.config import datum


class PHSGraph(nx.MultiDiGraph):
    """
    Class that stores and manipulates graph representation of \
port-Hamiltonian systems.
    """
    def __init__(self, netlist=None, label=None):

        nx.MultiDiGraph.__init__(self)
        self.core = PHSCore()
        self._idpar = 0
        self._idser = 0
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

    def set_analysis(self, verbose=False, plot=False):
        self.analysis = GraphAnalysis(self, verbose=verbose, plot=plot)

    def buildCore(self, verbose=False, plot=False, apply_connectors=True):
        self.set_analysis(verbose=verbose, plot=plot)
        self.analysis.perform()
        buildCore(self)
        core = self.core.__deepcopy__()
        if apply_connectors:
            core.apply_connectors()
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
            for e in edges[0]:
                self.remove_edges_from([(e[0], e[1], None) for e in edges[0]])
            sg = PHSGraph()

            for n in edges[1:3]:
                if not n == datum:
                    sg.add_edge(datum, n, attr_dict={'type': 'port',
                                                     'ctrl': '?',
                                                     'label': n})
            sg.add_edges_from(edges[0])
            sg.set_analysis()
            self._idser += 1
            self.add_edge(edges[1], edges[2],
                          attr_dict={'type': 'graph',
                                     'ctrl': '?',
                                     'label': 'serial{0}'.format(self._idser),
                                     'graph': sg})
            for degree in self.degree_iter():
                if degree[1] == 0:
                    self.remove_node(degree[0])
        return bool(len(se))

    def split_parallel(self):
        pe = parallel_edges(self)
        for edges in pe:
            n1, n2 = edges[0][:2]
            self.remove_edges_from([(n1, n2, k) for k in self[n1][n2]])
            try:
                self.remove_edges_from([(n2, n1, k) for k in self[n2][n1]])
            except KeyError:
                pass
            pg = PHSGraph()
            pg.add_edges_from(edges)

            pg.set_analysis()
            self._idpar += 1
            for n in (n1, n2):
                if not n == datum:
                    pg.add_edge(datum, n, attr_dict={'type': 'port',
                                                     'ctrl': '?',
                                                     'label': n})
            self.add_edge(n1, n2,
                          attr_dict={'type': 'graph',
                                     'ctrl': '?',
                                     'label':
                                         'parallel{0}'.format(self._idpar),
                                     'graph': pg})
        return bool(len(pe))

    def split_sp(self):
        flag = True
        while flag:
            change_s = self.split_serial()
            change_p = self.split_parallel()
            flag = any((change_s, change_p))

    @staticmethod
    def iter_analysis(graph):
        graph.analysis.iteration()
        for e in graph.edges(data=True):
            if e[-1]['type'] == 'graph':
                try:
                    PHSGraph.iter_analysis(e[-1]['graph'])
                except PHSUndefinedPotential:
                    pass
