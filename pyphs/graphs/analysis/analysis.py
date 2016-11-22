# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 08:54:45 2016

@author: Falaize
"""
import networkx
import numpy
from pyphs.misc.tools import myrange
from pyphs.graphs.config import datum
from pyphs.misc.matrices import get_ind_nonzeros_col, get_ind_nonzeros_row, \
    isequal


class Analysis:

    def __init__(self, graph):
        self._verbose = False
        self.nodes = graph.nodes()
        self.edges = graph.edges(data=True)
        # Compute incidence Matrix
        gamma = networkx.linalg.incidence_matrix(graph, oriented=True)
        # we use the other convention for orientation encoding in Gamma
        self.gamma = -numpy.matrix(gamma.todense())
        # init lambda with adjacency matrix
        self.lambd = numpy.abs(self.gamma)
        # get number of nodes and edges
        self.nn = len(self.nodes)
        self.ne = len(self.edges)
        # init list of nodes for analysis
        self.ic_nodes = range(0, self.nn)
        # Put datum node at the top of the node list
        if any(node == datum for node in self.nodes):
            index_datum = self.nodes.index(datum)
            self.move_node(index_datum, 0)
            # force realizability for datum (no edge imposes the potential)
            self.lambd[0, :] = 0
            # exclude datum from analysis
            self.ic_nodes.remove(self.nodes.index(datum))
        # Init lists of edges for analysis
        self.ec_edges = []
        self.fc_edges = []
        self.ic_edges = range(self.ne)
        # test for determinate edge (iter over ic_edges which length change)
        i = 0  # element in ic_edges to check
        while i < len(self.ic_edges):
            e = self.ic_edges[i]
            e_data = self.edges[e][2]
    #        print e, phs.ic_edges
    #        print phs.edges[e][:2], e_data
            # check if effort-controlled
            if e_data['ctrl'] is 'e':
                # move edge at the top of edge list and set Lambda(edge) to 0
                self.set_edge_ec(e)
            # check if flux-controlled
            elif e_data['ctrl'] is 'f':
                # move edge at the end of edge list
                self.set_edge_fc(e)
                if self.lambd[:, e].sum() == 1:
                    # edge 'e' imposes the potential on that node
                    # get node index
                    n = list(numpy.array(self.lambd)[:, e]).index(1)
                    # set node 'n' as determinate
                    self.set_node_dc((n, e))
            else:
                i += 1

    def iterate_fc(self):
        """
        method for realizability analysis
        iteration over all the edges in phs.fc_edges
        """
        for e in self.fc_edges:
            # assert the edge is not effort-controlled
            assert self.lambd[:, e].sum() != 0,\
                'flux-controlled edge {0!s} is effort-controlled'.format(
                self.get_edge_data(e, 'label'))
            # test for single 1 in Lambda
            if self.lambd[:, e].sum() == 1:
                # edge 'e' imposes the potential on that node
                # get node index
                n = list(numpy.array(self.lambd)[:, e]).index(1)
                # set node 'n' as determinate
                self.set_node_dc((n, e))

    def iterate_ic(self):
        """
        method for 'realizability_analysis()'
        iteration over all the edges in phs.ic_edges
        """
        # the length and elements of phs.ic_edges change over iteration...
        # use a counter which is incremented only if the edge is moved to ec/fc
        i = 0
        while i < len(self.ic_edges):
            e = self.ic_edges[i]
            # test for effort-controlled
            if self.lambd[:, e].sum() == 0:
                # moves edge at the begining of edge list, sets Lambda to 0
                self.set_edge_ec(e)
                # test for connector
                if self.get_edge_data(e, 'type') is 'connector':
                    # link realizability of the other edge of the connector
                    self.link_connector(e, 'e')
            else:
                i += 1

    def iterate_nodes(self):
        """
        method for 'realizability_analysis()'
        iteration over all the edges in phs.ic_edges
        """
        # iterate over indeterminate nodes
        for n in self.ic_nodes:
            # assert the potential on node n can be defined
            assert self.lambd[n, :].sum() != 0, \
                "potential on node {0!s} is not defined".format(self.nodes[n])
            # test for definite node
            if self.lambd[n, :].sum() == 1:
                # get index of the edge that imposes the potential on node n
                e = self.lambd[n, :].tolist()[0].index(1)
                # assert the potential is not imposed by efort-controlled edge
                assert e not in self.ec_edges, \
                    "potential on node {0!s} is imposed by effort-controlled \
edge {1!s}".format(self.nodes[n], self.get_edge_data(e, 'label'))
                # move to 'determinate nodes' and set edge as flux-controlled
                self.set_node_dc((n, e))
                # test for connector
                if self.get_edge_data(e, 'type') is 'connector':
                    # link realizability of the other edge of the connector
                    self.link_connector(e, 'f')

    def perform(self):
        # init memory of lambda to: check for change or stop while loop
        lambd_temp = numpy.zeros(self.lambd.shape)
        # realizability analysis on the ic_edges
        while (len(self.ic_edges) + len(self.ic_nodes) > 0):
            # loop while Lambda is changed
            while ((not isequal(lambd_temp, self.lambd)) &
                   (len(self.ic_edges) + len(self.ic_nodes) > 0)):
                # save Lambda for comparison in while condition
                lambd_temp = numpy.matrix(self.lambd, copy=True)
                # iterate on flux-controlled edges
                self.iterate_fc()
                # iterate on indeterminate edges
                self.iterate_ic()
                # iterate on indeterminate nodes
                self.iterate_nodes()
                # if locked, perform unlock
                if isequal(lambd_temp, self.lambd):
                    self.unlock()
        print '\n*** Realizability analysis succeed ***\n'

    def unlock(self):
        """
        unlock realizability analysis in case of indetermination. Here, if \
te columnss in lambda corresponding to two indeterminate control edges are \
the same, we select the first edge and set it to \
effort-controlled (0 in lambda).
        """
        flag = False
        ic_lambd = self.lambd[:, self.ic_edges]
        for n, row in enumerate(ic_lambd.tolist()):
            if sum(row) > 1:
                e = row.index(1)
                self.lambd[n, len(self.ec_edges) + e] = 0
                break
            if n == self.nn-1:
                flag = True
        if flag:
            lambd_icfc = self.lambd[:, self.ic_edges[0]:]
            for n, row in enumerate(lambd_icfc.tolist()):
                if sum(row) > 1:
                    e = row.index(1)
                    self.lambd[n, len(self.ec_edges) + e] = 0
                    break
        if self._verbose:
            print 'unlock'
            print numpy.sum(self.lambd, axis=1)
            raw_input()

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
        old_indices = range(self.nn)
        new_indices = myrange(self.nn, indi, indf)
        self.nodes = [self.nodes[n] for n in new_indices]
        self.gamma = self.gamma[new_indices, :]
        self.lambd = self.lambd[new_indices, :]
        for (old_i, new_i) in zip(old_indices, new_indices):
            self.ic_nodes[self.ic_nodes.index(old_i)] = new_i

    def move_edge(self, indi, indf):
        """
        move edge 'indi' to position 'indf' in
            - self.edges
            - self.Gamma
            - self.lambd
        """
        old_indices = range(self.ne)
        new_indices = myrange(self.ne, indi, indf)
        self.gamma = self.gamma[:, new_indices]
        self.lambd = self.lambd[:, new_indices]
        self.edges = [self.edges[n] for n in new_indices]
        return old_indices, new_indices

    def set_edge_ec(self, e):
        """
        move an edge from indeterminate to e_ctrl, and set self.lambd to 0
        """
        if self._verbose:
            print 'set_edge_ec', self.get_edge_data(e, 'label')
        # move new effort-controlled edges at the top of edges list
        old_indices, new_indices = self.move_edge(e, 0)
        # initial length of edges lists with ne = nec + nfc + len(phs.ic_edges)
        nec = len(self.ec_edges)
        nfc = len(self.fc_edges)
        # new edges lists with new(nec) = nec+1 and new(nic)=nic-1.
        indices = range(self.ne)
        self.ec_edges = indices[:nec+1]
        if nfc > 0:
            self.ic_edges = indices[nec+1:-nfc]
            self.fc_edges = indices[-nfc:]
        else:
            self.ic_edges = indices[nec+1:]
            self.fc_edges = []
        # set corresponding Lambda elements to 0
        self.lambd[:, 0] = 0
        if self._verbose:
            print 'edges', self.get_edges_data('label')
            print 'nodes', self.nodes
            print self.lambd
            raw_input()

    def set_edge_fc(self, e):
        """
        move an edge from indeterminate to flux-controlled, and remove \
controlled node from node list
        """
        if self._verbose:
            print 'set_edge_fc', self.get_edge_data(e, 'label')
        # move new flux-controlled edges at the end of edges list
        self.move_edge(e, self.ne-1)
        # initial length of edges lists with ne = nec + nfc + len(phs.ic_edges)
        nec = len(self.ec_edges)
        nfc = len(self.fc_edges)
        # new edges lists with new(nfc) = nfc+1 and new(nic)=nic-1.
        indices = range(self.ne)
        self.ec_edges = indices[:nec]
        self.ic_edges = indices[nec:-(nfc+1)]
        self.fc_edges = indices[-(nfc+1):]
        if self._verbose:
            print 'edges', self.get_edges_data('label')
            print 'nodes', self.nodes
            print self.lambd
            raw_input()

    def set_node_dc(self, (n, e)):
        """
        remove node 'n' from indeterminate nodes list, and check for a single \
1 on row 'n' and column 'e' of 'self.lambd'
        """
        if self._verbose:
            print 'set_node_dc', self.nodes[n]
        # set other Lambda elements to 0
        self.lambd[:, e] = 0
        self.lambd[n, :] = 0
        # set node 'n' controlled by edge 'e'
        self.lambd[n, e] = 1
        if n in self.ic_nodes:
            # remove node from list of indeterminate nodes
            self.ic_nodes.remove(n)
        if e in self.ic_edges:
            # remove edge from list of indeterminate edges
            self.set_edge_fc(e)
        if self._verbose:
            print 'edges', self.get_edges_data('label')
            print 'nodes', self.nodes
            print self.lambd
            raw_input()

    def rowindexGamma(self, c):
        """
        Return row indices of nonzero elements in column 'c' of 'self.gamma'
        """
        return get_ind_nonzeros_col(self.gamma, c)

    def colindexGamma(self, r):
        """
        Return column indices of nonzero elements in row 'r' of 'self.gamma'
        """
        return get_ind_nonzeros_row(self.gamma, r)

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
        # get connector
        if ctrl is 'e':
            # inverse connector coefficient
            self.edges[e][2]['alpha'] = self.edges[e][2]['alpha']**-1
            self.edges[link_e][2]['alpha'] = self.edges[link_e][2]['alpha']**-1
            # gyrator case
            if self.get_edge_data(e, 'connector_type') == 'gyrator':
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

    def build_phs(self, phs):
        from build import build_phs
        build_phs(self, phs)
