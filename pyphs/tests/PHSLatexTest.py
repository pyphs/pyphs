#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 18:24:27 2016

@author: Falaize
"""

from pyphs.tests.PHSNetlistTests import NetlistThieleSmallNL
from pyphs import PHSGraph
from pyphs.misc.latex import texdocument, core2tex, netlist2tex, graphplot2tex
import os

here = os.path.realpath(__file__)[:os.path.realpath(__file__).rfind(os.sep)]
path = os.path.join(here, 'test_core2tex.tex')


def TestCore2Tex():
    netlist = NetlistThieleSmallNL()
    graph = PHSGraph(netlist=netlist)
    core = graph.buildCore()
    content = netlist2tex(netlist)
    content += graphplot2tex(graph)
    content += core2tex(core)
    texdocument(content, path, title='test core2tex')
    os.remove(path)
    return True
