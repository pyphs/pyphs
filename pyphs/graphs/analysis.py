# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 08:54:45 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

import networkx
import numpy
from ..misc.tools import myrange, pause
from ..config import datum, EPS
from ..misc.plots.graphs import plot_analysis
from .exceptions import UndefinedPotential, CanNotUnlock


class GraphAnalysis:

    def __init__(self, graph, verbose=False, plot=False):
        self._plot = plot
        self._verbose = verbose
        self.ndatum = 0
        self.nodes = list(graph.nodes())
        self.edges = list(graph.edges(data=True))
        # Compute incidence Matrix
        Gamma = networkx.linalg.incidence_matrix(graph, oriented=True)
        # we use the other convention for orientation encoding in Gamma
        self.Gamma = -numpy.array(Gamma.todense())
        # init lambda with adjacency matrix
        self.Lambda = numpy.abs(self.Gamma)
        # get number of nodes and edges
        self.nn = len(self.nodes)
        self.ne = len(self.edges)

        def plot_analysis_self(show=True):
            plot_analysis(graph, self, show=show)

        self.plot = plot_analysis_self
        # init list of nodes for analysis
        self.ic_nodes = list(range(0, self.nn))
        # Put datum node at the top of the node list
        if any(node == datum for node in self.nodes):
            index_datum = self.nodes.index(datum)
            self.move_node(index_datum, 0)
            # force realizability for datum (no edge imposes the potential)
            self.Lambda[0, :] = 0
            # exclude datum from analysis
            index_datum = self.nodes.index(datum)
            self.ic_nodes.pop(self.ic_nodes.index(index_datum))
        # Init lists of edges for analysis
        self.ec_edges = []
        self.fc_edges = []
        self.ic_edges = list(range(self.ne))
        if self._plot:
            self.plot()
        # test for determinate edge (iter over ic_edges which length change)
        i = 0  # element in ic_edges to check
        while i < len(self.ic_edges):
            e = self.ic_edges[i]
            e_data = self.edges[e][2]
            # check if effort-controlled
            if e_data['ctrl'] is 'e':
                # move edge at the top of edge list and set Lambda(edge) to 0
                self.set_edge_ec(e)
            # check if flux-controlled
            elif e_data['ctrl'] is 'f':
                if self.Lambda[:, e].sum() == 1:
                    # edge 'e' imposes the potential on that node
                    # get node index
                    n = list(numpy.array(self.Lambda)[:, e]).index(1)
                    # set node 'n' as determinate
                    if n in self.ic_nodes:
                        self.set_node_dc((n, e))
                else:
                    # move edge at the end of edge list
                    self.set_edge_fc(e)

            else:
                i += 1

    def iterate_fc(self):
        """
Iteration over the list `graph.analysis.fc_edges` of a given graph.

        """
        for e in self.fc_edges:
            # assert the edge is not effort-controlled
            assert self.Lambda[:, e].sum() != 0,\
                'flux-controlled edge {0!s} is effort-controlled'.format(
                self.get_edge_data(e, 'label'))
            # test for single 1 in Lambda
            if self.Lambda[:, e].sum() == 1:
                # edge 'e' imposes the potential on that node
                # get node index
                n = list(numpy.array(self.Lambda)[:, e]).index(1)
                # set node 'n' as determinate
                if n in self.ic_nodes:
                    self.set_node_dc((n, e))

    def iterate_ic(self):
        """
Iteration over the list `graph.analysis.ic_edges` of a given graph.

        """
        # the length and elements of phs.ic_edges change over iteration...
        # use a counter which is incremented only if the edge is moved to ec/fc
        i = 0
        while i < len(self.ic_edges):
            e = self.ic_edges[i]
            # test for effort-controlled
            if self.Lambda[:, e].sum() == 0:
                # moves edge at the begining of edge list, sets Lambda to 0
                self.set_edge_ec(e)
                # do not increment i since e moved a top of self.ic_edges
            else:
                i += 1

    def iterate_nodes(self):
        """
Iteration over the list `graph.analysis.ic_nodes` of indeterminate nodes.
First, it is checked that the correponding row of matrix graph.analysis.la
        """
        # iterate over indeterminate nodes
        for n in self.ic_nodes:
            # assert the potential on node n can be defined
            if self.Lambda[n, :].sum() == 0:
                raise UndefinedPotential(self.nodes[n])

            # test for definite node
            if self.Lambda[n, :].sum() == 1:
                # get index of the edge that imposes the potential on node n
                e = numpy.nonzero(self.Lambda[n, :] == 1)[0][0]
                # assert the potential is not imposed by efort-controlled edge
                assert e not in self.ec_edges, \
                    "potential on node {0!s} is imposed by effort-controlled \
edge {1!s}".format(self.nodes[n], self.get_edge_data(e, 'label'))
                # move to 'determinate nodes' and set edge as flux-controlled
                if n in self.ic_nodes:
                    self.set_node_dc((n, e))

    def iteration(self):
        """
Execute an iteration over the lists:
    * indeterminate nodes with `graph.analysis.iterate_nodes()`
    * iterate on flux-controlled edges with  `graph.analysis.iterate_fc()`
    * iterate on indeterminate edges with `graph.analysis.iterate_ic()`

        """
        # init memory of lambda to: check for change or stop while loop
        self.Lambda_temp = numpy.ones(self.Lambda.shape)
        # loop while Lambda is changed
        while not isequal(self.Lambda_temp, self.Lambda):
            if self._verbose:
                print('###################################\nLoop Start\n')
                # save Lambda for comparison in while condition
            self.Lambda_temp = numpy.array(self.Lambda, copy=True)
            if self._verbose:
                print('###################################\nLambda_tempn')
                print(self.Lambda_temp)
                print('###################################\nLambda')
                print(self.Lambda)
                print('###################################\nLambda')
                print(list(numpy.array(self.Lambda_temp == self.Lambda).flatten()))
            # iterate on indeterminate nodes
            self.iterate_nodes()
            # iterate on flux-controlled edges
            self.iterate_fc()
            # iterate on indeterminate edges
            self.iterate_ic()

    def perform(self):
        # realizability analysis on the ic_edges
        while (len(self.ic_edges) + len(self.ic_nodes) > 0):
            self.iteration()
            # if locked, perform unlock
            if isequal(self.Lambda_temp, self.Lambda) & \
                    (len(self.ic_edges) + len(self.ic_nodes) > 0):
                self.unlock()
        if self._plot:
            self.plot()
        try:
            self.Gamma_ec = self.Gamma[1:, :len(self.ec_edges)]
            self.Gamma_fc = self.Gamma[1:, len(self.ec_edges):]
            self.iGamma_fc = numpy.linalg.inv(self.Gamma_fc)
        except numpy.linalg.LinAlgError:
            raise ValueError("""
!!! Realizability analysis did not succeed !!!\n

The elements have been divided in effort-controlled and flux-controlled, but \
the incidence matrix associated with the flux-controlled part is not \
invertible:
Gamma_fc=\n{0}
""".format(self.Gamma_fc))

    def unlock(self):
        """
unlock realizability analysis in case of indetermination. Here, if the columns
in lambda corresponding to two indeterminate control edges are the same, we
select the first edge which is not a conector (transformer or gyrator) and
define it as effort-controlled (0 column in lambda).
        """
        still_locked = True
        # for each row in block matrix extracted from the ic colums of Lambda
        for n, row in enumerate(self.Lambda[:, self.ic_edges].tolist()):
            # only if the node is overdeterminated
            if sum(row) > 1:
                col = self.Lambda[:, len(self.ec_edges)]  # first ic column
                e = 0
                while (row[e] != 1 and
                       sum(col) != 1 and
                       e < len(self.ic_edges)):
                    e += 1
                    col = self.Lambda[:, len(self.ec_edges) + e]
                if not e == (len(self.ic_edges) and not
                             self.get_edge_data(e, 'type')):
                    self.Lambda[n, len(self.ec_edges) + e] = 0
                    still_locked = False
                    break
        if still_locked:
            lambd_icfc = self.Lambda[:, self.ic_edges[0]:]
            for n, row in enumerate(lambd_icfc.tolist()):
                if sum(row) > 1:
                    e = 0
                    col = self.Lambda[:, len(self.ec_edges) + e]
                    while row[e] != 1 and \
                            not sum(col) >= 2 and \
                            e < len(self.ic_edges+self.fc_edges):
                        e += 1
                        col = self.Lambda[:, len(self.ec_edges) + e]
                    if not e == len(self.ic_edges+self.fc_edges):
                        self.Lambda[n, len(self.ec_edges) + e] = 0
                        still_locked = False
                        break
        if still_locked:
            raise CanNotUnlock
        self.verbose('unlock')

    def get_edges_data(self, key):
        """
        return a list of edges data 'key'
        """
        data_list = [edge[2][key] for edge in self.edges]
        return data_list

    def get_edge_data(self, index, key):
        """
        return the data 'key' associated to edge 'index'
        """
        data = self.edges[index][2][key]
        return data

    def move_node(self, indi, indf):
        """
        move node 'indi' to position 'indf' in
            - phs.nodes
            - phs.Gamma
            - phs.Lambda
        """
        old_indices = list(range(self.nn))
        new_indices = myrange(self.nn, indi, indf)
        self.nodes = [self.nodes[n] for n in new_indices]
        self.Gamma = self.Gamma[new_indices, :]
        self.Lambda = self.Lambda[new_indices, :]
        for (old_i, new_i) in zip(old_indices, new_indices):
            self.ic_nodes[self.ic_nodes.index(old_i)] = new_i

    def move_edge(self, indi, indf):
        """
        move edge 'indi' to position 'indf' in
            - self.edges
            - self.Gamma
            - self.Lambda
        """
        old_indices = list(range(self.ne))
        new_indices = myrange(self.ne, indi, indf)
        self.Gamma = self.Gamma[:, new_indices]
        self.Lambda = self.Lambda[:, new_indices]
        self.edges = [self.edges[n] for n in new_indices]
        return old_indices, new_indices

    def set_edge_ec(self, e):
        """
        move an edge from indeterminate to e_ctrl, and set self.Lambda to 0
        """
        # get edge label
        e_label = self.get_edge_data(e, 'label')
        if self._verbose:
            print('set_edge_ec', self.get_edge_data(e, 'label'))
        # move new effort-controlled edges at the top of edges list
        old_indices, new_indices = self.move_edge(e, 0)
        # initial length of edges lists with ne = nec + nfc + len(phs.ic_edges)
        nec = len(self.ec_edges)
        nfc = len(self.fc_edges)
        # new edges lists with new(nec) = nec+1 and new(nic)=nic-1.
        indices = list(range(self.ne))
        self.ec_edges = indices[:nec+1]
        if nfc > 0:
            self.ic_edges = indices[nec+1:-nfc]
            self.fc_edges = indices[-nfc:]
        else:
            self.ic_edges = indices[nec+1:]
            self.fc_edges = []
        # set corresponding Lambda elements to 0
        self.Lambda[:, 0] = 0
        # test for connector
        new_e = self.get_edges_data('label').index(e_label)
        if self.get_edge_data(new_e, 'type') is 'connector':
            # link realizability of the other edge of the connector
            self.link_connector(new_e, 'e')
        self.verbose('set_edge_ec')

    def set_edge_fc(self, e):
        """
        move an edge from indeterminate to flux-controlled, and remove \
controlled node from node list
        """
        if self._verbose:
            print('set_edge_fc', self.get_edge_data(e, 'label'))
        # get edge label
        e_label = self.get_edge_data(e, 'label')
        # move new flux-controlled edges at the end of edges list
        self.move_edge(e, self.ne-1)
        # initial length of edges lists with ne = nec + nfc + len(phs.ic_edges)
        nec = len(self.ec_edges)
        nfc = len(self.fc_edges)
        # new edges lists with new(nfc) = nfc+1 and new(nic)=nic-1.
        indices = list(range(self.ne))
        self.ec_edges = indices[:nec]
        self.ic_edges = indices[nec:-(nfc+1)]
        self.fc_edges = indices[-(nfc+1):]
        # test for connector
        new_e = self.get_edges_data('label').index(e_label)
        if self.get_edge_data(new_e, 'type') is 'connector':
            # link realizability of the other edge of the connector
            self.link_connector(new_e, 'f')
        self.verbose('set_edge_fc')

    def set_node_dc(self, args):
        """
        remove node 'n' from indeterminate nodes list, and check for a single \
1 on row 'n' and column 'e' of 'self.Lambda'
        """
        n, e = args
        if self._verbose:
            print('set_node_dc', self.nodes[n])
        # set other Lambda elements to 0
        self.Lambda[:, e] = 0
        self.Lambda[n, :] = 0
        # set node 'n' controlled by edge 'e'
        self.Lambda[n, e] = 1
        if n in self.ic_nodes:
            # remove node from list of indeterminate nodes
            self.ic_nodes.remove(n)
        if e in self.ic_edges:
            # remove edge from list of indeterminate edges
            self.set_edge_fc(e)
        self.verbose('set_node_dc')
        if self._plot:
            self.plot()

    def verbose(self, label):
        if self._verbose:
            print('------------------------\n')
            print(label + '\n')
            print('sum(lambda)')
            print(numpy.sum(self.Lambda, axis=1).T)
            edges = self.get_edges_data('label')
            print('ic_nodes\n', [self.nodes[i] for i in self.ic_nodes])
            print('ic_edges\n', [edges[i] for i in self.ic_edges])
            print('ec_edges\n', [edges[i] for i in self.ec_edges])
            print('fc_edges\n', [edges[i] for i in self.fc_edges])
            print(self.Lambda)
            pause()

    def link_connector(self, e, ctrl):
        """
        link realizability for connectors. the edge e has 'realizability', \
and the realizability of linked edge is chosen based on the connector type \
(transormer or gyrator).
        """
        # get edge label
        e_label = self.get_edge_data(e, 'label')
        # get linked edge index
        link_e = self.get_edges_data('link').index(e_label)
        # get linked edge index
        link_e_label = self.get_edge_data(link_e, 'label')
        if self._verbose:
            print('link', e_label, self.get_edge_data(e, 'connector_type'),
                  ctrl, link_e_label)
        # get connector
        if ctrl is 'e':
            # gyrator case
            if self.get_edge_data(e, 'connector_type') == 'gyrator':
                self.inverse_alpha(e)
                # assert linked edge is not flux controlled
                assert link_e not in self.fc_edges,\
                    'connector edges {0!s} and {1!s} are not \
compatible'.format(e_label, link_e_label)
                # if linked edge is indeterminate
                if link_e in self.ic_edges:
                    # move edge at top of edge list and set lambd to 0
                    self.set_edge_ec(link_e)
            # transformer case
            elif self.get_edge_data(e, 'connector_type') == 'transformer':
                self.inverse_alpha(e)
                # assert linked edge is not effort controlled
                assert link_e not in self.ec_edges,\
                    'connector edges {0!s} and {1!s} are not \
compatible'.format(e_label, link_e_label)
                # if linked edge is indeterminate
                if link_e in self.ic_edges:
                    # move edge at the end of edge list
                    self.set_edge_fc(link_e)

        if ctrl is 'f':
            # gyrator case
            if self.get_edge_data(e, 'connector_type') == 'gyrator':
                # assert linked edge is not effort controlled
                assert link_e not in self.ec_edges,\
                    'connector edges {0!s} and {1!s} are not \
compatible'.format(e_label, link_e_label)
                # if linked edge is indeterminate
                if link_e in self.ic_edges:
                    # move edge at the end of edge list
                    self.set_edge_fc(link_e)
            # transformer case
            elif self.get_edge_data(e, 'connector_type') == 'transformer':
                # assert linked edge is not flux controlled
                assert link_e not in self.fc_edges,\
                    'connector edges {0!s} and {1!s} are not \
compatible'.format(e_label, link_e_label)
                # if linked edge is indeterminate
                if link_e in self.ic_edges:
                    # move edge at top of edge list and set Lambda to 0
                    self.set_edge_ec(link_e)
        if self._verbose:
            print('link', e_label, ctrl, link_e_label)
            self.verbose('link')

    def inverse_alpha(self, e):
        alpha = self.edges[e][2]['alpha']
        if alpha is not None:
            self.edges[e][2]['alpha'] = alpha**-1


def isequal(M1, M2):
    """
    Test M1==M2 with M1 and M2 of type sympy.SparseMatrix or numpy.matrix
    """
    return all(numpy.array(M1-M2<EPS).flatten())
