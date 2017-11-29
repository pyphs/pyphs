# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 13:07:33 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

# from . import edges
from . import electronics
from . import mechanics
from . import connectors
from . import mechanics_dual
from . import magnetics
from . import beams
from . import pwl
from . import fraccalc
from . import transducers
from . import thermics

import os
end = os.path.realpath(__file__).rfind(os.sep)
path_to_dictionary = os.path.realpath(__file__)[:end]

__all__ = ['electronics', 'mechanics', 'magnetics', 'connectors', 'beams',
           'mechanics_dual', 'pwl', 'fraccalc', 'transducers', 'thermics',
           'path_to_dictionary']
