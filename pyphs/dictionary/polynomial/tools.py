#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 00:12:30 2017

@author: Falaize
"""

import sympy as sp
import numpy as np

def polynomial(var, coefficients):
    return sum(c*(var**i) for i, c in enumerate(coefficients))
