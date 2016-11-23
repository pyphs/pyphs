# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 22:17:28 2016

@author: Falaize
"""

from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

__licence__ = "CEA CNRS Inria Logiciel Libre License, version 2.1 (CeCILL-2.1)"
__author__ = "Antoine Falaize"
__maintainer__ = "Antoine Falaize"
__copyright__ = "Copyright 2012-2016"
__author_email__ = 'antoine.falaize@gmail.com'
__version__ = '0.1.9c3_DEV'

###############################################################################


setup(name='pyphs',
      version=__version__,
      description="Development Status :: 3 - Alpha",
      long_description=readme(),
      classifiers=[
        'Natural Language :: English',
        'Development Status :: 3 - Alpha',
        'Operating System :: MacOS :: MacOS X',
        'Environment :: MacOS X',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2 :: Only',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: ' + __licence__,
        'Topic :: Scientific/Engineering :: Physics'
      ],
      keywords='dynamical systems, numerical analysis, \
      passive systems, port-hamiltonian systems',
      url='https://github.com/A-Falaize/pyphs',
      author=__author__,
      author_email=__author_email__,
      license=__licence__,
      packages=[ 'pyphs', 
  			'pyphs.symbolics',
  			'pyphs.symbolics.structures',
  			'pyphs.simulations',
  			'pyphs.plots',
  			'pyphs.numerics',
  			'pyphs.misc',
  			'pyphs.misc.signals',
  			'pyphs.graphs',
  			'pyphs.graphs.analysis',
  			'pyphs.generation',
  			'pyphs.generation.codelatex',
  			'pyphs.generation.codecpp',
  			'pyphs.dictionary',
  			'pyphs.dictionary.classes',
  			'pyphs.dictionary.classes.connectors',
  			'pyphs.dictionary.classes.linears.',
  			'pyphs.dictionary.classes.nonlinears',
  			'pyphs.data',
                ],
      zip_safe=False,
      install_requires=[
          'numpy',
          'scipy',
          'sympy',
          'networkx',
          'progressbar',
      ],
      dependency_links=[
          'http://github.com/user/repo/tarball/master#egg=package-1.0'
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      )
