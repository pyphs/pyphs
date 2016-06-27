# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 15:45:17 2016

@author: Falaize
"""
import numpy
import sympy as sp
from pyphs.symbolics.tools import inverse, simplify
from pyphs.symbolics.calculus import jacobian
from pyphs.misc.tools import geteval


class Solver:
    """
    lambdify and link functions for runtimes, including implicite relation \
due to nonlinear components, with its jacobian matrix. Define also the solver \
for implicite functions.
    """
    def __init__(self, simu):
        # structure
        _init_structure(simu.phs, simu.config['fs'])

        obj = getattr(self, simu.config['solver'])
        iter_solver = obj(simu)
        simu.iter_solver = iter_solver

    def standard(self, simu):
        def iter_solver():
            # eval args
            vnl = simu.vnl()
            impfunc = simu.impfunc()
            jac_impfunc = simu.jac_impfunc()
            # compute inverse jacobian
            ijac_impfunc = numpy.linalg.inv(jac_impfunc)
            # build updates for args
            vnl = numpy.matrix(vnl).T - numpy.dot(ijac_impfunc, impfunc)
            vnl = vnl.T.tolist()[0]
            simu.set_vnl(vnl)
        return iter_solver

    def partial(self, simu):

        jac_impfunc = simu.phs.exprs.jac_impfunc
        simu.phs.exprs.setexpr('ijac_impfunc', inverse(jac_impfunc))

        def iter_solver():
            # eval args
            varsnl = simu.varsnl()
            impfunc = simu.impfunc()
            ijac_impfunc = simu.ijac_impfunc()
            # build updates for args
            v = numpy.matrix(varsnl).T - ijac_impfunc * numpy.matrix(impfunc).T
            varnl = v.T.tolist()[0]
            simu.set_varsnl(varnl)

        return iter_solver

    def full(self, simu):
        impfunc = sp.Matrix(simu.phs.exprs.impfunc)
        varsnl = sp.Matrix(simu.phs.exprs.varsnl)
        jac_impfunc = simu.phs.exprs.jac_impfunc
        ijac_impfunc = inverse(jac_impfunc)
        update_varnl = list(varsnl - ijac_impfunc * impfunc)
        attr = 'update_varnl'
        simu.phs.exprs.setexpr(attr, update_varnl)

        # def update args function
        def iter_solver():
            # eval args
            varsnl = getattr(simu, attr)()
            simu.set_varsnl(varsnl)

        return iter_solver


def _init_structure(phs, fs):
    """
    split system in xlin, xlin, wlin and wnlin, and stores structure in exprs
    """
    phs.exprs.build()
    # split linear and nonlinear parts
    dims_names = ['xl', 'xnl', 'wl', 'wnl', 'y']

    phs.inds._set_inds(dims_names)
    # get() and set() for structure matrices
    for name1 in dims_names:
        for name2 in dims_names:
            phs.struc._build_getset(phs, dims_names=dims_names)

    nxl, nwl = phs.dims.xl, phs.dims.wl

    temp1 = sp.diag(sp.eye(nxl)*phs.simu.config['fs'], sp.eye(nwl))
    temp2_1 = sp.Matrix.hstack(phs.struc.Mxlxl(), phs.struc.Mxlwl())
    temp2_2 = sp.Matrix.hstack(phs.struc.Mwlxl(), phs.struc.Mwlwl())
    temp2 = sp.Matrix.vstack(temp2_1, temp2_2)
    tempQZl = sp.diag(phs.exprs.Q/2, phs.exprs.Zl)
    phs.exprs.setexpr('iDl', temp1 - temp2*tempQZl)

    temp_1 = sp.Matrix.hstack(phs.struc.Mxlxl())
    temp_2 = sp.Matrix.hstack(phs.struc.Mwlxl())
    temp = sp.Matrix.vstack(temp_1, temp_2)
    phs.exprs.setexpr('barNlxl', temp)

    temp_1 = sp.Matrix.hstack(phs.struc.Mxlxnl(), phs.struc.Mxlwnl())
    temp_2 = sp.Matrix.hstack(phs.struc.Mwlxnl(), phs.struc.Mwlwnl())
    temp = sp.Matrix.vstack(temp_1, temp_2)
    phs.exprs.setexpr('barNlnl', temp)

    temp_1 = sp.Matrix.hstack(phs.struc.Mxly())
    temp_2 = sp.Matrix.hstack(phs.struc.Mwly())
    temp = sp.Matrix.vstack(temp_1, temp_2)
    phs.exprs.setexpr('barNly', temp)

    temp_1 = sp.Matrix.hstack(phs.struc.Mxnlxnl(), phs.struc.Mxnlwnl())
    temp_2 = sp.Matrix.hstack(phs.struc.Mwnlxnl(), phs.struc.Mwnlwnl())
    temp = sp.Matrix.vstack(temp_1, temp_2)
    phs.exprs.setexpr('barNnlnl', temp)

    temp_1 = sp.Matrix.hstack(phs.struc.Mxnlxl(), phs.struc.Mxnlwl())
    temp_2 = sp.Matrix.hstack(phs.struc.Mwnlxl(), phs.struc.Mwnlwl())
    temp = sp.Matrix.vstack(temp_1, temp_2)
    phs.exprs.setexpr('barNnll', temp*tempQZl)

    temp_1 = sp.Matrix.hstack(phs.struc.Mxnlxl())
    temp_2 = sp.Matrix.hstack(phs.struc.Mwnlxl())
    temp = sp.Matrix.vstack(temp_1, temp_2)
    phs.exprs.setexpr('barNnlxl', temp*phs.exprs.Q)

    temp_1 = sp.Matrix.hstack(phs.struc.Mxnly())
    temp_2 = sp.Matrix.hstack(phs.struc.Mwnly())
    temp = sp.Matrix.vstack(temp_1, temp_2)
    phs.exprs.setexpr('barNnly', temp)

    phs.exprs.setexpr('vl', phs.symbs.dx()[:nxl] + phs.symbs.w[:nwl])

    phs.exprs.setexpr('vnl', phs.symbs.dx()[nxl:] + phs.symbs.w[nwl:])
    phs.exprs.setexpr('fnl', phs.exprs.dxHd[nxl:] + phs.exprs.z[nwl:])
    jac_fnl = jacobian(phs.exprs.fnl, phs.exprs.vnl)
    phs.exprs.setexpr('jac_fnl', jac_fnl)

    nxnl, nwnl = phs.dims.xnl(), phs.dims.wnl()
    temp = sp.diag(sp.eye(nxnl)*phs.simu.config['fs'], sp.eye(nwnl))
    phs.exprs.setexpr('Inl', jac_fnl)

    from pyphs.misc.timer import timeout
    from pyphs.symbolics.tools import inverse
    Dl, success = timeout(inverse, phs.exprs.iDl, dur=60)
    if success:
        phs.exprs.setexpr('Dl', Dl)
        for name in ['xl', 'nl', 'y']:
            temp = Dl * getattr(phs.exprs, 'barNl'+name)
            phs.exprs.setexpr('Nl'+name, temp)
            temp1 = getattr(phs.exprs, 'barNnl'+name)
            temp2 = getattr(phs.exprs, 'Nl'+name)
            temp = temp1 + getattr(phs.exprs, 'barNnll')*temp2
            phs.exprs.setexpr('Nnl'+name, temp)

        temp1 = phs.exprs.Nnlxl*sp.Matrix(phs.symbs.x[:phs.dims.xl])
        temp2 = phs.exprs.Nnly*sp.Matrix(phs.symbs.u)
        phs.exprs.setexpr('c',
                          regularize_dims(temp1) +
                          regularize_dims(temp2))

        temp1 = phs.exprs.Inl*sp.Matrix(phs.exprs.vnl)
        temp2 = -phs.exprs.Nnlnl*sp.Matrix(phs.exprs.fnl)
        temp3 = -sp.Matrix(phs.exprs.c)
        phs.exprs.setexpr('impfunc',
                          regularize_dims(temp1) +
                          regularize_dims(temp2) +
                          regularize_dims(temp3))
        temp = sp.sqrt((phs.exprs.impfunc.T*phs.exprs.impfunc)[0, 0])
        phs.exprs.setexpr('res_impfunc', temp)

        phs.exprs.setexpr('jac_impfunc', jacobian(phs.exprs.impfunc,
                                                  phs.exprs.vnl))

        temp1 = sp.Matrix(phs.exprs.vnl)
        temp2 = phs.exprs.jac_impfunc
        temp3 = phs.exprs.impfunc
        phs.exprs.setexpr('update_nlin',
                          regularize_dims(temp1) +
                          regularize_dims(temp2*temp3))

        temp1 = phs.exprs.Nlxl*sp.Matrix(phs.symbs.x[:phs.dims.xl])
        temp2 = phs.exprs.Nlnl*sp.Matrix(phs.exprs.fnl)
        temp3 = phs.exprs.Nly*sp.Matrix(phs.symbs.u)
        phs.exprs.setexpr('update_lin',
                          regularize_dims(temp1) +
                          regularize_dims(temp2) +
                          regularize_dims(temp3))


def regularize_dims(vec):
    """
    return column vector of zeros if vec has no shape along 2nd dimension
    """
    if vec.shape[1] == 0:
        vec = sp.zeros(vec.shape[0], 1)
    return vec
