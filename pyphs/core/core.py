#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 18:26:56 2016

@author: Falaize
"""
from __future__ import division
import sympy
from pyphs.core.misc_tools import geteval
from pyphs.core.struc_tools import output_function
from pyphs.core.discrete_calculus import discrete_gradient
from pyphs.core.calculus import gradient, jacobian, hessian
from pyphs.core.dimensions import Dimensions
from pyphs.core.indices import Indices

###############################################################################


def symbols(obj):
    """
    Sympy 'symbols' function with real-valued assertion
    """
    return sympy.symbols(obj, real=True)

###############################################################################


def _build_get_mat(core, dims_names, name):
    """
    mat is ('matrix, ('m', 'n')) with matrix the matrix argument to define \
and 'x' and 'y' the variables that corresponds to block of struct.name
    """
    namei, namej = dims_names

    def get_mat():
        """
        return bloc (""" + namei + ', ' + namej + """) of structure matrix M.
        """
        debi, endi = getattr(core.inds, namei)()
        debj, endj = getattr(core.inds, namej)()
        return geteval(core, name)[debi:endi, debj:endj]
    return get_mat


def _build_set_mat(core, dims_names, name):
    """
    mat is ('matr', ('m', 'n')) with matr the matrix argument to define \
and 'x' and 'y' the variables that corresponds to block of struct.name
    """
    vari, varj = dims_names

    def set_mat(val):
        """
        set bloc (""" + vari + ', ' + varj + """) of structure matrix """ + \
            name + """ to val
        """
        if core.M.shape[0] != core.dims.tot():
            core.M = sympy.zeros(core.dims.tot())
        if name == 'J':
            Jab = sympy.Matrix(val)
            Rab = getattr(core, 'R'+vari + varj)()
            Rba = getattr(core, 'R'+varj + vari)()
            Mab = Jab - Rab
            Mba = -Jab.T - Rba
        if name == 'R':
            Jab = getattr(core, 'J'+vari + varj)()
            Jba = getattr(core, 'J'+varj + vari)()
            R = sympy.Matrix(val)
            Mab = Jab - R
            Mba = Jba - R.T
        if name == 'M':
            Mab = sympy.Matrix(val)
            Mba = getattr(core, 'M'+varj + vari)()
        debi, endi = getattr(core.inds, vari)()
        debj, endj = getattr(core.inds, varj)()
        core.M[debi:endi, debj:endj] = sympy.Matrix(Mab)
        if vari != varj:
            core.M[debj:endj, debi:endi] = sympy.Matrix(Mba)

    return set_mat

###############################################################################


class PHSCore:

    def __init__(self):

        # Init Flags
        self._built = False

        # init subs with empty dictionary
        setattr(self, 'subs', dict())

        # init symbols with empty lists
        setattr(self, 'symbs_names', set())
        for name in {'x', 'w', 'u', 'y', 'cu', 'cy', 'p'}:
            self._setsymb(name, list())

        # Ordered list of names of variables considered as arguments
        self.args_names = ('x', 'dx', 'w', 'u', 'p')

        setattr(self, 'exprs_names', set())
        self._setexpr('H', sympy.sympify(0))

        # init with empty lists
        self._setexpr('z', list())
        self._setexpr('g', list())

        # Get tools
        setattr(self, 'symbols', symbols)
        setattr(self, 'dims', Dimensions(self))
        setattr(self, 'inds', Indices(self))

        # Structure
        self.struc_names = list()
        self.connectors = list()
        self.M = sympy.zeros(0)
        setattr(self,
                '_struc_build_get_mat',
                lambda mat, name: _build_get_mat(self, mat, name))
        setattr(self,
                '_struc_build_set_mat',
                lambda mat, name: _build_set_mat(self, mat, name))
        self._struc_getset()

###############################################################################

    def __add__(core1, core2):

        # Concatenate lists of symbols
        for name in phs1.symbs_names:
            attr1 = getattr(core1, name)
            attr2 = getattr(core2, name)
            core1._setsymb(name, attr1 + attr2)

        # Update subs disctionary
        core1.subs.update(core2.subs)

        # Set Hamiltonian expression
        core1._setexpr('H', core1.H + core2.H)

        # Concatenate lists of expressions
        core1._setexpr('z', list(core1.z)+list(core2.z))
        core1._setexpr('g', list(core1.g)+list(core2.g))

        # Need build
        core1._built = False

        return core1


###############################################################################
###############################################################################
###############################################################################

# SYMBOLS

###############################################################################
###############################################################################
###############################################################################

    def dx(self):
        """
        Returns the symbols "dxi" associated with the differentials of the \
state with symbol "xi" for each "xi" in state vector 'CorePHS.x'.
        """
        return [self.symbols('d'+str(x)) for x in self.x]

    def args(self):
        """
        return list of symbols associated with arguments of numerical functions
        """
        # names of arguments for functions evaluation
        args = []
        for name in self.args_names:
            symbs = geteval(self, name)
            args += symbs
        return args

    def _setsymb(self, name, list_symbs):
        """
        Creates an attribute to the class: \
a list of symbols "name" (eg "x", "w" or "y") and add "name" to \
'CorePHS._symbols'.
        """
        if name not in self.symbs_names:
            self.symbs_names.add(name)
        setattr(self, name, list_symbs)

    def symbs_all(self):
        """
        Returns all the symbols in the lists with names from \
'CorePHS._symbols'.
        """
        symbs = set()
        for name in self.symbs_names:
            this_name_symbs = getattr(self, name)
            for symb in this_name_symbs:
                symbs.add(symb)
        return symbs

###############################################################################
###############################################################################
###############################################################################

# EXPRESSIONS

###############################################################################
###############################################################################
###############################################################################

    def exprs_build(self):
        """
        Build the following system functions as sympy expressions and append \
them as attributes to the exprs module:
    - 'dxH' the continuous gradient vector of storage scalar function exprs.H,
    - 'dxHd' the discrete gradient vector of storage scalar function exprs.H,
    - 'hessH' the continuous hessian matrix of storage scalar function exprs.H,
    - 'jacz' the continuous jacobian matrix of dissipative vector function \
exprs.z,
    - 'y' the continuous output vector function,
    - 'yd' the discrete output vector function.
        """

        self._setexpr('dxH', gradient(self.H, self.x))
        self._setexpr('dxHd', discrete_gradient(self.H, self.x, self.dx()))
        self._setexpr('hessH', hessian(self.H, self.x))

        self._setexpr('jacz', jacobian(self.z, self.w))

        y, yd = output_function(self)
        self._setexpr('output', y)
        self._setexpr('outputd', yd)

        self._exprs_built = True

    def _setexpr(self, name, expr):
        """
        Add the sympy expression 'expr' to the 'CorePHS' module, with \
argument 'name', and add 'name' to the set of expressions names \
'CorePHS.exprs_names'.
        """
        if name not in self.exprs_names:
            self.exprs_names.add(name)
        if name is 'H':
            expr = sympy.sympify(expr)
        setattr(self, name, expr)

    def freesymbols(self):
        """
        Retrun a set of freesymbols in all exprs in 'CorePHS.exprs_names'
        """
        symbs = set()
        for name in self.exprs_names:
            attr = getattr(self, name)
            if hasattr(attr, "__len__"):
                for expr in attr:
                    symbs.union(expr.free_symbols)
            else:
                symbs.union(attr.free_symbols)
        return symbs


###############################################################################
###############################################################################
###############################################################################

# EXPRESSIONS

###############################################################################
###############################################################################
###############################################################################

    def _struc_getset(self, dims_names=None):
        """
        define atttributes set and get for all structure matrices
        """
        for part in ['M', 'R', 'J']:
            if dims_names is None:
                dims_names = self.dims.names
            for vari in dims_names:
                for varj in dims_names:
                    self._struc_setblock(part, part+vari+varj, (vari, varj))

    def _struc_setblock(self, part, name, dims_names):
        "effectively adds get and set attributes"
        self.struc_names += (name, )
        setattr(self,
                name, self._struc_build_get_mat(dims_names, part))
        setattr(self,
                'set_'+name, self._struc_build_set_mat(dims_names, part))

    def J(self):
        """
        return conservative (skew-symetric) part of structure matrix M = J - R
        """
        return (self.M - self.M.T)/2.

    def R(self):
        """
        return resistive (symetric) part of structure matrix M = J - R
        """
        return -(self.M + self.M.T)/2.

###############################################################################
###############################################################################
###############################################################################

# TEST

###############################################################################
###############################################################################
###############################################################################

if __name__ == '__main__':
    import numpy as np
    phs1 = PHSCore()
    phs2 = PHSCore()
    phs1.x += [phs1.symbols('x1'), ]
    phs1.H += (1/2)*phs1.x[0]**2
    phs1.set_Jxx(np.array([[0, -1], [1, 0]]))
    phs2.x += [phs2.symbols('x2'), ]
    phs2.H += (1/2)*phs2.x[0]**2
    phs2.set_Jxx(np.array([[0, -1], [1, 0]]))
    phs = phs1 + phs2