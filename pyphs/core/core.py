#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 18:26:56 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

import sympy
import copy
from pyphs.core.misc_tools import geteval
from pyphs.core.calculus import gradient, jacobian
from pyphs.core.dimensions import Dimensions
from pyphs.core.indices import Indices
from pyphs.core.symbs_tools import (_assert_expr, _assert_vec, free_symbols,
                                    simplify)
from pyphs.core.struc_tools import reduce_linear_dissipations, \
    split_linear, output_function, move_stor, move_diss, move_port, \
    move_connector
from pyphs.latex import texdocument, core2tex
from pyphs.numerics.numeric import PHSNumericalEval


class PHSCore:
    """
    This is the base class for the core *Port-Hamiltonian Systems* structure
    in PyPHS.
    """

    _dxH = None

    def __init__(self, label=None):
        """
        Constructor for PHSCore objects.

        Parameter
        ----------

        label: None or string
            An optional label object (default is None).
        """

        # Init label
        self.label = label

        # init lists of symbols
        self.symbs_names = set()
        for name in {'x', 'w', 'u', 'y', 'cu', 'cy', 'p'}:
            self.setsymb(name, list())

        # Ordered list of symbols of variables considered as arguments
        self.args_names = ('x', 'dx', 'w', 'u', 'p')

        # init expressions (and lists of expressions)
        self.exprs_names = set()
        self.setexpr('H', sympy.sympify(0))
        self.setexpr('z', list())
        self.setexpr('g', list())

        # init tools
        self.dims = Dimensions(self)
        self.inds = Indices(self)

        # Structure
        self.struc_names = ['M', 'J', 'R']
        self.M = sympy.zeros(0)
        self._struc_build_get_mat = \
            lambda mat, name: _build_get_mat(self, mat, name)
        self._struc_build_set_mat = \
            lambda mat, name: _build_set_mat(self, mat, name)
        self._struc_getset()
        self.connectors = list()

        self.setexpr('Q', sympy.zeros(0, 0))

        # number of linear components
        setattr(self.dims, '_xl', 0)

        self.setexpr('Zl', sympy.zeros(0, 0))

        # number of linear components
        setattr(self.dims, '_wl', 0)

        names = ('xl', 'xnl', 'wl', 'wnl', 'y', 'cy')
        self.inds._set_inds(names, self)

        # get() and set() for structure matrices
        self._struc_getset(dims_names=names)

        def gen_lnl_accessors(name='dxH', dim_label='x'):
            return (lambda: geteval(self, name)[:getattr(self.dims,
                                                         dim_label+'l')()],
                    lambda: geteval(self, name)[getattr(self.dims,
                                                        dim_label+'l')():])

        # build accessors for nonlinear and linear parts
        for name in {'x', 'dx', 'dxH'}:
            lnl_accessors = gen_lnl_accessors(name, 'x')
            setattr(self, name+'l', lnl_accessors[0])
            setattr(self, name+'nl', lnl_accessors[1])

        for name in {'w', 'z'}:
            lnl_accessors = gen_lnl_accessors(name, 'w')
            setattr(self, name+'l', lnl_accessors[0])
            setattr(self, name+'nl', lnl_accessors[1])

        # Attributes to copy when calling the __copy__ method
        self.attrstocopy = {'label', 'subs', 'connectors'}

        # Dictionary for numerical substitution of all sympy.symbols
        self.subs = dict()

        # sympy.symbols method with special assumptions
        self.symbols = symbols

###############################################################################

    def __add__(core1, core2):

        core = PHSCore()

        assert set(core1.symbs_names) == set(core2.symbs_names)

        # Concatenate lists of symbols
        for name in core1.symbs_names:
            attr1 = getattr(core1, name)
            attr2 = getattr(core2, name)
            core.setsymb(name, attr1 + attr2)

        for vari in core.dims.names:
            for varj in core.dims.names:
                Mij1 = getattr(core1, 'M'+vari+varj)()
                Mij2 = getattr(core2, 'M'+vari+varj)()
                Mij = sympy.diag(Mij1, Mij2)
                if all(dim > 0 for dim in Mij.shape):
                    set_func = getattr(core, 'set_M'+vari+varj)
                    set_func(Mij)

        # Concatenate lists of symbols
        for name in core1.symbs_names:
            attr1 = getattr(core1, name)
            attr2 = getattr(core2, name)
            core1.setsymb(name, attr1 + attr2)

        # Update subs disctionary
        core1.subs.update(core2.subs)

        # Set Hamiltonian expression
        core1.setexpr('H', core1.H + core2.H)

        # Concatenate lists of expressions
        core1.setexpr('z', list(core1.z)+list(core2.z))
        core1.setexpr('g', list(core1.g)+list(core2.g))

        core1.connectors += core2.connectors

        for vari in core.dims.names:
            for varj in core.dims.names:
                Mij = getattr(core, 'M'+vari+varj)()
                if all(dim > 0 for dim in Mij.shape):
                    set_func = getattr(core1, 'set_M'+vari+varj)
                    set_func(Mij)

        # Need build
        core1._exprs_built = False

        return core1

    def __copy__(self):
        core = PHSCore()
        for name in (list(set().union(
                          self.attrstocopy,
                          self.exprs_names,
                          self.symbs_names)) +
                     ['M']):
            attr = getattr(self, name)
            setattr(core, name, copy.copy(attr))
        core.dims._xl = copy.copy(self.dims._xl)
        core.dims._wl = copy.copy(self.dims._wl)
        return core

    def __deepcopy__(self, memo=None):
        core = PHSCore()
        for name in (list(set().union(
                          self.attrstocopy,
                          self.exprs_names,
                          self.symbs_names)) +
                     ['M']):
            attr = getattr(self, name)
            setattr(core, name, copy.deepcopy(attr, memo))
        core.dims._xl = copy.copy(self.dims._xl)
        core.dims._wl = copy.copy(self.dims._wl)
        return core

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

    def dxH(self):
        """
        """
        if self._dxH is None:
            return gradient(self.H, self.x)
        else:
            return self._dxH

    def jacz(self):
        """
        """
        return jacobian(self.z, self.w)

    def output(self):
        """
        Return the expression for y.
        """
        return output_function(self)

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

    def setsymb(self, name, list_symbs):
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

    def setexpr(self, name, expr):
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
        Retrun a set of freesymbols in all exprs in 'PHSCore.exprs_names'
        """
        symbs = set()
        for name in self.exprs_names:
            attr = getattr(self, name)
            symbs.union(free_symbols(attr))
        return symbs


###############################################################################
###############################################################################
###############################################################################

# STRUCTURE

###############################################################################
###############################################################################
###############################################################################

    def init_M(self):
        """
        Init the structure matrix M = J - R with zeros(nx + nw + ny + nc)
        """
        self.M = sympy.zeros(self.dims.tot())

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
        self.struc_names = list(set(self.struc_names).union(set([name, ])))
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

    def split_linear(self, criterion=None):
        """
        Split the system into linear and nonlinear parts.
        """
        split_linear(self, criterion=criterion)

    def labels(self):
        """
        Return a list of the system's variables labels
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

    def build_evals(self):
        self.evals = PHSNumericalEval(self)

###############################################################################
###############################################################################
###############################################################################

# apply_subs

###############################################################################
###############################################################################
###############################################################################

    def apply_subs(self, subs=None, selfsubs=False):
        """
        replace all instances of key by value for each key:value in
\PHSCore.subs
        """
        if subs is None:
            subs = {}
        if selfsubs:
            subs.update(self.subs)
        for name in self.symbs_names:
            attr = getattr(self, name)
            attr = list(attr)
            for i, a in enumerate(attr):
                try:
                    attr[i] = a.subs(subs)
                except AttributeError:
                    pass
            setattr(self, name, attr)
        for name in self.exprs_names.union(['_dxH']):
            attr = getattr(self, name)
            if hasattr(attr, "shape"):
                ni, nj = attr.shape
                for i in range(ni):
                    for j in range(nj):
                        attr[i, j] = attr[i, j].subs(subs)
            elif hasattr(attr, "__len__"):
                attr = list(attr)
                for i, at in enumerate(attr):
                    attr[i] = at.subs(subs)
            else:
                try:
                    attr = attr.subs(subs)
                except:
                    # print('Warning: subs did not apply for {}'.format(name))
                    pass

            setattr(self, name, attr)
        self.M = self.M.subs(subs)
        if selfsubs:
            self.subs = {}
        else:
            self.subs.update(subs)
            for key in self.subs.keys():
                try:
                    self.subs[key] = self.subs[key].subs(subs)
                except AttributeError:
                    pass

    def is_nl(self):
        return bool(self.dims.xnl())

###############################################################################
###############################################################################
###############################################################################

# Connectors

    def add_connector(self, connector):
        """
        Add a connector which describes the connection of two ports from a \
unique PHScore.

        Usage
        ------
        core.add_connector(connectors)

        Parameter
        ---------
        connector: dict,
            The key and values are:

            * 'u': list of sympy.symbols for inputs,
            * 'y': list of sympy.symbols for outputs,
            * 'alpha': sympy.Expr for gain.

        Description
        -----------
        The resulting connexion reads:
            connector[u][1] = -connector[alpha] * connector[y][2]
            connector[u][2] = connector[alpha] * connector[y][1]
        """
        self.connectors += [connector, ]
        self.cu += list(connector['u'])
        self.cy += list(connector['y'])
        for u in connector['u']:
            if u in self.u:
                self.u.remove(self.u.index(u))
        for y in connector['y']:
            if y in self.y:
                self.y.remove(self.y.index(y))

    def apply_connectors(self):
        """
        Effectively connect inputs and outputs defined in core.connectors.
        """

        all_alpha = list()
        # recover connectors
        for i, c in enumerate(self.connectors):
            all_alpha.append(c['alpha'])
            if not self.cy[2*i] == c['y'][0]:
                new_index = self.cy.index(c['y'][0])
                self.move_connector(2*i, new_index)
            if not self.cy[2*i+1] == c['y'][1]:
                new_index = self.cy.index(c['y'][1])
                self.move_connector(2*i+1, new_index)

        nxwy = self.dims.x() + self.dims.w() + self.dims.y()

        switch_list = [alpha * sympy.Matrix([[0, -1], [1, 0]])
                       for alpha in all_alpha]
        Mswitch = sympy.diag(*switch_list)

        M = self.M.copy()
        # Gain matrix
        G_connectors = sympy.Matrix(M[:nxwy, nxwy:])
        # Observation matrix
        O_connectors = sympy.Matrix(M[nxwy:, :nxwy])
        # Interconnection Matrix due to the connectors
        M_connectors = G_connectors * Mswitch * O_connectors
        # Store new structure
        self.M = M[:nxwy, :nxwy] + M_connectors

        # clean
        self.cy = list()
        self.cu = list()
        self.connectors = list()

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
        self.H.simplify()

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
            w = _assert_vec(w)
            z = _assert_vec(z)
            assert len(w) == len(z), 'w and z should have same dimension.'
        except:
            _assert_expr(w)
            _assert_expr(w)
            w = (w, )
            z = (z, )
        self.w += list(w)
        self.z += map(simplify, list(z))

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
            assert len(u) == len(y), 'u and y should have same dimension.'
        else:
            _assert_expr(u)
            _assert_expr(y)
            u = (u, )
            y = (y, )
        self.u += list(u)
        self.y += list(y)

    def add_parameters(self, p):
        """
        Add a continuously varying parameter.

        Usage
        -----
        core.add_parameters(p)

        Parameter
        ----------
        p: sympy.Symbol or list of sympy.Symbol
            Single symbol or list of symbol associated with continuously \
varying parameter(s).
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

    def move_storage(self, indi, indf):
        move_stor(self, indi, indf)

    def move_dissipative(self, indi, indf):
        move_diss(self, indi, indf)

    def move_port(self, indi, indf):
        move_port(self, indi, indf)

    def move_connector(self, indi, indf):
        move_connector(self, indi, indf)


###############################################################################
###############################################################################
###############################################################################
# Latex

    def texwrite(self, filename=None, title=None):
        if filename is None:
            filename = 'core.tex'
        if title is None:
            title = r'PyPHS Core'
        texdocument(core2tex(self), title, filename=filename)

###############################################################################
###############################################################################
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
        return bloc (namei, namej) of structure matrix M.
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
        set bloc (vari, varj) of structure matrix name to val
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
