# -*- coding: utf-8 -*-
"""
Created on Sat May 21 10:57:32 2016

@author: Falaize
"""

import numpy

###############################################################################

# Below are the options for PLOTS

# Export format:
plot_format = 'pdf'

# Can be used to define commands to be use in plot axis and lines labels:
latex_preamble = [' ', ]


###############################################################################

# Below are the options for the DICTIONARY

# Minimal conductance for accelerating convergenc of solver (diode, triode
# and bipolar-junction transistors):
GMIN = 1e-12


###############################################################################

# Below are the options for NUMERICAL COMPUTATIONS

# Define the numerical tolerance such that |x|<EPS <=> x ~ 0
EPS = numpy.finfo(float).eps


###############################################################################

# Below are the options for GRAPH ANALYSIS

# label of datum node
datum = '#'


###############################################################################

# Below are the options for LATEX RENDERING in generated .tex files and plots

# path to latex compiler
latex_compiler_path = ':/usr/texbin'

# list of authors for latex exports
footnote = r'\footnote{\url{https://github.com/afalaize/pyphs}}'
authors = [r'The \textsc{PyPHS}' + footnote + ' development team']

# list of affiliations associated with the authors for latex exports
affiliations = [r'Project-team S3\footnote{\url{http://s3.ircam.fr}}\\' +
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
# !!! This should be a raw string (especially for Windows user, for which the
# path separator '\' will be escape) !!!!
eigen_path = r'This Should be your local path to the eigen library (it can be \
configured in the script "config.py" from your local pyphs installation).'

# You can automatize the compilation and execution of the c++ files by giving a
# shell script in "cpp_build_and_run_script" below. It is executed when the
# option "langage='c++'"" is used for the simulations. You can use the keyword
# 'phobj_path' to recover the path of the current PHobject (it is replaced at
# execution)
cpp_build_and_run_script = None

# The following is an example which uses xcode on mac osx. First, generate the
# c++ code for a dummy PortHamiltonianObject, Second, init an empty xcode
# project named "xcode_template_pyphs" Third, associate the dummmy pyphs c++
# files to that xcode project (this is to create the structure), and choose
# the compilation options to your liking and save. Finally, uncomment the
# following and inform the path to your template:
#
# xcode_template_path = '/Users/.../xcode_template_pyphs'
#
# cpp_build_and_run_script = """
#
# echo "Copy the xcode template project in the current PHobj.path"
# mkdir phobj_path/xcode
# cp -r """ + xcode_template_path + """/* phobj_path/xcode
#
# echo "Copy the cpp files in the xcode template project"
# cp -r phobj_path/cpp/* phobj_path/xcode/xcode_template_pyphs/
#
# echo "Build the xcode template project for release"
# xcodebuild -project phobj_path/xcode/xcode_template_pyphs.xcodeproj \
# -alltargets -configuration Release
#
# echo "Execute the xcode template project"
# phobj_path/xcode/build/Release/xcode_template_pyphs
#
# """

###############################################################################

standard_simulations = {'load_options': {'decim': 1, 'imin': 0, 'imax': None},
                        'fs': 48e3,
                        'path': None,
                        'language': 'python',
                        'timer': False,
                        'progressbar': False,
                        'files_to_save': ('x', 'dx', 'dxH', 'w', 'z', 'y'),
                        'numtol': EPS,
                        'gradient': 'discret', # in ['discret', 'theta', 'trapez']
                        'theta': 0.5,
                        'maxit': 100,
                        'split': False,
                        'eigen_path': eigen_path,
                        'cpp_build_and_run_script': None}

standard_global = standard_simulations
