#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 12:37:43 2018

@author: afalaize
"""

from pyphs.core.maths import gradient
from .graph import Graph
import sympy
from .tools import serial_next


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


def realizable_merge_storages(x, H):
    from pyphs import Core
    X = Core.symbols(('x'+'{}'*len(x)).format(*[str(xn)[1:] for xn in x]))
    return X, sympy.simplify(H.subs(dict([(xn, X) for xn in x])))


def nonrealizable_merge_dissipatives(w, z):
    from pyphs import Core

    y = Core.symbols('y:{0}'.format(len(w)))
    newW = Core.symbols(('w'+'{}'*len(w)).format(*[str(wn)[1:] for wn in w]))
    Y = Core.symbols('Y')

    iz = list(map(lambda arg: sympy.solve(arg[0]-arg[2], arg[1])[0],
                  zip(z, w, y)))
    W = sum([e.subs(yi, Y) for e, yi in zip(iz, y)]).simplify()
    iQ = sympy.solve(W-newW, Y)[0]

    [e.subs(yi, iQ) for (e, yi) in zip(z, y)]

    return newW, newZ


def realizable_merge_dissipatives(w, z):
    from pyphs import Core
    W = Core.symbols(('w'+'{}'*len(w)).format(*[str(wn)[1:] for wn in w]))
    return W, sum([zn.subs(dict([(wn, W) for wn in w])) for zn in z])


class SubGraph(Graph):

    def __init__(self, label):
        Graph.__init__(self, label=label)
        self._realizability = None

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
    def z_fc(self):
        z = []
        for e in self.fc_dissipatives:
            z.append(e[-1]['z'])
        return z

    @property
    def w_ec(self):
        w = []
        for e in self.ec_dissipatives:
            w.append(e[-1]['label'])
        return w

    @property
    def z_ec(self):
        z = []
        for e in self.ec_dissipatives:
            z.append(e[-1]['z'])
        return z

    def solve_realizability_issue(self):
        edges_stor = getattr(self, self.anti_realizability+'c_storages')
        if len(edges_stor) > 1:
            # Get new values for X and H
            X, H = nonrealizable_merge_storages(self.x_arc, self.dxH_arc)
            # Remove Energy associated with anti-realizable control sotroage
            self.core.H -= self.H_arc
            # Remove states associated with anti-realizable control sotroage
            for xn in self.x_arc:
                self.core.x.remove(xn)
            # remove edges
            self.remove_edge_from_list(edges_stor)
            # new component
            self.new_edge({'ctrl': self.anti_realizability,
                           'label': X,
                           'link': None,
                           'type': 'storage'
                           })

            # Append new state
            self.core.x.append(X)
            # ADD new energy
            self.core.H += H

            try:
                delattr(self, 'positions')
            except AttributeError:
                pass

        edges_diss = getattr(self, self.anti_realizability+'c_dissipatives')
        if len(edges_diss) > 1:
            W, Z = nonrealizable_merge_storages(self.w_arc, self.z_arc)
            for xn in self.x_arc:
                i = self.core.x.index(xn)
                self.core.w.pop(i)
                self.core.z.pop(i)
            self.core.w.append(W)
            self.core.z.append(Z)

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

    @property
    def subGraphNodes(self):
        """
        Get the nodes associated with the subgraph.
        """
        # read nodes from subgraph output edges
        nodes = set()
        for e in self.edges(data=True):
            if '_out_' in str(e[-1]['label']):
                nodes.update(e[:2])
        # remove datum
        if len(nodes) > 2:
            nodes.remove(self.datum)
        # return
        return nodes

    def serial_next(self, n1, n2):
        graph = self.to_undirected()
        return serial_next(graph, n1, n2)


class SubGraphParallel(SubGraph):

    def __init__(self, label):
        SubGraph.__init__(self, label)
        self._realizability = 'e'

    def new_edge(self, edata):
        e1 = self.edgeslist[1]
        n1, n2 = e1[:2]
        e = (n1, n2, edata)
        self.add_edge(e)


class SubGraphSerial(SubGraph):
    def __init__(self, label):
        SubGraph.__init__(self, label)
        self._realizability = 'f'

    @property
    def start_node(self):
        return self.edgeslist[0][0]

    @property
    def stop_node(self):
        return self.edgeslist[-2][1]

    def remove_edge_from_list(self, edges):
        """
        Remove a list of edges.
        """
        new_nodes = dict([(n, n) for n in self.nodes])
        for e in edges:
            e = list(e)
            for i, n in enumerate(e[:2]):
                e[i] = new_nodes[n]
            # Get edge key
            n1, n2 = e[:2]
            s = self.serial_next(n1, n2)
            for key in self[n1][n2].keys():
                if self[n1][n2][key]['label'] == e[-1]['label']:
                    break
            # Remove edge
            self.remove_edge(n1, n2, key)

            n3 = s[2]
            edata = self[n2][n3][0]
            for key in self[n2][n3].keys():
                if self[n2][n3][key]['label'] == edata['label']:
                    break
            # Remove edge
            self.remove_edge(n2, n3, key)
            # Add edge with new node
            self.add_edge(n1, n3, **edata)

            self.remove_orphan_nodes()
            new_nodes[n2] = n1

    def new_edge(self, edata):
        e1 = self.edgeslist[1]
        n1, n2 = e1[:2]
        n2temp = n2+'_'+str(edata['label'])
        self.add_edge(n1, n2temp, **edata)

        edataTemp = self[n1][n2][0]
        for key in self[n1][n2].keys():
            if self[n1][n2][key]['label'] == edataTemp['label']:
                break
        # Remove edge
        self.remove_edge(n1, n2, key)
        self.add_edge(n2temp, n2, **edataTemp)












