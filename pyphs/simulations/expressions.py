# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 18:15:12 2016

@author: Falaize
"""

import sympy as sp
from pyphs.symbolics.calculus import jacobian


def regularize_dims(vec):
    """
    return column vector of zeros if vec has no shape along 2nd dimension
    """
    if vec.shape[1] == 0:
        vec = sp.zeros(vec.shape[0], 1)
    return vec


class SimulationExpressions:
    def __init__(self, phs):

        self._names = []

        self.args = phs.symbs.args()
        self.subs = [symb for symb in phs.symbs.subs]

        self.ny = phs.dims.y()
        self.np = phs.dims.p()

        self.nsubs = len(self.subs)

        self.nx = phs.dims.x()
        self.nxl = phs.dims.xl
        self.nxnl = phs.dims.xnl()

        self.nw = phs.dims.w()
        self.nwl = phs.dims.wl
        self.nwnl = phs.dims.wnl()

        self.nargs = phs.dims.args()
        self.nl = self.nxl + self.nwl
        self.nnl = self.nxnl + self.nwnl

        self.setfunc('x', phs.symbs.x)
        self.setfunc('xl', phs.symbs.x[:self.nxl])
        self.setfunc('xnl', phs.symbs.x[self.nxl:])

        self.setfunc('dx', phs.symbs.dx())
        self.setfunc('dxl', phs.symbs.dx()[:self.nxl])
        self.setfunc('dxnl', phs.symbs.dx()[self.nxl:])

        self.setfunc('w', phs.symbs.w)
        self.setfunc('wl', phs.symbs.w[:self.nwl])
        self.setfunc('wnl', phs.symbs.w[self.nwl:])

        self.setfunc('dxH', phs.exprs.dxHd)
        self.setfunc('z', phs.exprs.z)

        self.setfunc('u', phs.symbs.u)
        self.setfunc('y', phs.exprs.yd)

        self.setfunc('p', phs.symbs.p)

        # Build iDl
        temp1 = sp.diag(sp.eye(self.nxl)*phs.simu.config['fs'],
                        sp.eye(self.nwl))
        temp2_1 = sp.Matrix.hstack(phs.struc.Mxlxl(), phs.struc.Mxlwl())
        temp2_2 = sp.Matrix.hstack(phs.struc.Mwlxl(), phs.struc.Mwlwl())
        temp2 = sp.Matrix.vstack(temp2_1, temp2_2)
        tempQZl = sp.diag(phs.exprs.Q/2, phs.exprs.Zl)
        self.setfunc('iDl', temp1 - temp2*tempQZl)

        # Build barNlxl
        temp_1 = sp.Matrix.hstack(phs.struc.Mxlxl())
        temp_2 = sp.Matrix.hstack(phs.struc.Mwlxl())
        temp = sp.Matrix.vstack(temp_1, temp_2)
        self.setfunc('barNlxl', temp*phs.exprs.Q)

        # Build barNlnl
        temp_1 = sp.Matrix.hstack(phs.struc.Mxlxnl(), phs.struc.Mxlwnl())
        temp_2 = sp.Matrix.hstack(phs.struc.Mwlxnl(), phs.struc.Mwlwnl())
        temp = sp.Matrix.vstack(temp_1, temp_2)
        self.setfunc('barNlnl', temp)

        # Build barNly
        temp_1 = sp.Matrix.hstack(phs.struc.Mxly())
        temp_2 = sp.Matrix.hstack(phs.struc.Mwly())
        temp = sp.Matrix.vstack(temp_1, temp_2)
        self.setfunc('barNly', temp)

        # Build barNnlnl
        temp_1 = sp.Matrix.hstack(phs.struc.Mxnlxnl(), phs.struc.Mxnlwnl())
        temp_2 = sp.Matrix.hstack(phs.struc.Mwnlxnl(), phs.struc.Mwnlwnl())
        temp = sp.Matrix.vstack(temp_1, temp_2)
        self.setfunc('barNnlnl', temp)

        # Build barNnll
        temp_1 = sp.Matrix.hstack(phs.struc.Mxnlxl(), phs.struc.Mxnlwl())
        temp_2 = sp.Matrix.hstack(phs.struc.Mwnlxl(), phs.struc.Mwnlwl())
        temp = sp.Matrix.vstack(temp_1, temp_2)
        self.setfunc('barNnll', temp*tempQZl)

        # Build barNnlxl
        temp_1 = sp.Matrix.hstack(phs.struc.Mxnlxl())
        temp_2 = sp.Matrix.hstack(phs.struc.Mwnlxl())
        temp = sp.Matrix.vstack(temp_1, temp_2)
        self.setfunc('barNnlxl', temp*phs.exprs.Q)

        # Build barNnly
        temp_1 = sp.Matrix.hstack(phs.struc.Mxnly())
        temp_2 = sp.Matrix.hstack(phs.struc.Mwnly())
        temp = sp.Matrix.vstack(temp_1, temp_2)
        self.setfunc('barNnly', temp)

        # Build Nyl
        temp = sp.Matrix.hstack(phs.struc.Myxl(), phs.struc.Mywl())
        self.setfunc('Nyl', temp)

        # Build Nynl
        temp = sp.Matrix.hstack(phs.struc.Myxnl(), phs.struc.Mywnl())
        self.setfunc('Nynl', temp)

        # Build Nynl
        self.setfunc('Nyy', phs.struc.Myy())

        # Build vl
        self.setfunc('vl', phs.symbs.dx()[:self.nxl] + phs.symbs.w[:self.nwl])

        # Build vnl
        self.setfunc('vnl', phs.symbs.dx()[self.nxl:] +
                     phs.symbs.w[self.nwl:])

        # Build fl
        self.setfunc('fl', phs.exprs.dxHd[:self.nxl] + phs.exprs.z[:self.nwl])

        # Build fnl
        self.setfunc('fnl', phs.exprs.dxHd[self.nxl:] + phs.exprs.z[self.nwl:])

        # Build dxHl
        self.setfunc('dxHl', phs.exprs.dxHd[:self.nxl])
        # Build dxHnl
        self.setfunc('dxHnl', phs.exprs.dxHd[:self.nxl])

        # Build zl
        self.setfunc('zl', phs.exprs.z[:self.nwl])
        # Build znl
        self.setfunc('znl', phs.exprs.z[:self.nwl])

        # Build fnl
        self.setfunc('fnl', phs.exprs.dxHd[self.nxl:] + phs.exprs.z[self.nwl:])

        # Build jac_fnl
        jac_fnl = jacobian(self.fnl_expr,
                           self.vnl_args)
        self.setfunc('jac_fnl', jac_fnl)

        nxnl, nwnl = phs.dims.xnl(), phs.dims.wnl()
        temp = sp.diag(sp.eye(nxnl)*phs.simu.config['fs'], sp.eye(nwnl))
        self.setfunc('Inl', temp)

        from pyphs.misc.timer import timeout
        from pyphs.symbolics.tools import inverse
        Dl, success = timeout(inverse, self.iDl_expr, dur=60)
        self.presolve = success
        if self.presolve:
            self.setfunc('Dl', Dl)
            self.build_presolve()

    def build_presolve(self):
        print '*** Resolution of linear subsystem succeed ***'
        for name in ['xl', 'nl', 'y']:
            temp = self.Dl_expr * getattr(self, 'barNl'+name+'_expr')
            self.setfunc('Nl'+name, temp)
            temp1 = getattr(self, 'barNnl'+name+'_expr')
            temp2 = getattr(self, 'Nl'+name+'_expr')
            temp = temp1 + getattr(self, 'barNnll'+'_expr')*temp2
            self.setfunc('Nnl'+name, temp)

        temp1 = self.Nnlxl_expr*sp.Matrix(self.xl_expr)
        temp2 = self.Nnly_expr*sp.Matrix(self.u_expr)
        self.setfunc('c', regularize_dims(temp1) + regularize_dims(temp2))

        temp1 = self.Inl_expr*sp.Matrix(self.vnl_expr)
        temp2 = -self.Nnlnl_expr*sp.Matrix(self.fnl_expr)
        temp3 = -sp.Matrix(self.c_expr)
        self.setfunc('impfunc',
                     regularize_dims(temp1) +
                     regularize_dims(temp2) +
                     regularize_dims(temp3))
        temp = sp.sqrt((self.impfunc_expr.T*self.impfunc_expr)[0, 0])
        self.setfunc('res_impfunc', temp)

        self.setfunc('jac_impfunc', jacobian(self.impfunc_expr,
                                             self.vnl_expr))

        temp1 = sp.Matrix(self.vnl_expr)
        temp2 = self.jac_impfunc_expr
        temp3 = self.impfunc_expr
        self.setfunc('update_nlin',
                     regularize_dims(temp1) +
                     regularize_dims(temp2*temp3))

        temp1 = self.Nlxl_expr*sp.Matrix(self.xl_expr)
        temp2 = self.Nlnl_expr*sp.Matrix(self.fnl_expr)
        temp3 = self.Nly_expr*sp.Matrix(self.u_expr)
        self.setfunc('update_lin',
                     regularize_dims(temp1) +
                     regularize_dims(temp2) +
                     regularize_dims(temp3))

    def get(self, name):
        "Return expression, arguments, indices and substitutions"
        expr = getattr(self, name + '_expr')
        args = getattr(self, name + '_args')
        inds = getattr(self, name + '_inds')
        subs = getattr(self, name + '_subs')
        return expr, args, inds, subs

    def setfunc(self, name, expr):
        from pyphs.symbolics.tools import free_symbols
        from pyphs.numerics.tools import find
        symbs = free_symbols(expr)
        args, inds = find(symbs, self.args)
        subs = symbs.difference(set(args))
        setattr(self, name+'_expr', expr)
        setattr(self, name+'_args', args)
        setattr(self, name+'_inds', inds)
        setattr(self, name+'_subs', subs)
        self._names.append(name)
