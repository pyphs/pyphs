#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 05:40:20 2017

@author: Falaize
"""

# Support for Python 2.x and Python 3.x
from __future__ import division

# retrieve the pyphs.PHSCore of a nonlinear RLC from the tutorial on PHSCore
from pyphs.tutorials.phscore import core as nlcore

from pyphs import PHSNumericalMethod, PHSNumericalCore, numcore2cpp


def cpp_nlcore_full():
    method = PHSNumericalMethod(nlcore)
    nums = PHSNumericalCore(method)
    numcore2cpp(nums)

    return True
