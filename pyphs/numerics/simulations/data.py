# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 10:22:56 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

from pyphs.misc.signals.waves import wavwrite
from pyphs.misc.plots.data import plot, plot_powerbal
import os
import numpy
from pyphs.numerics.tools import lambdify
from pyphs.misc.tools import find
from pyphs.core.tools import free_symbols
from pyphs.config import VERBOSE
import h5py


try:
    import itertools.izip as zip
except ImportError:
    pass


class BaseData:
    """
    =======
    Data
    =======

    Interface for pyphs.Simulation data files.

    Generators
    -----------
    t:
        Generator of simulation time values computed from simulation
        configuration.
    x, dx, dxH, w, z, u, y, p:
        Read from files in the folder specified by the simulation
        configuration.
    E, dtE, ps, pd:
        Compute the discrete energy's time variation, dissipated power, and
        sources power (respectively).
    wavewrite:
        Export data to wave file.
    plot:
        Plot selected data.
    plot_powerbal:
        Plot the power balance.
    """

    # ----------------------------------------------------------------------- #

    def __init__(self, method, config):

        if VERBOSE >= 1:
            print('Build data i/o...')

        # init configuration options
        self.config = config

        # init method
        self.method = method

    # ----------------------------------------------------------------------- #
    # fs
    def get_fs(self):
        return self.config['fs']

    fs = property(get_fs)

    # ----------------------------------------------------------------------- #
    # nt
    def get_nt(self):
        return self.config['nt']

    nt = property(get_nt)

    # ----------------------------------------------------------------------- #
    # ntplot
    ntplot = 1000

    # ----------------------------------------------------------------------- #
    # imin
    def get_imin(self):
        i = self.config['load']['imin']
        if i is None:
            return 0
        else:
            return i

    def set_imin(self, i):
        if i is None:
            self.config['load']['imin'] = i
        else:
            if not 0 <= i < self.imax:
                text = 'imin must be in [0, {0}].'
                raise ValueError(text.format(self.imax-1))
            if not isinstance(i, (int, float)):
                text = 'imin must be a positive integer: %s.' % str(i)
                raise ValueError(text)
            self.config['load']['imin'] = int(i)

    imin = property(get_imin, set_imin)

    # ----------------------------------------------------------------------- #
    # imax
    def get_imax(self):
        i = self.config['load']['imax']
        if i is None:
            return self.nt
        else:
            return i

    def set_imax(self, i):
        if i is None:
            self.config['load']['imax'] = i
        else:
            if not self.imin < i <= self.nt:
                text = 'imax must be in [{0}, {1}].'
                raise ValueError(text.format(self.imin+1, self.nt))
            if not isinstance(i, (int, float)):
                text = 'imax must be a positive integer: %s.' % str(i)
                raise ValueError(text)
            self.config['load']['imax'] = int(i)

    imax = property(get_imax, set_imax)

    # ----------------------------------------------------------------------- #
    # tmin
    def get_tmin(self):
        return self.imin/float(self.fs)

    def set_tmin(self, t):
        if t is None:
            self.imin = t
        else:
            tmin = 0.
            tmax = self.tmax
            if not tmin <= t <= tmax:
                text = 'tmin must be in [{0}, {1}].'
                raise ValueError(text.format(tmin, tmax))
            if not isinstance(t, (int, float)):
                text = 'tmin must be a positive value: %s.' % str(t)
                raise ValueError(text)
            imin = int(t*self.fs)
            self.imin = imin

    tmin = property(get_tmin, set_tmin)

    # ----------------------------------------------------------------------- #
    # tmax

    def get_tmax(self):
        return (self.imax-1)/float(self.fs)

    def set_tmax(self, t):
        if t is None:
            self.imax = t
        else:
            tmin = self.tmin
            tmax = (self.nt-1)*self.fs
            if not tmin <= t <= tmax:
                text = 'tmax must be in [{0}, {1}].'
                raise ValueError(text.format(tmin, tmax))
            if not isinstance(t, (int, float)):
                text = 'tmax must be a positive value: %s.' % str(t)
                raise ValueError(text)
            self.imax = int(t*self.fs)+1

    tmax = property(get_tmax, set_tmax)

    # ----------------------------------------------------------------------- #
    # decim

    def get_decim(self):
        return self.config['load']['decim']

    def set_decim(self, i):
        if i is None:
            self.config['load']['decim'] = 1
        else:
            if not 1 <= i or not isinstance(i, (int, float)):
                text = 'decim must be a strictly positive integer.'
                raise ValueError(text)
            self.config['load']['decim'] = int(i)

    decim = property(get_decim, set_decim)

    # ----------------------------------------------------------------------- #

    def subs(self):
        d = self.method.subs.copy()
        d[self.method.fs] = self.fs
        return d

    # ----------------------------------------------------------------------- #

    def __init_data__(self, sequ=None, seqp=None, nt=None):
        """
        Initialize the object and save the sequences for input u, parameters p
        and state initialisation x0 to files in the folder specified by the
        simulation configuration.

        Parameters
        ----------

        sequ: iterable or None, optional
            Input sequence wich elements are arrays with shape (dims.y(), ). If
            the lenght nt of the sequence is known (e.g. sequ is a list), the
            number of simulation time steps is set to nt. If None, a sequence
            with length nt of zeros with appropriate shape is used (default).

        seqp: iterable or None, optional
            Input sequence wich elements are arrays with shape (dims.p(), ). If
            (i) the lenght of sequ is not known, and (ii) the length nt of seqp
            is known (e.g. seqp is a list), the number of simulation time steps
            is set to nt=len(seqp). If None, a sequence with length nt of zeros
            with appropriate shape is used (default).

        nt: int or None:
            Number of time steps. If None, the lenght of either sequ or seqp
            must be known (default).

        """
        # get number of time-steps
        if nt is None:
            if hasattr(sequ, '__len__'):
                nt = len(sequ)
            elif hasattr(seqp, '__len__'):
                nt = len(seqp)
            else:
                raise ValueError("""Unknown number of iterations.
Please give either a list u (input sequence), a list p (sequence of parameters)
or an integer nt (number of time steps).'
    """)

        self.config['nt'] = nt = int(nt)
        
        # if sequ is not provided, a sequence of [[0]*ny]*nt is assumed
        if sequ is None:
            dimy = self.method.dims.y()
            value = [0,] * dimy if dimy > 0 else []
            sequ = (value for _ in range(nt))

        # if seqp is not provided, a sequence of [[0]*np]*nt is assumed
        if seqp is None:
            dimp = self.method.dims.p()
            value = [0,] * dimp if dimp > 0 else []
            seqp = (value for _ in range(nt))

        return sequ, seqp, nt

    # ----------------------------------------------------------------------- #

    def wavwrite(self, name, index, path=None, gain=1.,
                 fs=None, normalize=True, timefades=0.):
        """
        wavwrite
        ========

        Write data to wave file.

        Parameters
        ----------
        name: str
            Name of the data generator to export (e.g. 'x', 'y', 'dxH').

        index: int
            Index of the component of the data generator to read (e.g. if name
            is 'x' and index is 0, the signal is x[index]).

        path: str or None, optional
            Raw path to the generated wave file. Notice '.wav' is appended by
            default. If None, the simulation path and the data generator name
            is used (default).

        gain: float, optional
            Gain applied to the signal before writing to file. Default is 1.

        fs: float or None, optional
            Sample rate for the generated wave file. Resampling is performed
            with scipy.signal.resample. If None, the simulation samplerate is
            use (default).

        normalize: Bool
            If True, the signal is normalised by the maximum absolute value.
            Default is False.

        timefades: float, optional
            Fade-in and fade-out time to avoid clics. Default is 0.

        See also
        ---------
        pyphs.misc.signals.waves.wavwrite

        """
        if fs is None:
            fs = self.fs
        if path is None:
            path = self.config['path'] + os.sep + name + str(index)
        print(path)
        args = {'ind': index,
                'imin': self.imin, 'imax': self.imax, 'decim': 1,
                'postprocess': lambda e: gain*e}
        sig = getattr(self, name)(**args)
        wavwrite(sig, self.fs, path,
                 fs_out=fs, normalize=normalize, timefades=timefades)

    # ----------------------------------------------------------------------- #

    def plot_powerbal(self, mode='single', DtE='deltaH',
                      show=True, **loadopts):
        """
        Plot the power balance. mode is 'single' or 'multi' for single figure
        or multifigure (default is 'single').

        Parameters
        -----------
        imin: int or None, optional
            Starting index. If None, imin=0 (default).
        imax: int or None,
            Stoping index. If None, imax=data.nt (default).
        decim: int or None,
            decimation factor. If None, decim = int(data.nt/1000)
            (default).

        """
        options = self.config['load'].copy()
        options.update(loadopts)
        if 'decim' not in loadopts:
            options['decim'] = max((1, (self.imax-self.imin)//self.ntplot))
        plot_powerbal(self, mode=mode, DtE=DtE, show=show, **options)

    # ----------------------------------------------------------------------- #

    def plot(self, vars, show=True, label=None, **loadopts):
        """
        Plot simulation data

        Parameters
        ----------

        vars : list
            List of variables to plot. Elements can be a single string name or
            a tuples of strings (name, index). For each string element, every
            indices of variable name are ploted. For each tuple element, the
            element index of variable name is ploted.

        load : dict
            dictionary of signal load options, with keys
                * 'imin': starting index,
                * 'imax': stoping index,
                * 'decim': decimation factor.

        show : bool
            Acivate the call to matplotlib.pyplot.show

        """
        options = self.config['load'].copy()
        options.update(loadopts)
        if 'decim' not in loadopts:
            options['decim'] = max((1, (self.imax-self.imin)//self.ntplot))
        plot(self, vars, show=show, label=label, **options)

    # ----------------------------------------------------------------------- #

    __doc_template__ = """
    {0}
    ====

    Reader for simulation data {0} from file:\n{1}

    Parameters
    -----------
    ind: int or None, optional
        Index for the returned value {0}[ind]. If None, the full vector is
        returned (default).
    imin: int or None, optional
        Starting index. If None, imin=0 (default).
    imax: int or None,
        Stoping index. If None, imax=Inf (default).
    decim: int or None,
        decimation factor

    Returns
    -------

    {0}_generator: generator
        A python generator of value {0}[ind][i] for each time step i starting
        from index imin to index imax with decimation factor decim (i.e. the
        value is generated if i-imin % decim == 0).
    """

    def _build_generators(self):
        """
        Build most generators that read from txt files and render data.
        """

        # ------------------------------------------------------------------- #

        names = ['x', 'dx', 'w', 'u', 'p', 'y', 'dxH', 'z']
        for name in names:
            setattr(self, name, self.build_generator(name))


    # ----------------------------------------------------------------------- #

    def t(self, **loadopts):
        """
        t
        =

        Generator of simulation times values.

        Parameters
        -----------
        imin: int or None, optional
            Starting index. If None, imin=0 (default).
        imax: int or None,
            Stoping index. If None, imax=data.nt (default).
        decim: int or None,
            decimation factor

        Returns
        -------

        t_generator: generator
            A python generator of scalar time value t[i] for each time step i
            starting from index imin to index imax with decimation factor decim
            (i.e. the value is generated if i-imin % decim == 0).
        """
        options = self.config['load'].copy()
        options.update(loadopts)

        if options['imin'] is None:
            options['imin'] = 0
        if options['imax'] is None:
            options['imax'] = float('Inf')
        if options['decim'] is None:
            options['decim'] = 1

        def generator():
            for n in range(self.nt):
                yield n/self.fs
        i = 0
        for el in generator():
            if (options['imin'] <= i < options['imax'] and
                    not bool(i % options['decim'])):
                yield el
            i += 1

    # ----------------------------------------------------------------------- #

    def dtE(self, DtE='DxhDtx', **loadopts):
        """
        dtE
        ===

        Generator of discrete energy's time variation values.

        Parameters
        -----------
        imin: int or None, optional
            Starting index. If None, imin=0 (default).
        imax: int or None,
            Stoping index. If None, imax=data.nt (default).
        decim: int or None,
            decimation factor. If None, decim = 1 (default).
        DtE: str in {'deltaH', 'DxhDtx'}, optional
            Method for the computation of discrete energy's time variation. If
            DtE is 'deltaH', the output with index i is
            (H[t[i+1]]-H[t[i]]) * samplerate. If DtE is 'DxhDtx', the output
            with index i is (dxH[i] dot dtx[i]).

        Returns
        -------

        dtE_generator: generator
            A python generator of scalar discrete energy's time variation value
            DtE[i] for each time step i starting from index imin to index imax
            with decimation factor decim (i.e. the value is generated if
            i-imin % decim == 0).
        """
        options = self.config['load'].copy()
        options.update(loadopts)

        if DtE == 'deltaH':
            H_expr = self.method.H.subs(self.method.subs)
            H_symbs = free_symbols(H_expr)
            H_args, H_inds = find(H_symbs, self.method.args())
            H = lambdify(H_args, H_expr, theano=self.config['theano'])
            H_args = lambdify(self.method.args(), H_args,
                              theano=self.config['theano'])

            Hpost_expr = self.method.H.subs(self.subs())
            subs = {}
            for x, dx in zip(self.method.x, self.method.dx()):
                subs.update({x: x+dx})

            Hpost_expr = Hpost_expr.subs(subs)
            Hpost_symbs = free_symbols(Hpost_expr)
            Hpost_args, Hpost_inds = find(Hpost_symbs, self.method.args())
            Hpost = lambdify(Hpost_args, Hpost_expr,
                             theano=self.config['theano'])
            Hpost_args = lambdify(self.method.args(), Hpost_args,
                                  theano=self.config['theano'])
            for args, o in zip(self.args(**options), self.o(**options)):
                a = (list(args)+list(o))
                yield (Hpost(*Hpost_args(*a)) -
                       H(*H_args(*a)))*self.fs

        elif DtE == 'DxhDtx':
            for dtx, dxh in zip(self.dtx(**options), self.dxH(**options)):
                yield scalar_product(dtx, dxh)

    # ----------------------------------------------------------------------- #

    def E(self, **loadopts):
        """
        E
        ===

        Generator of discrete energy's values.

        Parameters
        -----------
        imin: int or None, optional
            Starting index. If None, imin=0 (default).
        imax: int or None,
            Stoping index. If None, imax=data.nt (default).
        decim: int or None,
            decimation factor. If None, decim = 1 (default).

        Returns
        -------

        E_generator: generator
            A python generator of scalar discrete energy's value E[i] for each
            time step i starting from index imin to index imax with decimation
            factor decim (i.e. the value is generated if i-imin % decim == 0).
        """
        options = self.config['load'].copy()
        options.update(loadopts)

        H_expr = self.method.H.subs(self.method.subs)
        H_symbs = free_symbols(H_expr)
        H_args, H_inds = find(H_symbs, self.method.args())
        H = lambdify(H_args, H_expr, theano=self.config['theano'])
        H_args = lambdify(self.method.args(), H_args,
                          theano=self.config['theano'])

        for args, o in zip(self.args(**options), self.o(**options)):
            a = (list(args)+list(o))
            yield H(*H_args(*a))

    # ----------------------------------------------------------------------- #

    def pd(self, **loadopts):
        """
        pd
        ==

        Generator of discrete dissipated power values.

        Parameters
        -----------
        imin: int or None, optional
            Starting index. If None, imin=0 (default).
        imax: int or None,
            Stoping index. If None, imax=data.nt (default).
        decim: int or None,
            decimation factor. If None, decim = 1 (default).

        Returns
        -------

        pd_generator: generator
            A python generator of scalar discrete dissipated power value pd[i]
            for each time step i starting from index imin to index imax with
            decimation factor decim (i.e. the value is generated if
            i-imin % decim == 0), with pd[i] = w[i] dot z[i].
        """
        options = self.config['load'].copy()
        options.update(loadopts)

        R_expr = self.method.R().subs(self.subs())

        R_symbs = free_symbols(R_expr)

        R_args, R_inds = find(R_symbs, self.method.args())

        R = lambdify(R_args, R_expr, theano=self.config['theano'])
        R_args = lambdify(self.method.args(), R_args,
                          theano=self.config['theano'])
        for w, z, a, b, args, o in zip(self.w(**options),
                                       self.z(**options),
                                       self.a(**options),
                                       self.b(**options),
                                       self.args(**options),
                                       self.o(**options)):
            yield scalar_product(w, z) + \
                scalar_product(a,
                               a,
                               R(*R_args(*(list(args)+list(o)))))

    # ----------------------------------------------------------------------- #

    def ps(self, **loadopts):
        """
        ps
        ==

        Generator of discrete sources power values.

        Parameters
        -----------
        imin: int or None, optional
            Starting index. If None, imin=0 (default).
        imax: int or None,
            Stoping index. If None, imax=data.nt (default).
        decim: int or None,
            decimation factor. If None, decim = 1 (default).

        Returns
        -------

        ps_generator: generator
            A python generator of scalar discrete sources power value ps[i]
            for each time step i starting from index imin to index imax with
            decimation factor decim (i.e. the value is generated if
            i-imin % decim == 0), with ps[i] = u[i] dot y[i].
        """
        options = self.config['load'].copy()
        options.update(loadopts)

        for u, y in zip(self.u(**options),
                        self.y(**options)):
            yield scalar_product(u, y)

    # ----------------------------------------------------------------------- #

    def o(self, ind=None, **loadopts):
        """
        o
        ==

        Generator of values for observers.

        Parameters
        -----------
        ind: int or None, optional
            Index of the observer. If None, values for every observers are
            returned (default).
        imin: int or None, optional
            Starting index. If None, imin=0 (default).
        imax: int or None,
            Stoping index. If None, imax=data.nt (default).
        decim: int or None,
            decimation factor. If None, decim = 1 (default).

        Returns
        -------

        ps_generator: generator
            A python generator of scalar discrete sources power value ps[i] for
            each time step i starting from index imin to index imax with
            decimation factor decim (i.e. the value is generated if
            i-imin % decim == 0), with ps[i] = u[i] dot y[i].
        """
        options = self.config['load'].copy()
        options.update(loadopts)

        obs_expr = [e.subs(self.subs())
                    for e in self.method.observers.values()]

        obs_symbs = free_symbols(obs_expr)
        index = len(self.method.args())-len(obs_expr)

        obs_args, obs_inds = find(obs_symbs, self.method.args()[:index])

        obs = lambdify(obs_args, obs_expr, theano=self.config['theano'])
        obs_args = lambdify(self.method.args()[:index], obs_args,
                            theano=self.config['theano'])

        if ind is None:
            for arg in self.args(**options):
                yield obs(*obs_args(*arg))
        else:
            for arg in self.args(**options):
                yield obs(*obs_args(*arg))[ind]

    # ----------------------------------------------------------------------- #

    def args(self, ind=None, **loadopts):
        """
        args
        ====

        Generator of values for arguments of numerical functions
        args=(x, dx, w, u, p).

        Parameters
        -----------
        ind: int or None, optional
            Index for the returned value args[ind]. If None, the full arguments
            vector is returned (default).
        imin: int or None, optional
            Starting index. If None, imin=0 (default).
        imax: int or None,
            Stoping index. If None, imax=data.nt (default).
        decim: int or None,
            decimation factor. If None, decim = 1 (default)

        Returns
        -------

        args_generator: generator
            A python generator of arguments of numerical functions value
            args[ind][i] for each time step i starting from index imin to index
            imax with decimation factor decim (i.e. the value is generated if
            i-imin % decim == 0).
        """
        options = self.config['load'].copy()
        options.update(loadopts)

        for x, dx, w, u, p in zip(self.x(**options),
                                  self.dx(**options),
                                  self.w(**options),
                                  self.u(**options),
                                  self.p(**options)):
            arg = x + dx + w + u + p
            if ind is None:
                yield arg
            else:
                yield arg[ind]

    # ----------------------------------------------------------------------- #

    def dtx(self, ind=None, **loadopts):
        """
        dtx
        ====

        Generator of state vector time variation values dtx ~ dx * samplerate.

        Parameters
        -----------
        ind: int or None, optional
            Index for the returned value dx[ind] * samplerate. If None, the
            full state vector variation dx[:] * samplerate is returned
            (default).
        imin: int or None, optional
            Starting index. If None, imin=0 (default).
        imax: int or None,
            Stoping index. If None, imax=data.nt (default).
        decim: int or None,
            decimation factor. If None, decim = 1 (default).

        Returns
        -------

        dtx_generator: generator
            A python generator of state vector time variation
            dx[ind][i] * samplerate for each time step i starting from index
            imin to index imax with decimation factor decim (i.e. the value is
            generated if i-imin % decim == 0).

        See Also
        ---------
        x, dx
        """

        options = self.config['load'].copy()
        options.update(loadopts)

        def dxtodtx(dx):
            return numpy.asfarray(dx)*self.fs

        for dtx in self.dx(postprocess=dxtodtx, ind=ind, **options):
            yield dtx

    # ----------------------------------------------------------------------- #

    def a(self, ind=None, **loadopts):
        """
        a
        =

        Generator of values for components of vector a in the core
        port-Hamiltonian structure b = J dot a, i.e. a = (dxH, z, u).

        Parameters
        -----------
        ind: int or None, optional
            Index for the returned value a[ind]. If None, the full vector is
            returned (default).
        imin: int or None, optional
            Starting index. If None, imin=0 (default).
        imax: int or None,
            Stoping index. If None, imax=data.nt (default).
        decim: int or None,
            decimation factor. If None, decim = 1 (default).

        Returns
        -------

        a_generator: generator
            A python generator of arguments of numerical functions value
            a[ind][i] for each time step i starting from index imin to index
            imax with decimation factor decim (i.e. the value is generated if
            i-imin % decim == 0).

        See also
        --------

        b

        """
        options = self.config['load'].copy()
        options.update(loadopts)

        for dxH, z, u in zip(self.dxH(**options),
                             self.z(**options),
                             self.u(**options)):
            if ind is None:
                yield dxH + z + u
            else:
                yield (dxH + z + u)[ind]

    # ----------------------------------------------------------------------- #

    def b(self, ind=None, **loadopts):
        """
        b
        =

        Generator of values for components of vector b in the core
        port-Hamiltonian structure b = J dot a, i.e. b = (dtx, w, y).

        Parameters
        -----------
        ind: int or None, optional
            Index for the returned value b[ind]. If None, the full vector is
            returned (default).
        imin: int or None, optional
            Starting index. If None, imin=0 (default).
        imax: int or None,
            Stoping index. If None, imax=data.nt (default).
        decim: int or None,
            decimation factor. If None, decim = 1 (default).

        Returns
        -------

        b_generator: generator
            A python generator of arguments of numerical functions value
            b[ind][i] for each time step i starting from index imin to index
            imax with decimation factor decim (i.e. the value is generated if
            i-imin % decim == 0).

        See also
        --------

        a

        """
        options = self.config['load'].copy()
        options.update(loadopts)

        for dtx, w, y in zip(self.dtx(**options),
                             self.w(**options),
                             self.y(**options)):
            if ind is None:
                yield list(dtx) + list(w) + list(y)
            else:
                yield [list(dtx) + list(w) + list(y)][ind]


class ASCIIData(BaseData):
    def init_data(self, sequ=None, seqp=None, nt=None):
        sequ, seqp, nt = BaseData.__init_data__(self, sequ, seqp, nt)
        # write input sequence
        self.write_data(self.config['path']+os.sep+'data', sequ, 'u')

        # write parameters sequence
        self.write_data(self.config['path']+os.sep+'data', seqp, 'p')
        self._build_generators()
    
    init_data.__doc__ = BaseData.__init_data__.__doc__

    def write_data(self, path, seq, var):
        if not os.path.exists(path):
            os.makedirs(path)
        with open(path + os.sep + var + '.txt', 'w') as _file:
            for el in seq:
                _file.write(list2str(el))

    def build_generator(self, name):
        "Build data_generator from data name."
        filename = os.path.join(self.config['path'], name + '.txt')
        default = self.config['load']

        def data_generator(**kwargs):
            """
            Generator that read file from path. Each line is returned as a list of
            floats, if index i is such that imin <= i < imax, with decimation factor
            decim. A function can be passed as postprocess, to be applied on each
            output.
            """
            imin = kwargs.get('imin', default['imin'])
            imax = kwargs.get('imax', default['imax'])
            decim = kwargs.get('decim', default['decim'])
            ind = kwargs.get('ind', None)
            postprocess = kwargs.get('postprocess', None)

            if ind is not None and not isinstance(ind, int):
                raise ValueError('Index should be an integer,not {0}'.format(type(ind)))

            with open(filename, "r") as f:
                for i, line in enumerate(f):
                    if (i < imin) or (imax <= i) or ((i - imin) % decim > 0):
                        continue
                    if ind is None:
                        # export full line
                        out = [float(x) for x in line.split()]
                        if postprocess is not None:
                            out = [postprocess(el) for el in out]
                        yield out
                    else:
                        # export selected index in line
                        out = float(line.split()[ind])
                        yield out if postprocess is None else postprocess(out)

        data_generator.__doc__ = self.__doc_template__.format(name, filename)
        return data_generator


# --------------------------------------------------------------------------- #

class h5Data(BaseData):
    def __init__(self, method, config, h5name='results.h5'):
        BaseData.__init__(self, method, config)
        self.h5filename = os.path.join(self.config['path'], 'data', h5name)
        self.h5file = h5py.File(self.h5filename, 'w')
        self._build_generators()

    def init_data(self, sequ=None, seqp=None, nt=None):
        sequ, seqp, nt = BaseData.__init_data__(self, sequ, seqp, nt)

        # Total number of samples to write for each time step
        vars = ['u', 'p'] + list(self.config['files'])
        dimvars = []
        for name in vars:
            val = self.method.inits_evals[name]
            if len(val.shape) == 0:
                dim = 1
            else:
                dim = val.shape[0]
            dimvars.append(dim)

        # Offsets defining the first element of each variable
        self.offsets = [sum(dimvars[:n]) for n in range(len(vars) + 1)]
        total = self.offsets[-1]

        # Define compound datatype
        names = ['%s%d' % (var, n) for var, l in zip(vars, dimvars)
                                   for n in range(l)]
        dt = numpy.dtype({
            'names': names,
            'formats': [numpy.float64,] * total})

        # Create a global dataset
        glob = self.h5file.create_dataset('_global', dtype=dt, shape=(self.nt,))
        glob[:] = numpy.zeros(self.nt, dtype=dt)

        # Write input and parameter data in HDF5 file
        dimu = self.method.dims.y()
        if dimu:
            tmp = numpy.vstack(sequ)
            offset = self.offsets[0]
            for n in range(dimu):
                glob[:, 'u%d' % n] = tmp[:, n] 

        dimp = self.method.dims.p()
        if dimp:
            tmp = numpy.vstack(seqp)
            offset = self.offsets[1]
            for n in range(dimp):
                glob[:, 'p%d' % n] = tmp[:, n]


        self.h5file.close()
    
    init_data.__doc__ = BaseData.__init_data__.__doc__

    def build_generator(self, name):
        "Build data_generator from data name."
        default = self.config['load']

        def data_generator(ind=None, **kwargs):
            """
            Generator that read file from path. Each line is returned as a list of
            floats, if index i is such that imin <= i < imax, with decimation factor
            decim. A function can be passed as postprocess, to be applied on each
            output.
            """
            imin = kwargs.get('imin', default['imin'])
            imax = kwargs.get('imax', default['imax'])
            decim = kwargs.get('decim', default['decim'])
            postprocess = kwargs.get('postprocess', None)

            if ind is not None:
                if not isinstance(ind, int):
                    raise ValueError('Index should be an integer,not {0}'.format(type(ind)))
                ind = name + str(ind)
            else:
                if name in ('x', 'dx', 'dxH'):
                    dim = self.method.dims.x()
                elif name in ('u', 'y'):
                    dim = self.method.dims.y()
                elif name in ('w', 'z'):
                    dim = self.method.dims.w()
                else:
                    dim = getattr(self.method.dims, name)()
                ind = [name + str(n) for n in range(dim)]
            
            with h5py.File(self.h5filename, "r", swmr=True) as h5file:
                data = h5file['_global'][imin:imax:decim]
                if len(ind) == 0:
                    return
                data = data[ind]
                print("Called generator for %s (shape: %s, %s)" % (name, data.shape, data.dtype))
                for el in  data:
                    if postprocess:
                        el = postprocess(el)
                    yield el

        data_generator.__doc__ = self.__doc_template__.format(name, self.h5filename)
        return data_generator

    # ----------------------------------------------------------------------- #

    def args(self, **kwargs):
        """
        args
        ====

        Generator of values for arguments of numerical functions
        args=(x, dx, w, u, p).

        Parameters
        -----------
        ind: int or None, optional
            Index for the returned value args[ind]. If None, the full arguments
            vector is returned (default).
        imin: int or None, optional
            Starting index. If None, imin=0 (default).
        imax: int or None,
            Stoping index. If None, imax=data.nt (default).
        decim: int or None,
            decimation factor. If None, decim = 1 (default)

        Returns
        -------

        args_generator: generator
            A python generator of arguments of numerical functions value
            args[ind][i] for each time step i starting from index imin to index
            imax with decimation factor decim (i.e. the value is generated if
            i-imin % decim == 0).
        """
##        options = self.config['load'].copy()
##        options.update(loadopts)

##        for x, dx, w, u, p in zip(self.x(**options),
##                                  self.dx(**options),
##                                  self.w(**options),
##                                  self.u(**options),
##                                  self.p(**options)):
##            arg = x + dx + w + u + p
##            if ind is None:
##                yield arg
##            else:
##                yield arg[ind]

        default = self.config['load']
        imin = kwargs.get('imin', default['imin'])
        imax = kwargs.get('imax', default['imax'])
        decim = kwargs.get('decim', default['decim'])
        postprocess = kwargs.get('postprocess', None)
        dimx, dimu, dimw, dimp = [getattr(self.method.dims, el)()
                                  for el in 'xywp']
        ind = ['x%d' % n for n in range(dimx)] \
            + ['dx%d' % n for n in range(dimx)] \
            + ['w%d' % n for n in range(dimw)] \
            + ['u%d' % n for n in range(dimu)] \
            + ['p%d' % n for n in range(dimp)]
        print('Called generator for args', kwargs)
            
        with h5py.File(self.h5filename, "r", swmr=True) as h5file:
            data = h5file['_global'][imin:imax:decim]
            for el in data[ind]:
                if postprocess:
                    value = postprocess(el)
                else:
                    value = el
                yield value

# --------------------------------------------------------------------------- #

Data = h5Data

def scalar_product(list1, list2, weight_matrix=None):
    list1, list2 = list(list1), list(list2)
    if weight_matrix is not None:
        return numpy.einsum('i,ij,j',
                            numpy.array(list1),
                            weight_matrix,
                            numpy.array(list2))
    else:
        return numpy.einsum('i,i',
                            numpy.array(list1),
                            numpy.array(list2))
