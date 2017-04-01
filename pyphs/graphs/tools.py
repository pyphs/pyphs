#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 15:23:49 2017

@author: Falaize
"""
import networkx as nx
from pyphs.config import datum


def serial_next(graph, n1, n2):
    assert not graph.is_directed()
    serial = [n1, n2]
    while graph.degree(serial[-1]) == 2 and not serial[-1] == datum:
        l = graph.neighbors(serial[-1])
        l.pop(l.index(serial[-2]))
        serial.append(l[0])
    return serial


def serial_edges(graph):
    g = graph.to_undirected()
    serial_nodes = list()
    all_edges = list()
    datum_end = False
    for node in g.nodes():
        if node not in serial_nodes and g.degree(node) == 2 \
                and not node == datum:
            n1, n2 = g[node]
            s1 = serial_next(g, node, n1)
            if s1[-1] == datum:
                datum_end = True
            s1.reverse()
            s2 = serial_next(g, node, n2)
            if s2[-1] == datum and datum_end:
                s2 = s2[:-1]
            s = s1[:-1] + s2
            serial_nodes += s
            edges = list()
            for i, n in enumerate(s[:-1]):
                edges.append(getedges(graph, (n, s[i+1]))[0])
            all_edges.append((edges, s[0], s[-1]))
    return all_edges


def parallel_edges(graph):
    g = graph.to_undirected()
    all_edges = list()
    for node in g.nodes():
        if g.degree(node) > 1 and not node == datum:
            nodes = g.neighbors(node)
            for n in nodes:
                edges = getedges(graph, (node, n))
                if len(edges) > 1:
                    all_edges.append(edges)
    return all_edges


def multi2single(graph):
    g = nx.Graph()
    for u, v in graph.edges_iter():
        g.add_edge(u, v)
    return g


def getedges(graph, nodes):
    s = set(nodes)
    edges = list()
    for e in graph.edges(data=True):
        if s.issuperset(set(e[:2])):
            edges.append(e)
    return edges


def forwardbackward(edges, nodes):
    f_edges = list()
    b_edges = list()
    for e in edges:
        if e[0] == nodes[0]:
            f_edges.append(e)
        else:
            b_edges.append(e)
    return f_edges, b_edges
