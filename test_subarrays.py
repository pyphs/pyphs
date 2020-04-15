#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 16:07:13 2020

@author: afalaize
"""

from pyphs import PHSMatrix, PHSSubArray, __version__, Core
from pyphs.examples.beam_cantilever.beam_cantilever import core

import sympy as sp
import numpy as np


N = 2

A = PHSSubArray('A', array=PHSMatrix(np.eye(N)))
B = PHSSubArray('B', array=PHSMatrix(np.eye(N)))
J = PHSMatrix([[0, A],
            [B, 0]])

a = list()
a_idxs = list()
for i, e in enumerate(core.x):
    if 'mK' in str(e):
        a.append(e)
        a_idxs.append(i)
xK = PHSSubArray("xbeamK", array=a)

print(xK)


a = Core.Vector(1,2,3)
b = Core.Vector(4,5,6)
