# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 20:42:02 2016

@author: Falaize
"""
from numerics.tools import EPS

config_simulation = {'numtol': EPS,
                     'maxit': 100,
                     'load_options': {'decim': 1,
                                      'imin': 0,
                                      'imax': None},
                     'solver': '1',
                     'timer': True,
                     'split': False}
