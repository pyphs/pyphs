#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 15:23:49 2017

@author: Falaize
"""
import networkx as nx
from pyphs.config import datum


def serial_next(graph, n1, n2, testDatum=True):
    """
    Continue the serial connnection [n1, n2, ...] and return an ordered list
    of nodes in the chain.

    Parameters
    ----------

    graph : pyphs.Graph
        Graph object that describes the connections structure.

    n1, n2 : nodes labels in the graph
        Serial chain to be continued [n1, ..., ni] <- [n1, ..., ni, ni+1]
        until degree(ni+1) > 2 or ni+1 is n1 (loop) or ni+1 is datum if
        testDatum parameter is True).

    testDatum : bool (optional)
        Stop at datum node. The default is True.

    Output
    ------

    nodes : list of nodes labels in the graph
        Ordered list of nodes in the serial chain.

    """
    # Undirected graph
    g = nx.Graph(graph)

    # Init list of nodes in the serial chain
    serial = [n1, n2]
    testDatumBool = serial[-1] != datum if testDatum else True
    # Continue serial chain until fork or datum
    while g.degree(serial[-1]) == 2 and testDatumBool:
        # get serial node label
        l = list(g.neighbors(serial[-1]))
        l.pop(l.index(serial[-2]))
        if not n1 == serial[-1]:
            # append list of nodes in the serial chain
            serial.append(l[0])
        else:
            break
        testDatumBool = serial[-1] != datum if testDatum else True
    return serial


def serial_edges(graph):
    """
    Return a list of the serial connections (tuples of edges) in the graph.

    Parameter
    ---------

    graph: pyphs.Graph object

    Output
    ------

    serialEdges : List of tuples
        Each element in the list is a tuple (edges, nStart, nStop) with the
        edges associated with a serial connection starting from node nStart
        to node nStop in the graph.

    """
    # Undirected graph only
    g = nx.Graph(graph)

    # init lists
    serial_nodes = list()
    all_edges = list()
    # Check for datum termination
    datum_end = False
    # for each node with degree 2 in the graph
    for node in g.nodes():

        if node not in serial_nodes and \
                g.degree(node) == 2 and \
                not node == datum:

            # neighbors of node
            neighbors = list(g.neighbors(node))
            n1, n2 = neighbors

            # continue the serial connection toward n1
            s1 = serial_next(g, node, n1)
            datum_end = s1[-1] == datum
            s1.reverse()

            # continue the serial connection toward n2
            s2 = serial_next(g, node, n2)
            if s2[-1] == datum and datum_end:
                s2 = s2[:-1]

            # nodes in the serial connection
            s = s1[:-1] + s2
            serial_nodes += s

            # recover list of edges
            edges = list()
            for i, n in enumerate(s[:-1]):
                edges.append(getedges(graph, (n, s[i+1]))[0])
            all_edges.append((edges, s[0], s[-1]))

    return all_edges


def parallel_edges(graph):
    """
    Return a list of the parallel connections (tuples of edges) in the graph.

    Parameter
    ---------

    graph: pyphs.Graph object

    Output
    ------

    serialEdges : List of tuples
        Each element in the list is a tuple of edges associated with a
        parallel connection.

    """
    g = nx.Graph(graph)

    all_edges = list()
    for node in g.nodes():
        if g.degree(node) > 1 and not node == datum:
            nodes = g.neighbors(node)
            for n in nodes:
                edges = getedges(graph, (node, n))
                if len(edges) > 1:
                    all_edges.append(edges)
    return all_edges


def getedges(graph, nodes):
    """
    Return a list of edges from graph that have both ends in the list of nodes.

    Parameter
    ---------

    graph: pyphs.Graph object

    nodes : list of nodes labels in graph

    Output
    ------

    edges : List of edges
        The list of all edges for which both nodes are in the list of nodes.

    """
    s = set(nodes)
    edges = list()
    for e in graph.edges(data=True):
        if s.issuperset(set(e[:2])):
            edges.append(e)
    return edges


def multi2single(graph):
    g = nx.Graph()
    for u, v, d in graph.edges(data=True):
        g.add_edge(u, v, **d)
    return g


def forwardbackward(edges, nodes):
    f_edges = list()
    b_edges = list()
    for e in edges:
        if e[0] == nodes[0]:
            f_edges.append(e)
        else:
            b_edges.append(e)
    return f_edges, b_edges
