# -*- coding: utf-8 -*-
"""
This is the tutorial 0 for pyphs.

Details can be found at: https://afalaize.github.io/pyphs/posts/phscore/

Created on Wed Feb  1 22:39:19 2017

@author: Falaize
"""

# Support for Python 2.x and Python 3.x
from __future__ import division, print_function, absolute_import

# import of external packages
import numpy  # numerical tools
import sympy  # symbolic tools

# retrieve the pyphs.PHSCore of a simple RLC from previous tutorial
from tuto_PHSCore import core

# load the pyphs.PHSNumericalEval class in the current namespace
from pyphs import PHSNumericalMethod

# instantiate a pyphs.PHSNumericalEval object associated with a pyphs.PHSCore
method = PHSNumericalMethod(core)

