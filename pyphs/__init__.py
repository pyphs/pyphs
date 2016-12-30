from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .core.core import PHSCore
from .phsobject import PHSObject
from .graphs.graph import PHSGraph
from .graphs.netlists import PHSNetlist
from .numerics import (PHSNumericalMethod, PHSNumericalCore, PHSNumericalEval,
                       PHSNumericalOperation, PHSNumericalMethodStandard)
from .simulations.simulation import PHSSimulation
from .misc.signals.synthesis import signalgenerator
from .GUI import PHSNetlistGUI
from .latex import core2tex, netlist2tex, graphplot2tex, document

__licence__ = "CEA CNRS Inria Logiciel Libre License, version 2.1 (CeCILL-2.1)"
__author__ = "Antoine Falaize"
__maintainer__ = "Antoine Falaize"
__copyright__ = "Copyright 2012-2016"
__version__ = '0.2_DEV'
__author_email__ = 'antoine.falaize@gmail.com'

__all__ = ['__version__', '__copyright__', '__author__', '__licence__',
           'PHSObject', 'PHSCore', 'PHSNetlist', 'PHSSimulation', 'PHSGraph',
           'signalgenerator', 'PHSNetlistGUI', 'PHSNumericalMethodStandard',
           'PHSNumericalOperation', 'PHSNumericalMethod', 'PHSNumericalCore',
           'PHSNumericalEval',
           'core2tex', 'netlist2tex', 'graphplot2tex', 'document']
