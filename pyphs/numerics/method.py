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
    def __init__(self, core, config=None):

        self.config = standard_simulations.copy()
        if config is None:
            config = {}
        self.config.update(config)

        self.core = core.__deepcopy__()
        self.core.split_linear(split=self.config['split'])
        self.fs = self.core.symbols('_fs')
        if self.config['fs'] is None:
            self.core.add_parameters(self.fs)
        else:
            self.core.subs.update({self.fs: self.config['fs']})

        # list of the method expressions names
        self.exprs_names = []

        # symbols for arguments of all functions
        self.args = self.core.args()

        # symbols for substitutions in all functions
        self.subs = self.core.subs

        self.update = []

        self.ny = self.core.dims.y()
        self.np = self.core.dims.p()

        self.nsubs = len(self.subs)

        self.nx = self.core.dims.x()
        self.nxl = self.core.dims.xl()
        self.nxnl = self.core.dims.xnl()

        self.nw = self.core.dims.w()
        self.nwl = self.core.dims.wl()
        self.nwnl = self.core.dims.wnl()

        self.nargs = self.core.dims.args()
        self.nl = self.nxl + self.nwl
        self.nnl = self.nxnl + self.nwnl

        self.setfunc('x', self.core.x)
        self.setfunc('xl', self.core.x[:self.nxl])
        self.setfunc('xnl', self.core.x[self.nxl:])

        self.setfunc('dx', self.core.dx())
        self.setfunc('dxl', self.core.dx()[:self.nxl])
        self.setfunc('dxnl', self.core.dx()[self.nxl:])

        self.setfunc('w', self.core.w)
        self.setfunc('wl', self.core.w[:self.nwl])
        self.setfunc('wnl', self.core.w[self.nwl:])

        self.setfunc('dxH', self.core.dxHd)
        self.setfunc('z', self.core.z)

        self.setfunc('u', self.core.u)
        self.setfunc('y', self.core.outputd)

        self.setfunc('p', self.core.p)

        self.setfunc('M', self.core.M)

        # Build iDl
        temp1 = sp.diag(sp.eye(self.nxl)*self.fs,
                        sp.eye(self.nwl))
        temp2_1 = sp.Matrix.hstack(self.core.Mxlxl(), self.core.Mxlwl())
        temp2_2 = sp.Matrix.hstack(self.core.Mwlxl(), self.core.Mwlwl())
        temp2 = sp.Matrix.vstack(temp2_1, temp2_2)
        tempQZl = sp.diag(self.core.Q/2, self.core.Zl)
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

        # Build Nyl
        temp = sp.Matrix.hstack(self.core.Myxl(), self.core.Mywl())
        self.setfunc('Nyl', temp)

        # Build Nynl
        temp = sp.Matrix.hstack(self.core.Myxnl(), self.core.Mywnl())
        self.setfunc('Nynl', temp)

        # Build Nynl
        self.setfunc('Nyy', self.core.Myy())

        # Build vl
        self.setfunc('vl', self.core.dx()[:self.nxl] + self.core.w[:self.nwl])

        # Build vnl
        self.setfunc('vnl', self.core.dx()[self.nxl:] +
                     self.core.w[self.nwl:])

        # Build fl
        self.setfunc('fl', self.core.dxHd[:self.nxl] + self.core.z[:self.nwl])

        # Build fnl
        self.setfunc('fnl', self.core.dxHd[self.nxl:] + self.core.z[self.nwl:])

        # Build dxHl
        self.setfunc('dxHl', self.core.dxHd[:self.nxl])
        # Build dxHnl
        self.setfunc('dxHnl', self.core.dxHd[:self.nxl])

        # Build zl
        self.setfunc('zl', self.core.z[:self.nwl])
        # Build znl
        self.setfunc('znl', self.core.z[:self.nwl])

        # Build fnl
        self.setfunc('fnl', self.core.dxHd[self.nxl:] + self.core.z[self.nwl:])

        # Build jac_fnl
        jac_fnl = jacobian(self.fnl_expr,
                           self.vnl_args)
        self.setfunc('jac_fnl', jac_fnl)

        nxnl, nwnl = self.core.dims.xnl(), self.core.dims.wnl()
        temp = sp.diag(sp.eye(nxnl)*self.fs, sp.eye(nwnl))
        self.setfunc('Inl', temp)

    def get(self, name):
        "Return expression, arguments, indices, substitutions and symbol."
        expr = getattr(self, name + '_expr')
        args = getattr(self, name + '_args')
        inds = getattr(self, name + '_inds')
        subs = getattr(self, name + '_subs')
        symb = getattr(self, name + '_symb')
        return expr, args, inds, subs, symb

    def setfunc(self, name, expr):
        "set sympy expression 'expr' as the attribute 'name'."
        setattr(self, name+'_expr', expr)
        setattr(self, name+'_symb', sp.symbols(name))
        self.exprs_names.append(name)
        if isinstance(expr, (PHSNumericalOperation, str)):
            pass
        else:
            symbs = free_symbols(expr)
            args, inds = find(symbs, self.args)
            subs = symbs.difference(set(args))
            setattr(self, name+'_args', args)
            setattr(self, name+'_inds', inds)
            setattr(self, name+'_subs', subs)

    def setupdate_exec(self, list_):
        self.update.append(('exec', list_))

    def setupdate_iter(self, list_, res_symb, step_symb):
        self.update.append(('iter', (list_, res_symb, step_symb)))
