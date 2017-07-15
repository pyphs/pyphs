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

# Below are the options for the DICTIONARY

# Minimal conductance for accelerating convergence of NL-solver (used e.g. in
# diodes, triode and bipolar-junction transistors):
GMIN = 1e-12


###############################################################################

# Below are the options for NUMERICAL COMPUTATIONS

# Define the numerical tolerance such that |x|<EPS <=> x ~ 0
EPS = numpy.finfo(float).eps

# Define the data type (defualt is float 32bi)
DTYPE = numpy.finfo(float).dtype.type

# Symbol for sample rate in symbolic numerical scheme Method
FS_SYMBS = 'F_S'
###############################################################################

# Below are the options for SYMBOLIC COMPUTATIONS

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

# Below are the options for LATEX RENDERING in generated .tex files and plots

# path to latex compiler
latex_compiler_path = ':/usr/texbin'

# list of authors for latex exports
footnote = r'\footnote{\url{https://afalaize.github.io/pyphs/}}'
authors = [r'The \textsc{PyPHS}' + footnote + ' development team']

# list of affiliations associated with the authors for latex exports
affiliations = [r'Project-team S3AM\footnote{\url{https://www.ircam.fr/recherche/equipes-recherche/systemes-et-signaux-sonores-audioacoustique-instruments-s3am/}}\\' +
                r'STMS, IRCAM-CNRS-UPMC (UMR 9912)\\' +
                r'1 Place Igor-Stravinsky, 75004 Paris, France']

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

# We use the Eigen C++ library for matrix algebra in the generated c++ code.
# Inform below the path to your local eigen library, e.g. if you provide
# EIGEN_PATH = r'/roor/path/subpath/eigen', PyPHS will include the following in
# the generated 'core.h': r'/roor/path/subpath/eigen/Eigen/Dense'
# !!! This should be a raw string (especially for Windows user) !!!!
# Example MacOSX: r'/Users/Falaize/Documents/DEV/c++/bibliotheques/eigen'
# Example Linux: r'/home/afalaize/Documents/DEV/C++/bibliotheques/eigen'
EIGEN_PATH = r'/Users/Falaize/Documents/DEV/c++/bibliotheques/eigen'

# We use the CMAKE build system to build the generated c++ sources. Below is
# the path to cmake executable (as returned e.g. on UNIX by `which cmake`).
# Example Linux: r'/usr/bin/cmake'
# Example MaOSX: r'/opt/local/bin/cmake'

CMAKE_PATH = r'/opt/local/bin/cmake'


 ###############################################################################

# Below are the options for SIMULATIONS

# Default samplerate (Hz)
FS = 48e3

# Hamiltonian gradient evaluation
# in {'discret', 'theta', 'trapez'}
GRADIENT = 'discret'

# Parameter of the theta numerical scheme:
# M(x+theta*dx) with gradient={'discret', 'theta'}
# grad(H(x+theta*dx)) with gradient='theta'
THETA = 0.5

# Path to save the simulation results. If None, the current
# working directory is used.
SIMULATION_PATH = None

# Activate the use of theano for numerical evaluations.
THEANO = False

# Simulation language in {'python', 'c++'}
# Notice the 'c++' option need an appropriate configuration
# of the EIGEN_PATH and SCRIPT above.
LANGUAGE = 'python'

# Split the structure into explicit (up to a matrix inversion) and implicit
# before the simulation. Then presolve (matrix inversion) for the explicit part
# at runtime before the implicit function solver iterations.
SPLIT = True

# Names of the files to save in PATH/data.
# Should be known elements of Numeric
# !!!    For ploting with the Data object, FILES must    !!!
# !!!   contain at least ('x', 'dx', 'dxH', 'w', 'z', 'y')  !!!
FILES = ('x', 'dx', 'dxH', 'w', 'z', 'y')

# Display minimal timing informations
TIMER = False

# Display a progressbar at runtime
PBAR = False

# Options for the data reader. The data are read from index imin
# to index imax, rendering one element out of the number decim
LOAD_OPTS = {'imin': 0, 'imax': None, 'decim': 1}

# Maximum number of iterations for implicit functions solvers
MAXIT = 100

simulations = {'fs': FS,
               'grad': GRADIENT,
               'theta': THETA,
               'path': SIMULATION_PATH,
               'lang': LANGUAGE,
               'timer': TIMER,
               'pbar': PBAR,
               'files': FILES,
               'eps': EPS,
               'maxit': int(MAXIT),
               'split': SPLIT,
               'eigen': EIGEN_PATH,
               'cmake': CMAKE_PATH,
               'load': LOAD_OPTS,
               'theano': THEANO}

###############################################################################

# Below are the options for PLOTS

# Export format:
plot_format = 'pdf'

# Can be used to define commands for latex rendering
# in plot axis and lines labels:
latex_preamble = [' ', ]
