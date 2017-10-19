#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 15:11:30 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

from unittest import TestCase
from .signalsTest import signal_synthesis, signal_waves
from .NetlistTests import test_netslist
from .GraphTests import (graph, target_edges, target_M, split_sp,
                            plot_Graph, plot_GraphAnalysis)
from .LatexTest import TestCore2Tex
from .SimulationTest import (simulation_rlc_with_split,
                                simulation_rlc_without_split,
                                simulation_rlc_without_split_theta,
                                simulation_rlc_without_split_trapez,
                                simulation_nlcore_full,
                                simulation_rlc_cpp)
from .SimulationPlotsTest import (plot_rlc_with_split,
                                     plot_power_balance_nlcore_with_split,
                                     plot_power_balance_rlc_with_split,
                                     TranferFunction)


from .CoreTests import (test_allsymbs, test_build_eval, test_freesymbols,
                           test_init_M, test_labels, test_pprint,
                           test_simplify, test_subsinverse)


from .cppTest import cpp_nlcore_full
import numpy as np


class TestNetlistInit(TestCase):
    def test_netlist_init_and_add_components(self):
        self.assertTrue(test_netslist())


class TestGraph(TestCase):
    def test_graph_build_from_netlist(self):
        edges = list(graph.edges(data=True))
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
        graph.to_core()
        graph.core.connect()
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

    def test_simulation_rlc_without_split_theta(self):
        self.assertTrue(simulation_rlc_without_split_theta())

    def test_simulation_rlc_without_split_trapez(self):
        self.assertTrue(simulation_rlc_without_split_trapez())

    def test_simulation_nlcore_full(self):
        self.assertTrue(simulation_nlcore_full())

    def test_simulation_rlc_cpp(self):
        self.assertTrue(simulation_rlc_cpp())


class TestCpp(TestCase):
    def test_cpp_nlcore_full(self):
        self.assertTrue(cpp_nlcore_full())


class TestExamples(TestCase):

    def test_import_examples1(self):
        from pyphs.examples.bjtamp.bjtamp import core as bjtamp_core
        self.assertTrue(True)

    def test_import_examples2(self):
        from pyphs.examples.connectors.connectors import core as connectors_core
        self.assertTrue(True)

    def test_import_examples3(self):
        from pyphs.examples.dlc.dlc import core as dlc_core
        self.assertTrue(True)

    def test_import_examples4(self):
        from pyphs.examples.fractional_derivator_ec.fractional_derivator_ec import core as fractional_derivator_ec_core
        self.assertTrue(True)

    def test_import_examples5(self):
        from pyphs.examples.fractional_derivator_fc.fractional_derivator_fc import core as fractional_derivator_fc_core
        self.assertTrue(True)

    def test_import_examples6(self):
        from pyphs.examples.fractional_integrator_ec.fractional_integrator_ec import core as fractional_integrator_ec_core
        self.assertTrue(True)

    def test_import_examples7(self):
        from pyphs.examples.fractional_integrator_fc.fractional_integrator_fc import core as fractional_integrator_fc_core
        self.assertTrue(True)

    def test_import_examples8(self):
        from pyphs.examples.mka.mka import core as mka_core
        self.assertTrue(True)

    def test_import_examples9(self):
        from pyphs.examples.mka_dual.mka_dual import core as mka_dual_core
        self.assertTrue(True)

    def test_import_examples10(self):
        from pyphs.examples.pwl.pwl import core as pwl_core
        self.assertTrue(True)

    def test_import_examples11(self):
        from pyphs.examples.rhodes.rhodes import core as rhodes_core
        self.assertTrue(True)

    def test_import_examples12(self):
        from pyphs.examples.rlc.rlc import core as rlc_core
        self.assertTrue(True)

    def test_import_examples13(self):
        from pyphs.examples.thielesmall.thielesmall import core as thielesmall_core
        self.assertTrue(True)

    def test_import_examples14(self):
        from pyphs.examples.thielesmall_dual.thielesmall_dual import core as thielesmall_dual_core
        self.assertTrue(True)

    def test_import_examples15(self):
        from pyphs.examples.heat_transfer.heat_transfer import core as heat_transfer_core
        self.assertTrue(True)

    def test_import_examples16(self):
        from pyphs.examples.magnetic_circuit.magnetic_circuit import core as magnetic_circuit_core
        self.assertTrue(True)

    def test_import_examples17(self):
        from pyphs.examples.thielesmall_NL.thielesmall_NL import core as thielesmall_NL_core
        self.assertTrue(True)

    def test_import_examples18(self):
        from pyphs.examples.triodeamp.triodeamp import core as triodeamp_core
        self.assertTrue(True)

    def test_import_examples19(self):
        from pyphs.examples.oscillator_nl.oscillator_nl import core as oscillator_nl_core
        self.assertTrue(True)

    def test_import_examples20(self):
        from pyphs.examples.oscillator_nl_dual.oscillator_nl_dual import core as oscillator_nl_dual_core
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


class TestSignals(TestCase):

    def test_signal_synthesis(self):
        self.assertTrue(signal_synthesis())

    def test_signal_waves(self):
        self.assertTrue(signal_waves())


class TestImportTutorials(TestCase):

    def test_tutorial_evaluation(self):
        from pyphs.tutorials import evaluation
        self.assertTrue(True)


class TestCorefunctions(TestCase):

    def test_build_eval(self):
        self.assertTrue(test_build_eval())

    def test_freesymbols(self):
        self.assertTrue(test_freesymbols())

    def test_init_M(self):
        self.assertTrue(test_init_M())

    def test_labels(self):
        self.assertTrue(test_labels())

    def test_pprint(self):
        self.assertTrue(test_pprint())

    def test_simplify(self):
        self.assertTrue(test_simplify())

    def test_subsinverse(self):
        self.assertTrue(test_subsinverse())

    def test_allsymbs(self):
        self.assertTrue(test_allsymbs())
