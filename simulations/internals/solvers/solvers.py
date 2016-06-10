# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 15:45:17 2016

@author: Falaize
"""
import numpy
from symbolics.tools import inverse, simplify
from symbolics.calculus import jacobian
import sympy as sp


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
        phs.exprs.setexpr('Q', phs.exprs.hessH[:phs.nxl, :phs.nxl])
        phs.exprs.setexpr('R', phs.exprs.jacz[:phs.nwl, :phs.nwl])

        Mx1 = J[:phs.nxl, :phs.nxl]
        Mx2 = J[:phs.nxl, phs.nxl:phs.nx()]
        Mx3 = J[:phs.nxl, phs.nx():phs.nx()+phs.nwl]
        Mx4 = J[:phs.nxl, phs.nx()+phs.nwl:phs.nx()+phs.nw()]
        Mx5 = J[:phs.nxl, phs.nx()+phs.nw():]

        Mw1 = J[phs.nx():phs.nx()+phs.nwl, :phs.nxl]
        Mw2 = J[phs.nx():phs.nx()+phs.nwl, phs.nxl:phs.nx()]
        Mw3 = J[phs.nx():phs.nx()+phs.nwl, phs.nx():phs.nx()+phs.nwl]
        Mw4 = J[phs.nx():phs.nx()+phs.nwl, phs.nx()+phs.nwl:phs.nx()+phs.nw()]
        Mw5 = J[phs.nx():phs.nx()+phs.nwl, phs.nx()+phs.nw():]

        Al = sp.Matrix.vstack(sp.Matrix.hstack(Mx1, Mx3),
                              sp.Matrix.hstack(Mw1, Mw3))
        Alx = sp.Matrix.vstack(sp.Matrix.hstack(Mx1),
                               sp.Matrix.hstack(Mw1))
        Bl = sp.Matrix.vstack(sp.Matrix.hstack(Mx2, Mx4),
                              sp.Matrix.hstack(Mw2, Mw4))
        Cl = sp.Matrix.vstack(Mx5,
                              Mw5)
        Id_coeffs = sp.diag(sp.eye(phs.nxl)*internal.fs, sp.eye(phs.nwl))
        JQR = Al*sp.diag(phs.exprs.Q/2, phs.exprs.R)
        Dl = Id_coeffs - JQR
        iDl = inverse(Dl)
        if phs.nxl + phs.nwl > 0:
            Vl1 = Alx*phs.exprs.Q*sp.Matrix(phs.symbs.x[:phs.nxl])
            if phs.nxnl + phs.nwnl > 0:
                Vl2 = Bl*sp.Matrix(phs.exprs.dxHd[phs.nxl:] +
                                   phs.exprs.z[phs.nwl:])
            else:
                Vl2 = sp.zeros(phs.nxl + phs.nwl, 1)
            if phs.ny() > 0:
                Vl3 = Cl*sp.Matrix(phs.symbs.u)
            else:
                Vl3 = sp.zeros(phs.nxl + phs.nwl, 1)
            iter_explicite = iDl*(Vl1 + Vl2 + Vl3)
            iter_explicite = simplify(list(iter_explicite))
        else:
            iter_explicite = sp.zeros(0, 0)
        phs.exprs.setexpr('iter_explicite', iter_explicite)

        # construct the non-linear implict function
        # structure
        Nx1 = J[phs.nxl:phs.nx(), :phs.nxl]
        Nx2 = J[phs.nxl:phs.nx(), phs.nxl:phs.nx()]
        Nx3 = J[phs.nxl:phs.nx(), phs.nx():phs.nx()+phs.nwl]
        Nx4 = J[phs.nxl:phs.nx(), phs.nx()+phs.nwl:phs.nx()+phs.nw()]
        Nx5 = J[phs.nxl:phs.nx(), phs.nx()+phs.nw():]

        Nw1 = J[phs.nx()+phs.nwl:phs.nx()+phs.nw(), :phs.nxl]
        Nw2 = J[phs.nx()+phs.nwl:phs.nx()+phs.nw(), phs.nxl:phs.nx()]
        Nw3 = J[phs.nx()+phs.nwl:phs.nx()+phs.nw(), phs.nx():phs.nx()+phs.nwl]
        Nw4 = J[phs.nx()+phs.nwl:phs.nx()+phs.nw(),
                phs.nx()+phs.nwl:phs.nx()+phs.nw()]
        Nw5 = J[phs.nx()+phs.nwl:phs.nx()+phs.nw(), phs.nx()+phs.nw():]

        Anl = sp.Matrix.vstack(sp.Matrix.hstack(Nx1, Nx3),
                               sp.Matrix.hstack(Nw1, Nw3))
        Bnl = sp.Matrix.vstack(sp.Matrix.hstack(Nx2, Nx4),
                               sp.Matrix.hstack(Nw2, Nw4))
        Cnl = sp.Matrix.vstack(Nx5,
                               Nw5)
        Id_coeffs = sp.diag(sp.eye(phs.nxnl)*internal.fs, sp.eye(phs.nwnl))
        if phs.nxnl + phs.nwnl > 0:
            Vnl2 = Bnl*sp.Matrix(phs.exprs.dxHd[phs.nxl:] +
                                 phs.exprs.z[phs.nwl:])
            if phs.nxl + phs.nwl > 0:
                Vnl1 = Anl*sp.Matrix(phs.exprs.dxHd[:phs.nxl] +
                                     phs.exprs.z[:phs.nwl])
                Vnl1 = Vnl1.subs(map(lambda symb, expr: (symb, expr),
                                     internal.varl_symbs,
                                     phs.exprs.iter_explicite))
            else:
                Vnl1 = sp.zeros(phs.nxnl + phs.nwnl, 1)
            if phs.ny() > 0:
                Vnl3 = Cnl*sp.Matrix(phs.symbs.u)
            else:
                Vnl3 = sp.zeros(phs.nxnl + phs.nwnl, 1)
            impfunc = Id_coeffs*sp.Matrix(internal.varnl_symbs) -\
                (Vnl1 + Vnl2 + Vnl3)
            res_impfunc = sp.sqrt((impfunc.T*impfunc)[0, 0])
            jac_impfunc = jacobian(impfunc, internal.varnl_symbs)
        else:
            # init dummy quantities
            impfunc = sp.zeros(0, 1)
            res_impfunc = sp.sympify(0)
            jac_impfunc = sp.zeros(0)
            # set solver to None
            internal.config['solver'] = None
        impfunc = impfunc
        res_impfunc = res_impfunc
        # append to list of lambdified functions
        phs.exprs.setexpr('impfunc', impfunc)
        phs.exprs.setexpr('res_impfunc', res_impfunc)
        phs.exprs.setexpr('jac_impfunc', jac_impfunc)

        if solver_name is None:
            # def update args function
            def iter_solver():
                # eval args
                return internal.varnl()
        else:
            iter_solver = getattr(self, solver_name)(internal, phs)
        internal.iter_solver = iter_solver

    def standard(self, internal, phs):
        def iter_solver():
            # eval args
            varnl = internal.varnl()
            impfunc = internal.impfunc()
            jac_impfunc = internal.jac_impfunc()
            # compute inverse jacobian
            ijac_impfunc = numpy.linalg.inv(jac_impfunc)
            # build updates for args
            v = numpy.matrix(varnl).T - ijac_impfunc * impfunc
            varnl = v.T.tolist()[0]
            internal.set_varnl(varnl)
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
