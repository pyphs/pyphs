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
from .PHSGraphTests import graph, target_edges, target_M, split_sp
from .PHSLatexTest import TestCore2Tex
from .PHSSimulationTest import (simulation_rlc_with_split,
                                simulation_rlc_without_split,
                                simulation_nlcore_full)
from .cppTest import cpp_nlcore_full
from .DictionaryTest import dlc, bjt
import numpy as np


#class TestPHSNetlistInit(TestCase):
#    def test_netlist_init_and_add_components(self):
#        netlist = NetlistThieleSmallNL()
#        self.assertTrue(netlist.netlist() == target_netlist)
#
#
#class TestPHSNetlistReadWrite(TestCase):
#    def test_netlist_write_and_read(self):
#        netlist = NetlistThieleSmallNL()
#        netlist.write()
#        filename = netlist.filename
#        netlist2 = PHSNetlist(filename, clear=False)
#        self.assertTrue(netlist2.netlist() == target_netlist)
#
#

class TestPHSGraph(TestCase):
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
                        if not res[-1]:
                            print(arg1, arg2)
                else:
                    res.append(arg1 == arg2)
                    if not res[-1]:
                        print(arg1, arg2)
        self.assertTrue(all(res))

    def test_graph_build_core(self):
        graph.buildCore()
        graph.core.apply_connectors()
        if not graph.core.x[:2] == graph.core.symbols(['xM', 'xL']):
            i = graph.core.x.index(graph.core.symbols('xM'))
            graph.core.move_storage(0, i)
            i = graph.core.x.index(graph.core.symbols('xL'))
            graph.core.move_storage(1, i)
        if not graph.core.w[:2] == graph.core.symbols(['wR', 'wA']):
            i = graph.core.w.index(graph.core.symbols('wR'))
            graph.core.move_dissipative(0, i)
            i = graph.core.w.index(graph.core.symbols('wA'))
            graph.core.move_dissipative(1, i)
        test_M = np.array(graph.core.M)-target_M
        results = (test_M == np.zeros(target_M.shape))
        self.assertTrue(all(list(results.flatten())))

    def test_split_sp(self):
        self.assertTrue(split_sp())


class TestCore2Latex(TestCase):
    def test_core_2_latex(self):
        self.assertTrue(TestCore2Tex())


class TestSimulation(TestCase):

    def test_simulation_rlc_with_split(self):
        self.assertTrue(simulation_rlc_with_split())

    def test_simulation_rlc_without_split(self):
        self.assertTrue(simulation_rlc_without_split())

    def test_simulation_nlcore_full(self):
        self.assertTrue(simulation_nlcore_full())


class TestCpp(TestCase):
    def test_cpp_nlcore_full(self):
        self.assertTrue(cpp_nlcore_full())


class TestDico(TestCase):

    def test_bjt(self):
        self.assertTrue(bjt())

    def test_dlc(self):
        self.assertTrue(dlc())
