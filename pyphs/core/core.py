#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 18:26:56 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

import sympy
import copy

from ..misc.tools import geteval
from ..config import VERBOSE
# Structure methods
from .structure.R import reduce_z
from .structure.splits import linear_nonlinear
from .structure.output import output_function as output
from .structure.moves import move_stor, move_diss, move_port, move_connector
from .structure.connectors import port2connector

from .maths import gradient, jacobian, inverse, hessian
from .structure.dimensions import Dimensions
from .structure.indices import Indices
from .tools import (types, free_symbols, sympify,
                    substitute_core, subsinverse_core, simplify_core)
from ..misc.latex import texdocument, core2tex

from collections import OrderedDict


class Core:
    """
    This is the base class for the core *Port-Hamiltonian Systems* structure
    in PyPHS.
    """

    # =====================================================================
    # Retrieve structure methods

    reduce_z = reduce_z
    linear_nonlinear = linear_nonlinear
    output = output

    move_storage = move_stor
    move_dissipative = move_diss
    move_port = move_port
    move_connector = move_connector

    def __init__(self, label=None):
        """
        Constructor for the Core Port-Hamiltonian structure object of pyphs.

        Parameter
        ----------

        label: None or string
            An optional label string used e.g. for plots (default is None).

        Returns
        -------

        core : Core
            A Core Port-Hamiltonian structure object.
        """

        # Init label
        if label is None:
            label = 'phs'
        self.label = label

        # =====================================================================

        # assertions for sympy symbols
        self.assertions = {'real': True}

        # Ordered list of variables considered as the systems's arguments
        self.args_names = ('x', 'dx', 'w', 'u', 'p', 'o')

        self.attrstocopy = {('dims', '_xl'), ('dims', '_wl'),
                            'connectors', 'force_wnl', 'subs', 'M', '_dxH',
                            'symbs_names', 'exprs_names', 'observers'}

        # Names for matrix structures
        self.struc_names = ['M', 'J', 'R']

        # =====================================================================

        # Returned by core.dxH(). If None, returns gradient(core.H, core.x).
        self._dxH = None

        # names for lists of symbols (x, w, ...)
        self.symbs_names = set()

        # Expressions names
        self.exprs_names = set()

        # Init structure
        self.M = types.matrix_types[0](sympy.zeros(0))

        # List of connectors
        self.connectors = list()

        # UNORDERED Dictionary of substitution {symbol: value}
        self.subs = OrderedDict()

        # ORDERED Dictionary of observers {symbol: expr}
        self.observers = OrderedDict()

        # List of dissipative variable symbols to be ignored in self.reduce_z
        self.force_wnl = list()

        # =====================================================================

        # init tools
        self.dims = Dimensions(self)
        self.inds = Indices(self)

        # init lists of symbols

        for name in {'x', 'w', 'u', 'y', 'cu', 'cy', 'p'}:
            self.setsymb(name, types.vector_types[0]())

        # init functions
        self.setexpr('H', sympify(0))
        self.setexpr('z', types.vector_types[0]())

        # Coefficient matrices for linear parts
        self.setexpr('Q', types.matrix_types[0](sympy.zeros(0, 0)))
        self.setexpr('Zl', types.matrix_types[0](sympy.zeros(0, 0)))

        # init tools
        self.dims = Dimensions(self)
        self.inds = Indices(self)

        # get() and set() for structure matrices
        names = ('x', 'w', 'y', 'cy', 'xl', 'xnl', 'wl', 'wnl')
        self._struc_getset(names)

        # build accessors for nonlinear and linear parts
        for name in {'x', 'dx', 'dxH'}:
            lnl_accessors = self._gen_lnl_accessors(name, 'x')
            setattr(self, name+'l', lnl_accessors[0])
            setattr(self, name+'nl', lnl_accessors[1])
        for name in {'w', 'z'}:
            lnl_accessors = self._gen_lnl_accessors(name, 'w')
            setattr(self, name+'l', lnl_accessors[0])
            setattr(self, name+'nl', lnl_accessors[1])

    # =========================================================================

    def __copy__(self):
        core = Core(label=None)
        for name in (list(set().union(
                          self.attrstocopy,
                          self.exprs_names,
                          self.symbs_names))):
            if isinstance(name, str):
                source = self
                target = core
                attr_name = name
            else:
                source = getattr(self, name[0])
                target = getattr(core, name[0])
                attr_name = name[1]
            attr = getattr(source, attr_name)
            try:
                setattr(target, attr_name, attr.copy())
            except AttributeError:
                setattr(target, attr_name, copy.copy(attr))
        core.label = copy.copy(self.label)
        return core

# copy.deepcopy should no be used, see sympy issue here:
# https://github.com/sympy/sympy/pull/7674
#    def __deepcopy__(self, memo=None):
#        core = Core(label=None)
#        for name in (list(set().union(
#                          self.attrstocopy,
#                          self.exprs_names,
#                          self.symbs_names))):
#            if isinstance(name, str):
#                source = self
#                target = core
#                attr_name = name
#            else:
#                source = getattr(self, name[0])
#                target = getattr(core, name[0])
#                attr_name = name[1]
#            attr = getattr(source, attr_name)
#            setattr(target, attr_name, copy.deepcopy(attr, memo))
#        core.label = copy.copy(self.label)
#        return core
#
    # =========================================================================

    def __add__(core1, core2):
        """
        Add core1 and core2 and return a new core.

        Every vectors are concatenated and structure matrices with same labels
        are diagonally stacked into a big (square) structure matrix.
        """
        assert set(core1.symbs_names) == set(core2.symbs_names)

        core = Core(label=core1.label)

        # Concatenate lists of symbols
        for name in core1.symbs_names:
            attr1 = getattr(core1, name)
            attr2 = getattr(core2, name)
            core.setsymb(name, attr1 + attr2)

        for vari in core.dims.names:
            for varj in core.dims.names:
                Mij1 = getattr(core1, 'M'+vari+varj)()
                Mij2 = getattr(core2, 'M'+vari+varj)()
                Mij = types.matrix_types[0](sympy.diag(Mij1, Mij2))
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

        # Update observers dictionary
        core.observers.update(core1.observers)
        core.observers.update(core2.observers)

        # Set Hamiltonian expression
        core.setexpr('H', core1.H + core2.H)

        # Concatenate lists of expressions
        core.setexpr('z', core1.z + core2.z)

        core.connectors = core1.connectors + core2.connectors
        core.force_wnl = core1.force_wnl + core2.force_wnl

        for vari in core.dims.names:
            for varj in core.dims.names:
                Mij = getattr(core, 'M'+vari+varj)()
                if all(dim > 0 for dim in Mij.shape):
                    set_func = getattr(core, 'set_M'+vari+varj)
                    set_func(Mij)

        return core
    # =========================================================================

    # SYMBOLS

    def dx(self):
        """
        dx
        **

        Returns the symbols "dxi" associated with the differentials of the
        state with symbol "xi" for each "xi" in state vector 'Core.x'. It
        is used in the numerical methods as the state increment
        :code:`x[n+1]=x[n]+dx[n]`.
        """
        return [self.symbols('d'+str(x)) for x in self.x]

    def z_symbols(self):
        """
        z_symbols
        **********

        Returns the symbols "zi" associated with the dissipation function
        "(zi, wi)" for each "wi" in dissipation variables vector
        'Core.w'.
        """
        return self.symbols(['z'+str(w)[1:] for w in self.w])

    def g(self):
        """
        g
        *

        Returns the symbols "gxi" associated with the gradient of the storage
        function w.r.t the state "xi" for each "xi" in state vector
        'Core.x'. It is used in the numerical methods as replacement symbols
        for the discrete evaluation of Hamiltonian's gradient in the structure
        matrix and dissipation function z.
        """
        return [self.symbols('g'+str(x)) for x in self.x]

    def o(self):
        """
        o
        *

        Returns the symbols "oi" associated with the i-th keyof dictionary
        'Core.observers'. It is used in the numerical methods as replacement
        symbols for the discrete evaluation of observers in the structure
        matrix and dissipation function z.
        """
        return list(self.observers.keys())

    def setsymb(self, name, symbs):
        """
        If name attribute does not exist, it is created with contents symbs
        and name is added to symbs_names. Else, attribute name is overwritten
        by symbs.
        """
        if name not in self.symbs_names:
            self.symbs_names.add(name)
        setattr(self, name, symbs)

    def allsymbs(self):
        """
        Returns all the symbols in the lists with names from
        'Core.symbs_names'.
        """
        symbs = set()
        for name in self.symbs_names:
            this_name_symbs = getattr(self, name)
            for symb in this_name_symbs:
                symbs.add(symb)
        for k in self.subs:
            for s in free_symbols(k):
                symbs.add(s)
            for s in free_symbols(self.subs[k]):
                symbs.add(s)
        return symbs

    # =========================================================================

    # EXPRESSIONS

    def setexpr(self, name, expr):
        """
        setexpr
        *******

        Add the sympy expression 'expr' to the object under argument 'name',
        and add 'name' to the set of expressions names 'core.exprs_names'.
        """
        if name not in self.exprs_names:
            self.exprs_names.add(name)
        setattr(self, name, expr)

    def freesymbols(self):
        """
        freesymbols
        ***********

        Retrun a set of freesymbols in all exprs referenced in
        'Core.exprs_names'.
        """
        symbs = set()
        for name in self.exprs_names:
            expr = geteval(self, name)
            symbs.union(free_symbols(expr))
        symbs.union(free_symbols(self.M))
        return symbs

    def dxH(self):
        """
        dxH
        ***

        Gradient of storage function
        :math:`\\mathtt{dxH}_i = \\frac{\\partial \\mathrm H}{\\partial x_i}`.

        Return
        ------
        dxH: list of sympy expressions
            If core._dxH is None, this is a shortcut for
            :code:`[core.H.diff(xi) for xi in core.x]`. Else, returns
            :code:`core._dxH` (as an example, :code:`Method.dxH()`
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
        jacz
        ***
        Return the jacobian of dissipative function
        :math:`\left[\\mathcal{J}_{\\mathbf z}\right]_{i,j}(\\mathbf w)=\\frac{\partial z_i}{\partial w_j}(\\mathbf w)`.
        """
        return jacobian(self.z, self.w)

    def hessH(self):
        """
        hessH
        ***
        Return the hessian matrix of the storage function
        :math:`\left[\\mathcal{J}_{\\mathbf z}\right]_{i,j}(\\mathbf w)=\\frac{\partial z_i}{\partial w_j}(\\mathbf w)`.
        """
        return hessian(self.H, self.x)

    # =========================================================================

    # STRUCTURE

    def init_M(self):
        """
        init_M
        ******

        Initialize the structure matrix M with appropriate number of zeros.

        """
        self.M = types.matrix_types[0](sympy.zeros(self.dims.tot()))

    def J(self):
        """
        J
        *

        Return the skew-symetric part of structure matrix
        :math:`\\mathbf{M} = \\mathbf{J} - \\mathbf{R}` associated with the
        conservative interconnection.

        Return
        ------

        J: sympy SparseMatrix
            :math:`\\mathbf{J} = \\frac{1}{2}(\\mathbf{M} - \\mathbf{M}^\intercal)`
        """
        return (self.M - self.M.T)/2.

    def R(self):
        """
        *
        R
        *

        Return the symetric part of structure matrix
        :math:`\\mathbf{M} = \\mathbf{J} - \\mathbf{R}` associated with the
        resistive interconnection.

        Return
        ------

        R: sympy SparseMatrix
            :math:`\\mathbf{R} = -\\frac{1}{2}(\\mathbf{M} + \\mathbf{M}^\intercal)`
        """
        return -(self.M + self.M.T)/2.

    # =========================================================================

    # LABELS

    def labels(self, i=None):
        """
        Return a list of the system's equations labels wich are by convention
        :code:`(x, w, y, cy)`. Every symbols (:code:`core.x`, ...) are
        converted to strings.

        Parameter
        ---------

        i : None or int
            If None, every symbols are returned, else the label with index i is
            returned (default is None).
        """
        labels = self.x + self.w + self.y + self.cy
        if i is None:
            return [str(el) for el in labels]
        else:
            return str(labels[i])

    # =========================================================================

    def simplify(self):
        """
        simplify
        **********

        Apply simplifications to every expressions.

        """
        simplify_core(self)

    # =========================================================================

    def substitute(self, **kwargs):
        """
        substitute
        **********

        Apply substitutions to every expressions.

        Keyword arguments
        -----------------

        subs : dictionary or None
            A dictionary with entries in the format :code:`{s: v}` with
            :code:`s` the sympy symbol to substitute by value :code:`v`, which
            value can be a numerical value (:code:`float, int`), a new sympy
            symbol or a sympy expression. Default is None.

        selfall : bool
            If True, every substitutions in the dictionary :code:`Core.subs`
             are applied and the dictionary is reinitialized to :code:`{}`.
             Default is False.

        selfexprs : bool
            If True, only substitutions in the dictionary :code:`Core.subs`
            that are not numerical values are applied.

        simplify : bool
            If True, every expressions are simplified after substitution.
            The default is True

        subsofsubs : bool
            If True, the substitution dictionary substitutes itself
            recursively. Default is True.
        """
        substitute_core(self, **kwargs)

    # =========================================================================

    def subsinverse(self):
        """
        subsinverse
        ***********

        Remove every occurence of inverse of symbols in core.subs. they are
        replaced by the same symbols with prefix 'inv', which is appended to
        the dictionary core.subs.

        """
        if VERBOSE >= 1:
            print("Remove Inverse of Parameters...")
        subsinverse_core(self)

    # =========================================================================

    # Connectors

    def add_connector(self, indices, alpha=None):
        """
        add_connector
        *************

        Add a connector which describes the connection of two ports from a
        unique core.

        Usage
        ------
        core.add_connector(indices, alpha)

        Parameters
        ----------
        indices: tuple of int
            The indices of the two ports to be connected.

        alpha: scalar quantity
            Coefficient of the connection.

        Description
        -----------
        The resulting connection reads:
            * :code:`core.u[indices[0]] = alpha * core.y[indices[1]]`,
            * :code:`core.u[indices[1]] = -alpha * core.y[indices[0]]`.

        Notice this method only stores a description of the connection in the
        :code:`core.connectors` argument. The connection will be effective only
        after calling the method :code:`core.connect()`.
        """
        if alpha is None:
            alpha = sympify(1.)
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
        for i in sorted_indices:
            port2connector(self, i)

    def connect(self):
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
            i_primal = getattr(self, 'cy').index(c['y'][0])
            self.move_connector(i_primal, 2*i)
            i_dual = getattr(self, 'cy').index(c['y'][1])
            self.move_connector(i_dual, 2*i+1)

        Mswitch_list = [alpha * sympy.Matrix([[0, -1],
                                              [1, 0]])
                        for alpha in all_alpha]
        Mswitch = types.matrix_types[0](sympy.diag(*Mswitch_list))

        nxwy = self.dims.x() + self.dims.w() + self.dims.y()
        # Gain matrix
        G_connectors = self.M[:nxwy, nxwy:]
        # Observation matrix
        O_connectors = self.M[nxwy:, :nxwy]
        N_connectors = types.matrix_types[0](sympy.eye(self.dims.cy()) -
                                             self.Mcycy() * Mswitch)

        try:
            iN_connectors = inverse(N_connectors, dosimplify=False)

            # Interconnection Matrix due to the connectors
            M_connectors = G_connectors*Mswitch*iN_connectors*O_connectors

            # Store new structure
            self.M = types.matrix_types[0](self.M[:nxwy, :nxwy] + M_connectors)

            # clean
            setattr(self, 'cy', list())
            setattr(self, 'cu', list())
            setattr(self, 'connectors', list())

        except ValueError:
            raise Exception('Can not resolve the connection.\n\nABORD')

    # =========================================================================

    # ADD COMPONENTS

    def add_storages(self, x, H):
        """
        Add storage components with state :math:`\\mathbf{x}` and energy
        :math:`\\mathrm{H}(\\mathbf{x}) \geq 0`.

        * State :math:`\\mathbf{x}` is appended to the current list of
        states symbols :code:`core.x`,
        * Expression :math:`\\mathrm{H}` is added to the current expression
        of the Hamiltonian :code:`core.H`.

        Parameters
        ----------

        x: one or several pyphs.symbols
            State symbols. Can be a single symbol or a list of symbols.

        H: sympy.Expr
            Must be a valid storage function with respect to the state
            :math:`\\mathbf{x}` with :math:`\\nabla^2\\mahtrm H(\\mathbf{x}) \\succeq 0`.
        """
        if isinstance(x, types.scalar_types):
            x = [x, ]
        elif isinstance(x, types.vector_types):
            pass
        else:
            x_types = types.scalar_types+types.vector_types
            raise TypeError('Type of x should be one of {}'.format(x_types))
        types.scalar_test(H)
        self.x += x
        self.H += H

    def add_dissipations(self, w, z):
        """
        Add dissipative components with variable :math:`\\mathbf{w}` and
        dissipative function :math:`\\mathrm{z}(\\mathbf{w})`.

        * Variable :math:`\\mathbf{w}` is appended to the current list of
        variables symbols :code:`core.w`,
        * Expression :math:`\\mathrm{z}` is appended to the current list of
        dissipative functions :code:`core.z`.

        Parameters
        ----------

        w: one or several pyphs.symbols
            Variable symbols. Can be a single symbol or a list of symbols.

        z: one or several sympy.Expr
            Must be a valid dissipative function with respect to the variable
        :math:`\\mathbf{w}` with :math:`\\nabla\\mahtrm z(\\mathbf{w}) \succeq 0`.
        """
        if isinstance(w, types.vector_types):
            types.vector_test(z)
        elif isinstance(w, types.scalar_types):
            types.scalar_test(z)
            w = [w, ]
            z = [z, ]
            w_types = types.scalar_types+types.vector_types
        else:
            text = 'Type of w and z should be one of {}'.format(w_types)
            raise TypeError(text)
        if not len(w) == len(z):
            raise TypeError('w and z should have same dimension.')
        self.w += w
        self.z += z

    def add_ports(self, u, y):
        """
        Add one or several ports with input :math:`{\\mathbf{u}}` and output
        :math:`{\\mathbf{y}}`.

        * Input :math:`\\mathbf{y}` is appended to the current list of input
        symbols :code:`core.u`,
        * ouput {\\mathbf{y}} is appended to the current list of ouputs
        :code:`core.y`.

        Parameters
        ----------

        u : one or several pyphs.symbols
            Inputs symbols. Can be a single symbol or a list of symbols.

        y : one or several sympy.Expr
            Outputs symbols. Can be a single symbol or a list of symbols.
        """
        if isinstance(u, types.vector_types):
            types.vector_test(y)
        elif isinstance(u, types.scalar_types):
            types.scalar_test(y)
            u = [u, ]
            y = [y, ]
            y_types = types.scalar_types+types.vector_types
        else:
            text = 'Type of u and y should be one of {}'.format(y_types)
            raise TypeError(text)
        if not len(u) == len(y):
            raise TypeError('u and y should have same dimension.')
        self.u += u
        self.y += y

    def add_parameters(self, p):
        """
        Add one or several parameters :math:`{\\mathbf{p}}`, which is
        appended to the current list of parameters symbols :code:`core.p`.
        Also, the parameters symbols are removed from the sustitution
        dictionary.

        Parameter
        ----------

        p : one or several pyphs.symbols
            Parameters symbols. Can be a single symbol or a list of symbols.
        """
        if isinstance(p, types.vector_types):
            pass
        elif isinstance(p, types.scalar_types):
            p = [p, ]
        self.p += p

        for par in p:
            if par in self.subs:
                self.subs.pop(par)


    def add_observer(self, obs):
        """
        add_observer
        *************

        Add a dictionary of observers
        Parameter
        ---------
        obs: dict
            Observers are couple {symb: expr}. They are evaluated during
            simulation at the begining of each time step.
        """
        self.observers.update(obs)

    # =========================================================================

    # Latex

    def texwrite(self, path=None, title=None,
                 authors=None, affiliations=None):
        """
        Write the port Hamiltonian Structure to a LaTeX file.

        Parameters
        ----------

        path : str
            Path to the file to write. If file does not exist, it is create,
            else it is overwritten. If None, the file 'core.tex' is created
            into current wirking directory (default).

        title : str
            LaTeX document title. If None, it is set to 'PyPHS Core' (default).

        authors : list of str
            List of authors. Default is None.

        affiliations : list of str
            List of affiliations for authors. It must have the same length
            as authors arguments. Default is None.
        """
        if path is None:
            path = '{}.tex'.format(self.label)
        if title is None:
            title = r'PyPHS Core'
        texdocument(core2tex(self), path, title=title,
                    authors=authors, affiliations=affiliations)

    # =========================================================================

    # Printings

    def pprint(self, **settings):
        """
        Print the PHS structure :math:`\\mathbf{b} = \\mathbf{M} \\cdot \\mathbf{a}`
        using sympy's pretty printings.

        Parameters
        ----------

        settings : dic
            Parameters for sympy.pprint function.

        See Also
        --------

        sympy.pprint

        """

        sympy.init_printing()

        b = types.matrix_types[0](self.dx() +
                                  self.w +
                                  self.y +
                                  self.cy)

        a = types.matrix_types[0](self.g() +
                                  self.z_symbols() +
                                  self.u +
                                  self.cu)

        sympy.pprint([b, self.M, a], **settings)

    # =========================================================================
    # Evaluation
    def to_evaluation(self, names='all', vectorize=True):
        """
        Return an object with all the numerical function associated with all
        or a selected set of symbolic functions from a given pyphs.Core.

        Notice this is not a dynamical object, so it has to be rebuild if the
        original core object is changed in any way.

        Parameters
        ----------

        names : list of strings or 'all' (optional)
            List of core's arguments names associated with the functions that
            will be lambdified. If 'all', the names for every arguments,
            every functions (including all systems matrices and sub-matrices),
            and every operations are considered (processing time increase
            quickly with original core's complexity).

        vectorize : bool (optional)
            If True, every functions are vectorized with numpy.vectorize.
            The default is True.

        Output
        ------

        evaluation : pyphs.Evaluation
            An object with all the numerical function associated with all
            or a selected set of symbolic functions from a given pyphs.Core.

        """
        from pyphs.numerics.tools._evaluation import Evaluation
        return Evaluation(self, names=names, vectorize=vectorize)

    # =========================================================================

    def to_method(self, config=None):
        """
        Return the PHS numerical method associated with the PHS core for the
        specified configuration.

        Parameter
        ---------

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

        Output
        ------

        method : pyphs.Method
            The PHS numerical method associated with the PHS core for the
            specified configuration.

        """

        from pyphs import Method
        return Method(self, config=config)

    # =========================================================================

    def to_simulation(self, config=None, inits=None):
        """
        Return a simulation associated with the PHS core for the
        specified configuration.

        Parameter
        ---------

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

        Output
        ------

        simulation : pyphs.Simulation
            The simulation associated with the PHS core for the
            specified configuration.

        """

        from pyphs import Method
        from pyphs.config import CONFIG_METHOD
        config_method = CONFIG_METHOD.copy()
        if config is None:
            config = {}
        for k in CONFIG_METHOD.keys():
            if k in config.keys():
                config_method.update({k: config[k]})
        method = Method(self, config=config_method)
        return method.to_simulation(config=config, inits=inits)

    # =========================================================================

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

    def _struc_build_get_mat(self, mat, name):
        """
        Add an accessor to a given matrix.

        Parameters
        ----------

        mat : ('matr', ('m', 'n'))
            with matr the matrix argument to define and 'x' and 'y' the
            variables that corresponds to block of core.name
        """
        return self._build_get_mat(mat, name)

    def _struc_build_set_mat(self, mat, name):
        """
        Add an accessor to a given matrix.

        Parameters
        ----------

        mat : ('matr', ('m', 'n'))
            with matr the matrix argument to define and 'x' and 'y' the
            variables that corresponds to block of core.name
        """
        return self._build_set_mat(mat, name)

    def _build_get_mat(self, dims_names, name):
        """
        mat is ('matrix, ('m', 'n')) with matrix the matrix argument to define
        and 'x' and 'y' the variables that corresponds to blocks of core.name
        """

        def get_mat():
            namei, namej = dims_names
            debi, endi = getattr(self.inds, namei)()
            debj, endj = getattr(self.inds, namej)()
            return geteval(self, name)[debi:endi, debj:endj]
        get_mat.__doc__ = """
        =====
        {0}{1}{2}
        =====
        Accessor to the submatrix :code:`core.{0}{1}{2}` with shape
        :code:`[core.dims.{1}(), core.dims.{2}()]`.
        """.format(name, dims_names[0], dims_names[1])
        return get_mat

    def _build_set_mat(self, dims_names, name):
        """
        mat is ('matr', ('m', 'n')) with matr the matrix argument to define
        and 'x' and 'y' the variables that corresponds to block of core.name
        """
        def set_mat(mat):
            vari, varj = dims_names
            if self.M.shape[0] != self.dims.tot():
                self.M = types.matrix_types[0](sympy.zeros(self.dims.tot()))
            if name == 'J':
                Jab = types.matrix_types[0](mat)
                Rab = getattr(self, 'R'+vari + varj)()
                Rba = getattr(self, 'R'+varj + vari)()
                Mab = Jab - Rab
                Mba = -Jab.T - Rba
            if name == 'R':
                Jab = getattr(self, 'J'+vari + varj)()
                Jba = getattr(self, 'J'+varj + vari)()
                R = types.matrix_types[0](mat)
                Mab = Jab - R
                Mba = Jba - R.T
            if name == 'M':
                Mab = types.matrix_types[0](mat)
                Mba = getattr(self, 'M'+varj + vari)()
            debi, endi = getattr(self.inds, vari)()
            debj, endj = getattr(self.inds, varj)()
            self.M[debi:endi, debj:endj] = types.matrix_types[0](Mab)
            if vari != varj:
                self.M[debj:endj, debi:endi] = types.matrix_types[0](Mba)
        set_mat.__doc__ = """
        =========
        set_{0}{1}{2}
        =========
        Mutator for the submatrix :code:`core.{0}{1}{2}` with shape
        :code:`[core.dims.{1}(), core.dims.{2}()]`.

        Parameter
        ---------
        mat: matrix like
            Can be
            * a list of core.dims.{1}() lists of core.dims.{2}() elements,
            * a numpy array with shape (core.dims{1}(), core.dims{2}()),
            * a sympy Matrix with shape (core.dims{1}(), core.dims{2}()).

        Remark
        ------

        The skew-symmetry/symmetry of core.J/core.R is preserved by the
        automatic replacement of matrix core.{0}{2}{1} with the transpose of
        core.{0}{1}{2} and appropriate sign.
        """.format(name, dims_names[0], dims_names[1])

        return set_mat

    # =============================================================================

    def _gen_lnl_accessors(self, name='dxH', dim_label='x'):
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
        Linear part of core.{0}. This is a shorcut for
    :code:`core.{0}[:core.dims.{1}l()]`.

    See also
    --------
    Core.split_linear() to split the system into linear and nonlinear
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
        Nonlinear part of core.{0}. This is a shorcut for
    :code:`core.{0}[core.dims.{1}l():]`.

    See also
    --------
    Core.split_linear() to split the system into linear and nonlinear
    storage and dissipative parts.
        """.format(name, dim_label)
        return (l_accessor, nl_accessor)
    # =========================================================================

    # SYMBOLS
    @ staticmethod
    def symbols(obj, *args, **kwargs):
        """
        sympy.symbols function with Core.assertions.
        """
        kwargs.update(Core().assertions)
        return sympy.symbols(obj, *args, **kwargs)
