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
from .tools import serial_edges, parallel_edges
from .exceptions import UndefinedPotential
from ..config import datum, VERBOSE
import os

description = "\
Class for graph representation of port-Hamiltonian systems and the automated \
generation of pyphs.Core by graph analysis."


class Graph(nx.MultiDiGraph):
    "{0}".format(description)

    # identifiers parallel edges
    _idpar = 0
    # identifiers serial edges
    _idser = 0

    # Datum
    datum = datum

    # -------------------------------------------------------------------------
    def __init__(self, netlist=None, label=None):
        """
        {0}

        Parameters
        ----------

        netlist : Netlist, str, or None (optional)
            If type is pyphs.Netlist, the graph is built with netlist.to_graph.
            If type is str, it is considered as a path to a '*.net' file from
            which a new pyphs.Netlist is created and the graph is built.
            If None, the graph is initialized as empty. Default is None.

        label : str or None (optional)
            Graph label. If None and a netlist is provided, the label is
            recovered from pyphs.Netlist.label value.

        Output
        ------

        graph : pyphs.Graph
            A networkx.MultiDiGraph object with additional methods and
            attributes for the generation of pyphs.Core objects by graph
            analysis.

        """.format(description)


        nx.MultiDiGraph.__init__(self)

        self.core = Core()

        # Read netlist and label
        if netlist is not None:

            from ..graphs import Netlist

            # build a netlist from path if netlist parameter is a string
            if isinstance(netlist, str):
                path = netlist
                netlist = Netlist(path)
            # pass if netlist is a pyphs.Netlist
            elif isinstance(netlist, Netlist):
                pass
            # else raise TypeError
            else:
                t = type(netlist)
                text = 'Can not understand netlist type {}'.format(t)
                raise TypeError(text)

            # store netlist
            self.netlist = netlist

            # graph label
            if label is None:
                # read the label from netlist
                label = os.path.basename(netlist.filename).split('.')[0]

            # Verbosity
            if VERBOSE >= 1:
                print('\nBuild graph {}...'.format(label))

            # read netlist and build graph
            self._build_from_netlist()

        elif label is None:
            label = 'graph'

        # graph label
        self.label = label

    def _build_analysis(self, verbose=False, plot=False):
        """
        Initialize the pyphs.graphs.analysis.GraphAnalysis object.
        """
        self.analysis = GraphAnalysis(self, verbose=verbose, plot=plot)

    def to_core(self, label=None, verbose=False, plot=False, connect=True,
                force=True):
        """
        Return the core PHS object associated with the graph.

        Parameters
        ----------

        label : str (optional)
            String label for the Core object (default None recovers the label
            from the graph).

        verbose : bool (optional)
            If True, the system pauses at each iteration of the graph analysis
            algorithm and a short description of the iteration is printed.
            Default is False.

        plot : bool (optional)
            If True, plot the graph at each iteration of the graph analysis
            algorithm. The color scheme for the edges and nodes reflects the
            state of the analysis process. Default is False.

        connect : bool (optional)
            If True, the method core.connect() is called before output of the
            pyphs.Core object, so that the transformers and gyrators are
            resolved in the structure matrix. Default is True.

        Output
        ------

        core : pyphs.Core
            The PHS core object associated with the graph.

        """
        # verbosity
        if VERBOSE >= 1:
            print('Build core {}...'.format(self.label))

        # check for graph analysis object
        if not hasattr(self, 'analysis'):
            self._build_analysis(verbose=verbose, plot=plot)

        # check for graph analysis object
        if not hasattr(self.analysis, 'iGamma_fc') or force:
            self.analysis.perform()

        # build Core (after graph analysis)
        buildCore(self)

        # returned core is a copy
        core = self.core.__copy__()

        # connect gyrators and transformers
        if connect:
            core.connect()

        # Core.label can be specified, else the Graph.label is recovered
        if label is None:
            label = self.label
        if not isinstance(label, str):
            raise TypeError('Core label not understood:\n{}'.format(label))
        core.label = label

        # Transfer reference to Netlist object
        if hasattr(self, 'netlist'):
            core._netlist = self.netlist

        return core

    def to_method(self, label=None, config=None):
        """
        Return the PHS numerical method associated with the PHS graph for the
        specified configuration.

        Parameter
        ---------

        label : str (optional)
            String label for the Core object (default None recovers the label
            from the graph).

        config : dict or None
            A dictionary of simulation parameters. If None, the standard
            pyphs.config.simulations is used (the default is None).
            keys and default values are

              'fs': 48e3,           # Sample rate (Hz)
              'grad': 'discret',    # In {'discret', 'theta', 'trapez'}
              'theta': 0.,          # Theta-scheme for the structure
              'split': False,       # split implicit from explicit part
              'maxit': 10,          # Max number of iterations for NL solvers
              'eps': 1e-16,         # Global numerical tolerance

        Output
        ------

        method : pyphs.Method
            The PHS numerical method associated with the PHS graph for the
            specified configuration.
        """

        core = self.to_core(label=label)
        return core.to_method(config=config)

    def to_simulation(self, label=None, config=None, inits=None):
        """
        Return the PHS simulation object associated with the PHS graph for the
        specified configuration.

        Parameter
        ---------

        label : str (optional)
            String label for the Core object (default None recovers the label
            from the graph).

        config : dict or None
            A dictionary of simulation parameters. If None, the standard
            pyphs.config.simulations is used (the default is None).
            keys and default values are

              'fs': 48e3,           # Sample rate (Hz)
              'grad': 'discret',    # In {'discret', 'theta', 'trapez'}
              'theta': 0.,          # Theta-scheme for the structure
              'split': False,       # split implicit from explicit part
              'maxit': 10,          # Max number of iterations for NL solvers
              'eps': 1e-16,         # Global numerical tolerance

        Output
        ------

        method : pyphs.Simulation
            The PHS simulation object associated with the PHS graph for the
            specified configuration.
        """

        core = self.to_core(label=label)
        return core.to_simulation(config=config, inits=inits)

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
        Plot the graph (enhanced networkx.plot method).
        """
        plot(self, filename=filename, ax=ax, show=show)

    def _split_serial(self):
        """
        Detect clusters of serial edges and replace them by equivalent
        subgraph.
        """

        from .subgraph import SubGraphSerial

        # list of clusters of serial edges
        se = serial_edges(self)
        for edges in se:
            # remove edges in serial cluster
            for e in edges[0]:
                self.remove_edges_from([(e[0], e[1], None) for e in edges[0]])
            # increment counter for parallel edges labels
            self._idser += 1
            sglabel = 'serial{0}'.format(self._idser)
            # instanciate a new subgraph
            sg = SubGraphSerial(sglabel)
            sg.core = self.core
            # add serial cluster edges
            sg.add_edges_from(edges[0])
            # add serial cluster edges
            for n in edges[1:3]:
                if not n == datum:
                    sg.add_edge(datum, n, **{'type': 'port',
                                             'ctrl': '?',
                                             'label': sglabel + '_out_' + n})
            # build subgraph analysis object
            sg._build_analysis()
            # add subgraph to root graph
            self.add_edge(edges[1], edges[2], **{'type': 'graph',
                                                 'ctrl': '?',
                                                 'label': sglabel,
                                                 'graph': sg})
        self.remove_orphan_nodes()
        # Return True if any change occured
        return bool(len(se))

    def remove_orphan_nodes(self):
        """
        Remove orphan nodes (with degree 0).
        """
        nodes_to_remove = list()
        for degree in self.degree():
            if degree[1] == 0:
                nodes_to_remove.append(degree[0])
        for node in nodes_to_remove:
            self.remove_node(node)

    def _split_parallel(self):
        """
        Detect clusters of parallel edges and replace them by equivalent
        subgraph.
        """

        from .subgraph import SubGraphParallel

        # list of paralell edges
        pe = parallel_edges(self)
        for edges in pe:
            # get the two nodes of the parallel connection
            n1, n2 = edges[0][:2]
            # remove forward edges
            self.remove_edges_from([(n1, n2, k) for k in self[n1][n2]])
            # remove backward edges if any
            try:
                self.remove_edges_from([(n2, n1, k) for k in self[n2][n1]])
            except KeyError:
                pass
            # increment counter for parallel edges labels
            self._idpar += 1
            pglabel = 'parallel{0}'.format(self._idpar)
            # instanciate a new subgraph
            pg = SubGraphParallel(pglabel)
            pg.core = self.core
            # add parallel edges
            pg.add_edges_from(edges)
            # build subgraph analysis object
            pg._build_analysis()
            # add control edge
            for n in (n1, n2):
                if not n == datum:
                    pg.add_edge(datum, n, **{'type': 'port',
                                             'ctrl': '?',
                                             'label': pglabel + '_out_' + n})
            # add subgraph to root graph
            self.add_edge(n1, n2, **{'type': 'graph',
                                     'ctrl': '?',
                                     'label':
                                     pglabel,
                                     'graph': pg})
        # Return True if any change occured
        return bool(len(pe))

    def assemble(self):
        """
        Re-assemble the subgraphs in the current graph
        """

        def assemble_subgraph(graph):
            """
            Resursive import of edges from subgraphs.
            """
            for e in graph.edgeslist:
                if e[-1]['type'] == 'graph':
                    subgraph = e[-1]['graph']
                    subgraph.core = Core()
                    assemble_subgraph(subgraph)
                    graph += subgraph

        assemble_subgraph(self)

        # remove edges
        for e in self.edgeslist:

            elabel = e[-1]['label']
            etype = e[-1]['type']

            if '_out_' in str(elabel) or etype == 'graph':
                # Remove edge
                self.remove_edge_from_list([e, ])

    def remove_edge_from_list(self, edges):
        """
        Remove a list of edges.
        """
        for e in edges:
            # Get edge key
            n1, n2 = e[:2]
            for key in self[n1][n2].keys():
                if self[n1][n2][key]['label'] == e[-1]['label']:
                    break

            # Remove edge
            self.remove_edge(n1, n2, key)

        self.remove_orphan_nodes()

    def split_sp(self):
        """
        Split the graph into a tree graph of serial/parallel subgraphs.
        """
        change = True
        while change:
            # check for serial connection
            change_s = self._split_serial()
            # check for parallel connection
            change_p = self._split_parallel()
            # Test for any change
            change = any((change_s, change_p))

    @property
    def subgraphs(self):
        """
        Get a list of subgraphs.
        """

        def getSubTree(graph):
            labels = {graph.label: graph}
            tree = {graph.label: dict()}
            for e in graph.edges(data=True):
                # if leaf is a subgraph
                if e[-1]['type'] == 'graph':
                    elabel = e[-1]['label']
                    egraph = e[-1]['graph']
                    labels[elabel] = graph
                    sublabels, subtree = getSubTree(egraph)
                    labels.update(sublabels)
                    tree[graph.label][elabel] = subtree[elabel]
            return labels, tree

        labels, tree = getSubTree(self)

        level = 0
        levels = dict()
        levels[level] = (list(tree.keys())[0], )
        continu = True
        while continu:
            continu = False
            level += 1
            levels[level] = ()
            for k in levels[level-1]:
                try:
                    gk = labels[k]
                    for e in gk.edges(data=True):
                        levels[level] += (e[-1]['label'], )
                        # if leaf is a subgraph
                        if e[-1]['type'] == 'graph':
                            continu = True
                except KeyError:
                    pass

        return labels, tree, levels

    def __add__(graph1, graph2):
        """
        Graph summation.
        """
        if hasattr(graph1, 'netlist') and hasattr(graph2, 'netlist'):
            graph1.netlist += graph2.netlist
        graph1.core += graph2.core
        graph1.add_edges_from(graph2.edges(data=True))
        if hasattr(graph1, 'positions'):
            delattr(graph1, 'positions')
        return graph1

    def _get_edgeslist(self):
        """
        Return a list of graph edges with data
        """
        return list(self.edges(data=True))
    edgeslist = property(_get_edgeslist)

    def _get_nodeslist(self):
        """
        Return a set of graph nodes
        """
        return set(self.nodes())
    nodeslist = property(_get_nodeslist)

    @staticmethod
    def iter_analysis(graph):
        """
        Recursive graph analysis over a serial_parallel tree graph.

        See Also
        --------
        pyphs.Graph.split_sp

        """
        # check for graph analysis object
        if not hasattr(graph, 'analysis'):
            graph._build_analysis()
        # analyze root graph
        graph.analysis.iteration()
        # iterate over leaves
        for e in graph.edges(data=True):
            # if leaf is a subgraph
            if e[-1]['type'] == 'graph':
                # iterate
                Graph.iter_analysis(e[-1]['graph'])
