# -*- coding: utf-8 -*-
"""
Created on Tue May 31 10:46:21 2016

@author: Falaize
"""
import sympy as sp
import numpy as np
from utils.calculus import mysimplify, mysymbolicinv
from utils.calculus import eps


def norm(lis):
    """
    return the norm of a vector given as a list
    """
    return np.sqrt(np.matrix(lis)*np.matrix(lis).T)[0, 0]


def args_ordering():
    """
    chosen ordering for the arguments of lambdified functions
    """
    ordering = 'x dx w u p'
    return ordering.split(' ')


def lambdify(args, expr):
    """
    call to lambdify with chosen options
    """
    return sp.lambdify(args, expr,
                       dummify=False,
                       modules=[{'MutableDenseMatrix': np.matrix,
                                 'ImmutableMatrix': np.matrix,
                                 'Piecewise': float},
                                'numpy'])


def get_free_symbols(phs, attr):
    obj = getattr(phs, attr)
    if isinstance(obj, list):
        symbs = set()
        for el in obj:
            assert isinstance(el, (sp.Expr, float, int))
            symbs = symbs.union(sp.sympify(el).free_symbols)
    else:
        assert isinstance(obj, (sp.Expr, sp.Matrix, sp.immutable.MatrixExpr)),\
            'got {0!s} obj {1!s} with type(obj): {2!s}'.format(attr, obj, type(obj))
        symbs = sp.sympify(obj.free_symbols)
    symbs_sort = []
    for var in args_ordering():
        for symb in getattr(phs, var):
            if symb in symbs:
                symbs_sort.append(symb)
    return symbs_sort


def self_lambdify(numerics):
    """
    lambdify all exprs of numerics
    """
    # list of variables quantities on which the lambdified functions depend
    variables = args_ordering()
    # list all variables
    symbs = []
    for name in variables:
        symb = getattr(numerics.phs, name)
        setattr(numerics, name+'_symbs', symb)
        setattr(numerics, name+'_inds',
                (len(symbs), len(symbs)+len(symb)))
        symbs += symb
    setattr(numerics, 'all_symbs', symbs)
    setattr(numerics, 'all_vals', [0, ]*len(numerics.all_symbs))

    # generators of 'get' and 'set':
    def get_generator(inds):
        def get_func():
            start, stop = inds
            return numerics.all_vals[start: stop]
        return get_func

    def set_generator(inds):
        def set_func(lis):
            start, stop = inds
            numerics.all_vals[start: stop] = lis[0: stop-start]
        return set_func

    def eval_generator(func_num_all_args):
        def eval_func():
            return func_num_all_args(*numerics.all_vals)
        return eval_func

    # get each variable in all_vals:
    for name in variables:
        inds = getattr(numerics, name+'_inds')
        setattr(numerics, name, get_generator(inds))
        setattr(numerics, 'set_'+name, set_generator(inds))

    # list all functions to lambdify
    numerics.funcs_to_lambdify = 'H dtx dxH dxHd z y Jx Jw Jy K Gx Gw J' +\
        numerics.funcs_to_lambdify
    for name in numerics.funcs_to_lambdify.split(' '):
        func_original = getattr(numerics.phs, name)
        symbs_in_func = get_free_symbols(numerics.phs, name)
        func_num_selected_args = lambdify(symbs_in_func, func_original)
        setattr(numerics.phs, name+'_num', func_num_selected_args)
        func_num_all_args = lambdify(numerics.all_symbs, func_original)
        setattr(numerics, name, eval_generator(func_num_all_args))


class numerics:
    """
    A system object that stores the current numerical state of a given phs.

    Parameters
    -----------

    phs : pypHs.pHobj

    x0 : init values for state vector

    """

    def __init__(self, phs, x0=None, fs=None, config=None):

        # init config
        if config is None:
            config = {}
        self.config = config_numerics()
        # update with provided dic
        self.config.update(config)
        # sample rate
        if fs is not None:
            assert isinstance(fs, (int, float)), 'fs should be int or float, \
                got {0!s}'.format(type(fs))
            fs = int(fs)
        else:
            fs = sp.symbols('fs', real=True)
        self.fs = fs
        self.ts = self.fs**(-1)
        # build phs if not yet
        if not hasattr(phs, 'dxH'):
            phs.build(print_latex=False)
        # copy phs in a new pHobj to subs
        from pypHs import pHobj
        temp = pHobj()
        from utils.structure import copy
        copy(phs, temp)
        # substitue symbols by values for the 'symbols' in 'phs.subs'
        temp.applySubs()
        # store phs structure
        self.phs = temp
        # build structure
        self_structure(self)
        # set build solver functions
        self_solver(self, self.config['solver'])
        # set build all numerical functions
        self_lambdify(self)
        # init value
        if x0 is None:
            x0 = [0, ]*temp.nx()
        else:
            assert isinstance(x0, list) and len(x0) == self.phs.nx()
        self.set_x(x0)

    def data_generator(self, var, ind=None, postprocess=None):
        from utils.io import data_generator
        import os
        filename = self.phs.folders['data']+os.sep+var+'.txt'
        load_options = self.config['load_options']
        generator = data_generator(filename, ind=ind, postprocess=postprocess,
                                   **load_options)
        return generator

    def update(self, u, p):
        """
        update with input 'u' and parameter 'p' on the time step (samplerate \
is numerics.fs).
        """
        # store u in numerics
        self.set_u(u)
        # store p in numerics
        self.set_p(p)
        # update state from previous iteration
        self.set_x(map(lambda e1, e2: e1 + e2, self.x(), self.dx()))
        # update nl variables (dxnl and wnl)
        self.update_nl()
        # update l variables (dxnl and wnl)
        self.update_l()

    def update_nl(self):
        # init it counter
        it = 0
        # init dx with 0
        self.set_dx([0, ]*self.phs.nx())
        # init step on iteration
        step = float('Inf')
        # init residual of implicite function
        res = float('Inf')
        # init args memory for computation of step on iteration
        old_varnl = [float('Inf'), ]*len(self.phs.varnl)
        # loop while res > tol, step > tol and it < itmax
        while res > self.config['numtol'] and step > self.config['numtol'] \
                and it < self.config['maxit']:
            # updated args
            varnl = self.iter_solver()
            self.set_dxnl(varnl[:self.phs.nxnl])
            self.set_wnl(varnl[self.phs.nxnl:])
            # eval residual
            res = self.res_impfunc()
            # eval norm step
            norm_step = norm([el1-el2 for (el1, el2) in zip(varnl, old_varnl)])
            norm_varnl = norm(varnl)+eps
            step = norm_step/(norm_varnl)
            # increment it
            it += 1
            # save args for comparison
            old_varnl = varnl

    def update_l(self):
        varl = self.iter_explicite()
        self.set_dxl(varl[:self.phs.nxl])
        self.set_wl(varl[self.phs.nxl:])


def self_structure(numerics):

    nx = numerics.phs.nx()
    nw = numerics.phs.nw()

    numerics.phs.y = numerics.phs.output
    numerics.phs.dtx = [el/numerics.ts for el in numerics.phs.dx]
    # check for split linear / non-linear, else set number of linear to 0.
    if numerics.config['split']:
        from utils.structure import split_linear
        split_linear(numerics.phs)
    elif not hasattr(numerics.phs, 'nxl'):
        numerics.phs.nxl = 0
        numerics.phs.nxnl = numerics.phs.nx()
        numerics.phs.nwl = 0
        numerics.phs.nwnl = numerics.phs.nw()

    # init list of functions to lambdify
    funcs_to_lambdify = ""

    # construct the linear update
    # variables
    nxl = numerics.phs.nxl
    nwl = numerics.phs.nwl
    dxl = numerics.phs.dx[:nxl]
    wl = numerics.phs.w[:nwl]
    numerics.phs.varl = dxl + wl
    funcs_to_lambdify += ' ' + 'varl'

    # set functions for linear parts
    def set_xl(lis):
        numerics.all_vals[0:nxl] = lis[0:nxl]
    setattr(numerics, 'set_xl', set_xl)

    def set_dxl(lis):
        numerics.all_vals[nx:nx+nxl] = lis[0:nxl]
    setattr(numerics, 'set_dxl', set_dxl)

    def set_wl(lis):
        numerics.all_vals[2*nx:2*nx+nwl] = lis[0:nwl]
    setattr(numerics, 'set_wl', set_wl)

    # linear coefficients with Hl = xl^T.Q.xl/2 and zl = R.wl
    numerics.phs.Q = numerics.phs.hess[:nxl, :nxl]
    numerics.phs.R = numerics.phs.Jacz[:nwl, :nwl]
    funcs_to_lambdify += ' ' + 'Q'
    funcs_to_lambdify += ' ' + 'R'

    # structure
    J = numerics.phs.J
    Mx1 = J[:nxl, :nxl]
    Mx2 = J[:nxl, nxl:nx]
    Mx3 = J[:nxl, nx:nx+nwl]
    Mx4 = J[:nxl, nx+nwl:nx+nw]
    Mx5 = J[:nxl, nx+nw:]

    Mw1 = J[nx:nx+nwl, :nxl]
    Mw2 = J[nx:nx+nwl, nxl:nx]
    Mw3 = J[nx:nx+nwl, nx:nx+nwl]
    Mw4 = J[nx:nx+nwl, nx+nwl:nx+nw]
    Mw5 = J[nx:nx+nwl, nx+nw:]

    Al = sp.Matrix.vstack(sp.Matrix.hstack(Mx1, Mx3),
                          sp.Matrix.hstack(Mw1, Mw3))
    Alx = sp.Matrix.vstack(sp.Matrix.hstack(Mx1),
                           sp.Matrix.hstack(Mw1))
    Bl = sp.Matrix.vstack(sp.Matrix.hstack(Mx2, Mx4),
                          sp.Matrix.hstack(Mw2, Mw4))
    Cl = sp.Matrix.vstack(Mx5,
                          Mw5)
    Id_coeffs = sp.diag(sp.eye(nxl)/numerics.ts, sp.eye(nwl))
    JQR = Al*sp.diag(numerics.phs.Q/2, numerics.phs.R)
    Dl = Id_coeffs - JQR
    iDl = mysymbolicinv(Dl)
    if nxl + nwl > 0:
        Vl1 = Alx*numerics.phs.Q*sp.Matrix(numerics.phs.x[:nxl])
        if numerics.phs.nxnl + numerics.phs.nwnl > 0:
            Vl2 = Bl*sp.Matrix(numerics.phs.dxHd[nxl:] + numerics.phs.z[nwl:])
        else:
            Vl2 = sp.zeros(nxl + nwl, 1)
        if numerics.phs.ny() > 0:
            Vl3 = Cl*sp.Matrix(numerics.phs.u)
        else:
            Vl3 = sp.zeros(nxl + nwl, 1)
        iter_explicite = iDl*(Vl1 + Vl2 + Vl3)
    else:
        iter_explicite = sp.zeros(0, 0)
    numerics.phs.iter_explicite = mysimplify(list(iter_explicite))
    funcs_to_lambdify += ' ' + 'iter_explicite'

    # construct the non-linear implict function
    # variables
    nxnl = numerics.phs.nxnl
    nwnl = numerics.phs.nwnl
    dxnl = numerics.phs.dx[nxl:]
    wnl = numerics.phs.w[nwl:]
    varnl = dxnl + wnl
    numerics.phs.varnl = varnl
    funcs_to_lambdify += ' ' + 'varnl'

    # set functions for non-linear parts
    def set_xnl(lis):
        numerics.all_vals[nxl:nx] = lis[0:nxnl]
    setattr(numerics, 'set_xnl', set_xnl)

    def set_dxnl(lis):
        numerics.all_vals[nx+nxl:2*nx] = lis[0:nxnl]
    setattr(numerics, 'set_dxnl', set_dxnl)

    def set_wnl(lis):
        numerics.all_vals[2*nx+nwl:2*nx+nw] = lis[0:nwnl]
    setattr(numerics, 'set_wnl', set_wnl)

    # structure
    J = numerics.phs.J
    Nx1 = J[nxl:nx, :nxl]
    Nx2 = J[nxl:nx, nxl:nx]
    Nx3 = J[nxl:nx, nx:nx+nwl]
    Nx4 = J[nxl:nx, nx+nwl:nx+nw]
    Nx5 = J[nxl:nx, nx+nw:]

    Nw1 = J[nx+nwl:nx+nw, :nxl]
    Nw2 = J[nx+nwl:nx+nw, nxl:nx]
    Nw3 = J[nx+nwl:nx+nw, nx:nx+nwl]
    Nw4 = J[nx+nwl:nx+nw, nx+nwl:nx+nw]
    Nw5 = J[nx+nwl:nx+nw, nx+nw:]

    Anl = sp.Matrix.vstack(sp.Matrix.hstack(Nx1, Nx3),
                           sp.Matrix.hstack(Nw1, Nw3))
    Bnl = sp.Matrix.vstack(sp.Matrix.hstack(Nx2, Nx4),
                           sp.Matrix.hstack(Nw2, Nw4))
    Cnl = sp.Matrix.vstack(Nx5,
                           Nw5)
    Id_coeffs = sp.diag(sp.eye(nxnl)/numerics.ts, sp.eye(nwnl))
    if nxnl + nwnl > 0:
        Vnl2 = Bnl*sp.Matrix(numerics.phs.dxHd[nxl:] + numerics.phs.z[nwl:])
        if nxl + nwl > 0:
            Vnl1 = Anl*sp.Matrix(numerics.phs.dxHd[:nxl] +
                                 numerics.phs.z[:nwl])
            Vnl1 = Vnl1.subs(map(lambda symb, expr: (symb, expr),
                                 numerics.phs.varl,
                                 numerics.phs.update_l))
        else:
            Vnl1 = sp.zeros(nxnl + nwnl, 1)
        if numerics.phs.ny() > 0:
            Vnl3 = Cnl*sp.Matrix(numerics.phs.u)
        else:
            Vnl3 = sp.zeros(nxnl + nwnl, 1)
        impfunc = Id_coeffs*sp.Matrix(varnl) - (Vnl1 + Vnl2 + Vnl3)
        res_impfunc = sp.sqrt(impfunc.T*impfunc)[0, 0]
        from utils.calculus import compute_jacobian
        jac_impfunc = compute_jacobian(impfunc, varnl)
    else:
        # init dummy quantities
        impfunc = sp.zeros(0, 1)
        res_impfunc = sp.sympify(0)
        jac_impfunc = sp.zeros(0)
        # set solver to None
        numerics.config['solver'] = None
    impfunc = mysimplify(impfunc)
    res_impfunc = mysimplify(res_impfunc)
    # append to list of lambdified functions
    numerics.phs.impfunc = impfunc
    funcs_to_lambdify += ' ' + 'impfunc'
    numerics.phs.res_impfunc = res_impfunc
    funcs_to_lambdify += ' ' + 'res_impfunc'
    numerics.phs.jac_impfunc = jac_impfunc
    funcs_to_lambdify += ' ' + 'jac_impfunc'

    setattr(numerics, 'funcs_to_lambdify', funcs_to_lambdify)


def self_solver(numerics, solver):
    """
    define the solver for implicite functions
    """
    if solver is None:

        # def update args function
        def iter_solver():
            # eval args
            return numerics.varnl()

    elif solver is '1':

        # def update args function
        def iter_solver():
            # eval args
            varnl = numerics.varnl()
            impfunc = numerics.impfunc()
            jac_impfunc = numerics.jac_impfunc()
            # compute inverse jacobian
            ijac_impfunc = np.linalg.inv(jac_impfunc)
            # build updates for args
            v = np.matrix(varnl).T - ijac_impfunc * impfunc
            varnl = v.T.tolist()[0]
            return varnl

    elif solver is '2':

        jac_impfunc = numerics.phs.jac_impfunc
        numerics.phs.ijac_impfunc = mysymbolicinv(jac_impfunc)
        numerics.funcs_to_lambdify += ' ijac_impfunc'

        # def update args function
        def iter_solver():
            # eval args
            varnl = numerics.varnl()
            impfunc = numerics.impfunc()
            ijac_impfunc = numerics.ijac_impfunc()
            # build updates for args
            v = np.matrix(varnl).T - ijac_impfunc * impfunc
            varnl = v.T.tolist()[0]
            return varnl

    elif solver is '3':

        impfunc = numerics.phs.impfunc
        varnl = sp.Matrix(numerics.phs.varnl)
        jac_impfunc = numerics.phs.jac_impfunc
        ijac_impfunc = mysymbolicinv(jac_impfunc)
        update_varnl = list(varnl - ijac_impfunc * impfunc)
        attr = 'update_varnl'
        setattr(numerics.phs, attr, update_varnl)
        numerics.funcs_to_lambdify += ' ' + attr

        # def update args function
        def iter_solver():
            # eval args
            varnl = getattr(numerics, attr)()
            return varnl

    setattr(numerics, 'iter_solver', iter_solver)
