# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 16:14:03 2016

@author: Falaize
"""
from pyphs.misc.tools import geteval
from solvers.solvers import Solver
from pyphs.misc.tools import norm
from pyphs.numerics.tools import find

class Internal:
    """
    structure of numerical arguments and numerical functions for simulation.
    """
    def __init__(self, config, phs):
        self.fs = config['fs']
        self.EPS = config['numtol']
        self.maxit = config['maxit']
        self.solver_id = config['solver']

        self.dims = phs.dims
        self.is_nl = bool(self.dims.xnl() + self.dims.wnl())
        # define all arguments 'args' and accessor to specific parts eg x, xl,
        # xnl, linear an dnonlinear variables varl=(dxl, wl), varl=(dxl, wl)
        init_args(self, phs)

        # init args values with 0
        setattr(self, 'args', [0, ]*self.dims.args())

        # init solver
        self.solver = Solver(self, phs, self.solver_id)

        # build numerical functions from functions in phs.exprs._names
        phs.build_nums()
        init_funcs(self, phs)

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
        self.set_x(map(lambda xi, dxi: xi + dxi, self.x(), self.dx()))
        if self.is_nl:
            # update nl variables (dxnl and wnl)
            self.update_nl()
        # update l variables (dxnl and wnl)
        self.update_l()

    def update_nl(self):
        # init it counter
        it = 0
        # init dx with 0
        self.set_dxnl([0, ]*self.dims.xnl())
        # init step on iteration
        step = float('Inf')
        # init residual of implicite function
        res = float('Inf')
        # init args memory for computation of step on iteration
        old_nlinvars = [float('Inf'), ]*(self.dims.xnl()+self.dims.wnl())
        # loop while res > tol, step > tol and it < itmax
        while res > self.EPS and step > self.EPS and it < self.maxit:
            # updated args
            self.iter_solver()
            # eval residual
            res = self.res_impfunc()
            # eval norm step
            norm_step = norm([el1-el2 for (el1, el2) in zip(self.nlinvars(),
                                                            old_nlinvars)])
            norm_varnl = norm(self.nlinvars()) + self.EPS
            step = norm_step/(norm_varnl)
            # increment it
            it += 1
            # save args for comparison
            old_nlinvars = self.nlinvars()

    def update_l(self):
        linvars = self.iter_explicite()
        self.set_linvars(linvars)


def init_args(internal, phs):
    """
    define accessors and mutators of numerical values associated to arguments
    """
    # generators of 'get' and 'set':
    def get_generator(inds):
        def get_func():
            return [internal.args[i] for i in inds]
        return get_func

    def set_generator(inds):
        def set_func(lis):
            for i in inds:
                elt = lis.pop(0)
                internal.args[i] = elt
        return set_func

    # def lists of linear variables linvars
    nxl = phs.dims.xl
    nwl = phs.dims.wl

    dic = {'linvars': list(phs.symbs.dx()[:nxl]) + list(phs.symbs.w[:nwl]),
           'nlinvars': list(phs.symbs.dx()[nxl:]) + list(phs.symbs.w[nwl:]),
           'x': phs.symbs.x,
           'dx': phs.symbs.dx(),
           'dxnl': phs.symbs.dx()[phs.dims.xl:],
           'w': phs.symbs.w,
           'u': phs.symbs.u,
           'p': phs.symbs.p}

    for name in dic:
        print name
        _, inds = find(dic[name], phs.symbs.args())
        setattr(internal, name + '_symbs', dic[name])
        setattr(internal, name, get_generator(inds))
        setattr(internal, 'set_' + name, set_generator(inds))


def init_funcs(internal, phs):
    """
    link and lambdify all funcions
    """
    # list of lambdified functions
    internal.funcs_names = phs.exprs._names

    # generator of evaluation functions
    def eval_generator(func, inds):
        def eval_func():
            args = (internal.args[el] for el in inds)
            return func(*args)
        return eval_func

    # link evaluation to internal values
    for name in internal.funcs_names:
        func = getattr(phs.nums, name)
        inds = getattr(phs.nums, name + '_inds')
        setattr(internal, name, eval_generator(func, inds))
