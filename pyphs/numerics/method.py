#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 11:13:24 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import sympy as sp
from pyphs.core.symbs_tools import free_symbols, simplify, matvecprod
from pyphs.core.calculus import jacobian
from pyphs.core.struc_tools import geteval
from pyphs.numerics.tools import find, PHSNumericalOperation, regularize_dims
from pyphs.config import standard_simulations
from pyphs.core.discrete_calculus import (discrete_gradient, gradient_theta,
                                          gradient_trapez)


class PHSNumericalMethod:
    """
    Base class for pyphs numerical methods
    """
    def __init__(self, core, config=None, args=None):
        """
        Parameters
        -----------

        core: pyphs.PHSCore
            The core Port-Hamiltonian structure on wich the method is build.

        config: dict or None
            A dictionary of simulation parameters. If None, the standard
            pyphs.config.standard_simulations is used (default is None).

        args: list of strings or None
            A list of symbols for arguments. If None, core.args() is used (the
            default is None).

        """

        # recover PHSNumericalOperation class
        self.operation = PHSNumericalOperation

        # set config
        self.config = standard_simulations.copy()
        if config is None:
            config = {}
        self.config.update(config)

        # set core
        self.core = core.__deepcopy__()

        # set sample rate as a symbol...
        self.fs = self.core.symbols('_fs')
        # ...  with associated parameter...
        if self.config['fs'] is None:
            self.core.add_parameters(self.fs)
        # ... or subs if an object is provided
        else:
            self.core.subs.update({self.fs: self.config['fs']})
        prepare_core(self.core, self.config)

        if self.config['split']:
            self.split_linear()

        # symbols for arguments of all functions
        if args is None:
            args = self.core.args()
        setattr(self, 'args', args)

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
        mats = (self.core.jacF(), )*2
        criterion = zip(mats, args)
        self.core.split_linear(criterion=criterion)


def prepare_core(core, config):
    subs_theta = {}
    subs_trapez = {}
    for i, (xi, dxi) in enumerate(zip(core.x, core.dx())):
        subs_theta[xi] = xi+config['theta']*dxi
        subs_trapez[xi] = xi+dxi

    # subs the structure
    def M_theta():
        core.M = simplify(core.M.subs(subs_theta))

    def M_trapez():
        core.M = simplify((core.M + core.M.subs(subs_trapez))/2)

    def z_theta():
        for i, z in enumerate(core.z):
            core.z[i] = z.subs(subs_theta)

    def z_trapez():
        for i, z in enumerate(core.z):
            core.z[i] = (z + z.subs(subs_trapez))/2

    # build discrete evaluation of the gradient
    if config['gradient'] == 'discret':
        dxHl = list(sp.Matrix(core.Q)*(sp.Matrix(core.xl()) + 0.5*sp.Matrix(core.dxl())))
        dxHnl = discrete_gradient(core.H, core.xnl(), core.dxnl(),
                                  config['numtol'])
        core._dxH = dxHl + dxHnl
        M_theta()
        z_theta()
    elif config['gradient'] == 'theta':
        core._dxH = gradient_theta(core.H,
                                   core.x,
                                   core.dx(),
                                   config['theta'])
        M_theta()
        z_theta()
    else:
        assert config['gradient'] == 'trapez', 'Unknown method for \
gradient evaluation: {}'.format(config['gradient'])
        core._dxH = gradient_trapez(core.H, core.x, core.dx())
        M_trapez()
        z_trapez()

    core.setexpr('dxH', core.dxH)

    set_structure(core, config)


def set_structure(core, config):

    setattr(core, 'QZl', lambda: sp.diag(core.Q/2., core.Zl))

    def I(n1):
        dimx, dimw = (getattr(core.dims, 'x'+n1)(),
                      getattr(core.dims, 'w'+n1)())
        return sp.diag(sp.eye(dimx)*config['fs'], sp.eye(dimw))
    setattr(core, 'I', I)

    def func_generator_Mv(n1, n2):
        def func():
            temp_1 = sp.Matrix.hstack(getattr(core, 'Mx'+n1+'x'+n2)(),
                                      getattr(core, 'Mx'+n1+'w'+n2)())
            temp_2 = sp.Matrix.hstack(getattr(core, 'Mw'+n1+'x'+n2)(),
                                      getattr(core, 'Mw'+n1+'w'+n2)())
            return sp.Matrix.vstack(temp_1, temp_2)
        return func

    def func_generator_y(n1):
        def func():
            temp_1 = sp.Matrix.hstack(getattr(core, 'Mx'+n1+'y')(),)
            temp_2 = sp.Matrix.hstack(getattr(core, 'Mw'+n1+'y')(),)
            return sp.Matrix.vstack(temp_1, temp_2)
        return func

    def func_generator_v(n1):
        def func():
            output = geteval(core, 'dx'+n1)+geteval(core, 'w'+n1)
            return output
        return func

    def func_generator_f(n1):
        def func():
            output = geteval(core, 'dxH'+n1)+geteval(core, 'z'+n1)
            return output
        return func

    def func_generator_F(n1):

        def func():
            temp = sp.zeros(len(geteval(core, 'v'+n1)), 1)
            v = geteval(core, 'v'+n1)
            Mvvl = geteval(core, 'Mv'+n1+'vl')
            Mvvnl = geteval(core, 'Mv'+n1+'vnl')
            Mvy = geteval(core, 'Mv'+n1+'y')
            temp += matvecprod(core.I(n1), sp.Matrix(v))
            temp -= matvecprod(Mvvl, sp.Matrix(core.fl()))
            temp -= matvecprod(Mvvnl, sp.Matrix(core.fnl()))
            temp -= matvecprod(Mvy, sp.Matrix(core.u))
            return list(temp)

        def func2():
            temp = sp.zeros(len(geteval(core, 'v')), 1)
            v = geteval(core, 'v')
            Mvv = geteval(core, 'Mvv')
            Mvy = geteval(core, 'Mvy')
            temp += matvecprod(core.I(''), sp.Matrix(v))
            temp -= matvecprod(Mvv, sp.Matrix(core.f()))
            temp -= matvecprod(Mvy, sp.Matrix(core.u))
            return list(temp)

        if n1 == '':
            return func2

        else:
            return func

    def func_generator_jacF(n1, n2):
        def func():
            F, v = geteval(core, 'F'+n1), geteval(core, 'v'+n2)
            return jacobian(F, v)
        return func

    def func_generator_G(n1):
        def func():
            Fn1 = geteval(core, 'F'+n1)
            vl = geteval(core, 'vl')
            JacFn1l = geteval(core, 'jacF'+n1+'l',)
            return list(regularize_dims(sp.Matrix(Fn1)) -
                        matvecprod(JacFn1l, sp.Matrix(vl)))

        def func2():
            F = geteval(core, 'F')
            vl = geteval(core, 'vl')
            JacFl = jacobian(F, vl)
            return list(regularize_dims(sp.Matrix(F)) -
                        matvecprod(JacFl, sp.Matrix(vl)))
        return func2 if n1 == '' else func

    def func_generator_jacG(n1, n2):
        def func():
            G, v = geteval(core, 'G'+n1), geteval(core, 'v'+n2)
            return jacobian(G, v)
        return func

    core.setexpr('v', func_generator_v(''))
    core.setexpr('f', func_generator_f(''))
    core.setexpr('Mvv', func_generator_Mv('', ''))
    core.setexpr('Mvy', func_generator_y(''))
    core.setexpr('F', func_generator_F(''))
    core.setexpr('G', func_generator_G(''))
    core.setexpr('jacF', func_generator_jacF('', ''))

    for n1 in ('l', 'nl'):
        core.setexpr('v'+n1, func_generator_v(n1))
        core.setexpr('f'+n1, func_generator_f(n1))
        core.setexpr('Mv'+n1+'y', func_generator_y(n1))
        core.setexpr('F'+n1, func_generator_F(n1))
        core.setexpr('G'+n1, func_generator_G(n1))
        for n2 in ('l', 'nl'):
            core.setexpr('Mv'+n1+'v'+n2, func_generator_Mv(n1, n2))
            core.setexpr('jacF'+n1+n2, func_generator_jacF(n1, n2))
            core.setexpr('jacG'+n1+n2, func_generator_jacG(n1, n2))

def set_execactions(method):

    #######################################
    method.setoperation('ud_x', method.operation('add', ('x', 'dx')))

    if method.core.dims.l() > 0:
        ijacFll = method.operation('inv', ('jacFll', ))
        temp = method.operation('dot', (-1., 'Gl'))
        ud_vl = method.operation('dot', ('ijacFll', temp))
    else:
        ijacFll = method.operation('copy', ('jacFll', ))
        ud_vl = method.operation('copy', ('Fl', ))

    method.setoperation('ijacFll', ijacFll)
    method.setoperation('ud_vl', ud_vl)

    # save_impfunc
    method.setoperation('save_Fnl', method.operation('copy', ('Fnl', )))

    if method.core.dims.nl() > 0 and method.core.dims.l() > 0:
        temp1 = method.operation('dot', (-1, 'Gl'))
        temp2 = method.operation('dot', ('ijacFll', temp1))
        temp3 = method.operation('dot', ('jacFnll', temp2))
        ud_Fnl = method.operation('add', ('Gnl', temp3))

        temp1 = method.operation('dot', (-1, 'jacGlnl'))
        temp2 = method.operation('dot', ('ijacFll', temp1))
        temp3 = method.operation('dot', ('jacFnll', temp2))
        jacFnl = method.operation('add', ('jacGnlnl', temp3))
        ijacFnl = method.operation('inv', ('jacFnl', ))

    elif method.core.dims.nl() > 0:
        ud_Fnl = method.operation('copy', ('Gnl', ))
        jacFnl = method.operation('copy', ('jacGnlnl', ))
        ijacFnl = method.operation('inv', ('jacFnl', ))

    else:
        ud_Fnl = method.operation('copy', ('Fnl', ))
        jacFnl = method.operation('copy', ('Fnl', ))
        ijacFnl = method.operation('copy', ('Fnl', ))

    method.setoperation('ud_Fnl', ud_Fnl)
    method.setoperation('jacFnl', jacFnl)
    method.setoperation('ijacFnl', ijacFnl)

    # res_impfunc
    method.setoperation('res_Fnl', method.operation('norm', ('Fnl', )))

    #######################################
    # step_impfunc
    temp1 = method.operation('prod', (-1., 'save_Fnl'))
    temp2 = method.operation('add', ('Fnl', temp1))
    step_Fnl = method.operation('norm', (temp2, ))
    method.setoperation('step_Fnl', step_Fnl)

    #######################################
    # ud_vnl
    temp1 = method.operation('dot', ('ijacFnl', 'Fnl'))
    temp2 = method.operation('prod', (-1., temp1))
    ud_vnl = method.operation('add', ('vnl', temp2))
    method.setoperation('ud_vnl', ud_vnl)

    #######################################
    #######################################
    #######################################

    list_ = []
    list_.append(('x', 'ud_x'))
    list_.append('jacFll')
    list_.append('jacFnll')
    list_.append('ijacFll')
    list_.append('Gl')
    list_.append('Gnl')
    list_.append(('Fnl', 'ud_Fnl'))
    list_.append('res_Fnl')
    method.set_execaction(list_)

    list_iter = []
    list_iter.append('save_Fnl')
    list_iter.append('jacGlnl')
    list_iter.append('jacGnlnl')
    list_iter.append('jacFnl')
    list_iter.append('ijacFnl')
    list_iter.append(('vnl', 'ud_vnl'))
    list_iter.append('Gl')
    list_iter.append('Gnl')
    list_iter.append(('Fnl', 'ud_Fnl'))
    list_iter.append('res_Fnl')
    list_iter.append('step_Fnl')
    method.set_iteraction(list_iter,
                          'res_Fnl',
                          'step_Fnl')

    list_ = []
    list_.append(('vl', 'ud_vl'))
    list_.append('dxH')
    list_.append('z')
    list_.append('y')
    method.set_execaction(list_)
