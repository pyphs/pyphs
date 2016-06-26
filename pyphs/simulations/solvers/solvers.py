# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 15:45:17 2016

@author: Falaize
"""
import numpy
import sympy as sp
from pyphs.symbolics.tools import inverse, simplify
from pyphs.symbolics.calculus import jacobian, hessian
from pyphs.misc.tools import geteval


class Solver:
    """
    lambdify and link functions for runtimes, including implicite relation \
due to nonlinear components, with its jacobian matrix. Define also the solver \
for implicite functions.
    """
    def __init__(self, internal, phs, solver_name):
        # structure
        _init_structure(phs, internal.fs)
        _init_updates(phs, internal.fs)

        iter_solver = getattr(self, solver_name)(internal, phs)
        internal.iter_solver = iter_solver

    def standard(self, internal, phs):
        def iter_solver():
            # eval args
            varsnl = internal.varsnl()
            impfunc = internal.impfunc()
            jac_impfunc = internal.jac_impfunc()
            # compute inverse jacobian
            ijac_impfunc = numpy.linalg.inv(jac_impfunc)
            # build updates for args
            v = numpy.matrix(varsnl).T - ijac_impfunc * numpy.matrix(impfunc).T
            varsnl = v.T.tolist()[0]
            internal.set_varsnl(varsnl)
        return iter_solver

    def partial(self, internal, phs):

        jac_impfunc = phs.exprs.jac_impfunc
        phs.exprs.setexpr('ijac_impfunc', inverse(jac_impfunc))

        def iter_solver():
            # eval args
            varsnl = internal.varsnl()
            impfunc = internal.impfunc()
            ijac_impfunc = internal.ijac_impfunc()
            # build updates for args
            v = numpy.matrix(varsnl).T - ijac_impfunc * numpy.matrix(impfunc).T
            varnl = v.T.tolist()[0]
            internal.set_varsnl(varnl)

        return iter_solver

    def full(self, internal, phs):
        impfunc = sp.Matrix(phs.exprs.impfunc)
        varsnl = sp.Matrix(phs.exprs.varsnl)
        jac_impfunc = phs.exprs.jac_impfunc
        ijac_impfunc = inverse(jac_impfunc)
        update_varnl = list(varsnl - ijac_impfunc * impfunc)
        attr = 'update_varnl'
        phs.exprs.setexpr(attr, update_varnl)

        # def update args function
        def iter_solver():
            # eval args
            varsnl = getattr(internal, attr)()
            internal.set_varsnl(varsnl)

        return iter_solver


def _init_structure(phs, fs):
    """
    split system in xlin, xlin, wlin and wnlin, and stores structure in exprs
    """
    # split linear and nonlinear parts
    dims_names = ['xl', 'xnl', 'wl', 'wnl', 'y']

    # get() and set() for structure matrices
    for name1 in dims_names:
        for name2 in dims_names:
            phs.struc._build_getset(phs, dims_names=dims_names)

    # linear coefficients with Hl = xl^T.Q.xl/2 and zl = R.wl
    phs.exprs.setexpr('Q', hessian(phs.exprs.H, phs.symbs.x[:phs.dims.xl]))
    phs.exprs.setexpr('R', jacobian(phs.exprs.z[:phs.dims.wl],
                                    phs.symbs.w[:phs.dims.wl]))
    iDw = sp.eye(phs.dims.wl)-phs.struc.Jwlwl()*phs.exprs.R
    phs.exprs.setexpr('iDw', iDw)
    Dw = inverse(iDw)
    phs.exprs.setexpr('Dw', Dw)

    temp_Awl = Dw*phs.struc.Jwlxl()
    temp_Bwl = Dw*phs.struc.Jwlxnl()
    temp_Cwl = Dw*phs.struc.Jwlwnl()
    temp_Dwl = Dw*phs.struc.Jwly()

    temp_Axl = phs.struc.Jxlxl() + phs.struc.Jxlwl() * phs.exprs.R * temp_Awl
    temp_Bxl = phs.struc.Jxlxnl() + phs.struc.Jxlwl() * phs.exprs.R * temp_Bwl
    temp_Cxl = phs.struc.Jxlwnl() + phs.struc.Jxlwl() * phs.exprs.R * temp_Cwl
    temp_Dxl = phs.struc.Jxly() + phs.struc.Jxlwl() * phs.exprs.R * temp_Dwl

    iDx = sp.eye(phs.dims.xl)*fs - sp.sympify(1./2.)*temp_Axl*phs.exprs.Q
    phs.exprs.setexpr('iDx', iDx)
    Dx = inverse(iDx)
    phs.exprs.setexpr('Dx', Dx)

    Axl = Dx*temp_Axl*phs.exprs.Q
    phs.exprs.setexpr('Axl', Axl)
    Bxl = Dx*temp_Bxl
    phs.exprs.setexpr('Bxl', Bxl)
    Cxl = Dx*temp_Cxl
    phs.exprs.setexpr('Cxl', Cxl)
    Dxl = Dx*temp_Dxl
    phs.exprs.setexpr('Dxl', Dxl)

    temp_A = phs.exprs.Q * (sp.eye(phs.dims.xl) + sp.sympify(1./2.)*Axl)
    temp_B = sp.sympify(1./2.)*phs.exprs.Q*Bxl
    temp_C = sp.sympify(1./2.)*phs.exprs.Q*Cxl
    temp_D = sp.sympify(1./2.)*phs.exprs.Q*Dxl

    temp_Axnl = phs.struc.Jxnlxl()+phs.struc.Jxnlwl()*phs.exprs.R*temp_Awl
    temp_Bxnl = phs.struc.Jxnlxnl()+phs.struc.Jxnlwl()*phs.exprs.R*temp_Bwl
    temp_Cxnl = phs.struc.Jxnlwnl()+phs.struc.Jxnlwl()*phs.exprs.R*temp_Cwl
    temp_Dxnl = phs.struc.Jxnly()+phs.struc.Jxnlwl()*phs.exprs.R*temp_Dwl

    Axnl = temp_Axnl*temp_A
    phs.exprs.setexpr('Axnl', Axnl)
    Bxnl = temp_Bxnl + temp_Axnl*temp_B
    phs.exprs.setexpr('Bxnl', Bxnl)
    Cxnl = temp_Cxnl + temp_Axnl*temp_C
    phs.exprs.setexpr('Cxnl', Cxnl)
    Dxnl = temp_Dxnl + temp_Axnl*temp_D
    phs.exprs.setexpr('Dxnl', Dxnl)

    temp_Awnl = phs.struc.Jwnlxl()+phs.struc.Jwnlwl()*phs.exprs.R*temp_Awl
    temp_Bwnl = phs.struc.Jwnlxnl()+phs.struc.Jwnlwl()*phs.exprs.R*temp_Bwl
    temp_Cwnl = phs.struc.Jwnlwnl()+phs.struc.Jwnlwl()*phs.exprs.R*temp_Cwl
    temp_Dwnl = phs.struc.Jwnly()+phs.struc.Jwnlwl()*phs.exprs.R*temp_Dwl

    Awnl = temp_Awnl*temp_A
    phs.exprs.setexpr('Awnl', Awnl)
    Bwnl = temp_Bwnl + temp_Awnl*temp_B
    phs.exprs.setexpr('Bwnl', Bwnl)
    Cwnl = temp_Cwnl + temp_Awnl*temp_C
    phs.exprs.setexpr('Cwnl', Cwnl)
    Dwnl = temp_Dwnl + temp_Awnl*temp_D
    phs.exprs.setexpr('Dwnl', Dwnl)

    Awl = temp_Awl*temp_A
    phs.exprs.setexpr('Awl', Awl)
    Bwl = temp_Bwl + temp_Awl*temp_B
    phs.exprs.setexpr('Bwl', Bwl)
    Cwl = temp_Cwl + temp_Awl*temp_C
    phs.exprs.setexpr('Cwl', Cwl)
    Dwl = temp_Dwl + temp_Awl*temp_D
    phs.exprs.setexpr('Dwl', Dwl)


def _build_eval(phs, name):
    """
    return expression for evaluation of update structure block with label name
    """
    if geteval(phs.dims, name) > 0:
        if phs.dims.xl > 0:
            Vxl = geteval(phs.exprs, 'A'+name) * \
                sp.Matrix(phs.symbs.x[:phs.dims.xl])
        else:
            Vxl = sp.zeros(geteval(phs.dims, name), 1)

        if phs.dims.xnl() > 0:
            Vxnl = geteval(phs.exprs, 'B'+name) * \
                sp.Matrix(phs.exprs.dxHd[phs.dims.xl:])
        else:
            Vxnl = sp.zeros(geteval(phs.dims, name), 1)

        if phs.dims.wnl() > 0:
            Vwnl = geteval(phs.exprs, 'C'+name) * \
                sp.Matrix(phs.exprs.z[phs.dims.wl:])
        else:
            Vwnl = sp.zeros(geteval(phs.dims, name), 1)

        if phs.dims.y() > 0:
            Vy = geteval(phs.exprs, 'D'+name) * \
                sp.Matrix(phs.symbs.u)
        else:
            Vy = sp.zeros(geteval(phs.dims, name), 1)

        expr = Vxl + Vxnl + Vwnl + Vy

    else:
        expr = sp.zeros(0, 0)

    return simplify(list(expr))


def _init_updates(phs, fs):
    """
    init expressions for update of internal tructure
    """

    expr_dxl = _build_eval(phs, 'xl')
    phs.exprs.setexpr('dxl', expr_dxl)
    expr_wl = _build_eval(phs, 'wl')
    phs.exprs.setexpr('wl', expr_wl)
    expr_varsl = expr_dxl + expr_wl
    phs.exprs.setexpr('varsl', list(phs.symbs.dx()[:phs.dims.xl]) +
                      list(phs.symbs.w[:phs.dims.wl]))
    phs.exprs.setexpr('eval_varsl', expr_varsl)

    expr_dxnl = _build_eval(phs, 'xnl')
    phs.exprs.setexpr('dxnl', expr_dxnl)
    expr_wnl = _build_eval(phs, 'wnl')
    phs.exprs.setexpr('wnl', expr_wnl)
    phs.exprs.setexpr('varsnl', list(phs.symbs.dx()[phs.dims.xl:]) +
                      list(phs.symbs.w[phs.dims.wl:]))

    if phs.dims.xnl() + phs.dims.wnl() > 0:
        mat_dxnl = sp.Matrix(phs.symbs.dx()[phs.dims.xl:])
        mat_expr_dxnl = sp.Matrix(expr_dxnl)
        expr_impfunc_dxnl = list(mat_dxnl*fs - mat_expr_dxnl)

        mat_wnl = sp.Matrix(phs.symbs.w[phs.dims.wl:])
        mat_expr_wnl = sp.Matrix(expr_wnl)
        expr_impfunc_wnl = list(mat_wnl - mat_expr_wnl)

        impfunc = expr_impfunc_dxnl + expr_impfunc_wnl
        mat_impfunc = sp.Matrix(impfunc)
        res_impfunc = sp.sqrt((mat_impfunc.T*mat_impfunc)[0, 0])
        jac_impfunc = jacobian(impfunc, list(phs.symbs.dx()[phs.dims.xl:]) +
                               list(phs.symbs.w[phs.dims.wl:]))
    else:
        # init dummy quantities
        impfunc = sp.zeros(0, 1)
        res_impfunc = sp.sympify(0)
        jac_impfunc = sp.zeros(0)

    impfunc = impfunc
    res_impfunc = res_impfunc
    # append to list of lambdified functions
    phs.exprs.setexpr('impfunc', impfunc)
    phs.exprs.setexpr('res_impfunc', res_impfunc)
    phs.exprs.setexpr('jac_impfunc', jac_impfunc)
