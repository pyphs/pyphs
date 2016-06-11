# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 16:14:03 2016

@author: Falaize
"""
from pyphs.numerics.tools import geteval
from solvers.solvers import Solver
from pyphs.misc.tools import norm


class Internal:
    """
    structure of numerical arguments and numerical functions for simulation.
    """
    def __init__(self, config, phs):
        self.fs = config['fs']
        self.EPS = config['numtol']
        self.maxit = config['maxit']
        self.solver_id = config['solver']

        # define all arguments 'args' and accessor to specific parts eg x, xl,
        # xnl, linear an dnonlinear variables varl=(dxl, wl), varl=(dxl, wl)
        init_args(self, phs)

        # init args values with 0
        setattr(self, 'args', [0, ]*self.nargs)

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
    # set dimensions
    def set_dim(name):
        dim_name = 'n'+name
        dim = geteval(phs, dim_name)
        setattr(internal, dim_name, dim)

    dims_names = ('x', 'w', 'y', 'p', 'xl', 'wl')
    for name in dims_names:
        set_dim(name)

    # define dimension of nonlinear parts of x and w
    nxnl = internal.nx - internal.nxl
    nwnl = internal.nw - internal.nwl
    setattr(internal, 'nxnl', nxnl)
    setattr(internal, 'nwnl', nwnl)

    # list of variables quantities on which the lambdified functions depend
    from pyphs.numerics.numeric import _args_names
    internal._args_names = _args_names
    args = []
    for name in internal.args_names:
        # get symbols and stores symbols
        symbs = geteval(phs.symbs, name)
        setattr(internal, name+'_symbs', symbs)
        # get symbols and stores index in all args
        inds = range(len(args), len(args)+len(symbs))
        setattr(internal, name+'_inds', inds)
        # append all args symbols
        args += symbs
    # stores all args symbols
    setattr(internal, 'args_symbs', args)
    # stores dima of all args
    setattr(internal, 'nargs', len(internal.args_symbs))

    # select linear and nonlinear parts and add to list of variables
    for names, dim in zip([['x', 'dx'], ['w']], ['x', 'w']):
        # apply to list [x, dx] with same dim x only
        for name in names:
            # get dimension of linear part
            diml = getattr(internal, 'n'+dim+'l')
            # get and stores symbols of linear parts
            l_symbs = getattr(internal, name+'_symbs')[:diml]
            setattr(internal, name+'l_symbs', l_symbs)
            # get and stores indices of linear parts
            l_inds = getattr(internal, name+'_inds')[:diml]
            setattr(internal, name+'l_inds', l_inds)
            # append to list of variable for which define accessor and mutator
            internal._args_names.append(name+'l')

            # get and stores symbols of nonlinear parts
            nl_symbs = getattr(internal, name+'_symbs')[diml:]
            setattr(internal, name+'nl_symbs', nl_symbs)
            # get and stores indices of nonlinear parts
            nl_inds = getattr(internal, name+'_inds')[diml:]
            setattr(internal, name+'nl_inds', nl_inds)
            # append to list of variable for which define accessor and mutator
            internal._args_names.append(name+'nl')

    # define varl=[dxl, wl] and varnl=[dxnl, wnl]
    for attr in ['l', 'nl']:
        name = 'var'+attr
        symbs = []
        inds = []
        for quantity in ['dx', 'w']:
            symbs += getattr(internal, quantity+attr+'_symbs')
            inds += getattr(internal, quantity+attr+'_inds')
        setattr(internal, name+'_inds', inds)
        setattr(internal, name+'_symbs', symbs)
        # append to list of variable for which define accessor and mutator
        internal._args_names.append(name)
    setattr(internal, 'nvarl', len(internal.varl_symbs))
    setattr(internal, 'nvarnl', len(internal.varnl_symbs))

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
