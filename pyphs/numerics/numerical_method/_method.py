#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 11:13:24 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import sympy as sp
from pyphs.core.maths import matvecprod, jacobian, sumvecs
from pyphs.core.tools import free_symbols, types
from pyphs.config import CONFIG_METHOD, VERBOSE, EPS_DG, FS_SYMBS
from pyphs.misc.tools import geteval, find, get_strings, remove_duplicates
from pyphs import Core
from ..cpp.method2cpp import method2cpp
from ..tools import Operation
from ._discrete_calculus import (discrete_gradient, gradient_theta,
                                 gradient_trapez)
import copy


class Method(Core):
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
        if label is None:
            label = core.label

        if VERBOSE >= 1:
            print('Build method {}...'.format(label))
        if VERBOSE >= 2:
            print('    Init Method...')

        # INIT Core object
        Core.__init__(self, label=label)

        # Save core
        self._core = core

        # Copy core content
        for name in (list(set().union(
                          core.attrstocopy,
                          core.exprs_names,
                          core.symbs_names))):
            if isinstance(name, str):
                source = core
                target = self
                attr_name = name
            else:
                source = getattr(core, name[0])
                target = getattr(self, name[0])
                attr_name = name[1]
            attr = getattr(source, attr_name)
            setattr(target, attr_name, copy.deepcopy(attr))

        # replace every expressions in subs
        self.substitute(selfexprs=True)

        # ------------- CLASSES ------------- #

        # recover Operation class
        self.Operation = Operation

        # ------------- ARGUMENTS ------------- #

        # Configuration parameters
        self.config = CONFIG_METHOD.copy()

        # update config
        if config is None:
            config = {}
        else:
            for k in config.keys():
                if not k in self.config.keys():
                    text = 'Configuration key "{0}" unknown.'.format(k)
                    raise AttributeError(text)
        self.config.update(config)

        # list of the method arguments names
        self.args_names = list()

        # list of the method expressions names
        self.funcs_names = list()

        # list of the method operations names
        self.ops_names = list()

        # list of the method update actions
        self.update_actions = list()

        # set sample rate as a symbol...
        self.fs = self.symbols(FS_SYMBS)

        if self.config['split']:
            if VERBOSE >= 2:
                print('    Split Linear/Nonlinear...')
            self.linear_nonlinear()

        if VERBOSE >= 2:
            print('    Build numerical structure...')
        # build the discrete evaluation for the gradient
        build_gradient_evaluation(self)
        # build the discrete evaluation for the structure
        build_structure_evaluation(self)
        # build method updates
        set_structure(self)

        if self.config['split']:
            if VERBOSE >= 2:
                print('    Split Implicit/Resolved...')
            # Split implicit equations from explicit equations
            self.explicit_implicit()
            if VERBOSE >= 2:
                print('    Re-Build numerical structure...')
            # build the discrete evaluation for the gradient
            build_gradient_evaluation(self)
            # build the discrete evaluation for the structure
            build_structure_evaluation(self)
            # build method updates
            set_structure(self)

        if VERBOSE >= 2:
                print('    Init update actions...')
        set_execactions(self)

        if VERBOSE >= 2:
                print('    Init arguments...')
        self.init_args()

        if VERBOSE >= 2:
                print('    Init functions...')
        self.init_funcs()

    def update_actions_deps(self):
        """
        Returns a list of update functions in :code:`update_actions` plus
        dependencies.
        """
        # recover the names of the method's update functions and operations
        names = remove_duplicates(get_strings(self.update_actions,
                                              remove=('exec', 'iter')))

        # recover the dependencies for in-place updates 'ud_...'
        for name in names:
            if name.startswith('ud_') and not name[3:] in names:
                names.append(name[3:])
        return names + ['dx', 'w', 'u', 'p']

    def args(self):
        return (self.x + self.dx() + self.w + self.u +
                self.p + self.o())

    def c(self):
        return (self.x + self.u + self.p + self.o())

    def init_args(self):
        needed = self.update_actions_deps()

        def names_lnl(s):
            return [s, s+'l', s+'nl']
        for n in ['x', 'dx', 'w', 'u', 'p', 'v', 'o']:
            for name in names_lnl(n):
                if name in needed:
                    try:
                        self.setarg(name)
                    except AttributeError:
                        pass

    def setarg(self, name):
        if VERBOSE >= 3:
            print('        Build {}'.format(name))
        expr = geteval(self, name)
        # retrieve expr symbols
        symbs = free_symbols(expr)
        # retrieve ordered symbols (args) and indices in self.args
        args, inds = find(symbs, self.args())
        setattr(self, name+'_expr', expr)
        setattr(self, name+'_args', args)
        setattr(self, name+'_inds', inds)
        self.args_names.append(name)

    def init_funcs(self):
        needed = self.update_actions_deps()
        for name in list(self.exprs_names) + list(self.struc_names):
            if name in needed:
                self.setfunc(name)
        if 'y' in needed:
            self.setfunc('y', geteval(self, 'output'))
        if 'fs' in needed:
            self.setfunc('fs', self.fs)

    def setfunc(self, name, expr=None):
        if VERBOSE >= 3:
            print('        Build {}'.format(name))
        if expr is None:
            expr = geteval(self, name)
        symbs = free_symbols(expr)
        args, inds = find(symbs, self.args())
        setattr(self, name+'_expr', expr)
        setattr(self, name+'_args', args)
        setattr(self, name+'_inds', inds)
        self.funcs_names.append(name)

    def setoperation(self, name, op):
        "set Operation 'op' as the attribute 'name'."
        setattr(self, name+'_op', op)
        setattr(self, name+'_deps', op.freesymbols)
        self.ops_names.append(name)

    def set_execaction(self, list_):
        self.update_actions.append(('exec', list_))

    def set_iteraction(self, list_, res_symb, step_symb):
        self.update_actions.append(('iter', (list_, res_symb, step_symb)))

    def explicit_implicit(self):
        v = geteval(self, 'v')
        jacF = geteval(self, 'jactempF')
        args = (v, )*2
        mats = (jacF[:, :self.dims.x()],
                jacF[:, self.dims.x():])*2
        criterion = list(zip(mats, args))
        self.linear_nonlinear(criterion=criterion)

    def to_numeric(self, inits=None, config=None):
        """
        Return a Numeric object for the evaluation of the PHS numerical method.

        Parameter
        ---------

        inits : dict or None (optional)
            Dictionary with variable name as keys and initialization values
            as value. E.g: inits = {'x': [0, 0, 1]} to initalize state x
            with dim(x) = 3, x[0] = x[1] = 0 and x[2] = 1.

        Return
        ------
        numeric : pyphs.Numeric
            Object for the numerical evaluation of the PHS numerical method.
        """
        from pyphs import Numeric
        return Numeric(self, inits=inits, config=config)

    def to_simulation(self, config=None, inits=None):
        """
        Return a Numeric object for the evaluation of the PHS numerical method.

        Parameter
        ---------

        inits : dict or None (optional)
            Dictionary with variable name as keys and initialization values
            as value. E.g: inits = {'x': [0, 0, 1]} to initalize state x
            with dim(x) = 3, x[0] = x[1] = 0 and x[2] = 1.

        Return
        ------
        numeric : pyphs.Simulation
            Object for the numerical evaluation of the PHS numerical method.
        """
        from pyphs import Simulation
        return Simulation(self, inits=inits, config=config)

def set_structure(method):
    set_getters_I(method)
    set_getters_v(method)
    set_getters_f(method)
    set_getters_blocks_M(method)
    set_getters_tempF(method)
    set_getters_Jac_tempF(method)
    set_getters_G(method)
    set_getters_Jac_G(method)


def set_getters_v(method):
    """
Append getters for vectors of unknown variables to method:
* method.v() <=> v = [dx, w],
* method.vl() <=> vl = [dxl, wl],
* method.vnl() <=> vnl = [dxnl, wnl].
    """
    def func_generator_v(suffix):
        "Getter generator"
        def func():
            "Getter"
            output = geteval(method, 'dx'+suffix)+geteval(method, 'w'+suffix)
            return output
        doc = "Getter for variable v{0} = [dx{0}, w{0}]".format(suffix)
        func.func_doc = doc
        return func

    # append getters
    for suffix in ('', 'l', 'nl'):
        setattr(method, 'v'+suffix, func_generator_v(suffix))


def set_getters_f(method):
    """
Append getters for expressions 'f' to method:
* method.f() <=> v = [dxH, z],
* method.fl() <=> vl = [dxHl, zl],
* method.fnl() <=> vnl = [dxHnl, znl].
    """
    # define getter generator
    def func_generator_f(suffix):
        "Getter generator"
        def func():
            output = geteval(method, 'dxH'+suffix)+geteval(method, 'z'+suffix)
            return output
        doc = "Getter for expressions f{0} = [dxH{0}, z{0}]".format(suffix)
        func.func_doc = doc
        return func

    # append getters
    for suffix in ('', 'l', 'nl'):
        method.setexpr('f'+suffix, func_generator_f(suffix))


def set_getters_blocks_M(method):
    """
Generators of getters for block matrices:
* method.Mvv() = [[Mxx, Mxw],
                [Mwx, Mww]]
* method.Mvlvl() = [[Mxlxl, Mxlwl],
                  [Mwlxl, Mwlwl]]
* method.Mvlvnl() = [[Mxlxnl, Mxlwnl],
                   [Mwlxnl, Mwlwnl]]
* method.Mvnlvl() = [[Mxnlxl, Mxnlwl],
                   [Mwnlxl, Mwnlwl]]
* method.Mvnlvnl() = [[Mxnlxnl, Mxnlwnl],
                    [Mwnlxnl, Mwnlwnl]]
* method.Mvly() = [[Mxly],
                 [Mwly]]
* method.Mvnly() = [[Mxnly],
                  [Mwnly]]
    """
    def func_generator_Mab(a, b):
        "Getter generator"
        def func():
            temp_1 = types.matrix_types[0].hstack(getattr(method,
                                                          'Mx'+a+'x'+b)(),
                                                  getattr(method,
                                                          'Mx'+a+'w'+b)())
            temp_2 = types.matrix_types[0].hstack(getattr(method,
                                                          'Mw'+a+'x'+b)(),
                                                  getattr(method,
                                                          'Mw'+a+'w'+b)())
            return types.matrix_types[0].vstack(temp_1, temp_2)
        doc = """
Getter for block M{0}{1} = [[Mx{0}x{1}, Mx{0}w{1}],
                            [Mw{0}x{1}, Mw{0}w{1}]]
""".format(a, b)
        func.func_doc = doc
        return func

    def func_generator_My(suffix):
        "Getter generator"
        def func():
            temp_1 = types.matrix_types[0].hstack(getattr(method, 'Mx'+suffix+'y')(),)
            temp_2 = types.matrix_types[0].hstack(getattr(method, 'Mw'+suffix+'y')(),)
            return types.matrix_types[0].vstack(temp_1, temp_2)
        doc = """
Getter for block M{0}y = [[Mx{0}y],
                          [Mw{0}y]]
""".format(suffix)
        func.func_doc = doc
        return func

    # append getters
    method.setexpr('Mvv', func_generator_Mab('', ''))
    method.setexpr('Mvy', func_generator_My(''))
    for a in ('l', 'nl'):
        method.setexpr('Mv{}y'.format(a),
                       func_generator_My(a))
        for b in ('l', 'nl'):
            method.setexpr('Mv{0}v{1}'.format(a, b),
                           func_generator_Mab(a, b))


def set_getters_tempF(method):

    def func_generator_tempF(suffix):
        "Getter generator"
        if suffix == '':
            def func():

                v = geteval(method, 'v')
                Mvv = geteval(method, 'Mvv')
                Mvy = geteval(method, 'Mvy')
                f = geteval(method, 'f')
                u = geteval(method, 'u')
                temp = [sp.sympify(0), ]*len(geteval(method, 'v'))
                temp = sumvecs(temp,
                               matvecprod(method.I(''), v),
                               [-e for e in matvecprod(Mvv, f)],
                               [-e for e in matvecprod(Mvy, u)])
                return temp
        else:
            def func():

                v = geteval(method, 'v'+suffix)
                Mvvl = geteval(method, 'Mv'+suffix+'vl')
                Mvvnl = geteval(method, 'Mv'+suffix+'vnl')
                Mvy = geteval(method, 'Mv'+suffix+'y')
                fl = geteval(method, 'fl')
                fnl = geteval(method, 'fnl')
                u = geteval(method, 'u')
                temp = [sp.sympify(0), ]*len(geteval(method, 'v'+suffix))
                temp = sumvecs(temp,
                               matvecprod(method.I(suffix), v),
                               [-e for e in matvecprod(Mvvl, fl)],
                               [-e for e in matvecprod(Mvvnl,fnl)],
                               [-e for e in matvecprod(Mvy, u)])
                return temp
        doc = """
Getter for function
F{0} = [[fs*dx{0}],] - [[Mv{0}vl, Mv{0}vnl, Mv{0}y]]. [[fl],
        [w{0}]]                                        [fnl],
                                                       [u]]
""".format(suffix)
        func.func_doc = doc
        return func

    # append getters
    method.setexpr('tempF', func_generator_tempF(''))
    for suffix in ('l', 'nl'):
        method.setexpr('tempF{}'.format(suffix), func_generator_tempF(suffix)())


def set_getters_Jac_tempF(method):

    def func_generator_Jac_tempF(n1, n2):
        def func():
            F, v = geteval(method, 'tempF'+n1), geteval(method, 'v'+n2)
            return jacobian(F, v)
        return func
    method.setexpr('jactempF', func_generator_Jac_tempF('', '')())
    for a in ('l', 'nl'):
        for b in ('l', 'nl'):
            method.setexpr('jactempF{0}{1}'.format(a, b),
                           func_generator_Jac_tempF(a, b))


def set_getters_G(method):
    def func_generator_G(a):
        if a == '':
            def func():
                F = geteval(method, 'tempF')
                vl = geteval(method, 'vl')
                JacFl = jacobian(F, vl)
                G = sumvecs(F,
                            [-e for e in matvecprod(JacFl, vl)])
                return list(G)
        else:
            def func():
                Fa = geteval(method, 'tempF'+a)
                vl = geteval(method, 'vl')
                JacFal = geteval(method, 'jactempF'+a+'l',)
                return sumvecs(Fa,
                               [-e for e in matvecprod(JacFal, vl)])
        return func

    method.setexpr('G', func_generator_G(''))
    for a in ('l', 'nl'):
        method.setexpr('G{}'.format(a),
                       func_generator_G(a))


def set_getters_Jac_G(method):

    def func_generator_jacG(a, b):
        def func():
            G, v = geteval(method, 'G'+a), geteval(method, 'v'+b)
            return jacobian(G, v)
        return func

    for a in ('l', 'nl'):
        for b in ('l', 'nl'):
            method.setexpr('jacG{0}{1}'.format(a, b),
                           func_generator_jacG(a, b))


def set_getters_I(method):
    def I(suffix):
        dimx, dimw = (getattr(method.dims, 'x'+suffix)(),
                      getattr(method.dims, 'w'+suffix)())
        out = types.matrix_types[0](sp.diag(sp.eye(dimx)*method.fs,
                                            sp.eye(dimw)))
        return types.matrix_types[0](out)
    setattr(method, 'I', I)


def set_update_x(method):
    # update the value of 'x' with the evaluation of 'ud_x'
    method.setoperation('ud_x', method.Operation('add', ('x', 'dx')))
    # add execaction to the update queue
    method.preimplicit.append(('x', 'ud_x'))


def set_update_observers(method):
    # update the value of 'o' with the evaluation of 'ud_o'
    method.setexpr('ud_o', [method.observers[k] for k in method.o()])
    # add execaction to the update queue
    method.preimplicit.append(('o', 'ud_o'))


def set_update_vl(method):

    ijactempFll = method.Operation('inv', ('jactempFll', ))
    method.setoperation('ijactempFll', ijactempFll)

    temp = method.Operation('dot', (-1., 'Gl'))
    ud_vl = method.Operation('dot', ('ijactempFll', temp))

    method.setoperation('ud_vl', ud_vl)

    method.preimplicit.append(('jactempFll'))
    method.preimplicit.append(('ijactempFll'))
    method.preimplicit.append(('Gl'))

    method.postimplicit.append(('vl', 'ud_vl'))


def set_update_vnl(method):

    # Implicite function and Jacobian
    if method.dims.l() > 0:

        temp1 = method.Operation('dot', (-1, 'Gl'))
        temp2 = method.Operation('dot', ('ijactempFll', temp1))
        temp3 = method.Operation('dot', ('jactempFnll', temp2))
        Fnl = method.Operation('add', ('Gnl', temp3))

        temp1 = method.Operation('dot', (-1, 'jacGlnl'))
        temp2 = method.Operation('dot', ('ijactempFll', temp1))
        temp3 = method.Operation('dot', ('jactempFnll', temp2))
        jacFnl = method.Operation('add', ('jacGnlnl', temp3))

    else:

        Fnl = method.Operation('copy', ('Gnl', ))

        jacFnl = method.Operation('copy', ('jacGnlnl', ))

    ijacFnl = method.Operation('inv', ('jacFnl', ))

    method.setoperation('Fnl', Fnl)
    method.setoperation('jacFnl', jacFnl)
    method.setoperation('ijacFnl', ijacFnl)

    # save implicit function
    method.setoperation('save_Fnl', method.Operation('copy', ('Fnl', )))

    # residual
    method.setoperation('res_Fnl', method.Operation('norm', ('Fnl', )))

    # progression step
    temp1 = method.Operation('prod', (-1., 'save_Fnl'))
    temp2 = method.Operation('add', ('Fnl', temp1))
    step_Fnl = method.Operation('norm', (temp2, ))
    method.setoperation('step_Fnl', step_Fnl)

    # update vnl
    temp1 = method.Operation('dot', ('ijacFnl', 'Fnl'))
    temp2 = method.Operation('prod', (-1., temp1))
    ud_vnl = method.Operation('add', ('vnl', temp2))
    method.setoperation('ud_vnl', ud_vnl)

    # -------- BEFORE ITERATIONS --------- #
    if method.dims.l() > 0:
        method.preimplicit.append(('jactempFnll'))
    method.preimplicit.append(('Gnl'))
    method.preimplicit.append('Fnl')
    method.preimplicit.append('res_Fnl')

    # -------- ITERATIONS --------- #
    method.implicit.append(('save_Fnl'))
    if method.dims.l() > 0:
        method.implicit.append('jacGlnl')
    method.implicit.append('jacGnlnl')
    method.implicit.append('jacFnl')
    method.implicit.append('ijacFnl')
    method.implicit.append(('vnl', 'ud_vnl'))
    if method.dims.l() > 0:
        method.implicit.append('Gl')
    method.implicit.append('Gnl')
    method.implicit.append('Fnl')
    method.implicit.append('res_Fnl')
    method.implicit.append('step_Fnl')


def set_execactions(method):

    #######################################

    method.preimplicit = list()
    method.implicit = list()
    method.postimplicit = list()

    set_update_x(method)
    set_update_observers(method)

    if method.dims.l() > 0:
        set_update_vl(method)
    if method.dims.nl() > 0:
        set_update_vnl(method)

    method.postimplicit.extend(['dxH', 'z', 'y'])

    method.set_execaction(method.preimplicit)
    if method.dims.nl() > 0:
        method.set_iteraction(method.implicit,
                              'res_Fnl',
                              'step_Fnl')
    method.set_execaction(method.postimplicit)


def build_gradient_evaluation(method):
    """
Build the symbolic expression for the numerical evaluation of the gradient
associated with the Core core and the chosen numerical method in the config
dictionary.
    """

    # build discrete evaluation of the gradient
    if method.config['grad'] == 'discret':
        # discrete gradient
        dxHl = list(types.matrix_types[0](method.Q)*(types.matrix_types[0](method.xl()) +
                    0.5*types.matrix_types[0](method.dxl())))
        dxHnl = discrete_gradient(method.H, method.xnl(), method.dxnl(),
                                  EPS_DG)
        method._dxH = dxHl + dxHnl

    elif method.config['grad'] == 'theta':
        # theta scheme
        method._dxH = gradient_theta(method.H,
                                     method.x,
                                     method.dx(),
                                     method.config['theta'])
    else:
        assert method.config['grad'] == 'trapez', 'Unknown method for \
gradient evaluation: {}'.format(method.config['grad'])
        # trapezoidal rule
        method._dxH = gradient_trapez(method.H, method.x, method.dx())

    # reference the discrete gradient for the Core in core.exprs_names
    method.setexpr('dxH', method.dxH)


def build_structure_evaluation(method):
    """
Build the substitutions of the state x associated with the Core core and
the chosen value for the theta scheme.

Parameters
----------

core: Core:
    Core structure on which the numerical evaluation is built.

theta: numeric in [0, 1] or 'trapez'
    If numeric, a theta scheme is used f(x) <- f(x+theta*dx). Else if theta is
    the string 'trapez', a trapezoidal rule is used f(x)<-0.5*(f(x)+f(x+dx)).

Output
------

None:
    In-place transformation of the Core.
    """

    # define theta parameter for the function 'build_structure_evaluation'
    if method.config['grad'] == 'trapez':
        theta = 'trapez'
    else:
        theta = method.config['theta']

    # substitutions associated with the chosen numerical method
    subs = {}

    # build substitutions associated with the gradient evaluation
    for i, (gi, gi_discret) in enumerate(zip(method.g(), method.dxH())):
        subs[gi] = gi_discret

    # if theta is a numeric => theta scheme
    if isinstance(theta, (int, float)):
        for i, (xi, dxi) in enumerate(zip(method.x, method.dx())):
            subs[xi] = xi+theta*dxi
        # Substitute symbols in core.M
        method.M = method.M.subs(subs)
        # Substitute symbols in core.z
        for i, z in enumerate(method.z):
            method.z[i] = z.subs(subs)

    # else if theta == 'trapez' => trapezoidal
    else:
        assert theta == 'trapez'
        for i, (xi, dxi) in enumerate(zip(method.x, method.dx())):
            subs[xi] = xi+dxi
        # Substitute symbols in core.M
        method.M = 0.5*(method.M + method.M.subs(subs))
        # Substitute symbols in core.z
        for i, z in enumerate(method.z):
            method.z[i] = 0.5*(z + z.subs(subs))
