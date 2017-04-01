#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 18:24:27 2016

@author: Falaize
"""

from pyphs.tests.data import NetlistThieleSmallNL
from pyphs import PHSGraph
from pyphs.latex import texdocument, core2tex


def TestCore2Tex():
    netlist = NetlistThieleSmallNL()
    graph = PHSGraph(netlist=netlist)
    core = graph.buildCore()
    content = core2tex(core)
    texdocument(content, 'test core2tex', 'test_core2tex.tex')
    return True
