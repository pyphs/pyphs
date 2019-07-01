#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 12:37:43 2018

@author: afalaize
"""

from pyphs.core.maths import gradient
from .graph import Graph
import sympy
import warnings
from .tools import serial_next
from networkx import Graph as nwxGraph
from networkx import chain_decomposition
from networkx import contracted_nodes
import copy


def merge_warning(type, before, after):
    text = "\n\nThe {0} components {1} have been merged into {2}\n"
    return text.format(type, before, after)


def nonrealizable_merge_storages(x, dxH):

    from pyphs import Core

    y = Core.symbols('y:{0}'.format(len(x)))
    X = Core.symbols(('x'+'{}'*len(x)).format(*[str(xn)[1:] for xn in x]))
    Y = Core.symbols('Y')

    idxH = list(map(lambda arg: sympy.solve(arg[0]-arg[2], arg[1])[0],
                zip(dxH, x, y)))
    Q = sum([e.subs(yi, Y) for e, yi in zip(idxH, y)]).simplify()
    iQ = sympy.solve(Q-X, Y)[0]

    [e.subs(yi, iQ) for (e, yi) in zip(idxH, y)]

    HH = [sympy.integrate(dxhn, xn) for dxhn, xn in zip(dxH, x)]
    newH = sum([Hn.subs(xn, fn)
                for (Hn, xn, fn)
                in zip(HH,
                       x,
                       [idxhn.subs(yi, iQ) for idxhn, yi in zip(idxH, y)])])

    return X, sympy.simplify(newH)


def realizable_merge_storages(x, dxH):

    from pyphs import Core
    X = Core.symbols(('x'+'{}'*len(x)).format(*[str(xn)[1:] for xn in x]))
    HH = [sympy.integrate(dxhn, xn) for dxhn, xn in zip(dxH, x)]
    newH = sum([Hn.subs(xn, X)
                for (Hn, xn)
                in zip(HH, x)])
    return X, sympy.simplify(newH)


def nonrealizable_merge_dissipatives(w, z):
    from pyphs import Core

    y = Core.symbols('y:{0}'.format(len(w)))
    newW = Core.symbols(('w'+'{}'*len(w)).format(*[str(wn)[1:] for wn in w]))
    Y = Core.symbols('Y')

    iz = list(map(lambda arg: sympy.solve(arg[0]-arg[2], arg[1])[0],
                  zip(z, w, y)))
    iZ = sum([e.subs(yi, Y) for e, yi in zip(iz, y)]).simplify()
    newZ = sympy.solve(iZ-newW, Y)[0]

    return newW, newZ


def realizable_merge_dissipatives(w, z):
    from pyphs import Core
    W = Core.symbols(('w'+'{}'*len(w)).format(*[str(wn)[1:] for wn in w]))
    return W, sum([zn.subs(dict([(wn, W) for wn in w])) for zn in z])


class SubGraph(Graph):

    _registered = {}

    def __init__(self, label=None, terminals=None):
        """
        Initialize an empty SubGraph.

        Parameters
        ----------

        label : str (optional)
            SubGraph label. If None, a label is generated (default).

        terminals : list of nodes labels
            Ordered list of terminals. The subgraph is replaced in the root
            graph by an edge terminals[0] -> terminals[1]

        """

        if label is None:
            label = 'subgraph'+str(len(SubGraph._registered))

        if terminals is None:
            terminals = []

        self.register(self, label)

        Graph.__init__(self, label=label)
        self._terminals = tuple(terminals)
        self._realizability = None

    @classmethod
    def register(cls, obj, label=None):
        cls._registered[label] = obj

    @property
    def orientations_dic(self):
        return dict([(e[-1]['label'], o)
                     for (e, o) in zip(self.edgeslist, self.orientations)])

    @property
    def fc_storages(self):
        edges = list()
        for edge in self.edges(data=True):
            if edge[-1]['type'] == 'storage' and edge[-1]['ctrl'] == 'f':
                edges.append(edge)
        return edges

    @property
    def ec_storages(self):
        edges = list()
        for edge in self.edges(data=True):
            if edge[-1]['type'] == 'storage' and edge[-1]['ctrl'] == 'e':
                edges.append(edge)
        return edges

    @property
    def fc_dissipatives(self):
        edges = list()
        for edge in self.edges(data=True):
            if edge[-1]['type'] == 'dissipative' and edge[-1]['ctrl'] == 'f':
                edges.append(edge)
        return edges

    @property
    def ec_dissipatives(self):
        edges = list()
        for edge in self.edges(data=True):
            if edge[-1]['type'] == 'dissipative' and edge[-1]['ctrl'] == 'e':
                edges.append(edge)
        return edges

    @property
    def ic_dissipatives(self):
        edges = list()
        for edge in self.edges(data=True):
            if edge[-1]['type'] == 'dissipative' and edge[-1]['ctrl'] == '?':
                edges.append(edge)
        return edges

    @property
    def x_fc(self):
        x = []
        for e in self.fc_storages:
            x.append(e[-1]['label'])
        return x

    @property
    def dxH_fc(self):
        return gradient(self.core.H, self.x_fc)

    @property
    def x_ec(self):
        x = []
        for e in self.ec_storages:
            x.append(e[-1]['label'])
        return x

    @property
    def dxH_ec(self):
        return gradient(self.core.H, self.x_ec)

    @property
    def w_fc(self):
        w = []
        for e in self.fc_dissipatives:
            w.append(e[-1]['label'])
        return w

    @property
    def w_ic(self):
        w = []
        for e in self.ic_dissipatives:
            w.append(e[-1]['label'])
        return w

    @property
    def w_ec(self):
        w = []
        for e in self.ec_dissipatives:
            w.append(e[-1]['label'])
        return w

    @property
    def z_fc(self):
        z = []
        for e in self.fc_dissipatives:
            z.append(copy.copy(e[-1]['z']))
        return z

    @property
    def z_ic(self):
        z = []
        for e in self.ic_dissipatives:
            z.append(copy.copy(e[-1]['z']))
        return z

    @property
    def z_ec(self):
        z = []
        for e in self.ec_dissipatives:
            z.append(copy.copy(e[-1]['z']))
        return z

    def merge_arc_storages(self):
        edges_stor = getattr(self, self.anti_realizability+'c_storages')
        change = len(edges_stor) > 1
        if change:
            # get nodes for new component
            if self.orientations_dic[edges_stor[0][-1]['label']] == 1:
                nodes = edges_stor[0][:2]
            else:
                nodes = edges_stor[0][1], edges_stor[0][0]
            # give every edges the positive direction
            oriented_dxH_arc = self.dxH_arc
            for i, xn in enumerate(self.x_arc):
                if self.orientations_dic[xn] == -1:
                    oriented_dxH_arc[i] = -oriented_dxH_arc[i].subs(xn, -xn)
            # Get new values for X and H
            X, H = nonrealizable_merge_storages(self.x_arc, oriented_dxH_arc)

            warnings.warn(merge_warning("storage", self.x_arc, X), Warning)

            # Remove Energy associated with anti-realizable control storage
            self.core.H -= self.H_arc
            # Remove states associated with anti-realizable control storage
            for xn in self.x_arc:
                self.core.x.remove(xn)
            # new component
            self.new_edge({'ctrl': self.anti_realizability,
                           'label': X,
                           'link': None,
                           'type': 'storage'
                           },
                          nodes)
            # Append new state
            self.core.x.append(X)
            # ADD new energy
            self.core.H += H
            # remove edges
            self.remove_edges_from_list(edges_stor, preserve_nodes=[nodes, ])
        return change

    def merge_arc_dissipatives(self):
        edges_diss = getattr(self, self.anti_realizability+'c_dissipatives')
        change = len(edges_diss) > 1
        if change:
            # get nodes for new component
            if self.orientations_dic[edges_diss[0][-1]['label']] == 1:
                nodes = edges_diss[0][:2]
            else:
                nodes = edges_diss[0][1], edges_diss[0][0]
            oriented_z_arc = self.z_arc
            for i, dic in enumerate(oriented_z_arc):
                oriented_z_arc[i] = dic[self.anti_realizability + '_ctrl']
            for i, wn in enumerate(self.w_arc):
                if self.orientations_dic[wn] == -1:
                    oriented_z_arc[i] = -oriented_z_arc[i].subs(wn, -wn)
            W, Z = nonrealizable_merge_dissipatives(self.w_arc, oriented_z_arc)

            warnings.warn(merge_warning("dissipative", self.w_arc, W), Warning)

            # remove edges
            for wn in self.w_arc:
                i = self.core.w.index(wn)
                self.core.w.pop(i)
                self.core.z.pop(i)
            # new component
            self.new_edge({'ctrl': self.anti_realizability,
                           'label': W,
                           'link': None,
                           'type': 'dissipative',
                           'z': {'{}_ctrl'.format(self.anti_realizability): Z},
                           },
                          nodes)
            self.core.add_dissipations(W, Z)
            # remove edges
            self.remove_edges_from_list(edges_diss, preserve_nodes=[nodes, ])
        return change

    def merge_rc_storages(self):
        edges_stor = getattr(self, self.realizability+'c_storages')
        change = len(edges_stor) > 1
        if change:
            # get nodes for new component
            if self.orientations_dic[edges_stor[0][-1]['label']] == 1:
                nodes = edges_stor[0][:2]
            else:
                nodes = edges_stor[0][1], edges_stor[0][0]
            # give every edges the positive direction
            oriented_dxH_rc = self.dxH_rc
            for i, xn in enumerate(self.x_rc):
                if self.orientations_dic[xn] == -1:
                    oriented_dxH_rc[i] = -oriented_dxH_rc[i].subs(xn, -xn)
            # Get new values for X and H
            X, H = realizable_merge_storages(self.x_rc, oriented_dxH_rc)

            warnings.warn(merge_warning("storage", self.x_rc, X), Warning)

            # Remove Energy associated with anti-realizable control storage
            self.core.H -= self.H_rc
            # Remove states associated with anti-realizable control storage
            for xn in self.x_rc:
                self.core.x.remove(xn)
            # new component
            self.new_edge({'ctrl': self.realizability,
                           'label': X,
                           'link': None,
                           'type': 'storage'
                           },
                          nodes)
            # Append new state
            self.core.x.append(X)
            # ADD new energy
            self.core.H += H
            # remove edges
            self.remove_edges_from_list(edges_stor, preserve_nodes=[nodes, ])
        return change

    def merge_rc_dissipatives(self):
        edges_diss = getattr(self, self.realizability+'c_dissipatives')
        change = len(edges_diss) > 1
        if change:
            # get nodes for new component
            if self.orientations_dic[edges_diss[0][-1]['label']] == 1:
                nodes = edges_diss[0][:2]
            else:
                nodes = edges_diss[0][1], edges_diss[0][0]
            oriented_z_rc = self.z_rc
            for i, dic in enumerate(oriented_z_rc):
                oriented_z_rc[i] = dic[self.realizability + '_ctrl']
            for i, wn in enumerate(self.w_rc):
                if self.orientations_dic[wn] == -1:
                    oriented_z_rc[i] = -oriented_z_rc[i].subs(wn, -wn)
            W, Z = realizable_merge_dissipatives(self.w_rc, oriented_z_rc)

            warnings.warn(merge_warning("dissipative", self.w_rc, W), Warning)

            # remove edges
            for wn in self.w_rc:
                i = self.core.w.index(wn)
                self.core.w.pop(i)
                self.core.z.pop(i)
            # new component
            self.new_edge({'ctrl': self.realizability,
                           'label': W,
                           'link': None,
                           'type': 'dissipative',
                           'z': {'{}_ctrl'.format(self.realizability): Z},
                           },
                          nodes)
            self.core.add_dissipations(W, Z)
            # remove edges
            self.remove_edges_from_list(edges_diss, preserve_nodes=[nodes, ])
        return change

    def merge_ic_dissipatives(self):
        edges_diss = self.ic_dissipatives
        change = len(edges_diss) > 1
        if change:
            # get nodes for new component
            if self.orientations_dic[edges_diss[0][-1]['label']] == 1:
                nodes = edges_diss[0][:2]
            else:
                nodes = edges_diss[0][1], edges_diss[0][0]

            # get edges ic
            oriented_z_ic = self.z_ic
            for i, dic in enumerate(oriented_z_ic):
                oriented_z_ic[i] = dic[self.realizability + '_ctrl']
            for i, wn in enumerate(self.w_ic):
                if self.orientations_dic[wn] == -1:
                    oriented_z_ic[i] = -oriented_z_ic[i].subs(wn, -wn)
            W, Zrc = realizable_merge_dissipatives(self.w_ic, oriented_z_ic)

            # get edges arc
            oriented_z_ic = self.z_ic
            for i, dic in enumerate(oriented_z_ic):
                oriented_z_ic[i] = dic[self.anti_realizability + '_ctrl']
            for i, wn in enumerate(self.w_ic):
                if self.orientations_dic[wn] == -1:
                    oriented_z_ic[i] = -oriented_z_ic[i].subs(wn, -wn)

            W, Zarc = nonrealizable_merge_dissipatives(self.w_ic,
                                                       oriented_z_ic)

            warnings.warn(merge_warning("dissipative", self.w_ic, W), Warning)

            # remove edges
            for wn in self.w_ic:
                i = self.core.w.index(wn)
                self.core.w.pop(i)
                self.core.z.pop(i)

            # new component
            self.new_edge({'ctrl': '?',
                           'label': W,
                           'link': None,
                           'type': 'dissipative',
                           'z': {'{}_ctrl'.format(self.realizability): Zrc,
                                 '{}_ctrl'.format(self.anti_realizability): Zarc},
                           },
                          nodes)
            self.core.add_dissipations(W, Zrc)
            # remove edges
            self.remove_edges_from_list(edges_diss, preserve_nodes=[nodes, ])
        return change

    def merge_all(self):
        change = True
        i = 0
        while change:
            change = False
            change = change or self.merge_ic_dissipatives()
            change = change or self.merge_rc_storages()
            change = change or self.merge_arc_storages()
            change = change or self.merge_rc_dissipatives()
            change = change or self.merge_arc_dissipatives()
            i += int(change)
        return bool(i)

    def merge_arc(self):
        self.merge_arc_storages()
        self.merge_arc_dissipatives()

    @property
    def realizability(self):
        return self._realizability

    @property
    def anti_realizability(self):
        if self.realizability == 'e':
            return 'f'
        elif self.realizability == 'f':
            return 'e'

    @property
    def x_rc(self):
        return getattr(self, 'x_{0}c'.format(self.realizability))

    @property
    def x_arc(self):
        return getattr(self, 'x_{0}c'.format(self.anti_realizability))

    @property
    def dxH_rc(self):
        return getattr(self, 'dxH_{0}c'.format(self.realizability))

    @property
    def dxH_arc(self):
        return getattr(self, 'dxH_{0}c'.format(self.anti_realizability))

    @property
    def H_rc(self):
        return sum([sympy.integrate(dxhn, xn) for dxhn, xn in zip(self.dxH_rc,
                                                                  self.x_rc)])

    @property
    def H_arc(self):
        return sum([sympy.integrate(dxhn, xn) for dxhn, xn in zip(self.dxH_arc,
                                                                  self.x_arc)])

    @property
    def w_rc(self):
        return getattr(self, 'w_{0}c'.format(self.realizability))

    @property
    def w_arc(self):
        return getattr(self, 'w_{0}c'.format(self.anti_realizability))

    @property
    def z_rc(self):
        return getattr(self, 'z_{0}c'.format(self.realizability))

    @property
    def z_arc(self):
        return getattr(self, 'z_{0}c'.format(self.anti_realizability))

#    def set_orientation_reference(self, orientation):
#        if not hasattr(self, '_orientation'):
#            self._orientation = orientation

    @property
    def terminals(self):
        """
        Get the terminal nodes associated with the subgraph.
        """
#        # read nodes from subgraph output edges
#        nodes = set()
#        for e in self.edges(data=True):
#            if '_out_' in str(e[-1]['label']):
#                nodes.update(e[:2])
#        # remove datum
#        if len(nodes) > 2:
#            nodes.remove(self.datum)
#        # return
#        return nodes
        return self._terminals


class SubGraphParallel(SubGraph):

    def __init__(self, label=None, terminals=None):
        SubGraph.__init__(self, label, terminals)
        self._realizability = 'e'

    def new_edge(self, edata, nodes=None):
        if nodes is None:
            e1 = self.edgeslist[0]
            nodes = e1[:2]
        self.add_edge(*nodes, **edata)

    @property
    def orientations(self):
        """
        Return a list of orientations values in {+1, -1} associated with the
        list self.edgeslist with +1 for the first edge in the list.
        """

        nodes = self.terminals

        orientations = list()

        for e in self.edgeslist:
            if tuple(e[:2]) == nodes:
                orientation = +1
            elif (e[1], e[0]) == nodes:
                orientation = -1
            elif '_out_' in str(e[-1]['label']):
                orientation = None
            else:
                raise ValueError('Orientation of the following edge can not \
be determined\n{}'.format(e))
            orientations.append(orientation)
#
#        n_pos = sum(map(lambda val: max(val, 0), orientations))
#        n_neg = -sum(map(lambda val: min(val, 0), orientations))
#        self.set_orientation_reference(int(n_pos >= n_neg)-int(n_neg > n_pos))
#
#        if self._orientation == -1:
#            orientations = [-o for o in orientations]

        return orientations


class SubGraphSerial(SubGraph):

    def serial_next(self, *args):
        return serial_next(self, *args)

    def __init__(self, label=None, terminals=None):
        SubGraph.__init__(self, label, terminals)
        self._realizability = 'f'

    @property
    def chain(self):
        """
        Return a list of tuples of nodes in the serial chain, rooted at datum
        if datum is in the chain.

        Warning
        -------

        Do not prerve the edges orientations

        """

        # set root
        if self.datum in self.nodes:
            root = self.datum
        else:
            root = None

        # Convert graph type to undirected graph with no parallel edge.
        simple_graph = nwxGraph(self)

        # Return chain decomposition
        return list(chain_decomposition(simple_graph,
                                        root=root))[0]

    @property
    def orientations(self):
        """
        Return a list of orientations values in {+1, -1} associated with the
        list self.edgeslist. The reference orentation is arbitrary.
        """
        chain = self.chain
        orientations = list()
        for e in self.edgeslist:
            if e[:2] in chain:
                orientation = +1
            elif (e[1], e[0]) in chain:
                orientation = -1
            else:
                raise ValueError('Orientation the following edge can not be \
determined\n{}'.format(e))
            orientations.append(orientation)

#        n_pos = sum(map(lambda val: max(val, 0), orientations))
#        n_neg = -sum(map(lambda val: min(val, 0), orientations))
#        self.set_orientation_reference(int(n_pos >= n_neg)-int(n_neg > n_pos))
#
#        if self._orientation == -1:
#            orientations = [-o for o in orientations]

        return orientations

    @property
    def start_node(self):
        return self.edgeslist[0][0]

    @property
    def stop_node(self):
        return self.edgeslist[-2][1]

    def remove_edges_from_list(self, edges, preserve_nodes=None):
        """
        Remove a list of edges from the current serial subgraph.
        """

        # init nodes to current nodes
        new_nodes = dict([(n, n) for n in self.nodes])

        # init list of preserved nodes
        if preserve_nodes is None:
            preserve_nodes = []

        # loop over edges
        for e in edges:

            # Allow setitem
            e = list(e)

            # Update nodes from new_nodes dictionary
            for i, n in enumerate(e[:2]):
                e[i] = new_nodes[n]

            # Get edge key
            n1, n2 = e[:2]
            for key in self[n1][n2].keys():
                if self[n1][n2][key]['label'] == e[-1]['label']:
                    break

            # Actually remove edge
            self.remove_edge(n1, n2, key)

            # reconnect the subgraph
            if not ((n1, n2) in preserve_nodes or
                    (n2, n1) in preserve_nodes):

                # new undirected graph
                undirected = nwxGraph(self)

                if n1 in self.terminals:
                    del_node, connect_node1 = n2, n1
                    connect_node2 = list(undirected.neighbors(del_node))[0]
                else:
                    del_node, connect_node1 = n1, n2
                    connect_node2 = list(undirected.neighbors(del_node))[0]

                # Add edge with new node
                contracted_edges = contracted_nodes(self,
                                                    connect_node1,
                                                    del_node,
                                                    self_loops=False).edges
                self.add_edges_from(contracted_edges)
                # Get edge key
                edge = self.nodes2edge(del_node, connect_node2)
                n1, n2 = edge[:2]
                for key in self[n1][n2].keys():
                    if self[n1][n2][key]['label'] == e[-1]['label']:
                        break
                data = edge[2]
                # Actually remove edge
                self.remove_edge(n1, n2, key)

                edge = self.nodes2edge(connect_node1, connect_node2)
                n1, n2 = edge[:2]
                for k in data:
                    self[n1][n2][0][k] = data[k]

                # store new node label
                new_nodes[del_node] = connect_node1

            self.remove_orphan_nodes()

    def new_edge(self, edata, nodes=None):
        """
        Add a new edge to the graph at arbitrary position. If not provided,
        nodes are chosen so that the edge has positive orientation.
        """
        if nodes is None:
            # get index of first positively oriented edge
            try:
                ind = self.orientations.index(1)
                n1, n2 = self.edgeslist[ind][:2]
                n2temp = 'N'+str(edata['label'])+'_'+n2
                nodes = n1, n2temp
            except ValueError:
                ind = 0
                n1, n2 = self.edgeslist[ind][:2]
                n2temp = 'N'+str(edata['label'])+'_'+n2
                nodes = n2temp, n1

            edataTemp = self[n1][n2][0]

            for key in self[n1][n2].keys():
                if self[n1][n2][key]['label'] == edataTemp['label']:
                    break

            # Remove edge
            self.remove_edge(n1, n2, key)

            # Add edge
            self.add_edge(n2temp, n2, **edataTemp)

        self.add_edge(*nodes, **edata)

    def nodes2edge(self, n1, n2):
        """
        Return the edges between n1 and n2 (undirected search).
        """
        for i, e in enumerate(self.edgeslist):
            if n1 in e and n2 in e:
                break
        return e

    def next_edge(self, n1, n2):
        """
        Return the next edge after n1 n2 as n1 - n2 - ?
        """
        return self.nodes2edge(*self.serial_next(n1, n2)[:2])
