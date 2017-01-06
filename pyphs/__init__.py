from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys

from .core.core import PHSCore
from .graphs.graph import PHSGraph
from .graphs.netlists import PHSNetlist
from .numerics import (PHSNumericalMethod, PHSNumericalCore,
                       PHSNumericalEval, PHSNumericalOperation,
                       PHSNumericalMethodStandard)
from .simulations.simulation import PHSSimulation
from .misc.signals.synthesis import signalgenerator
from .latex import core2tex, netlist2tex, graphplot2tex, document
from .cpp import numcore2cpp, simu2cpp

__licence__ = \
    "CEA CNRS Inria Logiciel Libre License, version 2.1 (CeCILL-2.1)"
__author__ = "Antoine Falaize"
__maintainer__ = "Antoine Falaize"
__copyright__ = "Copyright 2012-2016"
__version__ = '0.2.pre1'
__author_email__ = 'antoine.falaize@gmail.com'

__all__ = ['PHSCore', 'PHSNetlist', 'PHSSimulation', 'PHSGraph',
           'signalgenerator', 'PHSNumericalMethodStandard',
           'PHSNumericalOperation', 'PHSNumericalMethod', 'PHSNumericalCore',
           'PHSNumericalEval',
           'core2tex', 'netlist2tex', 'graphplot2tex', 'document',
           'numcore2cpp', 'simu2cpp']


def __licence_text__():
    "PRINT OF THE LICENCE"
    os.chdir(os.path.dirname(sys.argv[0]))
    file_ = open(r'./LICENCE.rst', "r")
    with file_ as openfileobject:
        for line in openfileobject:
            print(line)
