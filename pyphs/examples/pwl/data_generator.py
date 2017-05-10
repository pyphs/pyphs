#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 10 23:48:24 2017

@author: Falaize
"""

import numpy as np
import os
x = np.linspace(-4, 4, 11)
y = x**3

data_name = 'data'
path = os.path.join(os.getcwd(), data_name + '.txt')
np.savetxt(path, np.vstack((x, y)))
