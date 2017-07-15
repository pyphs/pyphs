# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 04:32:46 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import networkx as nx
from .analysis import GraphAnalysis
from .build import buildCore
from ..core.core import Core
from ..misc.plots.graphs import plot
from ..graphs import Netlist
from .tools import serial_edges, parallel_edges
from .exceptions import UndefinedPotential
from ..config import datum, VERBOSE
import os


class Graph(nx.MultiDiGraph):
    """
    Class that stores and manipulates graph representation of \
port-Hamiltonian systems.
    """
    def __init__(self, netlist=None, label=None):

        self.datum = datum

        nx.MultiDiGraph.__init__(self)

        self.core = Core()

        if netlist is not None:

            if isinstance(netlist, str):
                netlist = Netlist(netlist)

            elif not isinstance(netlist, Netlist):
                t = type(netlist)
                text = 'Can not understand netlist type {}'.format(t)
                raise TypeError(text)

            self.netlist = netlist

            self._build_from_netlist()

            if label is None:
                label = os.path.basename(netlist.filename).split('.')[0]

        if label is None:
            label = 'None'

        self.label = label

        if VERBOSE >= 1:
            print('Build graph {}...'.format(self.label))

        self._idpar = 0
        self._idser = 0

    def _set_analysis(self, verbose=False, plot=False):
        self.analysis = GraphAnalysis(self, verbose=verbose, plot=plot)

    def buildCore(self, verbose=False, plot=False, connect=True):
        if VERBOSE >= 1:
            print('Build core {}...'.format(self.label))

        self._set_analysis(verbose=verbose, plot=plot)

        self.analysis.perform()

        buildCore(self)

        core = self.core.__copy__()

        if connect:
            core.connect()

        core.label = self.label

        return core

    def _build_from_netlist(self):
        """
        build the graph of the system from the netlist structure (see \
    'netlists' module).
        """
        from importlib import import_module
        for line in self.netlist:
            dic_name = 'pyphs.dictionary.' + line['dictionary']
            dic = import_module(dic_name)
            name = line['component'].lower()
            klass = name[0].upper() + name[1:]
            component = getattr(dic, klass)
            component_graph = component(line['label'],
                                        line['nodes'],
                                        **line['arguments'])
            self += component_graph

    def plot(self, filename=None, ax=None, show=True):
        """
        Plot the graph (networkx.plot method).
        """
        plot(self, filename=filename, ax=ax, show=show)

    def _split_serial(self):
        se = serial_edges(self)
        for edges in se:
            for e in edges[0]:
                self.remove_edges_from([(e[0], e[1], None) for e in edges[0]])
            sg = Graph()

            for n in edges[1:3]:
                if not n == datum:
                    sg.add_edge(datum, n, attr_dict={'type': 'port',
                                                     'ctrl': '?',
                                                     'label': n})
            sg.add_edges_from(edges[0])
            sg._set_analysis()
            self._idser += 1
            self.add_edge(edges[1], edges[2],
                          attr_dict={'type': 'graph',
                                     'ctrl': '?',
                                     'label': 'serial{0}'.format(self._idser),
                                     'graph': sg})
            nodes_to_remove = list()
            for degree in self.degree_iter():
                if degree[1] == 0:
                    nodes_to_remove.append(degree[0])

            for node in nodes_to_remove:
                self.remove_node(node)
        return bool(len(se))

    def _split_parallel(self):
        pe = parallel_edges(self)
        for edges in pe:
            n1, n2 = edges[0][:2]
            self.remove_edges_from([(n1, n2, k) for k in self[n1][n2]])
            try:
                self.remove_edges_from([(n2, n1, k) for k in self[n2][n1]])
            except KeyError:
                pass
            pg = Graph()
            pg.add_edges_from(edges)

            pg._set_analysis()
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
            change_s = self._split_serial()
            change_p = self._split_parallel()
            flag = any((change_s, change_p))

    def __add__(graph1, graph2):
        if hasattr(graph1, 'netlist') and hasattr(graph2, 'netlist'):
            graph1.netlist += graph2.netlist
        graph1.core += graph2.core
        graph1.add_edges_from(graph2.edges(data=True))
        return graph1

    @staticmethod
    def iter_analysis(graph):
        graph.analysis.iteration()
        for e in graph.edges(data=True):
            if e[-1]['type'] == 'graph':
                try:
                    Graph.iter_analysis(e[-1]['graph'])
                except UndefinedPotential:
                    pass
