#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 14:59:51 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

from .tools import cr
from .tools import dic2array

import os
import string


def netlist2tex(netlist):
    from pyphs import path_to_templates
    with open(os.path.join(path_to_templates,
                           'latex', 'netlist.template'), 'r') as f:
        template = string.Template(f.read())
    subs = {}
    # --------------------------------------------------------------------------
    subs['netlist'] = ""
    if netlist.nlines() > 0:
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
            subs['netlist'] += str_table + cr(0) + r" \\" + cr(0)
        subs['netlist'] = subs['netlist'][:-1]
    return template.substitute(subs)


def graphplot2tex(graph, label=None, folder=None, show=False):
    """
    associate the plot of the graph to a latex figure
    """
    from pyphs import path_to_templates
    with open(os.path.join(path_to_templates,
                           'latex', 'graph.template'), 'r') as f:
        template = string.Template(f.read())
    subs = {}
    from pyphs.config import plot_format
    if label is None:
        if hasattr(graph, 'label'):
            label = graph.label
        else:
            label = 'NoName'
    if folder is None:
        folder = os.getcwd()
    path = os.path.join(folder, label + r'_graph.' + plot_format)
    graph.plot(filename=path, show=show)
    subs['ne'] = graph.number_of_edges()
    subs['nn'] = graph.number_of_nodes()
    subs['figpath'] = path
    return template.substitute(subs)
