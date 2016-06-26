# -*- coding: utf-8 -*-
"""
Created on Tue May 24 11:20:26 2016

@author: Falaize
"""
from pyphs.misc.io import write_data
import config
import time
from internals.internal import Internal
from processes import process_py, process_cpp


class Simulation:
    """
    object that stores data and methods for simulation of PortHamiltonianObject
    """
    def __init__(self, phs, opts=None):
        """
        Parameters
        -----------

        opts : dic of configuration options

            keys and default values are

                * 'language': 'python',
                * 'fs': 48e3,
                * 'numtol': EPS,
                * 'maxit': 100,
                * 'split': True
                * 'solver': 'standard',
                * 'timer': True,
                * 'load_options': {'decim': 1,
                                   'imin': 0,
                                   'imax': None}
        """

        # init configuration options
        if opts is None:
            opts = {}
        self.config = config.standard
        self.config.update(opts)

        # split system into linear and nonlinear parts
        if self.config['split']:
            # apply split if not already
            if not hasattr(phs, 'nxl'):
                from pyphs.symbolics.structures.tools import split_linear
                split_linear(phs)
        else:
            # set all components as nonlinear
            phs.dims.xl = phs.dims.wl = 0

        # build the numerical update evaluation structure
        self.internal = Internal(self.config, phs)

        # init input and parameters sequences, and get number of time steps

#, sequ=None, seqp=None,
 #                nt=None, x0=None
 #       init_data(phs, sequ, seqp, x0, nt)

    def process(self, phs):
        """
        process simulation for all time steps
        """
        if self.config['timer']:
            tstart = time.time()

        # language is 'py' or 'cpp'
        assert self.config['language'] in ('c++', 'python'),\
            'language "{0!s}" unknown'.format(self.config['language'])

        if self.config['language'] == 'c++':
            process_cpp(phs)
        elif self.config['language'] == 'python':
            process_py(self)

        if self.config['timer']:
            tstop = time.time()

        if self.config['timer']:
            time_it = ((tstop-tstart)/float(self.nt))
            print 'time per iteration: {0!s} s'.format(format(time_it, 'f'))
            time_ratio = time_it*self.config['fs']
            print 'ratio compared to real-time: {0!s}'.format(format(
                time_ratio, 'f'))


        if self.presubs:
            phs.apply_subs()

        self.dims = phs.dims
        self.is_nl = bool(self.dims.xnl() + self.dims.wnl())
        # define all arguments 'args' and accessor to specific parts eg x, xl,
        # xnl, linear an dnonlinear variables varl=(dxl, wl), varl=(dxl, wl)
        init_args(self, phs)

        # init args values with 0
        setattr(self, 'args', [0, ]*self.dims.args())

        # init solver
        self.solver = Solver(self, phs, self.solver_id)

        # define state variation
        phs.exprs.setexpr('dtx', [el*self.fs for el in phs.symbs.dx()])

        # build numerical functions from functions in phs.exprs._names
        phs.build_exprs()
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
        old_varsnl = [float('Inf'), ]*(self.dims.xnl()+self.dims.wnl())
        # loop while res > tol, step > tol and it < itmax
        while res > self.EPS and step > self.EPS and it < self.maxit:
            # updated args
            self.iter_solver()
            # eval residual
            res = self.res_impfunc()
            # eval norm step
            step = norm([el1-el2 for (el1, el2) in zip(self.varsnl(),
                                                       old_varsnl)])
            # increment it
            it += 1
            # save args for comparison
            old_varsnl = self.varsnl()

    def update_l(self):
        varsl = self.eval_varsl()
        self.set_varsl(varsl)


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

    dic = {'varsl': list(phs.symbs.dx()[:nxl]) + list(phs.symbs.w[:nwl]),
           'varsnl': list(phs.symbs.dx()[nxl:]) + list(phs.symbs.w[nwl:]),
           'x': phs.symbs.x,
           'dx': phs.symbs.dx(),
           'dxnl': phs.symbs.dx()[nxl:],
           'w': phs.symbs.w,
           'u': phs.symbs.u,
           'p': phs.symbs.p}

    for name in dic:
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


def init_data(phs, sequ, seqp, x0, nt):
    # get number of time-steps
    if hasattr(sequ, 'index'):
        nt = len(sequ)
    elif hasattr(sequ, 'index'):
        nt = len(seqp)
    else:
        assert nt is not None, 'Unknown number of \
iterations. Please tell either sequ (input sequence), seqp \
(sequence of parameters) or nt (number of time steps).'
        assert isinstance(nt, int), 'number of time steps is not integer, \
got {0!s} '.format(nt)

    # if sequ is not provided, a sequence of [[0]*ny]*nt is assumed
    if sequ is None:
        def generator_u():
            for _ in range(nt):
                if phs.dims.y() > 0:
                    yield [0, ]*phs.dims.y()
                else:
                    yield ""
        sequ = generator_u()
    # if seqp is not provided, a sequence of [[0]*np]*nt is assumed
    if seqp is None:
        def generator_p():
            for _ in range(nt):
                if phs.dims.p() > 0:
                    yield [0, ]*phs.dims.p()
                else:
                    yield ""
        seqp = generator_p()

    if x0 is None:
        x0 = [0, ]*phs.dims.x()
    else:
        assert isinstance(x0, list) and \
            len(x0) == phs.dims.x() and \
            isinstance(x0[0], (float, int)), 'x0 not understood, got \
{0!s}'.format(x0)

    # write input sequence
    write_data(phs, sequ, 'u')
    # write parameters sequence
    write_data(phs, seqp, 'p')
    # write initial state
    write_data(phs, [x0, ], 'x0')
    return nt
