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
from .exceptions import IndeterminateRealizability
from ..config import datum, VERBOSE, GRAPHS_LAYOUT, GRAPHS_ITERATIONS
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

    # ----------------------------------------------------------------------- #

    def _build_analysis(self, verbose=False, plot=False):
        """
        Initialize the pyphs.graphs.analysis.GraphAnalysis object.
        """
        # Build analysis object
        self.analysis = GraphAnalysis(self, verbose=verbose, plot=plot)

    def perform_analysis(self, verbose=False, plot=False, solve_arc=True,
                         force=True):
        """
        Perform realizability analysis. Create analysis object first if needed.

        Parameter
        ---------

        verbose : bool (optional)
            If True, the system pauses at each iteration of the graph analysis
            algorithm and a short description of the iteration is printed.
            Default is False.

        plot : bool (optional)
            If True, plot the graph at each iteration of the graph analysis
            algorithm. The color scheme for the edges and nodes reflects the
            state of the analysis process. Default is False.

        solve_arc : bool (optional)
            If True, the anti-realizable components are merged to produce a
            realizable graph. Te default is True.

        force : bool (optional)
            If False, the analysis is performed only if it has not been
            performed previously. If True, the analysis is forced in any case.
            Default is True.

        """

        # verbosity
        if VERBOSE >= 1:
            print('Analyze  {}...'.format(self.label))

        # check for graph analysis object
        if not hasattr(self, 'analysis') or force:

            # Cope with anti-realizable connections
            self.sp_split()
            self.sp_merge_arc()
            self.sp_assemble()

            self._build_analysis(verbose=verbose, plot=plot)

        # check for existing inverse Gamma matrix for flux-controled edges
        # or force
        if not hasattr(self.analysis, 'iGamma_fc') or force:
            # Perform realizability analysis
            self.analysis.perform()

    # ----------------------------------------------------------------------- #

    def read_realizability_from_analysis(self):
        """
        Read realizability for edges in self.analysis object and change
        self.edges 'ctrl' data accordingly.
        """

        # init analysis if needed
        self.perform_analysis()

        def read_realizability(edges):
            """
            read realizability from list of edges indices and update self.edges
            """

            for i in edges:
                label = self.analysis.get_edge_data(i, 'label')
                if i in self.analysis.fc_edges:
                    ctrl = 'f'
                elif i in self.analysis.ec_edges:
                    ctrl = 'e'
                else:
                    text = "Unnown realizablity for edge {}"
                    edge = self.analysis.edges
                    raise IndeterminateRealizability(text.format(edge))
                for e in self.edgeslist:
                    if e[-1]['label'] == label:
                        e[-1]['ctrl'] = ctrl

        # read realizibility for storages, dissipatives, ports and
        # connectors edges
        for edges in (self.analysis.stor_edges,
                      self.analysis.diss_edges,
                      self.analysis.port_edges,
                      self.analysis.conn_edges):
            read_realizability(edges)

    # ----------------------------------------------------------------------- #

    def to_core(self, label=None, connect=True, merge_all=False, verbose=False,
                plot=False, solve_arc=True, force=True):
        """
        Return the core PHS object associated with the graph.

        Parameters
        ----------

        label : str (optional)
            String label for the Core object (default None recovers the label
            from the graph).

        connect : bool (optional)
            If True, the method core.connect() is called before output of the
            pyphs.Core object, so that the transformers and gyrators are
            resolved in the structure matrix. Default is True.

        merge_all : bool (optional)
            If True, the graph is split again into serial/parallel subgraphs to
            merge all compatible components.

        verbose : bool (optional)
            If True, the system pauses at each iteration of the graph analysis
            algorithm and a short description of the iteration is printed.
            Default is False.

        plot : bool (optional)
            If True, plot the graph at each iteration of the graph analysis
            algorithm. The color scheme for the edges and nodes reflects the
            state of the analysis process. Default is False.

        solve_arc : bool (optional)
            If True, the anti-realizable components are merged to produce a
            realizable graph. Te default is True.

        force : bool (optional)
            If False, the analysis is performed only if it has not been
            performed previously. If True, the analysis is forced in any case.
            Default is True.

        Output
        ------

        core : pyphs.Core
            The PHS core object associated with the graph.

        """

        if merge_all:
            self.sp_split()
            self.sp_merge_all()
            # assemble serial/parallel edges into current graph
            self.sp_assemble()

        self.perform_analysis(verbose=verbose, plot=plot, solve_arc=solve_arc,
                              force=force)

        # verbosity
        if VERBOSE >= 1:
            print('Build core {}...'.format(self.label))

        # build Core
        buildCore(self)

        if merge_all:
            # Read realizability for every edges
            self.read_realizability_from_analysis()
            # split into serial/parallel edges
            self.sp_split()
            self.sp_merge_all()
            # assemble serial/parallel edges into current graph
            self.sp_assemble()
            # Perform realizability analysis again
            self.perform_analysis(force=True)
            # build Core again
            buildCore(self)

        # The returned core is a copy
        core = self.core.__copy__()

        # connect gyrators and transformers
        if connect:
            core.connect()

        # Core.label can be specified, else the Graph.label is recovered
        if label is None:
            label = str(self.label)
        if not isinstance(label, str):
            raise TypeError('Core label not understood:\n{}'.format(label))
        core.label = label

        # Transfer reference to Netlist object
        if hasattr(self, 'netlist'):
            core._netlist = self.netlist

        return core

    # ----------------------------------------------------------------------- #

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

    def to_simulation(self, label=None, config=None, inits=None, erase=True):
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

        erase : bool (optional)
            If True and a h5file exists with same path than simulation data,
            it is erased. Else, it is used to initialize the data object. The
            default is True.

        Output
        ------

        method : pyphs.Simulation
            The PHS simulation object associated with the PHS graph for the
            specified configuration.
        """

        core = self.to_core(label=label)
        return core.to_simulation(config=config, inits=inits, erase=erase)

    # ----------------------------------------------------------------------- #

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

    # ----------------------------------------------------------------------- #

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
            # define subgraph terminals
            terminals = edges[1], edges[2]
            # instanciate a new subgraph
            sg = SubGraphSerial(sglabel, terminals)
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
            # define subgraph terminals
            terminals = n1, n2
            # instanciate a new subgraph
            # instanciate a new subgraph
            pg = SubGraphParallel(pglabel, terminals)
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

    def sp_assemble(self):
        """
        Assemble subgraphs in current graph.
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

        # remove '_out_' and subgraphs edges
        for e in self.edgeslist:
            # get type and label
            elabel = e[-1]['label']
            etype = e[-1]['type']
            if '_out_' in str(elabel) or etype == 'graph':
                self.remove_edges_from_list([e, ])

    def sp_split(self):
        """
        Split the graph into a tree graph of serial/parallel subgraphs.
        """
        change = True
        while change:
            # check for parallel connection
            change_p = self._split_parallel()
            # check for serial connection
            change_s = self._split_serial()
            # Test for any change
            change = any((change_s, change_p))

    def sp_merge_all(self):
        """
        Apply subgraph.merge_all() for all subgraphs.
        """
        subgraphs = self.sp_subgraphs
        for label in subgraphs.keys():
            try:
                subgraphs[label].merge_all()
            except AttributeError:
                pass

    def sp_merge_arc(self):
        """
        Apply subgraph.merge_arc() for all subgraphs.
        """
        subgraphs = self.sp_subgraphs
        for label in subgraphs.keys():
            try:
                subgraphs[label].merge_arc()
            except AttributeError:
                pass

    @property
    def sp_subgraphs(self):
        """
        Return a dictionary with subgraphs labels as keys and associated
        (serialor parallel) Subgraph objects as values for every subgraphs
        rooted in self.
        """

        def get_subgraphs(graph):
            # list of labels
            subgraphs = {graph.label: graph}
            for e in graph.edges(data=True):
                # if leaf is a subgraph
                if e[-1]['type'] == 'graph':
                    # get label and subgraphs
                    elabel = e[-1]['label']
                    egraph = e[-1]['graph']
                    # update graph dictionary
                    subgraphs[elabel] = egraph
                    # get sub-sub-graphs
                    subsubgraphs = get_subgraphs(egraph)
                    subgraphs.update(subsubgraphs)
            return subgraphs

        return get_subgraphs(self)

    @property
    def sp_subgraphs_tree(self):
        """
        Get a tree of serial/parallel subgraphs objects rooted in self.
        """

        def get_subgraphs_tree(graph):
            tree = {graph.label: dict()}
            for e in graph.edges(data=True):
                # if leaf is a subgraph
                if e[-1]['type'] == 'graph':
                    elabel = e[-1]['label']
                    egraph = e[-1]['graph']
                    subtree = get_subgraphs_tree(egraph)
                    tree[graph.label][elabel] = subtree[elabel]
            return tree

        return get_subgraphs_tree(self)

    @property
    def sp_subgraphs_levels(self):
        """
        Get a dictionary with integers as keys and serial/parallel subgraphs
        labels as values. The integers are associated with the levels of the
        subgraphs in the tree returned by self.sp_subgraphs_tree.
        """

        level = 0
        levels = dict()
        levels[level] = (list(self.sp_subgraphs_tree.keys())[0], )
        continu = True
        subgraphs = self.sp_subgraphs
        while continu:
            continu = False
            level += 1
            levels[level] = ()
            for k in levels[level-1]:
                try:
                    gk = subgraphs[k]
                    for e in gk.edges(data=True):
                        levels[level] += (e[-1]['label'], )
                        # if leaf is a subgraph
                        if e[-1]['type'] == 'graph':
                            continu = True
                except KeyError:
                    pass

        return levels

    @staticmethod
    def iter_analysis(graph):
        """
        Recursive graph analysis over a serial_parallel tree graph.

        See Also
        --------
        pyphs.Graph.sp_split

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

    # ----------------------------------------------------------------------- #
    def remove_edges_from_list(self, *args, **kwargs):
        """
        Remove a list of edges.

        Parameters
        ----------

        edges : list of edges
            List of edges to remove from the graph. Each edge is a tuple
            (N1, N2, data) with nodes labels N1, N2 and edge data (dict).

        See also
        --------

        Graph.edgeslist

        """
        for e in args[0]:
            # Get edge key
            n1, n2 = e[:2]
            for key in self[n1][n2].keys():
                if self[n1][n2][key]['label'] == e[-1]['label']:
                    break

            # Remove edge
            self.remove_edge(n1, n2, key)

        self.remove_orphan_nodes()

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

    # ----------------------------------------------------------------------- #

    def __add__(graph1, graph2):
        """
        Graph summation.
        """
        if hasattr(graph1, 'netlist') and hasattr(graph2, 'netlist'):
            graph1.netlist += graph2.netlist
        graph1.core += graph2.core
        graph1.add_edges_from(graph2.edges(data=True))
        return graph1

    @property
    def edgeslist(self):
        """
        Return a list of graph edges with data
        """
        return list(self.edges(data=True))

    @property
    def nodeslist(self):
        """
        Return a set of graph nodes
        """
        return set(self.nodes())

    # ----------------------------------------------------------------------- #

    def set_positions(self, reset=False, layout=None):
        """
        Set the positions of nodes for plots.

        Parameter
        ---------

        reset : bool
            If True, the positions are

        layout : str in {'spring', 'circular'}
            Specifies the layout for the nodes. If None, the layout defined in
            pyphs.config.GRAPHS_LAYOUT is used.

        Output
        ------

        positions : dict
            Dictionary with nodes labels as keys and nodes positions as values.
            Values are given as 1 dimension, 2 elements numpy.ndarray.
        """
        if not hasattr(self, 'positions') or reset:
            if layout is None:
                layout = GRAPHS_LAYOUT
            else:
                assert layout in ('circular', 'spring')
            if layout == 'spring':
                self.positions = nx.spring_layout(self,
                                                  iterations=GRAPHS_ITERATIONS)
            elif layout == 'circular':
                self.positions = nx.circular_layout(self)

        return self.positions
