#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 12:43:23 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import numpy as np
import networkx as nx

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from pyphs.config import plot_format

from pyphs.graphs.netlists import datum
from pyphs.graphs.tools import multi2single, getedges
# pos = spring_layout(graph, iterations=200)


LAYOUT = 'spring'
ITERATIONS = 500


def node_color(node):
    if node == datum:
        return 'lightsalmon'
    else:
        return 'gainsboro'


def draw_nodes(graph, ax=None, layout=None, colors=None):
    if ax is None:
        ax = plt.axes(frameon=False)
    if colors is None:
        colors = [node_color(node) for node in graph.nodes()]
    if not hasattr(graph, 'positions'):
        if layout is None:
            layout = LAYOUT
        else:
            assert layout in ('circular', 'spring')
        if layout == 'spring':
            graph.positions = nx.spring_layout(graph, iterations=ITERATIONS)
        elif layout == 'circular':
            graph.positions = nx.circular_layout(graph)
    nx.draw_networkx_nodes(graph, graph.positions, ax=ax,
                           node_size=800, node_color=colors, lw=2)
    nx.draw_networkx_labels(graph, graph.positions, ax=ax)


def midle(nodes):
    return (nodes[0]+nodes[1])/2.


def vector(nodes):
    return nodes[1] - nodes[0]


def direction(v):
    return v/length(v)


def length(v):
    return np.sqrt(np.dot(v, v))


def orthogonal(v):
    mat = np.array([[0., 1.],
                    [-1., 0.]])
    return np.dot(mat, v)


def angle(d):
    return np.degrees((np.arctan(d[1]/d[0]) + np.pi/2 % np.pi) - np.pi/2)


def type_colors(type_):
    if type_ == 'storage':
        colors = ('blue', 'lightskyblue')
    elif type_ == 'dissipative':
        colors = ('green', 'lightsage')
    elif type_ == 'port':
        colors = ('red', 'lightsalmon')
    else:
        colors = ('k', 'gainsboro')
    return colors


def draw_edge(edge, pos, ax, move=0., forward=True, colors_type=None,
              draw=True):
    nodes = [pos[n] for n in edge[:2]]
    if colors_type is None:
        colors = type_colors(edge[-1]['type'])
    else:
        colors = type_colors(colors_type)
    if draw:
        conectionstyle = 'arc3, rad={0}'.format(move)
        patch = mpatches.FancyArrowPatch(*nodes,
                                         connectionstyle=conectionstyle,
                                         arrowstyle='wedge',
                                         mutation_scale=20.0,
                                         lw=2,
                                         edgecolor=colors[0],
                                         facecolor=colors[1])
        ax.add_patch(patch)

    bbox_props = dict(boxstyle="round, pad=0.3", fc=colors[1], ec=colors[0],
                      lw=2, alpha=1)
    v = vector(nodes)
    m = midle(nodes)
    d = direction(v)
    d_o = orthogonal(d)

    P0, P2 = nodes
    P1 = m + move*length(v)*d_o

    m1 = midle([P0, P1])
    m2 = midle([P1, P2])
    text_pos = midle([m1, m2])
    ax.text(list(text_pos)[0],
            list(text_pos)[1],
            edge[-1]['label'],
            ha="center", va="center",
            rotation=angle(d),
            size=12,
            bbox=bbox_props)


def moves(nodes, nedges, pos):
    MAX_ANGLE = np.pi/2
    m = list()
    if bool(nedges % 2):
        m.append(0.)
        nedges -= 1
    [m.append(((i+1)/(nedges+1))*MAX_ANGLE) for i in range(nedges//2)]
    [m.append(-((i+1)/(nedges+1))*MAX_ANGLE) for i in range(nedges//2)]
    return m


def draw_edges(graph, ax):
    for nodes in multi2single(graph).edges_iter():
        edges = getedges(graph, nodes)
        nedges = len(edges)
        for edge, move in zip(edges, moves(nodes, nedges, graph.positions)):
            if not edge[0] == nodes[0]:
                move = -move
            draw_edge(edge, graph.positions, ax, move=move)


def plot(graph, filename=None, ax=None, layout=None):
    """
    plot of a PHSGraph
    """
    if ax is None:
        fig = plt.figure()
        ax = plt.axes(frameon=False)
    draw_nodes(graph, ax=ax)
    draw_edges(graph, ax)
    plt.tight_layout()
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)

    plt.show()
    if filename is not None:
        if not filename[-4:] == '.' + plot_format:
            filename += '.' + plot_format
        fig.savefig(filename)


def plot_analysis(graph, analysis):

    nodes_colors = list()
    ic_nodes_labels = [analysis.nodes[i] for i in analysis.ic_nodes]
    for node in graph.nodes():
        if node in ic_nodes_labels:
            nodes_colors.append('lightsalmon')
        else:
            nodes_colors.append('lightsage')
    plt.figure()
    ax = plt.axes(frameon=False)
    draw_nodes(graph, ax=ax, colors=nodes_colors)

    ic_edges_labels = \
        [analysis.get_edges_data('label')[i]
         for i in analysis.ic_edges]

    fc_edges_labels = \
        [analysis.get_edges_data('label')[i]
         for i in analysis.fc_edges]

    ec_edges_labels = \
        [analysis.get_edges_data('label')[i]
         for i in analysis.ec_edges]

    for nodes in multi2single(graph).edges_iter():
        edges_colors = list()
        edges_copy = list()
        edges_draw = list()
        edges = getedges(graph, nodes)
        for edge in edges:
            if edge[-1]['label'] in ic_edges_labels:
                edges_copy.append(edge)
                edges_colors.append('port')
                edges_draw.append(True)
            elif edge[-1]['label'] in fc_edges_labels:
                    i = analysis.fc_edges[fc_edges_labels.index(
                            edge[-1]['label'])]
                    col = analysis.lambd[:, i]
                    if sum(col) > 1:
                        edges_copy.append(edge)
                        edges_colors.append('storage')
                    elif sum(col) == 1:
                        inode2 = graph.nodes()[list(col).index(1)]
                        inode1 = edge[0] if edge[1] == inode2 else edge[1]
                        edges_copy.append((inode1, inode2, edge[-1]))
                        edges_colors.append('dissipative')
                    edges_draw.append(True)
            elif edge[-1]['label'] in ec_edges_labels:
                i = analysis.ec_edges[ec_edges_labels.index(edge[-1]['label'])]
                edges_copy.append(edge)
                edges_colors.append('dissipative')
                edges_draw.append(False)
        nedges = len(edges_copy)
        moves_ = moves(nodes, nedges, graph.positions)
        for e in range(nedges):
            edge = edges_copy[e]
            move = moves_[e]
            color = edges_colors[e]
            draw = edges_draw[e]
            if not edge[0] == nodes[0]:
                move = -move
            draw_edge(edge, graph.positions, ax, move=move,
                      colors_type=color, draw=draw)
    plt.tight_layout()
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    plt.show()
