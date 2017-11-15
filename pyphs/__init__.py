from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .core.core import Core
from .graphs.graph import Graph
from .graphs import datum
from .graphs.netlists import Netlist
from .numerics import (Method, Numeric,
                       Evaluation, Operation)
from .numerics.simulations.simulation import Simulation
from .misc.signals.synthesis import signalgenerator
from .misc.latex import core2tex, netlist2tex, graphplot2tex, texdocument
from .numerics.cpp.method2cpp import method2cpp
from .numerics.cpp.simu2cpp import simu2cpp

from .config import path_to_configuration_file

from .examples import path_to_examples
from .tutorials import path_to_tutorials

__licence__ = \
    "CEA CNRS Inria Logiciel Libre License, version 2.1 (CeCILL-2.1)"
__author__ = "Antoine Falaize"
__maintainer__ = "Antoine Falaize"
__copyright__ = "Copyright 2012-2017"
__version__ = '0.1.15b'
__author_email__ = 'antoine.falaize@gmail.fr'

__all__ = ['Core', 'Netlist', 'Simulation', 'Graph', 'datum',
           'signalgenerator', 'Operation', 'Method',
           'Numeric', 'Evaluation',
           'core2tex', 'netlist2tex', 'graphplot2tex', 'texdocument',
           'method2cpp', 'simu2cpp', 'path_to_configuration_file',
           'path_to_examples', 'path_to_tutorials']
