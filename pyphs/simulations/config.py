# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 20:42:02 2016

@author: Falaize
"""

from pyphs.numerics.config import EPS
standard = {'numtol': EPS,
            'maxit': 100,
            'load_options': {'decim': 1,
                             'imin': 0,
                             'imax': None},
            'method': 'standard',
            'solver': 'standard',
            'fs': 48e3,
            'language': 'python',
            'timer': False,
            'presubs': False,
            'split': False,
            'progressbar': False}
