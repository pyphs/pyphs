#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 11:13:24 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

from pyphs.core.maths import matvecprod
from pyphs.core.tools import types, simplify
from pyphs.config import VERBOSE
from pyphs.numerics.cpp.method2cpp import method2cpp
from pyphs.numerics.numerical_method._method import Method
import sympy


class MethodInvMat(Method):
    """
    Pyphs symbolic numerical methods for faust code generation
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
              'split': True,        # split implicit from explicit part
              'maxit': 10,          # Max number of iterations for NL solvers
        """
        Method.__init__(self, core, config=config, label=label)

        if VERBOSE >= 2:
            print('    Build {}'.format('ijactempFll'))
        self.setexpr('ijactempFll', self.jactempFll().inverse_LU())

        if VERBOSE >= 2:
            print('    Build {}'.format('ud_vl'))
        ud_vl = matvecprod(-self.ijactempFll, self.Gl())
        self.setexpr('ud_vl', list(ud_vl))

        if VERBOSE >= 2:
            print('    Build {}'.format('Fnl'))
        temp = matvecprod(self.jactempFnll()*self.ijactempFll, self.Gl())
        Fnl = list(types.matrix_types[0](self.Gnl()) -
                   types.matrix_types[0](temp))

        if VERBOSE >= 2:
            print('    Simplify {}'.format('jacFnlnl'))
        jacFnlnl = simplify(self.jacGnlnl() -
                            self.jactempFnll()*self.ijactempFll*self.jacGlnl())

        if VERBOSE >= 2:
            print('    Inverse {}'.format('jacFnlnl'))
        if jacFnlnl.shape == (0, 0):
            ijacFnlnl = jacFnlnl
        else:
            ijacFnlnl = jacFnlnl.inv()

        if VERBOSE >= 2:
            print('    Build {} for Faust code generation'.format('ud_vnl'))
        ud_vnl = list(sympy.simplify(types.matrix_types[0](self.vnl()) -
                      types.matrix_types[0]((matvecprod(ijacFnlnl, Fnl)))))
        self.setexpr('ud_vnl', list(ud_vnl))

        self.init_funcs()

    def c(self):
        return (self.x + self.u + self.o())
