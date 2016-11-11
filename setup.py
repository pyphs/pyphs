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
__version__ = '0.1.6'
__author_email__ = 'antoine.falaize@gmail.com'


###############################################################################


setup(name='pyphs',
      version=__version__,
      description="Development Status :: 4 - Beta",
      long_description=readme(),
      classifiers=[
        'Natural Language :: English',
        'Development Status :: 4 - Beta',
        'Operating System :: MacOS :: MacOS X',
        'Environment :: MacOS X',
        'Programming Language :: Python :: 2',
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
      license="""
Copyright or (c) or Copr. Project-Team S3 (Sound Signals and Systems) and Analysis/Synthesis team, Laboratory of Sciences and Technologies of Music and Sound (UMR 9912), IRCAM-CNRS-UPMC, 1 place Igor Stravinsky, F-75004 Paris contributor(s) : Antoine Falaize, Thomas Hélie, Thu Jul 9 23:11:37 2015 corresponding contributor: antoine.falaize@ircam.fr

This software (pyphs) is a computer program whose purpose is to generate C++ code for the simulation of multiphysics system described by graph structures, through  a port-Hamiltonian formulation of the system dynamics. It is composed of a single python package 'pyphs'. This software is governed by the CeCILL-B license under French law and abiding by the rules of distribution of free software. You can use, modify and/ or redistribute the software under the terms of the CeCILL-B license as circulated by CEA, CNRS and INRIA at the following URL "http://www.cecill.info".

As a counterpart to the access to the source code and rights to copy, modify and redistribute granted by the license, users are provided only with a limited warranty and the software's author, the holder of the economic rights, and the successive licensors have only limited liability. In this respect, the user's attention is drawn to the risks associated with loading, using, modifying and/or developing or reproducing the software by the user in light of its specific status of free software, that may mean that it is complicated to manipulate, and that also therefore means that it is reserved for developers and experienced professionals having in-depth computer knowledge. Users are therefore encouraged to load and test the software's suitability as regards their requirements in conditions enabling the security of their systems and/or data to be ensured and, more generally, to use and operate it in the same conditions as regards security.
""",
      packages=['pyphs'],
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
