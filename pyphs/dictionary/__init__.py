# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 13:07:33 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

# from . import edges
from . import electronics
from . import magnetics
from . import mechanics
from . import thermics
from . import mechanics_dual
from . import connectors
from . import fraccalc
from . import pwl
from . import beams
from . import transducers

import os
end = os.path.realpath(__file__).rfind(os.sep)
path_to_dictionary = os.path.realpath(__file__)[:end]

__all__ = ['electronics', 'magnetics', 'mechanics', 'thermics',
           'mechanics_dual',
           'connectors', 'fraccalc', 'pwl',
           'beams', 'transducers',
           'path_to_dictionary']
