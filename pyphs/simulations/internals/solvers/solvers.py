# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 15:45:17 2016

@author: Falaize
"""
import numpy
import sympy as sp
from pyphs.symbolics.tools import inverse, simplify
from pyphs.symbolics.calculus import jacobian


class Solver:
    """
    lambdify and link functions for runtimes, including implicite relation \
due to nonlinear components, with its jacobian matrix. Define also the solver \
for implicite functions.
    """
    def __init__(self, internal, phs, solver_name):
        # structure
        J = phs.struc.J
        phs.exprs.setexpr('dtx', [el*internal.fs for el in phs.symbs.dx()])

        # linear coefficients with Hl = xl^T.Q.xl/2 and zl = R.wl
        phs.exprs.setexpr('Q', phs.exprs.hessH[:phs.dims.xl, :phs.dims.xl])
        phs.exprs.setexpr('R', phs.exprs.jacz[:phs.dims.wl, :phs.dims.wl])

        Mx1 = J[:phs.dims.xl, :phs.dims.xl]
        Mx2 = J[:phs.dims.xl, phs.dims.xl:phs.dims.x()]
        Mx3 = J[:phs.dims.xl, phs.dims.x():phs.dims.x()+phs.dims.wl]
        Mx4 = J[:phs.dims.xl,
                phs.dims.x()+phs.dims.wl:phs.dims.x()+phs.dims.w()]
        Mx5 = J[:phs.dims.xl, phs.dims.x()+phs.dims.w():]

        Mw1 = J[phs.dims.x():phs.dims.x()+phs.dims.wl, :phs.dims.xl]
        Mw2 = J[phs.dims.x():phs.dims.x()+phs.dims.wl,
                phs.dims.xl:phs.dims.x()]
        Mw3 = J[phs.dims.x():phs.dims.x()+phs.dims.wl,
                phs.dims.x():phs.dims.x()+phs.dims.wl]
        Mw4 = J[phs.dims.x():phs.dims.x()+phs.dims.wl,
                phs.dims.x()+phs.dims.wl:phs.dims.x()+phs.dims.w()]
        Mw5 = J[phs.dims.x():phs.dims.x()+phs.dims.wl,
                phs.dims.x()+phs.dims.w():]

        Al = sp.Matrix.vstack(sp.Matrix.hstack(Mx1, Mx3),
                              sp.Matrix.hstack(Mw1, Mw3))
        Alx = sp.Matrix.vstack(sp.Matrix.hstack(Mx1),
                               sp.Matrix.hstack(Mw1))
        Bl = sp.Matrix.vstack(sp.Matrix.hstack(Mx2, Mx4),
                              sp.Matrix.hstack(Mw2, Mw4))
        Cl = sp.Matrix.vstack(Mx5,
                              Mw5)
        Id_coeffs = sp.diag(sp.eye(phs.dims.xl)*internal.fs,
                            sp.eye(phs.dims.wl))
        JQR = Al*sp.diag(phs.exprs.Q/2, phs.exprs.R)
        Dl = Id_coeffs - JQR
        iDl = inverse(Dl)
        if phs.dims.xl + phs.dims.wl > 0:
            Vl1 = Alx*phs.exprs.Q*sp.Matrix(phs.symbs.x[:phs.dims.xl])
            if phs.dims.xnl() + phs.dims.wnl() > 0:
                Vl2 = Bl*sp.Matrix(phs.exprs.dxHd[phs.dims.xl:] +
                                   phs.exprs.z[phs.dims.wl:])
            else:
                Vl2 = sp.zeros(phs.dims.xl + phs.dims.wl, 1)
            if phs.dims.y() > 0:
                Vl3 = Cl*sp.Matrix(phs.symbs.u)
            else:
                Vl3 = sp.zeros(phs.dims.xl + phs.dims.wl, 1)
            iter_explicite = iDl*(Vl1 + Vl2 + Vl3)
            iter_explicite = simplify(list(iter_explicite))
        else:
            iter_explicite = sp.zeros(0, 0)
        phs.exprs.setexpr('iter_explicite', iter_explicite)

        # construct the non-linear implict function
        # structure
        Nx1 = J[phs.dims.xl:phs.dims.x(), :phs.dims.xl]
        Nx2 = J[phs.dims.xl:phs.dims.x(), phs.dims.xl:phs.dims.x()]
        Nx3 = J[phs.dims.xl:phs.dims.x(),
                phs.dims.x():phs.dims.x()+phs.dims.wl]
        Nx4 = J[phs.dims.xl:phs.dims.x(),
                phs.dims.x()+phs.dims.wl:phs.dims.x()+phs.dims.w()]
        Nx5 = J[phs.dims.xl:phs.dims.x(), phs.dims.x()+phs.dims.w():]

        Nw1 = J[phs.dims.x()+phs.dims.wl:phs.dims.x()+phs.dims.w(),
                :phs.dims.xl]
        Nw2 = J[phs.dims.x()+phs.dims.wl:phs.dims.x()+phs.dims.w(),
                phs.dims.xl:phs.dims.x()]
        Nw3 = J[phs.dims.x()+phs.dims.wl:phs.dims.x()+phs.dims.w(),
                phs.dims.x():phs.dims.x()+phs.dims.wl]
        Nw4 = J[phs.dims.x()+phs.dims.wl:phs.dims.x()+phs.dims.w(),
                phs.dims.x()+phs.dims.wl:phs.dims.x()+phs.dims.w()]
        Nw5 = J[phs.dims.x()+phs.dims.wl:phs.dims.x()+phs.dims.w(),
                phs.dims.x()+phs.dims.w():]

        Anl = sp.Matrix.vstack(sp.Matrix.hstack(Nx1, Nx3),
                               sp.Matrix.hstack(Nw1, Nw3))
        Bnl = sp.Matrix.vstack(sp.Matrix.hstack(Nx2, Nx4),
                               sp.Matrix.hstack(Nw2, Nw4))
        Cnl = sp.Matrix.vstack(Nx5,
                               Nw5)
        Id_coeffs = sp.diag(sp.eye(phs.dims.xnl())*internal.fs,
                            sp.eye(phs.dims.wnl()))
        if phs.dims.xnl() + phs.dims.wnl() > 0:
            Vnl2 = Bnl*sp.Matrix(phs.exprs.dxHd[phs.dims.xl:] +
                                 phs.exprs.z[phs.dims.wl:])
            if phs.dims.xl + phs.dims.wl > 0:
                Vnl1 = Anl*sp.Matrix(phs.exprs.dxHd[:phs.dims.xl] +
                                     phs.exprs.z[:phs.dims.wl])
                dic_sub = {}
                for symb, expr in zip(internal.linvars_symbs,
                                      phs.exprs.iter_explicite):
                    dic_sub.update({symb: expr})
                Vnl1 = Vnl1.subs(dic_sub)
            else:
                Vnl1 = sp.zeros(phs.dims.xnl() + phs.dims.wnl(), 1)
            if phs.dims.y() > 0:
                Vnl3 = Cnl*sp.Matrix(phs.symbs.u)
            else:
                Vnl3 = sp.zeros(phs.dims.xnl + phs.dims.wnl, 1)
            impfunc = Id_coeffs*sp.Matrix(internal.nlinvars_symbs) -\
                (Vnl1 + Vnl2 + Vnl3)
            res_impfunc = sp.sqrt((impfunc.T*impfunc)[0, 0])
            jac_impfunc = jacobian(impfunc, internal.nlinvars_symbs)
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

        iter_solver = getattr(self, solver_name)(internal, phs)
        internal.iter_solver = iter_solver

    def standard(self, internal, phs):
        def iter_solver():
            # eval args
            nlinvars = internal.nlinvars()
            impfunc = internal.impfunc()
            jac_impfunc = internal.jac_impfunc()
            # compute inverse jacobian
            ijac_impfunc = numpy.linalg.inv(jac_impfunc)
            # build updates for args
            v = numpy.matrix(nlinvars).T - ijac_impfunc * impfunc
            nlinvars = v.T.tolist()[0]
            internal.set_nlinvars(nlinvars)
        return iter_solver

    def symbolic_inverse(self, internal, phs):

        jac_impfunc = phs.exprs.jac_impfunc
        phs.exprs.setexpr('ijac_impfunc', inverse(jac_impfunc))

        def iter_solver():
            # eval args
            varnl = internal.varnl()
            impfunc = internal.impfunc()
            ijac_impfunc = internal.ijac_impfunc()
            # build updates for args
            v = numpy.matrix(varnl).T - ijac_impfunc * impfunc
            varnl = v.T.tolist()[0]
            internal.set_varnl(varnl)

        return iter_solver

    def symbolic_iteration(self, internal, phs):
        impfunc = phs.impfunc
        varnl = numpy.Matrix(internal.varnl_symbs)
        jac_impfunc = phs.jac_impfunc
        ijac_impfunc = inverse(jac_impfunc)
        update_varnl = list(varnl - ijac_impfunc * impfunc)
        attr = 'update_varnl'
        phs.exprs.setexpr(attr, update_varnl)

        # def update args function
        def iter_solver():
            # eval args
            varnl = getattr(internal, attr)()
            internal.set_varnl(varnl)

        return iter_solver
