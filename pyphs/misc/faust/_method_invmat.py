#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 11:13:24 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import sympy as sp
from pyphs.core.maths import matvecprod, jacobian, sumvecs
from pyphs.core.tools import free_symbols, types, simplify
from pyphs.config import CONFIG_METHOD, VERBOSE, EPS_DG, FS_SYMBS
from pyphs.misc.tools import geteval, find, get_strings, remove_duplicates
from pyphs import Core
from pyphs.numerics.cpp.method2cpp import method2cpp
from pyphs.numerics.tools import Operation
from pyphs.numerics.numerical_method._method import Method
from pyphs.numerics.numerical_method._discrete_calculus import (discrete_gradient, gradient_theta,
                                 gradient_trapez)
import copy


class MethodInvMat(Method):
    """
    Base class for pyphs symbolic numerical methods.
    """

    to_cpp = method2cpp

    def __init__(self, core, config=None, label=None):
        """
        Parameters
        -----------

        core: pyphs.Core
            The core Port-Hamiltonian structure on wich the method is build.

        config: dict or None
            A dictionary of simulation parameters. If None, the standard
            pyphs.config.simulations is used (the default is None).
            keys and default values are

              'fs': 48e3,           # Sample rate (Hz)
              'grad': 'discret',    # In {'discret', 'theta', 'trapez'}
              'theta': 0.,          # Theta-scheme for the structure
              'split': False,       # split implicit from explicit part
              'maxit': 10,          # Max number of iterations for NL solvers
              'eps': 1e-16,         # Global numerical tolerance
        """
        Method.__init__(self, core, config=config, label=label)

        if VERBOSE >= 2:
            print('    Build {}'.format('ijactempFll'))
        self.setexpr('ijactempFll', self.jactempFll().inverse_LU())
        if VERBOSE >= 2:
            print('    Build {}'.format('ud_vl'))
        ud_vl = matvecprod(self.ijactempFll, self.Gl())
        self.setexpr('ud_vl', list(ud_vl))

        if VERBOSE >= 2:
            print('    Build {}'.format('Fnl'))
        Fnl = list(types.matrix_types[0](self.Gnl()) - types.matrix_types[0](matvecprod(self.jactempFnll()*self.ijactempFll, self.Gl())))

        if VERBOSE >= 2:
            print('    simplify {}'.format('jacFnlnl'))
        jacFnlnl = simplify(self.jacGnlnl() - self.jactempFnll()*self.ijactempFll*self.jacGlnl())
        if VERBOSE >= 2:
            print('    Build {}'.format('ijacFnlnl'))

        if jacFnlnl.shape == (0, 0):
            ijacFnlnl = jacFnlnl
        else:
            ijacFnlnl = jacFnlnl.inv()

        if VERBOSE >= 2:
            print('    Build {}'.format('ud_vnl'))
        ud_vnl = list(types.matrix_types[0](self.vnl()) - types.matrix_types[0]((matvecprod(ijacFnlnl, Fnl))))
        self.setexpr('ud_vnl', list(ud_vnl))

        self.init_funcs()

    def c(self):
        return (self.x + self.u + self.o())
