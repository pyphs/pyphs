#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 15:11:30 2016

@author: Falaize
"""
from unittest import TestCase
from pyphs import PHSNetlist
from PHSNetlistTests import NetlistThieleSmallNL, target_netlist
from PHSGraphTests import graph, target_edges, target_M
from PHSLatexTest import TestCore2Tex
import numpy as np

class TestPHSNetlistInit(TestCase):
    def test_netlist_init_and_add_components(self):
        netlist = NetlistThieleSmallNL()
        self.assertTrue(netlist.netlist() == target_netlist)


class TestPHSNetlistReadWrite(TestCase):
    def test_netlist_write_and_read(self):
        netlist = NetlistThieleSmallNL()
        netlist.write()
        filename = netlist.filename
        netlist2 = PHSNetlist(filename, clear=False)
        self.assertTrue(netlist2.netlist() == target_netlist)


class TestPHSGraphBuildFromNetlist(TestCase):
    def test_graph_build_from_netlist(self):
        self.assertTrue(graph.edges(data=True) == target_edges)


class TestPHSGraphBuildCore(TestCase):
    def test_graph_build_from_netlist(self):
        graph.buildCore()
        test_M = np.array(graph.Core.M)-target_M
        results = (test_M == np.zeros(target_M.shape))
        self.assertTrue(all(list(results.flatten())))


class TestCore2Latex(TestCase):
    def test_core_2_latex(self):
        self.assertTrue(TestCore2Tex())
