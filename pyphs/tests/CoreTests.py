#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 15:14:26 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function


def test_simplify():
    from pyphs.examples.rlc.rlc import core
    core.simplify()
    return True


def test_build_eval():
    from pyphs.examples.rlc.rlc import core
    core.to_evaluation()
    return True


def test_subsinverse():
    from pyphs.examples.rlc.rlc import core
    core.subsinverse()
    return True


def test_allsymbs():
    from pyphs.examples.rlc.rlc import core
    core.allsymbs()
    return True


def test_freesymbols():
    from pyphs.examples.rlc.rlc import core
    core.freesymbols()
    return True


def test_init_M():
    from pyphs.examples.rlc.rlc import core
    core.init_M()
    return True


def test_labels():
    from pyphs.examples.rlc.rlc import core
    core.labels()
    return True


def test_pprint():
    from pyphs.examples.rlc.rlc import core
    core.pprint()
    return True
