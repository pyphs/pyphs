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
import matplotlib.path as mpath
import matplotlib.patches as mpatches

from pyphs.config import plot_format

# pos = spring_layout(graph, iterations=200)


template_layout = 'spring'


def draw_nodes(graph, ax=None, pos=None, layout=None):
    if ax is None:
        ax = plt.axes(frameon=False)
    if pos is None:
        if layout is None:
            layout = template_layout
        else:
            assert layout in ('circular', 'spring')
        if layout == 'spring':
            pos = nx.spring_layout(graph, iterations=200)
        elif layout == 'circular':
            pos = nx.circular_layout(graph)

    nx.draw_networkx_nodes(graph, pos, ax=ax,
                           node_size=800, node_color='w', lw=2)
    nx.draw_networkx_labels(graph, pos, ax=ax)
    return pos


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
#    def func(v_ortho):
#        return np.array([np.dot(v_ortho, v),
#                        np.dot(v_ortho, v_ortho)-1])
#    return root(func, v + np.random.randn(2)).x
    return np.dot(mat, v)


def multi2single(graph):
    g = nx.Graph()
    for u, v in graph.edges_iter():
        g.add_edge(u, v)
    return g


def getedges(graph, nodes):
    s = set(nodes)
    edges = list()
    for e in graph.edges_iter(data=True):
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


def angle(d):
    return np.degrees((np.arctan(d[1]/d[0]) + np.pi/2 % np.pi) - np.pi/2)


def draw_edge(edge, pos, ax, move=0., forward=True):
    nodes = [pos[n] for n in edge[:2]]
    v = vector(nodes)
    m = midle(nodes)
    d = direction(v)
    d_o = orthogonal(d)
    Path = mpath.Path
    path_data = [
        (Path.MOVETO, list(nodes[0])),
        (Path.CURVE3, list(m + move*d_o)),
        (Path.CURVE3, list(nodes[1])),
        ]
    codes, verts = zip(*path_data)
    path = mpath.Path(verts, codes)
    if edge[-1]['type'] == 'storage':
        color = ('blue', 'lightskyblue')
    elif edge[-1]['type'] == 'dissipative':
        color = ('green', 'lightsage')
    elif edge[-1]['type'] == 'port':
        color = ('red', 'lightsalmon')
    else:
        color = ('k', 'gainsboro')
    patch = mpatches.PathPatch(path, facecolor='none',
                               edgecolor=color[0], lw='3')
    ax.add_patch(patch)

    bbox_props = dict(boxstyle="round,pad=0.3", fc=color[1], ec=color[0],
                      lw=2, alpha=1)
    text_pos = m + (move)*d_o
    t = ax.text(list(text_pos)[0],
                list(text_pos)[1],
                edge[-1]['label'],
                ha="center", va="center",
                rotation=angle(d),
                size=12,
                bbox=bbox_props)


def unitdistance(v, n=2.):
    l = length(v)
    return l/2./n


def moves(nodes, nedges, pos):
    v = vector([pos[n] for n in nodes])
    m = list()
    if bool(nedges % 2):
        m.append(0.)
        nedges -= 1
    [m.append((i+1)*unitdistance(v)) for i in range(nedges//2)]
    [m.append(-(i+1)*unitdistance(v)) for i in range(nedges//2)]
    return m


def draw_edges(graph, pos, ax):
    for nodes in multi2single(graph).edges_iter():
        edges = getedges(graph, nodes)
        nedges = len(edges)
        for edge, move in zip(edges, moves(nodes, nedges, pos)):
            draw_edge(edge, pos, ax, move=move)


def plot(graph, filename=None, ax=None, layout=None):
    """
    plot of a PHSGraph
    """
    if ax is None:
        fig = plt.figure()
        ax = plt.axes(frameon=False)
    pos = nx.spring_layout(graph, iterations=200)
    draw_nodes(graph, ax=ax, pos=pos)
    draw_edges(graph, pos, ax)
    plt.tight_layout()
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)

    plt.show()
    if filename is not None:
        if not filename[-4:] == '.' + plot_format:
            filename += '.' + plot_format
        fig.savefig(filename)
