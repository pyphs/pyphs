# -*- coding: utf-8 -*-
"""
Created on Sat May 21 10:57:32 2016

@author: Falaize
"""

import numpy
import os

# Define the path to this file
here = os.path.realpath(__file__)[:os.path.realpath(__file__).rfind(os.sep)]
path_to_configuration_file = os.path.join(here, 'config.py')

###############################################################################

# Below are the options for the INTERFACE

# Verbose level in [0, 1, 2, 3]
VERBOSE = 1


###############################################################################

# Below are the options for NUMERICAL COMPUTATIONS also used in the DICTIONARY.

# Define the data type (default is float 32bit)
DTYPE = numpy.finfo(float).dtype.type

# Default samplerate (Hz)
FS = 48e3

# Define the numerical tolerance such that |x|<EPS <=> x = 0
# EPS = numpy.finfo(float).eps    # numpy tolerance
EPS = 1e-12                     # custom tolerance

# Define the numerical tolerance for the discrete gradient:
# |dx|<EPS_DG <=> dxH = H'
EPS_DG = numpy.finfo(float).eps

# Activate the use of theano for python numerical evaluations. This produce
# code that need to be compiled with inherent time cost but faster evaluations.
# Need a proper theano installation.
THEANO = False

# Maximum number of iterations for implicit functions solvers (Newton-Raphson).
MAXIT = 100

# Minimal conductance for accelerating convergence of NL-solver (used e.g. in
# diodes, triode and bipolar-junction transistors):
GMIN = 1e-12

# Assemble dictionary of parameters
CONFIG_NUMERIC = {'fs': FS,
                  'eps': EPS,
                  'maxit': int(MAXIT),
                  'theano': THEANO,
                  'gmin': GMIN,
                  'dtype': DTYPE}


###############################################################################

# Below are the options for SYMBOLIC COMPUTATIONS

# Symbol for sample rate in symbolic numerical scheme Method
FS_SYMBS = 'F_S'

# Simplification method for sympy expressions:
# -'simplify' tries a lot of simplifications and select the best w.r.t
#   a "length" criterion (slow).
# - 'factor' tries to factorise expressions (recommanded)
SIMPLIFY = 'factor'

# Simplification trial time before timeout and abord (expressed in second)
TIMEOUT = 10.

###############################################################################

# Below are the options for GRAPH ANALYSIS

# label of datum node
datum = '#'

###############################################################################

# Graphs plot options

# Nodes layout in {'circular', 'spring'}
GRAPHS_LAYOUT = 'circular'

# Number of iteration for layout optimization
GRAPHS_ITERATIONS = 1000

###############################################################################

# Below are the options for LATEX RENDERING in generated .tex files and plots

# In equations:
# use “p/q” instead of “frac{p}{q}” when the denominator is simple enough
fold_short_frac = False

# The delimiter to wrap around matrices, in {“[”, “(”}
mat_delim = "("

# Which matrix environment string to use, in {“smallmatrix”, “matrix”, “array”}
mat_str = 'array'

# multiplication symbol, in {None, “ldot”, “dot”, “times”}
mul_symbol = 'dot'

# Special characters to be ignored
special_chars = ['#']

###############################################################################

# Below are the options for C++ files rendering and execution inside python.

# Data type for real numbers in {'float', 'double'}.
FLOAT = 'double'

# We use the CMAKE build system to build the generated c++ sources. Below is
# the path to cmake executable (as returned e.g. on UNIX by `which cmake`).
# Example Linux: r'/usr/local/bin/cmake'
# Example MaOSX: r'/opt/local/bin/cmake'

CMAKE_PATH = r'/usr/local/bin/cmake'


CONFIG_CPP = {'float': FLOAT,
              'cmake': CMAKE_PATH
              }

###############################################################################

# Below are the options for symbolic numerical METHOD

# Hamiltonian gradient evaluation
# in {'discret', 'theta', 'trapez'}
GRADIENT = 'discret'

# Parameter of the theta numerical scheme:
# M(x+theta*dx) with gradient={'discret', 'theta'}
# grad(H(x+theta*dx)) with gradient='theta'
THETA = 0.

# Split the structure into explicit (up to a matrix inversion) and implicit
# before the simulation. Then presolve (matrix inversion) for the explicit part
# at runtime before the implicit function solver iterations.
SPLIT = True

CONFIG_METHOD = {'grad': GRADIENT,
                 'theta': THETA,
                 'split': SPLIT,
                 'epsdg': EPS_DG}

###############################################################################

# Below are the options for SIMULATIONS

# Path to save the simulation results. If None, the current
# working directory is used.
SIMULATION_PATH = None

# Simulation language in {'python', 'c++'}
# Notice the 'c++' option need an appropriate configuration (see website).
LANGUAGE = 'python'

# Data names in the global datasapce of the hdf5 file saved in PATH/data.
# Any VECTOR element in Numeric object can be added to the dataset.
# !!!    For ploting with the Data object, DNAMES must      !!!
# !!!   contain at least ('x', 'dx', 'dxH', 'w', 'z', 'y')  !!!
DNAMES = ('x', 'dx', 'dxH', 'w', 'z', 'y')

# Display minimal timing informations
TIMER = False

# Display a progressbar at runtime
PBAR = False

# Options for the data reader. The data are read from index start
# to index stop, rendering one element out of the number step
LOAD_OPTS = {'start': 0, 'stop': None, 'step': 1}

CONFIG_SIMULATION = {'path': SIMULATION_PATH,
                     'lang': LANGUAGE,
                     'timer': TIMER,
                     'pbar': PBAR,
                     'dnames': DNAMES,
                     'load': LOAD_OPTS}

###############################################################################

# Below are the options for PLOTS

# Export format:
plot_format = 'pdf'

###############################################################################

# Below are the options for RST rendering

# RST equations format in {'mathjax', 'latex'}
RST_EQUATIONS = 'mathjax'

RST = {'equations': RST_EQUATIONS}
