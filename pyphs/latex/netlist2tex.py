#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 14:59:51 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

from pyphs.latex.tools import cr
from pyphs.latex.latex import dic2array


def netlist2tex(netlist):
    str_netlist = cr(2)
    if netlist.nlines() > 0:
        str_netlist += r"\section{System netlist}" + cr(2)
        str_netlist += r"\begin{center}" + cr(1)
        str_netlist += r"\texttt{" + cr(0)
        str_netlist += r"\begin{tabular}{llllll}" + cr(0)
        str_netlist += r"\hline" + cr(0)
        str_netlist += "line & label & dictionary.component & nodes & \
parameters " + r"\\ \hline" + cr(1)
        l = 0
        for comp in netlist:
            l += 1
            latex_line = r"$\ell_" + str(l) + r"$"
            latex_dic = str(comp['dictionary'])
            latex_comp = str(comp['component'])
            latex_label = str(comp['label'])
            latex_nodes = str(comp['nodes'])
            latex_args = r'$\left\{ ' + dic2array(comp['arguments']) +\
                r'\right.$'
            str_table = \
                r'{0} & {1} & {2}.{3} & {4} & {5}'.format(latex_line,
                                                          latex_label,
                                                          latex_dic,
                                                          latex_comp,
                                                          latex_nodes,
                                                          latex_args)
            str_netlist += str_table + cr(0) + r" \\" + cr(0)
        str_netlist += r"\hline" + cr(0)
        str_netlist += r"\end{tabular}" + cr(1)
        str_netlist += r"}" + cr(1)
        str_netlist += r"\end{center}" + cr(1)
    return str_netlist


def graphplot2tex(graph, name=None, path=None):
    """
    associate the plot of the graph to a latex figure
    """
    import os
    from pyphs.config import plot_format
    if name is None:
        if hasattr(graph, 'label'):
            name = graph.label
        else:
            name = 'graph'
    if path is None:
        path = os.getcwd()
    filename = path + os.sep + name + '.' + plot_format
    graph.plot(filename=filename)
    string = cr(2) + r"""\begin{figure}[!h]
\begin{center}
\includegraphics[width=\linewidth]{""" + filename + r"""}
%
\caption{\label{fig:graph""" + name +\
        r"""} Graph of system \texttt{""" + name + r"""}. }
\end{center}
\end{figure}
%"""
    return string
