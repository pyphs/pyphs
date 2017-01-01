#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 11:13:24 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import sympy as sp
from pyphs.core.calculus import jacobian
from pyphs.core.symbs_tools import free_symbols
from pyphs.numerics.tools import find, PHSNumericalOperation
from pyphs.config import standard_simulations


class PHSNumericalMethod:
    """
    Base class for pyphs numerical methods
    """
    def __init__(self, core, config=None, args=None):

        # recover PHSNumericalOperation class
        self.operation = PHSNumericalOperation

        # set config
        self.config = standard_simulations.copy()
        if config is None:
            config = {}
        self.config.update(config)

        # set core
        self.core = core.__deepcopy__()
        self.core.split_linear(split=self.config['split'])

        # set sample rate as a symbol with subs if provided
        self.fs = self.core.symbols('_fs')
        if self.config['fs'] is None:
            self.core.add_parameters(self.fs)
        else:
            self.core.subs.update({self.fs: self.config['fs']})

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
        self.init_struc()

    def init_args(self):

        self.setarg('x', self.core.x)
        self.setarg('xl', self.core.x[:self.core.dims.xl()])

        self.setarg('dx', self.core.dx())

        self.setarg('w', self.core.w)

        self.setarg('u', self.core.u)

        self.setarg('p', self.core.p)

        self.setarg('vl',
                    self.core.dx()[:self.core.dims.xl()] +
                    self.core.w[:self.core.dims.wl()])
        self.setarg('vnl',
                    self.core.dx()[self.core.dims.xl():] +
                    self.core.w[self.core.dims.wl():])

    def init_funcs(self):

        self.setfunc('dxH', self.core.dxHd)

        self.setfunc('z', self.core.z)

        self.setfunc('y', self.core.outputd)

        self.setfunc('fnl',
                     self.core.dxHd[self.core.dims.xl():] +
                     self.core.z[self.core.dims.wl():])

        jac_fnl = jacobian(self.fnl_expr,
                           self.vnl_args)
        self.setfunc('jac_fnl', jac_fnl)

        nxnl, nwnl = self.core.dims.xnl(), self.core.dims.wnl()
        temp = sp.diag(sp.eye(nxnl)*self.fs, sp.eye(nwnl))
        self.setfunc('Inl', temp)

    def init_struc(self):

        # Build iDl
        temp1 = sp.diag(sp.eye(self.core.dims.xl())*self.fs,
                        sp.eye(self.core.dims.wl()))
        temp2_1 = sp.Matrix.hstack(self.core.Mxlxl(), self.core.Mxlwl())
        temp2_2 = sp.Matrix.hstack(self.core.Mwlxl(), self.core.Mwlwl())
        temp2 = sp.Matrix.vstack(temp2_1, temp2_2)
        tempQZl = sp.diag(self.core.Q/2., self.core.Zl)
        self.setfunc('iDl', temp1 - temp2*tempQZl)

        # Build barNlxl
        temp_1 = sp.Matrix.hstack(self.core.Mxlxl())
        temp_2 = sp.Matrix.hstack(self.core.Mwlxl())
        temp = sp.Matrix.vstack(temp_1, temp_2)
        self.setfunc('barNlxl', temp*self.core.Q)

        # Build barNlnl
        temp_1 = sp.Matrix.hstack(self.core.Mxlxnl(), self.core.Mxlwnl())
        temp_2 = sp.Matrix.hstack(self.core.Mwlxnl(), self.core.Mwlwnl())
        temp = sp.Matrix.vstack(temp_1, temp_2)
        self.setfunc('barNlnl', temp)

        # Build barNly
        temp_1 = sp.Matrix.hstack(self.core.Mxly())
        temp_2 = sp.Matrix.hstack(self.core.Mwly())
        temp = sp.Matrix.vstack(temp_1, temp_2)
        self.setfunc('barNly', temp)

        # Build barNnlnl
        temp_1 = sp.Matrix.hstack(self.core.Mxnlxnl(), self.core.Mxnlwnl())
        temp_2 = sp.Matrix.hstack(self.core.Mwnlxnl(), self.core.Mwnlwnl())
        temp = sp.Matrix.vstack(temp_1, temp_2)
        self.setfunc('barNnlnl', temp)

        # Build barNnll
        temp_1 = sp.Matrix.hstack(self.core.Mxnlxl(), self.core.Mxnlwl())
        temp_2 = sp.Matrix.hstack(self.core.Mwnlxl(), self.core.Mwnlwl())
        temp = sp.Matrix.vstack(temp_1, temp_2)
        self.setfunc('barNnll', temp*tempQZl)

        # Build barNnlxl
        temp_1 = sp.Matrix.hstack(self.core.Mxnlxl())
        temp_2 = sp.Matrix.hstack(self.core.Mwnlxl())
        temp = sp.Matrix.vstack(temp_1, temp_2)
        self.setfunc('barNnlxl', temp*self.core.Q)

        # Build barNnly
        temp_1 = sp.Matrix.hstack(self.core.Mxnly())
        temp_2 = sp.Matrix.hstack(self.core.Mwnly())
        temp = sp.Matrix.vstack(temp_1, temp_2)
        self.setfunc('barNnly', temp)

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
