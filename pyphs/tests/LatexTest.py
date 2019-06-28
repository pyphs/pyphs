#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 18:24:27 2016

@author: Falaize
"""

from pyphs.tests.NetlistTests import NetlistThieleSmallNL
from pyphs import Graph
from pyphs.misc.latex import texdocument, core2tex, graphplot2tex, netlist2tex
import shutil
import os

here = os.path.realpath(__file__)[:os.path.realpath(__file__).rfind(os.sep)]


def TestCore2Tex():
    netlist = NetlistThieleSmallNL()
    graph = Graph(netlist=netlist)
    core = graph.to_core()
    folder = os.path.join(here, 'temp')
    if not os.path.exists(folder):
        os.mkdir(folder)
    path = os.path.join(folder, 'test_core2tex.tex')
    content = netlist2tex(netlist)
    content += graphplot2tex(graph, folder=folder)
    content += core2tex(core)
    texdocument(content, path, title='test core2tex')
    shutil.rmtree(folder)
    return True
