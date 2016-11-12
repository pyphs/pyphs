# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 17:09:05 2016

@author: Falaize
"""


from unittest import TestCase


class TestRLC(TestCase):
    def test_rlc(self):
        from test_RLC_python import run_test
        self.assertTrue(run_test())


class TestTS(TestCase):
    def test_ts(self):
        from test_ThieleSmall import run_test
        self.assertTrue(run_test())



