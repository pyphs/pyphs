# -*- coding: utf-8 -*-
"""
Copyright or © or Copr. Antoine Falaize and Thomas Hélie

Affiliation:
Project-Team S3 (Sound Signals and Systems), Analysis/Synthesis team,
Laboratory of Sciences and Technologies of Music and Sound (UMR 9912),
IRCAM-CNRS-UPMC,
1 place Igor Stravinsky, F-75004 Paris

contributor(s) : Antoine Falaize, Thomas Hélie, Thu Jul 9 23:11:37 2015
corresponding contributor: antoine.falaize@ircam.fr

This software (pypHs) is a computer program whose purpose is to generate C++
code for the simulation of multiphysics system described by graph structures.
It is composed of a library (pypHs.py) and a dictionnary (Dictionnary.py)

This software is governed by the CeCILL-B license under French law and
abiding by the rules of distribution of free software.  You can  use,
modify and/ or redistribute the software under the terms of the CeCILL-B
license as circulated by CEA, CNRS and INRIA at the following URL
"http://www.cecill.info".

As a counterpart to the access to the source code and  rights to copy,
modify and redistribute granted by the license, users are provided only
with a limited warranty  and the software's author,  the holder of the
economic rights, and the successive licensors  have only  limited liability.

In this respect, the user's attention is drawn to the risks associated
with loading,  using,  modifying and/or developing or reproducing the
software by the user in light of its specific status of free software,
that may mean  that it is complicated to manipulate,  and  that  also
therefore means  that it is reserved for developers  and  experienced
professionals having in-depth computer knowledge. Users are therefore
encouraged to load and test the software's suitability as regards their
requirements in conditions enabling the security of their systems and/or
data to be ensured and,  more generally, to use and operate it in the
same conditions as regards security.

The fact that you are presently reading this means that you have had
knowledge of the CeCILL-B license and that you accept its terms.

Created on Thu Jun  2 21:33:07 2016

@author: Antoine Falaize
"""

from __future__ import absolute_import

from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open

from os import path

from pyphs import __author__, __version__, __licence__, __author_email__


###############################################################################
here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

###############################################################################


setup(name='pyphs',
      version=__version__,
      description="Development Status :: 3 - Alpha",
      long_description=long_description,
      classifiers=[
        'Natural Language :: English',
        'Development Status :: 3 - Alpha',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: ' + __licence__,
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Physics'
      ],
      keywords='dynamical systems, numerical analysis, \
      passive systems, port-hamiltonian systems',
      url='https://github.com/aFalaize/pyphs',
      author=__author__,
      author_email=__author_email__,
      license=__licence__,
      packages=find_packages(exclude=['docs', 'examples']),
      zip_safe=False,
      install_requires=[
          'numpy',
          'scipy',
          'sympy',
          'networkx',
          'progressbar2',
          'matplotlib',
          'stopit'
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      )
