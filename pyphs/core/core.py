#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 18:26:56 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

import sympy
from .misc_tools import geteval
from .discrete_calculus import discrete_gradient
from .calculus import gradient, jacobian, hessian
from .dimensions import Dimensions
from .indices import Indices
from .symbs_tools import _assert_expr, _assert_vec
from .struc_tools import reduce_linear_dissipations, split_linear, \
    output_function

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

    def __init__(self, label=None):

        # Init label
        self.label = label

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

        core = PHSCore()
        # Concatenate lists of symbols
        for name in core1.symbs_names:
            attr1 = getattr(core1, name)
            attr2 = getattr(core2, name)
            core._setsymb(name, attr1 + attr2)

        for vari in core.dims.names:
            for varj in core.dims.names:
                Mij1 = getattr(core1, 'M'+vari+varj)()
                Mij2 = getattr(core2, 'M'+vari+varj)()
                Mij = sympy.diag(Mij1, Mij2)
                if all([dim > 0 for dim in Mij.shape]):
                    set_func = getattr(core, 'set_M'+vari+varj)
                    set_func(Mij)

        # Concatenate lists of symbols
        for name in core1.symbs_names:
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

        core1.connectors += core2.connectors

        for vari in core.dims.names:
            for varj in core.dims.names:
                Mij = getattr(core, 'M'+vari+varj)()
                if all([dim > 0 for dim in Mij.shape]):
                    set_func = getattr(core1, 'set_M'+vari+varj)
                    set_func(Mij)

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

# STRUCTURE

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

    def build_R(self):
        """
        Build resistsive structure matrix R in PHS structure (J-R) associated \
with the linear dissipative components. Notice the associated \
dissipative variables w are no more accessible.
        """
        reduce_linear_dissipations(self)

    def split_linear(self):
        """
        Split the system into linear and nonlinear parts.
        """
        split_linear(self)

    def apply_connectors(self):
        """
        Effectively connect inputs and outputs defined in phs.connectors.
        """
        nxwy = self.dims.x() + self.dims.w() + self.dims.y()
        switch_list = [connector['alpha'] * sympy.Matrix([[0, 1], [-1, 0]])
                       for connector in self.connectors]
        Mswitch = sympy.diag(*switch_list)
        M = self.M
        G_connectors = sympy.Matrix(M[:nxwy, nxwy:])
        J_connectors = G_connectors * Mswitch * G_connectors.T
        M = M[:nxwy, :nxwy] + J_connectors
        self.cy = []
        self.cu = []
        self.connectors = []
        self.M = M

    def labels(self):
        """
        Return a list of edges labels
        """
        labels = list(self.x) + \
            list(self.w) + \
            list(self.y) + \
            list(self.cy)
        return [str(el) for el in labels]

    def get_label(self, n):
        """
        return label of edge n
        """
        return self.labels[n]

###########################################################################
###########################################################################
###############################################################################
###############################################################################
###############################################################################

# apply_subs

###############################################################################
###############################################################################
###############################################################################

    def apply_subs(self, subs=None):
        """
        replace all instances of key by value for each key:value in
\PHSCore.subs
        """
        if subs is None:
            subs = {}
        subs.update(self.subs)
        for name in self.symbs_names:
            attr = getattr(self, name)
            attr = list(attr)
            for i in range(len(attr)):
                try:
                    attr[i] = attr[i].subs(subs)
                except:
                    pass
            setattr(self, name, attr)
        for name in self.exprs_names:
            attr = getattr(self, name)
            if hasattr(attr, "__len__"):
                attr = list(attr)
                for i, at in enumerate(attr):
                    try:
                        attr[i] = at.subs(subs)
                    except:
                        pass
            else:
                attr = attr.subs(subs)
            setattr(self, name, attr)
        self.M = self.M.subs(subs)
        self.subs = {}

    def is_nl(self):
        return bool(self.dims.xnl())

###############################################################################
###############################################################################
###############################################################################

# ADD COMPONENTS

###############################################################################
###############################################################################
###############################################################################

    def add_storages(self, x, H):
        """
        Add a storage component with state x and energy H.
        * State x is append to the current list of states symbols,
        * Expression H is added to the current expression of Hamiltonian.

        Parameters
        ----------

        x : str, symbol, or list of
        H : sympy.Expr
        """
        try:
            hasattr(x, 'index')
            x = _assert_vec(x)
        except:
            _assert_expr(x)
            x = (x, )
        self.x += list(x)
        self.H += H

    def add_dissipations(self, w, z):
        """
        Add a dissipative component with dissipation variable w and \
dissipation function z.

        Parameters
        ----------

        w : str, symbol, or list of
        z : sympy.Expr or list of
        """
        try:
            hasattr(w, 'index')
            w = _assert_vec(w)
            z = _assert_vec(z)
            assert len(w) == len(z), 'w and z should be have same\
 dimension.'
        except:
            _assert_expr(w)
            _assert_expr(w)
            w = (w, )
            z = (z, )
        self.w += list(w)
        self.z += list(z)

    def add_ports(self, u, y):
        """
        Add one or several ports with input u and output y.

        Parameters
        ----------

        u : str, symbol, or list of
        y : str, symbol, or list of
        """
        if hasattr(u, '__len__'):
            u = _assert_vec(u)
            y = _assert_vec(y)
            assert len(u) == len(y), 'u and y should be have same\
 dimension.'
        else:
            _assert_expr(u)
            _assert_expr(y)
            u = (u, )
            y = (y, )
        self.u += list(u)
        self.y += list(y)

    def add_connectors(self, connectors):
        """
        add a connector (gyrator or transformer)
        """
        self.connectors += [connectors, ]
        self.cu = list(connectors['u'])
        self.cy = list(connectors['y'])

    def add_parameters(self, p):
        """
        add a continuously varying parameter
        """
        try:
            hasattr(p, '__len__')
            p = _assert_vec(p)
        except:
            _assert_expr(p)
            p = (p, )
        self.p += list(p)

###############################################################################
###############################################################################
###############################################################################

# TEST

###############################################################################
###############################################################################
###############################################################################

if __name__ == '__main__':
    import numpy as np
    core1 = PHSCore()
    core2 = PHSCore()
    core1.x += [core1.symbols('x1'), ]
    core1.H += (1/2)*core1.x[0]**2
    core1.set_Jxx(np.array([[1]]))
    core2.x += [core2.symbols('x2'), ]
    core2.H += (1/2)*core2.x[0]**2
    core2.set_Jxx(np.array([2]))
    core = core1 + core2
