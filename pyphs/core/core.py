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
                                    simplify, inverse)
from pyphs.core.struc_tools import (_build_R, split_linear,
                                    output_function, move_stor, move_diss,
                                    move_port, move_connector, port2connector)
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
            "Generator of functions to access the linear and nonlinear parts"
            def l_accessor():
                dim = getattr(self.dims, dim_label+'l')()
                return geteval(self, name)[:dim]
            l_accessor.__doc__ = """
=====
{0}l
=====
Accessor to the linear part of vector {0}. 

Return
------
{0}l: list of sympy expressions
    Linear part of core.{0}. This is a shorcut for \
:code:`core.{0}[:core.dims.{1}l()]`.
    
See also
--------
:code:`PHSCore.split_linear()` to split the system into linear and nonlinear 
storage and dissipative parts.
            """.format(name, dim_label)
            def nl_accessor():
                dim = getattr(self.dims, dim_label+'l')()
                return geteval(self, name)[dim:]
            nl_accessor.__doc__ = """
=====
{0}l
=====
Accessor to the nonlinear part of vector {0}. 

Return
------
{0}l: list of sympy expressions
    Nonlinear part of core.{0}. This is a shorcut for \
:code:`core.{0}[core.dims.{1}l():]`.
    
See also
--------
:code:`PHSCore.split_linear()` to split the system into linear and nonlinear 
storage and dissipative parts.
            """.format(name, dim_label)
            return (l_accessor, nl_accessor)
        

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

        core = PHSCore(label=core1.label)

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
            core.setsymb(name, attr1 + attr2)

        # Update subs disctionary
        core.subs = {}
        core.subs.update(core1.subs)
        core.subs.update(core2.subs)

        # Set Hamiltonian expression
        core.setexpr('H', core1.H + core2.H)

        # Concatenate lists of expressions
        core.setexpr('z', list(core1.z)+list(core2.z))

        core.connectors = core1.connectors + core2.connectors

        for vari in core.dims.names:
            for varj in core.dims.names:
                Mij = getattr(core, 'M'+vari+varj)()
                if all(dim > 0 for dim in Mij.shape):
                    set_func = getattr(core, 'set_M'+vari+varj)
                    set_func(Mij)

        # Need build
        core._exprs_built = False

        return core

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
state with symbol "xi" for each "xi" in state vector 'PHSCore.x'.
        """
        return [self.symbols('d'+str(x)) for x in self.x]

    def g(self):
        """
        Returns the symbols "gxi" associated with the gradient of the storage\
function w.r.t the state "xi" for each "xi" in state vector 'PHSCore.x'.
        """
        return [self.symbols('g'+str(x)) for x in self.x]

    def dxH(self):
        """
===
dxH
===
Gradient of storage function \
:math:`\\mathtt{dxH}_i = \\frac{\\partial \\mathrm H}{\\partial x_i}`.

Return
------
dxH: list of sympy expressions
    If core._dxH is None, this is a shortcut for \
:code:`[core.H.diff(xi) for xi in core.x]`. Else, returns \
:code:`core._dxH` (as an example, :code:`PHSNumericalMethod.core.dxH()` \
returns the discrete gradient expression).

See also
---------
:code:`pyphs.core.calculus.gradient`
        """
        if self._dxH is None:
            return gradient(self.H, self.x)
        else:
            return self._dxH

    def jacz(self):
        """
Return the jacobian of dissipative function 
:math:`\left[\\mathcal{J}_{\\mathbf z}\right]_{i,j}(\\mathbf w)=\\frac{\partial z_i}{\partial w_j}(\\mathbf w)`.
        """
        return jacobian(self.z, self.w)

    def output(self):
        """
Return the expression for output \
:math:`\\mathbf y=\\mathbf M_{\\mathtt{yx}}\\cdot \\nabla \mathrm H + \\mathbf M_{\\mathtt{yw}}\\cdot \\mathbf z+ \\mathbf M_{\\mathtt{yy}}\\cdot \\mathbf u+ \\mathbf M_{\\mathtt{ycy}}\\cdot \\mathbf{c_u}`.
        """
        return output_function(self)

    def args(self):
        """
====
args
====

Return list of symbols associated with quantities that are considered as
the arguments of the system exppressions. This quantities are:
* the state :code:`core.x`,
* the state variation :code:`core.dx()`,
* the static variable :code:`core.w`,
* the input :code:`core.u`, and
* the parameter :code:`core.p`.

Return
------
args: list of sympy symbols
    This is a shorcut for :code:`core.x+core.dx()+core.w+core.u+core.p`.
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
Retrun a set of freesymbols in all exprs referenced in 'PHSCore.exprs_names'
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
======
init_M
======

Init the structure matrix \
:code:`core.M = sympy.zeros(core.dims.tot(), core.dims.tot())`.
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
=
J
=

Return the skew-symetric part of structure matrix \
:math:`\\mathbf{M} = \\mathbf{J} - \\mathbf{R}` associated with the \
conservative interconnection.

Return
------

J: sympy Matrix
    :math:`\\mathbf{J} = \\frac{1}{2}(\\mathbf{M} - \\mathbf{M}^\intercal)`
        """
        return (self.M - self.M.T)/2.

    def R(self):
        """
=
R
=

Return the symetric part of structure matrix \
:math:`\\mathbf{M} = \\mathbf{J} - \\mathbf{R}` associated with the \
resistive interconnection.

Return
------

R: sympy Matrix
    :math:`\\mathbf{R} = -\\frac{1}{2}(\\mathbf{M} + \\mathbf{M}^\intercal)`
        """
        return -(self.M + self.M.T)/2.

    build_R = _build_R

    split_linear = split_linear

    def labels(self):
        """
Return a list of the system's equations labels wich are by convention \
:code:`(x, w, y, cy)`. Every symbols (:code:`core.x`, ...) are converted \
to strings.
        """
        labels = list(self.x) + \
            list(self.w) + \
            list(self.y) + \
            list(self.cy)
        return [str(el) for el in labels]

    def get_label(self, n):
        """
        Return label of edge n
        """
        return self.labels[n]

###########################################################################
###########################################################################

    def build_evals(self):
        """
===========
build_evals
===========

Instantiate a :code:`pyphs.PHSNumericalEval` object in :code:`core.evals` \
with numerical evaluation of every :code:`core` expressions through sympy \
lambdification. It is not dynamic so it must be re-build at any change in \
the :code:`core` expressions.

See also
---------
:code:`pyphs.numerics.numeric.PHSNumericalEval` class and \
:code:`pyphs.numerics.tools.lambdify` function.
"""

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
==========
apply_subs
==========

Apply substitutions to every expressions.

Parameters
-----------
subs: dictionary or None
    A dictionary with entries in the format :code:`{s: v}` with \
:code:`s` the sympy symbol to substitute by value :code:`v`, which value \
can be a numerical value (:code:`float, int`), a new sympy symbol or a \
sympy expression. Default is None.

selfsubs: bool
    If True, every the substitutions in the dictionary :code:`PHSCore.subs`\
 are applied and the dictionary is reinitialized to :code:`{}`. Default is \
False.
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

        self.subs.update(subs)
        for k in subs.keys():
            try:
                self.subs.pop(k)
            except KeyError:
                pass

###############################################################################
###############################################################################
###############################################################################

# Connectors

    def add_connector(self, indices, alpha):
        """
=============
add_connector
=============

Add a connector which describes the connection of two ports from a \
unique PHScore.

Usage
------
core.add_connector(indices, alpha)

Parameters
---------
indices: tuple of int
    The indices of the two ports to be connected.

alpha: scalar quantity
    Coefficient of the connection.

Description
-----------
The resulting connection reads:
    * :code:`core.u[indices[0]] = alpha * core.y[indices[1]]`,
    * :code:`core.u[indices[1]] = -alpha * core.y[indices[0]]`.

Notice this method only stores a description of the connection in the \
:code:`core.connectors` argument. The connection will be effective only \
after a call to the :code:`core.apply_connectors()` method.
        """
        assert indices[0] != indices[1], 'Can not connect a port to itself: \
indices={}.'.format(indices)
        u = list()
        y = list()
        for i in indices:
            assert i < self.dims.y(), 'Port index {} is not known. Can not \
add the connector'.format(i)
            u.append(self.u[i])
            y.append(self.y[i])
        connector = {'u': u,
                     'y': y,
                     'alpha': alpha}
        self.connectors += [connector, ]
        sorted_indices = list(copy.deepcopy(indices))
        sorted_indices.sort()
        sorted_indices.reverse()
        for n, i in enumerate(sorted_indices):
            port2connector(self, i)

    def apply_connectors(self):
        """
Effectively connect inputs and outputs defined in core.connectors.

See also
--------
See help of method :code:`core.add_connector` for details.
        """

        all_alpha = list()
        # recover connectors and sort cy and cu
        for i, c in enumerate(self.connectors):
            all_alpha.append(c['alpha'])
            i_primal = self.cy.index(c['y'][0])
            self.move_connector(i_primal, 2*i)
            i_dual = self.cy.index(c['y'][1])
            self.move_connector(i_dual, 2*i+1)

        Mswitch_list = [alpha * sympy.Matrix([[0, -1],
                                              [1, 0]])
                        for alpha in all_alpha]
        Mswitch = sympy.diag(*Mswitch_list)

        nxwy = self.dims.x() + self.dims.w() + self.dims.y()
        # Gain matrix
        G_connectors = sympy.Matrix(self.M[:nxwy, nxwy:])
        # Observation matrix
        O_connectors = sympy.Matrix(self.M[nxwy:, :nxwy])

        N_connectors = sympy.eye(self.dims.cy()) - self.Mcycy() * Mswitch

        try:
            iN_connectors = inverse(N_connectors, dosimplify=True)

            # Interconnection Matrix due to the connectors
            M_connectors = G_connectors*Mswitch*iN_connectors*O_connectors

            # Store new structure
            self.M = self.M[:nxwy, :nxwy] + M_connectors

            # clean
            self.cy = list()
            self.cu = list()
            self.connectors = list()

        except ValueError:
            raise Exception('Can not resolve the connection.\n\nABORD')

###############################################################################
###############################################################################
###############################################################################


# ADD COMPONENTS

###############################################################################
###############################################################################
###############################################################################

    def add_storages(self, x, H):
        """
Add storage components with state :math:`\\mathbf{x}` and energy \
:math:`\\mathrm{H}(\\mathbf{x}) \geq 0`.

* State :math:`\\mathbf{x}` is appended to the current list of \
states symbols :code:`core.x`,
* Expression :math:`\\mathrm{H}` is added to the current expression \
of the Hamiltonian :code:`core.H`.

Parameters
----------

x: one or several pyphs.symbols
    State symbols. Can be a single symbol or a list of symbols.
    
H: sympy.Expr
    Must be a valid storage function with respect to the state \
:math:`\\mathbf{x}` with :math:`\\nabla^2\\mahtrm H(\\mathbf{x}) \succeq 0`.
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
Add dissipative components with variable :math:`\\mathbf{w}` and \
dissipative function :math:`\\mathrm{z}(\\mathbf{w})`.

* Variable :math:`\\mathbf{w}` is appended to the current list of \
variables symbols :code:`core.w`,
* Expression :math:`\\mathrm{z}` is appended to the current list of \
dissipative functions :code:`core.z`.

Parameters
----------

w: one or several pyphs.symbols
    Variable symbols. Can be a single symbol or a list of symbols.
    
z: one or several sympy.Expr
    Must be a valid dissipative function with respect to the variable \
:math:`\\mathbf{w}` with :math:`\\nabla\\mahtrm z(\\mathbf{w}) \succeq 0`.
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
        self.z += list(map(simplify, list(z)))

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

    move_storage = move_stor

    move_dissipative = move_diss

    move_port = move_port

    move_connector = move_connector

###############################################################################
###############################################################################
###############################################################################
# Latex

    def texwrite(self, path=None, title=None,
                 authors=None, affiliations=None):
        if path is None:
            path = 'core.tex'
        if title is None:
            title = r'PyPHS Core'
        texdocument(core2tex(self), path, title=title,
                    authors=authors, affiliations=affiliations)

    def pprint(self, **settings):
        sympy.init_printing()
        
        b = sympy.Matrix(self.dx() + 
                         self.w + 
                         self.y + 
                         self.cy)
        
        a = sympy.Matrix(self.g() + 
                         self.symbols(['z'+str(w)[1:] for w in self.w]) + 
                         self.u + 
                         self.cu)
        
        sympy.pprint([b, self.M, a], **settings)
    

###############################################################################
###############################################################################
###############################################################################
# Latex

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
        debi, endi = getattr(core.inds, namei)()
        debj, endj = getattr(core.inds, namej)()
        return geteval(core, name)[debi:endi, debj:endj]
    get_mat.__doc__ = """
=====
{0}{1}{2}
=====
Accessor to the submatrix :code:`core.{0}{1}{2}` with shape \
:code:`[core.dims.{1}(), core.dims.{2}()]`.
    """.format(name, dims_names[0], dims_names[1])
    return get_mat


def _build_set_mat(core, dims_names, name):
    """
    mat is ('matr', ('m', 'n')) with matr the matrix argument to define \
and 'x' and 'y' the variables that corresponds to block of struct.name
    """
    vari, varj = dims_names

    def set_mat(mat):
        if core.M.shape[0] != core.dims.tot():
            core.M = sympy.zeros(core.dims.tot())
        if name == 'J':
            Jab = sympy.Matrix(mat)
            Rab = getattr(core, 'R'+vari + varj)()
            Rba = getattr(core, 'R'+varj + vari)()
            Mab = Jab - Rab
            Mba = -Jab.T - Rba
        if name == 'R':
            Jab = getattr(core, 'J'+vari + varj)()
            Jba = getattr(core, 'J'+varj + vari)()
            R = sympy.Matrix(mat)
            Mab = Jab - R
            Mba = Jba - R.T
        if name == 'M':
            Mab = sympy.Matrix(mat)
            Mba = getattr(core, 'M'+varj + vari)()
        debi, endi = getattr(core.inds, vari)()
        debj, endj = getattr(core.inds, varj)()
        core.M[debi:endi, debj:endj] = sympy.Matrix(Mab)
        if vari != varj:
            core.M[debj:endj, debi:endi] = sympy.Matrix(Mba)
    set_mat.__doc__ = """
=========
set_{0}{1}{2}
=========
Mutator for the submatrix :code:`core.{0}{1}{2}` with shape \
:code:`[core.dims.{1}(), core.dims.{2}()]`.

Parameter
---------
mat: matrix like 
    Can be a list of core.dims.{1}() lists of core.dims.{2}() elements, or\
 numpy array or sympy Matrix with shape \
:code:`[core.dims{1}(), core.dims{2}()]`.

Remark
------

The skew-symmetry/symmetry of :code:`core.J`/:code:`core.R` are preserved \
by the automatic replacement of matrix :code:`core.{0}{2}{1}` with the \
transpose of :code:`core.{0}{1}{2}` and appropriate sign.
    """.format(name, dims_names[0], dims_names[1])

    return set_mat
