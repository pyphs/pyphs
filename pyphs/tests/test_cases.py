#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 15:11:30 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

from unittest import TestCase
from pyphs import PHSNetlist
from .PHSNetlistTests import NetlistThieleSmallNL, target_netlist
from .PHSGraphTests import graph, target_edges, target_M
from .PHSLatexTest import TestCore2Tex
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
        edges = graph.edges(data=True)
        edges.sort()
        res = []
        for l1, l2 in zip(target_edges, edges):
            print(' ')
            for arg1, arg2 in zip(l1, l2):
                if isinstance(arg1, dict):
                    for k in arg1.keys():
                        res.append(arg1 == arg2)
                else:
                    res.append(arg1 == arg2)
        self.assertTrue(all(res))


class TestPHSGraphBuildCore(TestCase):
    def test_graph_build_core(self):
        graph.buildCore()
        test_M = np.array(graph.core.M)-target_M
        results = (test_M == np.zeros(target_M.shape))
        self.assertTrue(all(list(results.flatten())))


class TestCore2Latex(TestCase):
    def test_core_2_latex(self):
        self.assertTrue(TestCore2Tex())
