# -*- coding: utf-8 -*-
"""
Created on Tue May 24 11:20:26 2016

@author: Falaize
"""
from solvers.solvers import Solver
from pyphs.misc.tools import norm
from pyphs.numerics.tools import find
from processes import process_py, process_cpp
import config
import time


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

        self.phs = phs

    def init(self, sequ=None, seqp=None, x0=None, nt=None, opts=None):
        if opts is None:
            opts = {}
        self.config.update(opts)
        self.init_phs()
        self.phs.data.init_data(sequ, seqp, x0, nt)
        init_args(self)

        # init args values with 0
        setattr(self, 'args', [0, ]*self.phs.dims.args())

        # init solver
        self.solver = Solver(self)

        # define state variation
        self.phs.exprs.setexpr('dtx',
                               [el*self.config['fs']
                                   for el in self.phs.symbs.dx()])

        # build numerical functions from functions in phs.exprs._names
        self.phs.funcs.build()
        init_funcs(self)

    def init_phs(self):
        """
        """
        if self.config['presubs']:
            self.phs.apply_subs()

        # split system into linear and nonlinear parts
        force_nolin = not self.config['split']
        from pyphs.symbolics.structures.tools import split_linear
        split_linear(self.phs, force_nolin=force_nolin)

    def process(self):
        """
        process simulation for all time steps
        """
        if self.config['timer']:
            tstart = time.time()

        # language is 'py' or 'cpp'
        assert self.config['language'] in ('c++', 'python'),\
            'language "{0!s}" unknown'.format(self.config['language'])

        if self.config['language'] == 'c++':
            process_cpp(self.phs)
        elif self.config['language'] == 'python':
            process_py(self)

        if self.config['timer']:
            tstop = time.time()

        if self.config['timer']:
            time_it = ((tstop-tstart)/float(self.config['nt']))
            print 'time per iteration: {0!s} s'.format(format(time_it, 'f'))
            time_ratio = time_it*self.config['fs']
            print 'ratio compared to real-time: {0!s}'.format(format(
                time_ratio, 'f'))

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
        if self.phs.is_nl():
            # update nl variables (dxnl and wnl)
            self.update_nl()
        # update l variables (dxnl and wnl)
        self.update_l()

    def update_nl(self):
        # init it counter
        it = 0
        # init dx with 0
        self.set_dxnl([0, ]*self.phs.dims.xnl())
        # init step on iteration
        step = float('Inf')
        # init residual of implicite function
        res = float('Inf')
        # init args memory for computation of step on iteration
        old_varsnl = [float('Inf'), ]*(self.phs.dims.xnl() +
                                       self.phs.dims.wnl())
        # loop while res > tol, step > tol and it < itmax
        while res > self.config['numtol'] and step > self.config['numtol']\
                and it < self.config['maxit']:
            # updated args
            self.iter_solver()
            # eval residual
            res = self.res_impfunc()
            # eval norm step
            step = norm([el1-el2 for (el1, el2) in zip(self.vnl(),
                                                       old_varsnl)])
            # increment it
            it += 1
            # save args for comparison
            old_varsnl = self.vnl()

    def update_l(self):
        vl = self.update_lin().T.tolist()[0]
        self.set_vl(vl)


def init_args(simulation):
    """
    define accessors and mutators of numerical values associated to arguments
    """
    # generators of 'get' and 'set':
    def get_generator(inds):
        def get_func():
            return [simulation.args[i] for i in inds]
        return get_func

    def set_generator(inds):
        def set_func(lis):
            for i in inds:
                elt = lis.pop(0)
                simulation.args[i] = elt
        return set_func

    # def lists of linear variables linvars
    nxl = simulation.phs.dims.xl
    nwl = simulation.phs.dims.wl

    dic = {'vl': list(simulation.phs.symbs.dx()[:nxl]) +
           list(simulation.phs.symbs.w[:nwl]),
           'vnl': list(simulation.phs.symbs.dx()[nxl:]) +
           list(simulation.phs.symbs.w[nwl:]),
           'x': simulation.phs.symbs.x,
           'dx': simulation.phs.symbs.dx(),
           'dxnl': simulation.phs.symbs.dx()[nxl:],
           'w': simulation.phs.symbs.w,
           'u': simulation.phs.symbs.u,
           'p': simulation.phs.symbs.p}

    for name in dic:
        _, inds = find(dic[name], simulation.phs.symbs.args())
        setattr(simulation, name + '_symbs', dic[name])
        setattr(simulation, name, get_generator(inds))
        setattr(simulation, 'set_' + name, set_generator(inds))


def init_funcs(simulation):
    """
    link and lambdify all funcions
    """
    # list of lambdified functions
    simulation.funcs_names = simulation.phs.exprs._names

    # generator of evaluation functions
    def eval_generator(func, inds):
        def eval_func():
            args = (simulation.args[el] for el in inds)
            return func(*args)
        return eval_func

    # link evaluation to internal values
    for name in simulation.funcs_names:
        func = getattr(simulation.phs.funcs, name)
        inds = getattr(simulation.phs.funcs, name + '_inds')
        setattr(simulation, name, eval_generator(func, inds))
