# -*- coding: utf-8 -*-
"""
Created on Tue May 24 11:20:26 2016

@author: Falaize
"""
from misc.io import write_data
from misc.tools import progressbar
from config import standard_config
from data import Data
from numerics.tools import geteval
import time


class Simulation:
    """
    object that stores data and methods for simulation of PortHamiltonianObject
    """
    def __init__(self, phs, fs, sequ=None, seqp=None,
                 language='python', nt=None, x0=None):
        """
        Parameters
        -----------

        fs : float, sample rate

        sequ : iterable of tuples of inputs values

        seqp : iterable of tuples of parameters values

        language : 'c++' or 'python'

        nt : number of time steps (x goes to x[nt+1])
        """
        self.config = standard_config
        self.config.update({'fs': fs,
                            'language': language})
        # build data i/o structure
        self.data = Data(self, phs)

        if isinstance(sequ, (list, tuple)):
            nt = len(sequ)
        elif isinstance(seqp, (list, tuple)):
            nt = len(seqp)
        else:
            assert nt is not None, 'Unknown number of \
    iterations. Please tell either sequ (input sequence), seqp \
    (sequence of parameters) or nt (number of time steps).'
            assert isinstance(nt, int), 'number of time steps is not integer, \
got {0!s} '.format(nt)

        # if seq_u is not provided, a sequence of [[0]*ny]*nt is assumed
        if sequ is None:
            def generator_u():
                for _ in range(nt):
                    if phs.ny() > 0:
                        yield [0, ]*phs.ny()
                    else:
                        yield ""
            sequ = generator_u()
        # if seq_p is not provided, a sequence of [[0]*np]*nt is assumed
        if seqp is None:
            def generator_p():
                for _ in range(nt):
                    if phs.np() > 0:
                        yield [0, ]*phs.np()
                    else:
                        yield ""
            seqp = generator_p()

        self.nt = nt

        if x0 is None:
            x0 = [0, ]*phs.nx()
        else:
            assert isinstance(x0, list) and \
                len(x0) == phs.nx() and \
                isinstance(x0[0], (float, int)), 'x0 not understood, got \
{0!s}'.format(x0)
        write_data(phs, sequ, 'u')
        write_data(phs, seqp, 'p')
        write_data(phs, [x0, ], 'x0')

        self._build_internal(phs)

    def _build_internal(self, phs):
        # init internal attr with empty object
        class Internal:
            pass  # do nothing
        self.internal = Internal()
        # list of variables quantities on which the lambdified functions depend
        variables = phs.nums.args_names
        # list all variables
        args = []
        for name in variables:
            symbs = geteval(phs.symbs, name)
            setattr(self.internal, name+'_symbs', symbs)
            setattr(self.internal, name+'_inds',
                    (len(args), len(args)+len(symbs)))
            args += symbs
        setattr(self.internal, 'all_symbs', args)
        setattr(self.internal, 'all_vals', [0, ]*len(self.internal.all_symbs))

        # generators of 'get' and 'set':
        def get_generator(inds):
            def get_func():
                start, stop = inds
                return self.internal.all_vals[start: stop]
            return get_func

        def set_generator(inds):
            def set_func(lis):
                start, stop = inds
                self.internal.all_vals[start: stop] = lis[0: stop-start]
            return set_func

        def eval_generator(func, inds):
            def eval_func():
                args = (self.internal.all_vals[el] for el in inds)
                return func(*args)
            return eval_func

        # get each variable in all_vals:
        for name in variables:
            inds = getattr(self.internal, name+'_inds')
            setattr(self.internal, name, get_generator(inds))
            setattr(self.internal, 'set_'+name, set_generator(inds))

        # build numerical functions from functions in phs.exprs._names
        phs.build_nums()

        # link evaluation to internal values
        for name in phs.exprs._names:
            func = getattr(phs.nums, name)
            inds = getattr(phs.nums, 'inds_' + name)
            setattr(self.internal, name, eval_generator(func, inds))

    def update(self, u, p):
        """
        update with input 'u' and parameter 'p' on a sigle  time step \
(the samplerate is simulation.config['fs']).
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

    def process(self):

        if self.config['timer']:
            tstart = time.time()
        # language is 'py' or 'cpp'
        assert self.config['language'] in ('c++', 'python'), 'language \
"{0!s}" unknown'.format(self.config['language'])
        if self.config['language'] == 'c++':
            process_cpp(self)
        elif self.config['language'] == 'python':
            process_py(self)
        if self.config['timer']:
            tstop = time.time()
        # load data from 'phs.path/data/'
        from utils.io import load_all
        load_all(self)
        if self.config['timer']:
            time_per_it = ((tstop-tstart)/float(self.nt))
            print 'time per iteration: \
{0!s} s'.format(format(time_per_it, 'f'))
            ratio_to_real_time = time_per_it*self.config['fs']
            print 'ratio compared to real-time: {0!s}\
'.format(format(ratio_to_real_time, 'f'))


def process_py(numerics):

    # get generators of u and p
    seq_u = numerics.data_generator('u')
    seq_p = numerics.data_generator('p')

    from utils.io import open_files, close_files, dump_files
    files_to_open = 'x dx dxH dxHd w z y'
    files = open_files(numerics.phs, files_to_open)

    # init time step
    n = 0
    print "\n*** Simulation ***\n"
    for (u, p) in zip(seq_u, seq_p):
        numerics.update(u=u, p=p)
        dump_files(numerics, files)
        n += 1
        progressbar(n/float(numerics.nt))

    time.sleep(0.1)
    close_files(files)


def process_cpp(numerics):

    numerics.phs.writeCppCode()

    from pyphs_config import cpp_build_and_run_script
    if cpp_build_and_run_script is None:
        import os
        print"\no==========================================================\
        ==o\n"
        print " Please, execute:\n" + numerics.phs.folders['cpp'] + \
            os.path.sep + \
            "/main.cpp"
        print"\no==========================================================\
        ==o\nWaiting....\n"
        raw_input()
    elif type(cpp_build_and_run_script) is str:
        import subprocess
        # Replace generic term 'phobj_path' by actual object path
        script = cpp_build_and_run_script.replace('phobj_path',
                                                  numerics.phs.path)
        # exec Build and Run script
        p = subprocess.Popen(script, shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        for line in iter(p.stdout.readline, ''):
            print line,


def presolve(phs):

    phs.iDw = sp.eye(phs.nwl()) - phs.J3*phs.R()
    phs.Dw = sp.Matrix.inv(phs.iDw, method='LU')

    #######################################################################

    phs.A1 = phs.Dw*phs.K1.T
    phs.B1 = phs.Dw*phs.K3.T
    phs.C1 = phs.Dw*phs.M2
    phs.D1 = phs.Dw*phs.G3
    #######################################################################
    phs.tildeA2 = phs.J1-phs.K1*phs.R()*phs.A1
    phs.tildeB2 = phs.M1-phs.K1*phs.R()*phs.B1
    phs.tildeC2 = -(phs.K2+phs.K1*phs.R()*phs.C1)
    phs.tildeD2 = phs.G1-phs.K1*phs.R()*phs.D1
    #######################################################################

    phs.iDx = sp.eye(phs.nxl())*phs.fs - phs.tildeA2*phs.Q()/2.
    phs.Dx = phs.iDx.inv()

    phs.A2 = phs.Dx*phs.tildeA2*phs.Q()
    phs.B2 = phs.Dx*phs.tildeB2
    phs.C2 = phs.Dx*phs.tildeC2
    phs.D2 = phs.Dx*phs.tildeD2

    phs.A3 = phs.Q()*(sp.eye(phs.nxl()) +
                      (sp.sympify(1)/sp.sympify(2))*phs.A2)
    phs.B3 = (sp.sympify(1)/sp.sympify(2))*phs.Q()*phs.B2
    phs.C3 = (sp.sympify(1)/sp.sympify(2))*phs.Q()*phs.C2
    phs.D3 = (sp.sympify(1)/sp.sympify(2))*phs.Q()*phs.D2

    phs.tildeA4 = -(phs.M1.T + phs.K3*phs.R()*phs.A1)
    phs.tildeB4 = (phs.J2 - phs.K3*phs.R()*phs.B1)
    phs.tildeC4 = -(phs.K4 + phs.K3*phs.R()*phs.C1)
    phs.tildeD4 = (phs.G2 - phs.K3*phs.R()*phs.D1)

    phs.A4 = phs.tildeA4*phs.A3
    phs.B4 = phs.tildeB4+phs.tildeA4*phs.B3
    phs.C4 = phs.tildeC4+phs.tildeA4*phs.C3
    phs.D4 = phs.tildeD4+phs.tildeA4*phs.D3

    phs.tildeA5 = (phs.K2.T - phs.M2.T*phs.R()*phs.A1)
    phs.tildeB5 = (phs.K4.T - phs.M2.T*phs.R()*phs.B1)
    phs.tildeC5 = (phs.J4 - phs.M2.T*phs.R()*phs.C1)
    phs.tildeD5 = (phs.G4 - phs.M2.T*phs.R()*phs.D1)

    phs.A5 = phs.tildeA5*phs.A3
    phs.B5 = (phs.tildeB5+phs.tildeA5*phs.B3)
    phs.C5 = (phs.tildeC5+phs.tildeA5*phs.C3)
    phs.D5 = (phs.tildeD5+phs.tildeA5*phs.D3)

    phs.A6 = phs.A1*phs.A3
    phs.B6 = (phs.B1+phs.A1*phs.B3)
    phs.C6 = (phs.C1+phs.A1*phs.C3)
    phs.D6 = (phs.D1+phs.A1*phs.D3)

    if phs.nxnl() > 0:
        MdxHnl = sp.Matrix.vstack(phs.B2, phs.B6) * \
                sp.Matrix(list(phs.discdxHnl))
    else:
        MdxHnl = sp.zeros(phs.nxl()+phs.nwl(), 1)
    Mznl = sp.Matrix.vstack(phs.C2, phs.C6)*sp.Matrix(list(phs.znl()))\
        if phs.nwnl() > 0 else sp.zeros(phs.nxl()+phs.nwl(), 1)
    Mxl = sp.Matrix.vstack(phs.A2, phs.A6)*sp.Matrix(phs.xl())\
        if phs.nxl() > 0 else sp.zeros(phs.nxl()+phs.nwl(), 1)
    Mu = sp.Matrix.vstack(phs.D2, phs.D6)*phs.Gains()*sp.Matrix(phs.u)\
        if phs.ny() > 0 else sp.zeros(phs.nxl()+phs.nwl(), 1)
    phs.Fl = parallel_factorize(list(Mxl + MdxHnl + Mznl + Mu))\
        if parallelize else list(Mxl + MdxHnl + Mznl + Mu)

    #######################################################################
    if phs.isNL:
        phs.isNL = True
        phs.A = sp.Matrix.vstack(phs.A4.as_mutable(),
                                 phs.A5.as_mutable())
        hstack1 = sp.Matrix.hstack(phs.B4.as_mutable(),
                                   phs.C4.as_mutable())
        hstack2 = sp.Matrix.hstack(phs.B5.as_mutable(),
                                   phs.C5.as_mutable())
        phs.B = sp.Matrix.vstack(hstack1, hstack2)
        phs.C = sp.Matrix.vstack(phs.D4.as_mutable(),
                                 phs.D5.as_mutable())
        Mxl = phs.A*sp.Matrix(phs.xl()) if phs.nxl() > 0 \
            else sp.zeros(phs.nxnl()+phs.nwnl(), 1)
        Mu = phs.C*phs.Gains()*sp.Matrix(phs.u) if phs.ny() > 0 \
            else sp.zeros(phs.nxnl()+phs.nwnl(), 1)
        varNL = sp.Matrix([dxnlm*phs.fs for dxnlm in phs.dxnl()]+phs.wnl())
        FNL = phs.B*sp.Matrix(list(phs.discdxHnl) + phs.znl())
        IF = list(varNL - FNL - Mxl - Mu)
        phs.ImpFunc = sp.Matrix(parallel_factorize(IF)) if parallelize \
            else sp.Matrix(IF)

        JacFnl = sp.zeros(phs.nxnl() + phs.nwnl(), phs.nxnl() + phs.nwnl())
        nlvar = phs.dxnl() + phs.wnl()
        for n in range(phs.nxnl()+phs.nwnl()):
            for m in range(phs.nxnl()+phs.nwnl()):
                el_Jac = phs.ImpFunc[n, 0].diff(nlvar[m])
                JacFnl[n, m] = sp.simplify(el_Jac)
        phs.JacFnl = sp.Matrix(JacFnl)

        phs.iJacFnl = sp.Matrix.inv(JacFnl, method='LU')

        Fnl = list((-phs.iJacFnl*sp.Matrix(phs.ImpFunc)))
        phs.Fnl = sp.Matrix(parallel_factorize(Fnl)) if parallelize \
            else sp.Matrix(Fnl)
        matImpFunc = sp.Matrix(phs.ImpFunc)
        phs.Fnl_residual = (matImpFunc.T*matImpFunc)[0, 0]
    else:
        phs.Fnl = []
        phs.Fnl_residual = []
        phs.isNL = False


def split_structure(phs):
    """
    Split Linear and Nonlinear parts.
    """

    phs.J1 = phs.Jx[:phs.nxl(), :phs.nxl()]
    phs.M1 = phs.Jx[:phs.nxl(), phs.nxl():]
    phs.J2 = phs.Jx[phs.nxl():, phs.nxl():]

    phs.K1 = phs.K[:phs.nxl(), :phs.nwl()]
    phs.K2 = phs.K[:phs.nxl(), phs.nwl():]
    phs.K3 = phs.K[phs.nxl():, :phs.nwl()]
    phs.K4 = phs.K[phs.nxl():, phs.nwl():]

    phs.G1 = phs.Gx[:phs.nxl(), :]
    phs.G2 = phs.Gx[phs.nxl():, :]

    phs.J3 = phs.Jw[:phs.nwl(), :phs.nwl()]
    phs.M2 = phs.Jw[:phs.nwl(), phs.nwl():]
    phs.J4 = phs.Jw[phs.nwl():, phs.nwl():]

    phs.G3 = phs.Gw[:phs.nwl(), :]
    phs.G4 = phs.Gw[phs.nwl():, :]

    #######################################################################

    phs.JJ = (phs.J - phs.J.T)/sp.sympify(2.)
    phs.RJ = (phs.J + phs.J.T)/sp.sympify(2.)

    #######################################################################

    if sum(phs.RJ) != sp.sympify(0):
        phs.PDJ = -(sp.Matrix(phs.discdxH + phs.z +
                              list(phs.Gains()*sp.Matrix(phs.u))).T *
                    phs.RJ*sp.Matrix(phs.discdxH + phs.z +
                    list(phs.Gains() * sp.Matrix(phs.u))))[0, 0]

    for n in range(phs.nt):

        u = phs.seq_u[n]
        p = phs.seq_p[p]

        dxl = dx[:nxl]
        dxnl = dx[nxl:]

        wnl = w[nwl:]

        if phs.isNL:
            VarNL = dxnl + wnl
            it = 0
            step = 1
            res = 1
            while ((it < nbit_NR) & (res > phs.numtol) &
                   (step > phs.numtol**2)):

                VarNL = [e1+e2 for (e1, e2) in
                         zip(VarNL, phs.Fnl_n(*(VarNL + x + u + pars)))]
                it += 1
                res = phs.Fnl_residual_n(*(VarNL + x + u + pars))

            dxnl, wnl = VarNL[:nxnl], VarNL[nxnl:]

        ###################################################################
        Varl = phs.Fl_n(*(x + dxnl + wnl + u + pars))
        print "Varl:", Varl
        dxl, wl = Varl[:nxl], Varl[nxl:]
        ###################################################################
        dx, w = dxl + dxnl, wl + wnl
        ###################################################################
        z = phs.z_n(*(x + w + pars))
        dxH = phs.dxH_n(*(x + dx + pars))
        ###################################################################
        y = phs.y_n(*(x + dx + w + u + pars))
        ###################################################################
        x = [sum(pair) for pair in zip(x, dx)]
        ###################################################################
        PdInStructure = phs.PDJ_n(*(x + dx + w + u + pars))

        phs.seq_x.append(x)
        phs.seq_dtx.append([e/float(ts) for e in dx])
        phs.seq_dxH.append(dxH)
        phs.seq_w.append(w)
        phs.seq_z.append(z)
        phs.seq_y.append(y)
        phs.SeqH.append(phs.H_n(*x+pars))
        phs.seq_pd.append(sum([e1*e2 for (e1, e2) in zip(z, w)]) +
                          PdInStructure)
        phs.seq_ps.append(sum([e1*e2 for (e1, e2) in zip(y, u)]))
        phs.seq_dtE.append(sum([e1*e2/float(ts)
                                for (e1, e2) in zip(dxH, dx)]))


