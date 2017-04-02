# -*- coding: utf-8 -*-
"""
Created on Sat May 21 10:57:32 2016

@author: Falaize
"""

import numpy

###############################################################################

# Below are the options for the DICTIONARY

# Minimal conductance for accelerating convergence of NL-solver (used e.g. in
# diodes, triode and bipolar-junction transistors):
GMIN = 1e-12


###############################################################################

# Below are the options for NUMERICAL COMPUTATIONS

# Define the numerical tolerance such that |x|<EPS <=> x ~ 0
EPS = numpy.finfo(float).eps


###############################################################################

# Below are the options for SYMBOLIC COMPUTATIONS

# Define the simplification trial time before timeout and abord
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
# generates “p/q” instead of “frac{p}{q}” when the denominator is simple enough
fold_short_frac = False

# The delimiter to wrap around matrices. Can be one of “[”, “(”
mat_delim = "("

# Which matrix environment string to emit. “smallmatrix”, “matrix”, “array”
mat_str = 'array'

# multiplication symbol: None, “ldot”, “dot”, or “times”
mul_symbol = 'dot'

# Special characters
special_chars = ['#']

###############################################################################

# Below are the options for C++ files rendering and execution inside python.

# We use the Eigen C++ library for matrix algebra in the generated c++ code.
# Inform below the path to your local eigen library, e.g. if you provide
# eigen_path = r'/roor/path/subpath/eigen', PyPHS will include the following in
# the generated 'core.h': r'/roor/path/subpath/eigen/Eigen/Dense'
# !!! This should be a raw string (especially for Windows user) !!!!
EIGEN_PATH = r'eigen'

# You can automatize the compilation and execution of the c++ files by giving a
# shell script in "cpp_build_and_run_script" below. It is executed when the
# option "langage='c++'"" is used for the simulations. You can use the keyword
# 'simulation_path' to recover the path of the current PHobject (it is replaced
# at execution)
SCRIPT = None

# The following is an example which uses xcode on mac osx. First, generate the
# c++ code for a dummy PortHamiltonianObject, Second, init an empty xcode
# project named "xcode_template_pyphs" Third, associate the dummmy pyphs c++
# files to that xcode project (this is to create the structure), and choose
# the compilation options to your liking and save. Finally, uncomment the
# following and inform the path to your template:
#
# XCODE_PATH = '/Users/.../xcode_template_pyphs'
#
# SCRIPT = """
#
# echo "Copy the xcode template project in the current 'simulation_path'"
# mkdir simulation_path/xcode
# cp -r """ + XCODE_PATH + """/* simulation_path/xcode
#
# echo "Copy the cpp files in the xcode template project"
# cp -r simulation_path/cpp/* simulation_path/xcode/xcode_template_pyphs/
#
# echo "Build the xcode template project for release"
# xcodebuild -project simulation_path/xcode/xcode_template_pyphs.xcodeproj \
# -alltargets -configuration Release
#
# echo "Execute the xcode template project"
# simulation_path/xcode/build/Release/xcode_template_pyphs
#
# """

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

# Simulation language in {'python', 'c++'}
# Notice the 'c++' option need an appropriate configuration
# of the EIGEN_PATH and SCRIPT above.
LANGUAGE = 'python'

# Split the structure into explicit (up to a matrix inversion) and implicit
# before the simulation. Then presolve (matrix inversion) for the explicit part
# at runtime before the implicit function solver iterations.
SPLIT = True

# Names of the files to save in PATH/data.
# Should be known elements of PHSNumericalCore
# !!!    For ploting with the PHSData object, FILES must    !!!
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
               'script': SCRIPT,
               'load': LOAD_OPTS}

###############################################################################

# Below are the options for PLOTS

# Export format:
plot_format = 'pdf'

# Can be used to define commands for latex rendering
# in plot axis and lines labels:
latex_preamble = [' ', ]
