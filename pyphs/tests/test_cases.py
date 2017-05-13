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
from .PHSGraphTests import (graph, target_edges, target_M, split_sp, 
                            plot_Graph, plot_GraphAnalysis)
from .PHSLatexTest import TestCore2Tex
from .PHSSimulationTest import (simulation_rlc_with_split,
                                simulation_rlc_without_split,
                                simulation_nlcore_full,
                                simulation_rlc_cpp)
from .PHSSimulationPlotsTest import (plot_rlc_with_split,
                                     plot_power_balance_nlcore_with_split,
                                     plot_power_balance_rlc_with_split,
                                     TranferFunction)
from .cppTest import cpp_nlcore_full
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

    def test_plot_Graph(self):
        self.assertTrue(plot_Graph())

    def test_plot_GraphAnalysis(self):
        self.assertTrue(plot_GraphAnalysis())

        

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
        
    def test_simulation_rlc_cpp(self):
        self.assertTrue(simulation_rlc_cpp())


class TestCpp(TestCase):
    def test_cpp_nlcore_full(self):
        self.assertTrue(cpp_nlcore_full())


class TestExamples(TestCase):

    def test_import_examples(self):
        from pyphs.examples.bjtamp.bjtamp import core as bjtamp_core
        from pyphs.examples.connectors.connectors import core as connectors_core
        from pyphs.examples.dlc.dlc import core as dlc_core
        from pyphs.examples.fractional_derivator_ec.fractional_derivator_ec import core as fractional_derivator_ec_core
        from pyphs.examples.fractional_derivator_fc.fractional_derivator_fc import core as fractional_derivator_fc_core
        from pyphs.examples.fractional_integrator_ec.fractional_integrator_ec import core as fractional_integrator_ec_core
        from pyphs.examples.fractional_integrator_fc.fractional_integrator_fc import core as fractional_integrator_fc_core
        from pyphs.examples.mka.mka import core as mka_core
        from pyphs.examples.mka_dual.mka_dual import core as mka_dual_core
        from pyphs.examples.pwl.pwl import core as pwl_core
        from pyphs.examples.rhodes.rhodes import core as rhodes_core
        from pyphs.examples.rlc.rlc import core as rlc_core
        from pyphs.examples.thielesmall.thielesmall import core as thielesmall_core
        from pyphs.examples.thielesmall_dual.thielesmall_dual import core as thielesmall_dual_core
        self.assertTrue(True)

class TestPlots(TestCase):
    def test_plot_rlc_with_split(self):
        self.assertTrue(plot_rlc_with_split())

    def test_plot_power_balance_nlcore_with_split(self):
        self.assertTrue(plot_power_balance_nlcore_with_split())

    def test_plot_power_balance_rlc_with_split(self):
        self.assertTrue(plot_power_balance_rlc_with_split())

    def test_Transfer_function(self):
        self.assertTrue(TranferFunction())
        