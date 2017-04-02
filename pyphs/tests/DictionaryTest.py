#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 05:40:20 2017

@author: Falaize
"""

# Support for Python 2.x and Python 3.x
from __future__ import division

# retrieve the pyphs.PHSCore of a nonlinear RLC from the tutorial on PHSCore


def dlc():
    from pyphs.examples.dlc.dlc import core
    core.build_R()
    assert core.dims.w() == 1
    return True


def bjt():
    from pyphs.examples.bjtamp.bjtamp import core
    core.build_R()
    assert core.dims.w() == 2
    return True
