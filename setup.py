# -*- coding: utf-8 -*-
"""
Copyright or © or Copr. Antoine Falaize and Thomas Hélie

Affiliations:
Team M2N, LaSIE (CNRS, UMR 7356), La Rochelle.
Team S3AM, IRCAM (CNRS, UMR 9912), Paris.

contributors:
Antoine Falaize, Thomas Hélie.

corresponding contributor:
antoine.falaize@gmail.fr

----------------------------------------------------------------------------

This software (pypHs) is a Python (Py) package dedicated to the simulation of
multiphysical Port-Hamiltonian Systems (PHS) described by graph structures.

This software is governed by the CeCILL-B license under French law and
abiding by the rules of distribution of free software.  You can  use,
modify and/ or redistribute the software under the terms of the CeCILL-B
license as circulated by CEA, CNRS and INRIA at the following URL
"http://www.cecill.info".

As a counterpart to the access to the source code and rights to copy,
modify and redistribute granted by the license, users have to properly cite
this package whenever they use it. Additionally, the user is provided only
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

# Python 2 back-portability
from __future__ import absolute_import

# PyPI setup tools
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open

# Os specific methods to manage paths
from os import path

# Recover metadata from pyphs.__init__.py
from pyphs import __author__, __version__, __licence__, __author_email__

# ----------------------------------------------------------------------
# Recover README from source
here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'),
          encoding='utf-8') as f:
    long_description = f.read()

# ----------------------------------------------------------------------
# Define PyPI setup configuration

setup(name='pyphs',
      version=__version__,
      description="Development Status :: 4 - Beta",
      long_description=long_description,
      classifiers=[
        'Natural Language :: English',
        'Development Status :: 4 - Beta',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: ' + __licence__,
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Physics'
      ],
      keywords='dynamical systems, numerical analysis, \
      passive systems, port-hamiltonian systems, C++, Latex',
      url='https://github.com/pyphs/pyphs',
      author=__author__,
      author_email=__author_email__,
      license=__licence__,
      packages=find_packages(exclude=['docs', ]),
      zip_safe=False,
      include_package_data=True,
      install_requires=['numpy>=1.9.3',
                        'scipy>=0.16.0',
                        'sympy>=1.1.1',
                        'networkx>=2.0',
                        'progressbar2>=2.3',
                        'matplotlib>=2.0.0',
                        'stopit>=1.1.1',
                        'nose>=1.3.7'
                        ],
      test_suite='nose.collector',
      tests_require=['nose'],
      )
