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
from pyphs.config import standard_numerics


class PHSNumericalMethod:
    """
    Base class for pyphs numerical methods
    """
    def __init__(self, core, **config):

        # init config with standard configuration options
        self.config = standard_numerics.copy()

        # update with provided config
        self.config.update(config)

        # list of the method expressions names
        self.exprs_names = []

        # symbols for arguments of all functions
        self.args = core.args()

        # symbols for substitutions in all functions
        self.subs = core.subs

        self.update = []

        self.ny = core.dims.y()
        self.np = core.dims.p()

        self.nsubs = len(self.subs)

        self.nx = core.dims.x()
        self.nxl = core.dims.xl()
        self.nxnl = core.dims.xnl()

        self.nw = core.dims.w()
        self.nwl = core.dims.wl()
        self.nwnl = core.dims.wnl()

        self.nargs = core.dims.args()
        self.nl = self.nxl + self.nwl
        self.nnl = self.nxnl + self.nwnl

        self.setfunc('x', core.x)
        self.setfunc('xl', core.x[:self.nxl])
        self.setfunc('xnl', core.x[self.nxl:])

        self.setfunc('dx', core.dx())
        self.setfunc('dxl', core.dx()[:self.nxl])
        self.setfunc('dxnl', core.dx()[self.nxl:])

        self.setfunc('w', core.w)
        self.setfunc('wl', core.w[:self.nwl])
        self.setfunc('wnl', core.w[self.nwl:])

        self.setfunc('dxH', core.dxHd)
        self.setfunc('z', core.z)

        self.setfunc('u', core.u)
        self.setfunc('y', core.outputd)

        self.setfunc('p', core.p)

        self.setfunc('M', core.M)

        # Build iDl
        temp1 = sp.diag(sp.eye(self.nxl)*self.config['fs'],
                        sp.eye(self.nwl))
        temp2_1 = sp.Matrix.hstack(core.Mxlxl(), core.Mxlwl())
        temp2_2 = sp.Matrix.hstack(core.Mwlxl(), core.Mwlwl())
        temp2 = sp.Matrix.vstack(temp2_1, temp2_2)
        tempQZl = sp.diag(core.Q/2, core.Zl)
        self.setfunc('iDl', temp1 - temp2*tempQZl)

        # Build barNlxl
        temp_1 = sp.Matrix.hstack(core.Mxlxl())
        temp_2 = sp.Matrix.hstack(core.Mwlxl())
        temp = sp.Matrix.vstack(temp_1, temp_2)
        self.setfunc('barNlxl', temp*core.Q)

        # Build barNlnl
        temp_1 = sp.Matrix.hstack(core.Mxlxnl(), core.Mxlwnl())
        temp_2 = sp.Matrix.hstack(core.Mwlxnl(), core.Mwlwnl())
        temp = sp.Matrix.vstack(temp_1, temp_2)
        self.setfunc('barNlnl', temp)

        # Build barNly
        temp_1 = sp.Matrix.hstack(core.Mxly())
        temp_2 = sp.Matrix.hstack(core.Mwly())
        temp = sp.Matrix.vstack(temp_1, temp_2)
        self.setfunc('barNly', temp)

        # Build barNnlnl
        temp_1 = sp.Matrix.hstack(core.Mxnlxnl(), core.Mxnlwnl())
        temp_2 = sp.Matrix.hstack(core.Mwnlxnl(), core.Mwnlwnl())
        temp = sp.Matrix.vstack(temp_1, temp_2)
        self.setfunc('barNnlnl', temp)

        # Build barNnll
        temp_1 = sp.Matrix.hstack(core.Mxnlxl(), core.Mxnlwl())
        temp_2 = sp.Matrix.hstack(core.Mwnlxl(), core.Mwnlwl())
        temp = sp.Matrix.vstack(temp_1, temp_2)
        self.setfunc('barNnll', temp*tempQZl)

        # Build barNnlxl
        temp_1 = sp.Matrix.hstack(core.Mxnlxl())
        temp_2 = sp.Matrix.hstack(core.Mwnlxl())
        temp = sp.Matrix.vstack(temp_1, temp_2)
        self.setfunc('barNnlxl', temp*core.Q)

        # Build barNnly
        temp_1 = sp.Matrix.hstack(core.Mxnly())
        temp_2 = sp.Matrix.hstack(core.Mwnly())
        temp = sp.Matrix.vstack(temp_1, temp_2)
        self.setfunc('barNnly', temp)

        # Build Nyl
        temp = sp.Matrix.hstack(core.Myxl(), core.Mywl())
        self.setfunc('Nyl', temp)

        # Build Nynl
        temp = sp.Matrix.hstack(core.Myxnl(), core.Mywnl())
        self.setfunc('Nynl', temp)

        # Build Nynl
        self.setfunc('Nyy', core.Myy())

        # Build vl
        self.setfunc('vl', core.dx()[:self.nxl] + core.w[:self.nwl])

        # Build vnl
        self.setfunc('vnl', core.dx()[self.nxl:] +
                     core.w[self.nwl:])

        # Build fl
        self.setfunc('fl', core.dxHd[:self.nxl] + core.z[:self.nwl])

        # Build fnl
        self.setfunc('fnl', core.dxHd[self.nxl:] + core.z[self.nwl:])

        # Build dxHl
        self.setfunc('dxHl', core.dxHd[:self.nxl])
        # Build dxHnl
        self.setfunc('dxHnl', core.dxHd[:self.nxl])

        # Build zl
        self.setfunc('zl', core.z[:self.nwl])
        # Build znl
        self.setfunc('znl', core.z[:self.nwl])

        # Build fnl
        self.setfunc('fnl', core.dxHd[self.nxl:] + core.z[self.nwl:])

        # Build jac_fnl
        jac_fnl = jacobian(self.fnl_expr,
                           self.vnl_args)
        self.setfunc('jac_fnl', jac_fnl)

        nxnl, nwnl = core.dims.xnl(), core.dims.wnl()
        temp = sp.diag(sp.eye(nxnl)*self.config['fs'], sp.eye(nwnl))
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
        if isinstance(expr, PHSNumericalOperation):
            args = expr.freesymbols
            setattr(self, name+'_args', args)
        else:
            symbs = free_symbols(expr)
            args, inds = find(symbs, self.args)
            subs = symbs.difference(set(args))
            setattr(self, name+'_args', args)
            setattr(self, name+'_inds', inds)
            setattr(self, name+'_subs', subs)

    def setupdate_exec(self, list_):
        self.update += [{'exec': list_}]

    def setupdate_iter(self, list_, res_symb, step_symb):
        self.update += [{'iter': (list_, res_symb, step_symb)}]
