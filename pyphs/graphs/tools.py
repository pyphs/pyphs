# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 12:44:35 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

import networkx as nx
import matplotlib.pyplot as plt
from pyphs.config import plot_format


def plot(graph, filename=None, ax=None):
    """
    plot of a PHSGraph
    """
    pos = nx.circular_layout(graph)  # spring
    if ax is None:
        fig = plt.figure()
        ax = plt.axes(frameon=False)
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    nx.draw_networkx(graph, pos)
    edge_labels = {(u, v, ): d['label']
                   for u, v, d in graph.edges(data=True)}
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels,
                                 label_pos=0, font_size=7)
    plt.show()
    if filename is not None:
        fig.savefig(filename + '.' + plot_format)
