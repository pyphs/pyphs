# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 12:45:31 2016

@author: Falaize
"""

# path to latex compiler
compiler_path = ':/usr/texbin'

# author for latex exports
authors = ['Antoine Falaize', 'John Doe']
affiliations = [r'Project-team S3\footnote{\url{http://s3.ircam.fr}}, \\' +
                r'STMS, IRCAM-CNRS-UPMC (UMR 9912), \\' +
                r'1 Place Igor-Stravinsky, 75004 Paris, France']*2

# Emit “p / q” instead of “frac{p}{q}” when the denominator is simple enough
fold_short_frac = False

# The delimiter to wrap around matrices. Can be one of “[”, “(”
mat_delim = "("

# Which matrix environment string to emit. “smallmatrix”, “matrix”, “array”
mat_str = 'array'

# multiplication symbol: None, “ldot”, “dot”, or “times”
mul_symbol = 'dot'
