# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 16:14:03 2016

@author: Falaize
"""
from numerics.tools import geteval
from solvers.solvers import Solver
from misc.tools import norm


class Internal:
    """
    structure of numerical arguments and numerical functions for simulation.
    """
    def __init__(self, config, phs):
        self.fs = config['fs']
        self.EPS = config['numtol']
        self.maxit = config['maxit']

        init_args(self, phs)
        # init solver
        self.solver_id = config['solver']
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
        # update nl variables (dxnl and wnl)
        self.update_nl()
        # update l variables (dxnl and wnl)
        self.update_l()

    def update_nl(self):
        # init it counter
        it = 0
        # init dx with 0
        self.set_dx([0, ]*self.nx)
        # init step on iteration
        step = float('Inf')
        # init residual of implicite function
        res = float('Inf')
        # init args memory for computation of step on iteration
        old_varnl = [float('Inf'), ]*self.nxnl
        # loop while res > tol, step > tol and it < itmax
        while res > self.EPS and step > self.EPS and it < self.maxit:
            # updated args
            self.iter_solver()
            # eval residual
            res = self.res_impfunc()
            # eval norm step
            norm_step = norm([el1-el2 for (el1, el2) in zip(self.varnl(),
                                                            old_varnl)])
            norm_varnl = norm(self.varnl()) + self.EPS
            step = norm_step/(norm_varnl)
            # increment it
            it += 1
            # save args for comparison
            old_varnl = self.varnl()

    def update_l(self):
        varl = self.iter_explicite()
        self.set_varl(varl)


def init_args(internal, phs):
    """
    define accessors and mutators of numerical values associated to arguments
    """
    # get dimensions
    for dim in ['x', 'w', 'y', 'p', 'xl', 'wl']:
        setattr(internal, 'n'+dim, geteval(phs, 'n'+dim))
    setattr(internal, 'nxnl', phs.nx() - phs.nxl)
    setattr(internal, 'nwnl', phs.nw() - phs.nwl)
    setattr(internal, 'nvarl', phs.nxl + phs.nwl)
    setattr(internal, 'nvarnl', internal.nxnl + internal.nwnl)

    # list of variables quantities on which the lambdified functions depend
    phs.build_nums()
    internal.args_names = list(phs.nums.args_names)
    args = []
    for name in internal.args_names:
        symbs = geteval(phs.symbs, name)
        setattr(internal, name+'_symbs', symbs)
        inds = range(len(args), len(args)+len(symbs))
        setattr(internal, name+'_inds', inds)
        args += symbs
    setattr(internal, 'args_symbs', args)
    setattr(internal, 'args', [0, ]*len(internal.args_symbs))

    # select linear and nonlinear parts and add to list of variables
    for names, dim in zip([['x', 'dx'], ['w']], ['x', 'w']):
        for name in names:
            diml = getattr(internal, 'n'+dim+'l')
            l_symbs = getattr(internal, name+'_symbs')[:diml]
            nl_symbs = getattr(internal, name+'_symbs')[diml:]
            setattr(internal, name+'l_symbs', l_symbs)
            setattr(internal, name+'nl_symbs', nl_symbs)
            l_inds = getattr(internal, name+'_inds')[:diml]
            nl_inds = getattr(internal, name+'_inds')[diml:]
            setattr(internal, name+'l_inds', l_inds)
            setattr(internal, name+'nl_inds', nl_inds)
            internal.args_names += [name+'l', name+'nl']

    for attr in ['l', 'nl']:
        name = 'var'+attr
        symbs = []
        inds = []
        for quantity in ['dx', 'w']:
            symbs += getattr(internal, quantity+attr+'_symbs')
            inds += getattr(internal, quantity+attr+'_inds')
        setattr(internal, name+'_inds', inds)
        setattr(internal, name+'_symbs', symbs)
        internal.args_names += [name, ]

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

    # get each variable in all_vals:
    for name in internal.args_names:
        inds = getattr(internal, name+'_inds')
        setattr(internal, name, get_generator(inds))
        setattr(internal, 'set_'+name, set_generator(inds))


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
        inds = getattr(phs.nums, 'inds_' + name)
        setattr(internal, name, eval_generator(func, inds))
