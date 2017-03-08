from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .core.core import PHSCore
from .graphs.graph import PHSGraph
from .graphs import netlist2core
from .graphs.netlists import PHSNetlist
from .numerics import (PHSNumericalMethod, PHSNumericalCore,
                       PHSNumericalEval, PHSNumericalOperation)
from .simulations.simulation import PHSSimulation
from .misc.signals.synthesis import signalgenerator
from .latex import core2tex, netlist2tex, graphplot2tex, texdocument
from .cpp.numcore2cpp import numcore2cpp
from .cpp.simu2cpp import simu2cpp

__licence__ = \
    "CEA CNRS Inria Logiciel Libre License, version 2.1 (CeCILL-2.1)"
__author__ = "Antoine Falaize"
__maintainer__ = "Antoine Falaize"
__copyright__ = "Copyright 2012-2016"
__version__ = '0.1.9.1'
__author_email__ = 'antoine.falaize@ircam.fr'

__all__ = ['PHSCore', 'PHSNetlist', 'PHSSimulation', 'PHSGraph',
           'signalgenerator', 'PHSNumericalOperation', 'PHSNumericalMethod',
           'PHSNumericalCore', 'PHSNumericalEval',
           'core2tex', 'netlist2tex', 'graphplot2tex', 'texdocument',
           'numcore2cpp', 'simu2cpp', 'netlist2core']
