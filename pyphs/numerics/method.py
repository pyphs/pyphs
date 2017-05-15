#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 11:13:24 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import sympy as sp
from pyphs.core.symbs_tools import free_symbols, matvecprod, simplify
from pyphs.core.calculus import jacobian
from pyphs.core.struc_tools import geteval
from pyphs.numerics.tools import find, PHSNumericalOperation, regularize_dims
from pyphs.config import simulations
from pyphs.core.discrete_calculus import (discrete_gradient, gradient_theta,
                                          gradient_trapez)

try:
    import itertools.imap as map
except ImportError:
    pass


class PHSNumericalMethod:
    """
    Base class for pyphs numerical methods
    """

    # recover PHSNumericalOperation class
    operation = PHSNumericalOperation

    def __init__(self, core, config=None, args=None):
        """
        Parameters
        -----------

        core: pyphs.PHSCore
            The core Port-Hamiltonian structure on wich the method is build.

        config: dict or None
            A dictionary of simulation parameters. If None, the standard
            pyphs.config.simulations is used (default is None).

        args: list of strings or None
            A list of symbols for arguments. If None, core.args() is used (the
            default is None).

        """
        print('Build numerical method...')

        # set config
        self.config = simulations.copy()
        if config is None:
            config = {}
        self.config.update(config)

        # set core
        self.core = core.__deepcopy__()
        if self.config['split']:
            self.core.split_linear()

        # symbols for arguments of all functions
        if args is None:
            args = self.core.args()
        setattr(self, 'args', args)

        # set sample rate as a symbol...
        self.fs = self.core.symbols('f_s')
        # ...  with associated parameter...
        if self.config['fs'] is None:
            self.core.add_parameters(self.fs)
        # ... or subs if an object is provided
        else:
            self.core.subs.update({self.fs: self.config['fs']})

        prepare_core(self.core, self.config)

        if self.config['split']:
            self.split_linear()

        # ------------- INIT LISTS ------------- #

        # list of the method arguments names
        setattr(self, 'args_names', list())

        # list of the method expressions names
        setattr(self, 'funcs_names', list())

        # list of the method operations names
        setattr(self, 'ops_names', list())

        # list of the method update actions
        setattr(self, 'update_actions', list())

        self.init_args()
        self.init_funcs()
        set_execactions(self)

    def init_args(self):
        def names_lnl(s):
            return [s, s+'l', s+'nl']
        for n in ['x', 'dx', 'w', 'u', 'p', 'v']:
            for name in names_lnl(n):
                try:
                    arg = geteval(self.core, name)
                    self.setarg(name, arg)
                except AttributeError:
                    pass

    def init_funcs(self):
        for name in list(self.core.exprs_names):
            if not hasattr(self, name + '_expr'):
                self.setfunc(name, geteval(self.core, name))
        self.setfunc('y', geteval(self.core, 'output'))
        self.setfunc('fs', self.fs)

    def build_struc(self):
        for name in list(self.core.struc_names):
            self.setfunc(name, geteval(self.core, name))

    def get(self, name):
        "Return expression, arguments, indices, substitutions and symbol."
        expr = getattr(self, name + '_expr')
        args = getattr(self, name + '_args')
        inds = getattr(self, name + '_inds')
        return expr, args, inds

    def setarg(self, name, expr):
        symbs = free_symbols(expr)
        args, inds = find(symbs, self.args)
        setattr(self, name+'_expr', expr)
        setattr(self, name+'_args', args)
        setattr(self, name+'_inds', inds)
        self.args_names.append(name)

    def setfunc(self, name, expr):
        "set sympy expression 'expr' as the attribute 'name'."
        symbs = free_symbols(expr)
        args, inds = find(symbs, self.args)
        setattr(self, name+'_expr', expr)
        setattr(self, name+'_args', args)
        setattr(self, name+'_inds', inds)
        self.funcs_names.append(name)

    def setoperation(self, name, op):
        "set PHSNumericalOperation 'op' as the attribute 'name'."
        setattr(self, name+'_op', op)
        setattr(self, name+'_deps', op.freesymbols)
        self.ops_names.append(name)

    def set_execaction(self, list_):
        self.update_actions.append(('exec', list_))

    def set_iteraction(self, list_, res_symb, step_symb):
        self.update_actions.append(('iter', (list_, res_symb, step_symb)))

    def split_linear(self):
        args = (self.core.v(), )*2
        jacF = self.core.jactempF()
        mats = (jacF[:, :self.core.dims.x()],
                jacF[:, self.core.dims.x():])*2
        criterion = list(zip(mats, args))
        self.core.split_linear(criterion=criterion)


def prepare_core(core, config):
    """
============
prepare_core
============

Build the symbolic functions for the numerical method update.

Parameters
----------

core: PHSCore
    Original core on which the numerical method is built.

config: dic
    Dictionary of configuration parameters based on the pyphs.config.simulation
    dictionary.

Output
------
None:
    In-place definition of the numerical functions within the PHSCore
    """

    # build the discrete evaluation for the gradient
    build_gradient_evaluation(core, config)

    # define theta parameter for the function 'build_structure_evaluation'
    if config['grad'] == 'trapez':
        theta = 'trapez'
    else:
        theta = config['theta']

    # build the discrete evaluation for the structure
    build_structure_evaluation(core, theta=theta)

    # build method updates
    set_structure(core, config)


def set_getters_v(core):
    """
Append getters for vectors of unknown variables to core:
* core.v() <=> v = [dx, w],
* core.vl() <=> vl = [dxl, wl],
* core.vnl() <=> vnl = [dxnl, wnl].
    """
    def func_generator_v(suffix):
        "Getter generator"
        def func():
            "Getter"
            output = geteval(core, 'dx'+suffix)+geteval(core, 'w'+suffix)
            return output
        doc = "Getter for variable v{0} = [dx{0}, w{0}]".format(suffix)
        func.func_doc = doc
        return func

    # append getters
    for suffix in ('', 'l', 'nl'):
        core.setexpr('v'+suffix, func_generator_v(suffix))


def set_getters_f(core):
    """
Append getters for expressions 'f' to core:
* core.f() <=> v = [dxH, z],
* core.fl() <=> vl = [dxHl, zl],
* core.fnl() <=> vnl = [dxHnl, znl].
    """
    # define getter generator
    def func_generator_f(suffix):
        "Getter generator"
        def func():
            output = geteval(core, 'dxH'+suffix)+geteval(core, 'z'+suffix)
            return output
        doc = "Getter for expressions f{0} = [dxH{0}, z{0}]".format(suffix)
        func.func_doc = doc
        return func

    # append getters
    for suffix in ('', 'l', 'nl'):
        core.setexpr('f'+suffix, func_generator_f(suffix))


def set_getters_blocks_M(core):
    """
Generators of getters for block matrices:
* core.Mvv() = [[Mxx, Mxw],
                [Mwx, Mww]]
* core.Mvlvl() = [[Mxlxl, Mxlwl],
                  [Mwlxl, Mwlwl]]
* core.Mvlvnl() = [[Mxlxnl, Mxlwnl],
                   [Mwlxnl, Mwlwnl]]
* core.Mvnlvl() = [[Mxnlxl, Mxnlwl],
                   [Mwnlxl, Mwnlwl]]
* core.Mvnlvnl() = [[Mxnlxnl, Mxnlwnl],
                    [Mwnlxnl, Mwnlwnl]]
* core.Mvly() = [[Mxly],
                 [Mwly]]
* core.Mvnly() = [[Mxnly],
                  [Mwnly]]
    """
    def func_generator_Mab(a, b):
        "Getter generator"
        def func():
            temp_1 = sp.Matrix.hstack(getattr(core, 'Mx'+a+'x'+b)(),
                                      getattr(core, 'Mx'+a+'w'+b)())
            temp_2 = sp.Matrix.hstack(getattr(core, 'Mw'+a+'x'+b)(),
                                      getattr(core, 'Mw'+a+'w'+b)())
            return sp.Matrix.vstack(temp_1, temp_2)
        doc = """
Getter for block M{0}{1} = [[Mx{0}x{1}, Mx{0}w{1}],
                            [Mw{0}x{1}, Mw{0}w{1}]]
""".format(a, b)
        func.func_doc = doc
        return func

    def func_generator_My(suffix):
        "Getter generator"
        def func():
            temp_1 = sp.Matrix.hstack(getattr(core, 'Mx'+suffix+'y')(),)
            temp_2 = sp.Matrix.hstack(getattr(core, 'Mw'+suffix+'y')(),)
            return sp.Matrix.vstack(temp_1, temp_2)
        doc = """
Getter for block M{0}y = [[Mx{0}y],
                          [Mw{0}y]]
""".format(suffix)
        func.func_doc = doc
        return func

    # append getters
    core.setexpr('Mvv', func_generator_Mab('', ''))
    core.setexpr('Mvy', func_generator_My(''))
    for a in ('l', 'nl'):
        core.setexpr('Mv{}y'.format(a),
                     func_generator_My(a))
        for b in ('l', 'nl'):
            core.setexpr('Mv{0}v{1}'.format(a, b),
                         func_generator_Mab(a, b))


def set_getters_tempF(core):

    def func_generator_tempF(suffix):
        "Getter generator"
        if suffix == '':
            def func():
                temp = sp.zeros(len(geteval(core, 'v')), 1)
                v = geteval(core, 'v')
                Mvv = geteval(core, 'Mvv')
                Mvy = geteval(core, 'Mvy')
                temp += matvecprod(core.I(''), sp.Matrix(v))
                temp -= matvecprod(Mvv, sp.Matrix(core.f()))
                temp -= matvecprod(Mvy, sp.Matrix(core.u))
                return list(temp)
        else:
            def func():
                temp = sp.zeros(len(geteval(core, 'v'+suffix)), 1)
                v = geteval(core, 'v'+suffix)
                Mvvl = geteval(core, 'Mv'+suffix+'vl')
                Mvvnl = geteval(core, 'Mv'+suffix+'vnl')
                Mvy = geteval(core, 'Mv'+suffix+'y')
                temp += matvecprod(core.I(suffix), sp.Matrix(v))
                temp -= matvecprod(Mvvl, sp.Matrix(core.fl()))
                temp -= matvecprod(Mvvnl, sp.Matrix(core.fnl()))
                temp -= matvecprod(Mvy, sp.Matrix(core.u))
                return list(temp)
        doc = """
Getter for function
F{0} = [[fs*dx{0}],] - [[Mv{0}vl, Mv{0}vnl, Mv{0}y]]. [[fl],
        [w{0}]]                                        [fnl],
                                                       [u]]
""".format(suffix)
        func.func_doc = doc
        return func

    # append getters
    core.setexpr('tempF', func_generator_tempF(''))
    for suffix in ('l', 'nl'):
        core.setexpr('tempF{}'.format(suffix), func_generator_tempF(suffix))


def set_getters_Jac_tempF(core):

    def func_generator_Jac_tempF(n1, n2):
        def func():
            F, v = geteval(core, 'tempF'+n1), geteval(core, 'v'+n2)
            return jacobian(F, v)
        return func
    core.setexpr('jactempF', func_generator_Jac_tempF('', ''))
    for a in ('l', 'nl'):
        for b in ('l', 'nl'):
            core.setexpr('jactempF{0}{1}'.format(a, b),
                         func_generator_Jac_tempF(a, b))


def set_getters_G(core):
    def func_generator_G(a):
        if a == '':
            def func():
                F = geteval(core, 'tempF')
                vl = geteval(core, 'vl')
                JacFl = jacobian(F, vl)
                G = map(simplify, list(regularize_dims(sp.Matrix(F)) -
                                       matvecprod(JacFl, sp.Matrix(vl))))
                return list(G)
        else:
            def func():
                Fa = geteval(core, 'tempF'+a)
                vl = geteval(core, 'vl')
                JacFal = geteval(core, 'jactempF'+a+'l',)
                return list(regularize_dims(sp.Matrix(Fa)) -
                            matvecprod(JacFal, sp.Matrix(vl)))
        return func

    core.setexpr('G', func_generator_G(''))
    for a in ('l', 'nl'):
        core.setexpr('G{}'.format(a),
                     func_generator_G(a))


def set_getters_Jac_G(core):

    def func_generator_jacG(a, b):
        def func():
            G, v = geteval(core, 'G'+a), geteval(core, 'v'+b)
            return jacobian(G, v)
        return func

    for a in ('l', 'nl'):
        for b in ('l', 'nl'):
            core.setexpr('jacG{0}{1}'.format(a, b),
                         func_generator_jacG(a, b))


def set_getters_I(core, config):
    def I(suffix):
        dimx, dimw = (getattr(core.dims, 'x'+suffix)(),
                      getattr(core.dims, 'w'+suffix)())
        return sp.diag(sp.eye(dimx)*config['fs'], sp.eye(dimw))
    setattr(core, 'I', I)


def set_structure(core, config):
    set_getters_I(core, config)
    set_getters_v(core)
    set_getters_f(core)
    set_getters_blocks_M(core)
    set_getters_tempF(core)
    set_getters_Jac_tempF(core)
    set_getters_G(core)
    set_getters_Jac_G(core)


def set_update_x(method):
    # update the value of 'x' with the evaluation of 'ud_x'
    method.setoperation('ud_x', method.operation('add', ('x', 'dx')))
    # add execaction to the update queue
    method.preimplicit.append(('x', 'ud_x'))


def set_update_vl(method):

    ijactempFll = method.operation('inv', ('jactempFll', ))
    method.setoperation('ijactempFll', ijactempFll)

    temp = method.operation('dot', (-1., 'Gl'))
    ud_vl = method.operation('dot', ('ijactempFll', temp))

    method.setoperation('ud_vl', ud_vl)

    method.preimplicit.append(('jactempFll'))
    method.preimplicit.append(('ijactempFll'))
    method.preimplicit.append(('Gl'))

    method.postimplicit.append(('vl', 'ud_vl'))


def set_update_vnl(method):

    # Implicite function and Jacobian
    if method.core.dims.l() > 0:

        temp1 = method.operation('dot', (-1, 'Gl'))
        temp2 = method.operation('dot', ('ijactempFll', temp1))
        temp3 = method.operation('dot', ('jactempFnll', temp2))
        Fnl = method.operation('add', ('Gnl', temp3))

        temp1 = method.operation('dot', (-1, 'jacGlnl'))
        temp2 = method.operation('dot', ('ijactempFll', temp1))
        temp3 = method.operation('dot', ('jactempFnll', temp2))
        jacFnl = method.operation('add', ('jacGnlnl', temp3))

    else:

        Fnl = method.operation('copy', ('Gnl', ))

        jacFnl = method.operation('copy', ('jacGnlnl', ))

    ijacFnl = method.operation('inv', ('jacFnl', ))

    method.setoperation('Fnl', Fnl)
    method.setoperation('jacFnl', jacFnl)
    method.setoperation('ijacFnl', ijacFnl)

    # save implicit function
    method.setoperation('save_Fnl', method.operation('copy', ('Fnl', )))

    # residual
    method.setoperation('res_Fnl', method.operation('norm', ('Fnl', )))

    # progression step
    temp1 = method.operation('prod', (-1., 'save_Fnl'))
    temp2 = method.operation('add', ('Fnl', temp1))
    step_Fnl = method.operation('norm', (temp2, ))
    method.setoperation('step_Fnl', step_Fnl)

    # update vnl
    temp1 = method.operation('dot', ('ijacFnl', 'Fnl'))
    temp2 = method.operation('prod', (-1., temp1))
    ud_vnl = method.operation('add', ('vnl', temp2))
    method.setoperation('ud_vnl', ud_vnl)

    # -------- BEFORE ITERATIONS --------- #
    if method.core.dims.l() > 0:
        method.preimplicit.append(('jactempFnll'))
    method.preimplicit.append(('Gnl'))
    method.preimplicit.append('Fnl')
    method.preimplicit.append('res_Fnl')

    # -------- ITERATIONS --------- #
    method.implicit.append(('save_Fnl'))
    if method.core.dims.l() > 0:
        method.implicit.append('jacGlnl')
    method.implicit.append('jacGnlnl')
    method.implicit.append('jacFnl')
    method.implicit.append('ijacFnl')
    method.implicit.append(('vnl', 'ud_vnl'))
    if method.core.dims.l() > 0:
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

    if method.core.dims.l() > 0:
        set_update_vl(method)
    if method.core.dims.nl() > 0:
        set_update_vnl(method)

    method.postimplicit.extend(['dxH', 'z', 'y'])

    method.set_execaction(method.preimplicit)
    if method.core.dims.nl() > 0:
        method.set_iteraction(method.implicit,
                              'res_Fnl',
                              'step_Fnl')
    method.set_execaction(method.postimplicit)



def build_gradient_evaluation(core, config):
    """
Build the symbolic expression for the numerical evaluation of the gradient
associated with the PHSCore core and the chosen numerical method in the config
dictionary.
    """

    # build discrete evaluation of the gradient
    if config['grad'] == 'discret':
        # discrete gradient
        dxHl = list(sp.Matrix(core.Q)*(sp.Matrix(core.xl()) +
                    0.5*sp.Matrix(core.dxl())))
        dxHnl = discrete_gradient(core.H, core.xnl(), core.dxnl(),
                                  config['eps'])
        core._dxH = dxHl + dxHnl

    elif config['grad'] == 'theta':
        # theta scheme
        core._dxH = gradient_theta(core.H,
                                   core.x,
                                   core.dx(),
                                   config['theta'])
    else:
        assert config['grad'] == 'trapez', 'Unknown method for \
gradient evaluation: {}'.format(config['gradient'])
        # trapezoidal rule
        core._dxH = gradient_trapez(core.H, core.x, core.dx())

    # reference the discrete gradient for the PHSCore in core.exprs_names
    core.setexpr('dxH', core.dxH)


def build_structure_evaluation(core, theta=0.5):
    """
Build the substitutions of the state x associated with the PHSCore core and
the chosen value for the theta scheme.

Parameters
----------

core: PHSCore:
    Core structure on which the numerical evaluation is built.

theta: numeric in [0, 1] or 'trapez'
    If numeric, a theta scheme is used f(x) <- f(x+theta*dx). Else if theta is
    the string 'trapez', a trapezoidal rule is used f(x)<-0.5*(f(x)+f(x+dx)).

Output
------

None:
    In-place transformation of the PHSCore.
    """

    # substitutions associated with the chosen numerical method
    subs = {}

    # build substitutions associated with the gradient evaluation
    for i, (gi, gi_discret) in enumerate(zip(core.g(), core.dxH())):
        subs[gi] = gi_discret

    # if theta is a numeric => theta scheme
    if isinstance(theta, (int, float)):
        for i, (xi, dxi) in enumerate(zip(core.x, core.dx())):
            subs[xi] = xi+theta*dxi
        # Substitute symbols in core.M
        core.M = core.M.subs(subs)
        # Substitute symbols in core.z
        for i, z in enumerate(core.z):
            core.z[i] = z.subs(subs)

    # else if theta == 'trapez' => trapezoidal
    else:
        assert theta == 'trapez'
        for i, (xi, dxi) in enumerate(zip(core.x, core.dx())):
            subs[xi] = xi+dxi
        # Substitute symbols in core.M
        core.M = 0.5*(core.M + core.M.subs(subs))
        # Substitute symbols in core.z
        for i, z in enumerate(core.z):
            core.z[i] = 0.5*(z + z.subs(subs))
