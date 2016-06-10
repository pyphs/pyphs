# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 12:44:35 2016

@author: Falaize
"""


def plot(graph, save=None):
    """
    plot of a pyphs.graph
    """

    import networkx as nx
    import matplotlib.pyplot as plt
    from pyphs.configs.plots import plot_format

    pos = nx.spring_layout(graph)
    fig = plt.figure()
    ax = plt.axes(frameon=False)
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    nx.draw_networkx(graph, pos)
    edge_labels = {(u, v, ): d['label']
                   for u, v, d in graph.edges(data=True)}
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels,
                                 label_pos=0.3, font_size=15)
    plt.show()
    if save is not None:
        fig.savefig(save + '.' + plot_format)
