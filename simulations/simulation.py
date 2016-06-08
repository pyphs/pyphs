# -*- coding: utf-8 -*-
"""
Created on Tue May 24 11:20:26 2016

@author: Falaize
"""
from misc.io import write_data
from misc.tools import progressbar
from config import standard_config
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

        if not hasattr(phs, 'nums'):
            phs.build_nums()

        if isinstance(sequ, (list, tuple)):
            nt = len(sequ)
        elif isinstance(seqp, (list, tuple)):
            nt = len(seqp)
        else:
            assert nt is not None, 'Unknown number of \
    iterations. Please tell either seq_u (input sequence), seq_p \
    (sequence of parameters) or nt (number of time steps).'
            assert isinstance(nt, int), 'number of time steps in not int, \
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


