# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 20:42:02 2016

@author: Falaize
"""
from numerics.tools import EPS

standard_config = {'numtol': EPS,
                   'maxit': 10,
                   'load_options': {'decim': 1,
                                    'imin': 0,
                                    'imax': None},
                   'solver': 'standard',
                   'fs': 48e3,
                   'language': 'python',
                   'timer': True,
                   'split': None}
