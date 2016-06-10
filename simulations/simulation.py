# -*- coding: utf-8 -*-
"""
Created on Tue May 24 11:20:26 2016

@author: Falaize
"""
from misc.io import write_data
from config import standard_config
from data import Data
from symbolics.structures.tools import split_linear
from symbolics.tools import simplify, inverse
import time
import sympy as sp
from internals.internal import Internal
from processes import process_py, process_cpp


class Simulation:
    """
    object that stores data and methods for simulation of PortHamiltonianObject
    """
    def __init__(self, phs, config=None, sequ=None, seqp=None,
                 nt=None, x0=None):
        """
        Parameters
        -----------

        config : dic of configuration options

            keys and default values are

             * 'language': 'python',
             * 'numtol': EPS,
             * 'maxit': 100,
             * 'load_options': {'decim': 1,
                                'imin': 0,
                                'imax': None},
            * 'solver': '1',
            * 'timer': True,
            * 'fs': 48e3,
            * 'split': None

        sequ : iterable of tuples of inputs values

        seqp : iterable of tuples of parameters values

        language : 'c++' or 'python'

        nt : number of time steps (x goes to x[nt+1])
        """
        # init configuration options
        if config is None:
            config = {}
        self.config = standard_config
        self.config.update(config)
        # split system into linear and nonlinear parts
        if self.config['split']:
            # apply split if not already
            if not hasattr(phs, 'nxl'):
                split_linear(phs)
        else:
            # set all components as nonlinear
            phs.nxl = phs.nwl = 0
            phs.nxnl, phs.nwnl = phs.nx(), phs.nw()
        # build the numerical update evaluation structure
        self.internal = Internal(self.config, phs)
        # init input and parameters sequences, and get number of time steps
        init_data(self, phs, sequ, seqp, x0, nt)

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
            process_cpp(self)
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


def self_structure(numerics):

    nx = numerics.phs.nx()
    nw = numerics.phs.nw()

    numerics.phs.y = numerics.phs.output
    numerics.phs.dtx = [el/numerics.ts for el in numerics.phs.dx]

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
    iDl = inverse(Dl)
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
    numerics.phs.iter_explicite = simplify(list(iter_explicite))
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
    impfunc = simplify(impfunc)
    res_impfunc = simplify(res_impfunc)
    # append to list of lambdified functions
    numerics.phs.impfunc = impfunc
    funcs_to_lambdify += ' ' + 'impfunc'
    numerics.phs.res_impfunc = res_impfunc
    funcs_to_lambdify += ' ' + 'res_impfunc'
    numerics.phs.jac_impfunc = jac_impfunc
    funcs_to_lambdify += ' ' + 'jac_impfunc'

    setattr(numerics, 'funcs_to_lambdify', funcs_to_lambdify)


def init_data(simulation, phs, sequ, seqp, x0, nt):
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
    simulation.nt = nt

    # if sequ is not provided, a sequence of [[0]*ny]*nt is assumed
    if sequ is None:
        def generator_u():
            for _ in range(simulation.nt):
                if phs.ny() > 0:
                    yield [0, ]*phs.ny()
                else:
                    yield ""
        sequ = generator_u()
    # if seqp is not provided, a sequence of [[0]*np]*nt is assumed
    if seqp is None:
        def generator_p():
            for _ in range(simulation.nt):
                if phs.np() > 0:
                    yield [0, ]*phs.np()
                else:
                    yield ""
        seqp = generator_p()

    if x0 is None:
        x0 = [0, ]*phs.nx()
    else:
        assert isinstance(x0, list) and \
            len(x0) == phs.nx() and \
            isinstance(x0[0], (float, int)), 'x0 not understood, got \
{0!s}'.format(x0)

    # build data i/o structure
    simulation.data = Data(simulation, phs)
    # write input sequence
    write_data(phs, sequ, 'u')
    # write parameters sequence
    write_data(phs, seqp, 'p')
    # write initial state
    write_data(phs, [x0, ], 'x0')
