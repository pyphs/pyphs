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
    # converters

    def time2index(self, t, m='min'):
        """

        Convert time value to time index.

        Parameters
        ----------

        t: float
            Time value

        m: str (optional)
            Output mode in {'min', 'max'}, corresponding to floor and ceil
            value repsectively.

        Return
        ------

        i: int
            Time index.

        """
        if m == 'min':
            return int(t*self.fs)
        elif m == 'max':
            return int(t*self.fs)+1
        else:
            raise ValueError('unknown m={}'.format(m))

    def index2time(self, i, m='min'):
        """

        Convert time index to time value.

        Parameters
        ----------

        i: int
            Time index.

        m: str (optional)
            Output mode in {'min', 'max'}, corresponding to floor and ceil
            value repsectively.

        Return
        ------

        t: float
            Time value

        """
        if m == 'min':
            return i/float(self.fs)
        elif m == 'max':
            return (i-1)/float(self.fs)
        else:
            raise ValueError('unknown m={}'.format(m))

    # ----------------------------------------------------------------------- #
    # tmin
    def get_tmin(self):
        return self.index2time(self.imin, m='min')

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
        self.imin = self.time2index(t, m='min')

    tmin = property(get_tmin, set_tmin)

    # ----------------------------------------------------------------------- #
    # tmax

    def get_tmax(self):
        return self.index2time(self.imin, m='max')

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
            self.imax = self.time2index(t, m='max')

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

            def generator_sequ():
                value = [0, ] * dimy if dimy > 0 else []
                for _ in range(nt):
                    yield value

            sequ = generator_sequ()

        # if seqp is not provided, a sequence of [[0]*np]*nt is assumed
        if seqp is None:
            dimp = self.method.dims.p()

            def generator_seqp():
                value = [0, ] * dimp if dimp > 0 else []
                for _ in range(nt):
                    yield value

            seqp = generator_seqp()

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
        if not self._open:
            self.open()
            close = True
        else:
            close = False

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

        if not self._open:
            self.open()
            close = True
        else:
            close = False

        if 'decim' not in loadopts:
            options['decim'] = max((1, (self.imax-self.imin)//self.ntplot))
        plot_powerbal(self, mode=mode, DtE=DtE, show=show, **options)

        if close:
            self.close()

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
        if not self._open:
            self.open()
            close = True
        else:
            close = False

        options = self.config['load'].copy()
        options.update(loadopts)
        if 'decim' not in loadopts:
            options['decim'] = max((1, (self.imax-self.imin)//self.ntplot))
        plot(self, vars, show=show, label=label, **options)

        if close:
            self.close()

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

    def _build_options(self, loadopts):
        """
        Return a dictionary of load options imin, imax and decim.
        """

        options = self.config['load'].copy()
        options.update(loadopts)

        if options['imin'] is None:
            options['imin'] = 0
        if options['imax'] is None:
            options['imax'] = self.nt
        if options['decim'] is None:
            options['decim'] = 1
        if 'tmin' in loadopts:
            options['imin'] = self.time2index(options.pop('tmin'), m='min')
        if 'tmax' in loadopts:
            options['imax'] = self.time2index(options.pop('tmax'), m='max')

        return options

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

        options = self._build_options(loadopts)

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

        options = self._build_options(loadopts)

        if not self._open:
            self.open()
            close = True
        else:
            close = False

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

        if close:
            self.close()

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

        options = self._build_options(loadopts)

        if not self._open:
            self.open()
            close = True
        else:
            close = False

        H_expr = self.method.H.subs(self.method.subs)
        H_symbs = free_symbols(H_expr)
        H_args, H_inds = find(H_symbs, self.method.args())
        H = lambdify(H_args, H_expr, theano=self.config['theano'])
        H_args = lambdify(self.method.args(), H_args,
                          theano=self.config['theano'])

        for args, o in zip(self.args(**options), self.o(**options)):
            a = (list(args)+list(o))
            yield H(*H_args(*a))

        if close:
            self.close()

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

        options = self._build_options(loadopts)

        if not self._open:
            self.open()
            close = True
        else:
            close = False

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

        if close:
            self.close()

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

        options = self._build_options(loadopts)

        if not self._open:
            self.open()
            close = True
        else:
            close = False

        for u, y in zip(self.u(**options),
                        self.y(**options)):
            yield scalar_product(u, y)

        if close:
            self.close()

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

        options = self._build_options(loadopts)

        if not self._open:
            self.open()
            close = True
        else:
            close = False

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

        if close:
            self.close()

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

        options = self._build_options(loadopts)

        if not self._open:
            self.open()
            close = True
        else:
            close = False

        for x, dx, w, u, p in zip(self.x(**options),
                                  self.dx(**options),
                                  self.w(**options),
                                  self.u(**options),
                                  self.p(**options)):
            arg = numpy.hstack((x, dx, w, u, p))
            if ind is None:
                yield arg
            else:
                yield arg[ind]

        if close:
            self.close()

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

        options = self._build_options(loadopts)

        if not self._open:
            self.open()
            close = True
        else:
            close = False

        def dxtodtx(dx):
            return numpy.asfarray(dx)*self.fs

        for dtx in self.dx(postprocess=dxtodtx, ind=ind, **options):
            yield dtx

        if close:
            self.close()

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

        options = self._build_options(loadopts)

        if not self._open:
            self.open()
            close = True
        else:
            close = False

        for dxH, z, u in zip(self.dxH(**options),
                             self.z(**options),
                             self.u(**options)):
            if ind is None:
                yield numpy.hstack((dxH, z, u))
            else:
                yield numpy.hstack((dxH, z, u))[ind]

        if close:
            self.close()

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

        if not self._open:
            self.open()
            close = True
        else:
            close = False

        for dtx, w, y in zip(self.dtx(**options),
                             self.w(**options),
                             self.y(**options)):
            if ind is None:
                yield numpy.hstack((dtx, w, y))
            else:
                yield numpy.hstack((dtx, w, y))[ind]

        if close:
            self.close()


class ASCIIData(BaseData):

    # -------------------------------------------------------------------------
    def init_data(self, sequ=None, seqp=None, nt=None):

        sequ, seqp, nt = BaseData.__init_data__(self, sequ, seqp, nt)
        # write input sequence
        self.write_data(self.config['path']+os.sep+'data', sequ, 'u')

        # write parameters sequence
        self.write_data(self.config['path']+os.sep+'data', seqp, 'p')

        self._build_generators()

    init_data.__doc__ = BaseData.__init_data__.__doc__

    # -------------------------------------------------------------------------

    def write_data(self, path, seq, var):
        if not os.path.exists(path):
            os.makedirs(path)
        with open(path + os.sep + var + '.txt', 'w') as _file:
            for el in seq:
                _file.write(list2str(el))

    # -------------------------------------------------------------------------

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

class HDFData(BaseData):

    # global data name
    dname = 'global'

    # ----------------------------------------------------------------------- #

    def __init__(self, method, config, h5name='results.h5', clear=False):

        # BaseData
        BaseData.__init__(self, method, config)

        # HDF5 file name and path
        self.h5name = h5name
        self.h5path = os.path.join(self.folder, self.h5name)

        # data names
        self.names = ['u', 'p'] + list(self.config['files'])

        if os.path.exists(self.h5path):
            # read hdf5
            self.h5read()
        else:
            # new hdf5 file
            self.h5init()

        self._build_generators()

    # ----------------------------------------------------------------------- #

    def dimsinit(self):
        """
        Init the object attributes for dimensions
        """

        # dictionary {'var': dim}
        self.dims = dict(self.method_dims)

        # dictionary {'var': (imin, imax)}
        self.inds = dict()

        # imin in global
        imin = 0

        for name in self.names:

            # imax in global
            imax = imin + self.dims[name]

            # save indices
            self.inds[name] = (imin, imax)

            # imin in global
            imin = imax

    # ----------------------------------------------------------------------- #

    def h5init(self):
        """
        Clear and init the hdf5 file.
        """

        self.dimsinit()

        # Init folder
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)

        # Remove existing file
        if os.path.exists(self.h5path):
            os.remove(self.h5path)

        # Create HDF5 file
        with h5py.File(self.h5path, 'w') as f:

            # save ordered list of names
            names = [n.encode("ascii", "ignore") for n in self.names]
            f.create_dataset('names', (len(names), 1), 'S10', names)

            # save dimensions and indices
            for name in self.names:
                grp = f.create_group(name)
                grp.attrs['dim'] = self.dims[name]
                grp.attrs['inds'] = self.inds[name]

            maxshape = (None, )

            data = numpy.zeros(self.dim).astype(self.dtype)

            # Create a global dataset
            f.create_dataset(self.dname, data=data, dtype=self.dtype,
                             maxshape=maxshape)

    # ----------------------------------------------------------------------- #

    @property
    def dtype(self):
        return numpy.dtype({'names': list(map(str, range(self.dim))),
                            'formats': [numpy.float64] * self.dim})

    # ----------------------------------------------------------------------- #

    def h5read(self):
        """
        Read the hdf5 file and inits dimensions.
        """

        file_dims = list()

        # Read HDF5 file and extract dimensions
        with h5py.File(self.h5path, 'r') as f:
            names = [n.decode() for n in f['names'][:, 0]]
            for name in names:
                print()
                file_dims.append((name, f[name].attrs['dim']))

        if not file_dims == self.method_dims:
            text = 'hdf5 dims do not coincide with method dims: \n{0} != {1}'
            raise AttributeError(text.format(file_dims, self.method_dims))

        self.dimsinit()

        self._open = False

    # ----------------------------------------------------------------------- #

    @property
    def elements(self):
        """
        return the list of global elements names
        """
        # Define compound datatype
        return ['%s%d' % (var, n)
                for var, l in self.method_dims
                for n in range(l)]

    @property
    def h5_nt(self):
        """
        return the number of timesteps in the timeserie
        """
        return self.h5file[self.dname].shape[0]

    # ----------------------------------------------------------------------- #

    @property
    def method_dims(self):
        """
        return the dimensions of method attributes in self.names
        """
        dims = list()

        for name in self.names:

            if name in ('x', 'dx', 'dxH'):
                dim = self.method.dims.x()
            elif name in ('u', 'y'):
                dim = self.method.dims.y()
            elif name in ('w', 'z'):
                dim = self.method.dims.w()
            else:
                dim = getattr(self.method.dims, name)()

            dims.append((name, dim))

        return dims

    # ----------------------------------------------------------------------- #

    @property
    def folder(self):
        """
        return the path to the HDF5 file folder
        """
        return os.path.join(self.config['path'], 'data')

    # ----------------------------------------------------------------------- #

    @property
    def dim(self):
        """
        return the dimension of a single global element.
        """
        d = 0
        for k in self.dims:
            d += self.dims[k]
        return int(d)

    # ----------------------------------------------------------------------- #

    def open(self):
        """
        open hdf5 file
        """
        self.h5file = h5py.File(self.h5path, 'a')
        self._open = True

    def close(self):
        """
        close hdf5 file
        """
        self.h5file.close()
        self._open = False

    # ----------------------------------------------------------------------- #

    def init_data(self, sequ=None, seqp=None, nt=None):

        sequ, seqp, nt = BaseData.__init_data__(self, sequ, seqp, nt)

        self.open()

        # Init shape
        self.h5file[self.dname].resize(nt, axis=0)

        data = {'u': sequ, 'p': seqp}

        v = numpy.zeros(self.dim)
        for j, elts in enumerate(zip(*[data[k] for k in data])):
            for i, k in enumerate(data):
                v[slice(*self.inds[k])] = elts[i]
            self.h5file[self.dname][j] = numpy.asarray(v, dtype=self.dtype)[0]

        self.close()

    init_data.__doc__ = BaseData.__init_data__.__doc__

    # ----------------------------------------------------------------------- #

    def __getitem__(self, value):
        """
        Read from g5file[global].
        """

        # value contains var name and var slice
        if isinstance(value, tuple) and len(value) == 2:
            vname, vslice = value
            tslice = None
        # value contains var name, var slice, and time slice
        elif isinstance(value, tuple) and len(value) == 3:
            vname, vslice, tslice = value
        # value contains var name only
        else:
            tslice = None
            vslice = None

        assert isinstance(vname, str)
        assert vname in self.inds

        if tslice is None:
            tslice = slice(None, None, None)
        if vslice is None:
            vslice = slice(*self.inds[vname])
        elif isinstance(vslice, int):
            vslice += self.inds[vname][0]
        else:
            if vslice.start is not None:
                start = vslice.start+self.inds[vname][0]
            else:
                start = self.inds[vname][0]
            if vslice.stop is not None:
                stop = vslice.stop+self.inds[vname][0]
            else:
                stop = self.inds[vname][1]
            step = vslice.step
            vslice = slice(start, stop, step)

        if not self._open:
            self.open()
            close = True
        else:
            close = False

        output = self.h5file[self.dname][tslice, vslice]

        if close:
            self.close()

        return output

    # ----------------------------------------------------------------------- #

    def _build_reader(self, imin, imax):

        def func(i=None):
            if i is None:
                s = slice(imin, imax)
            else:
                s = i
            return self.h5file['args'][:, s]

        return func

    # ----------------------------------------------------------------------- #

    def build_generator(self, name):
        "Build data_generator from data name."

        def data_generator(ind=None, **kwargs):

            postprocess = kwargs.pop('postprocess', None)

            options = self._build_options(kwargs)
            slicet = slice(options['imin'], options['imax'], options['decim'])

            if ind is not None:
                if not isinstance(ind, int):
                    text = 'Index should be an integer,not {0}'
                    raise ValueError(text.format(type(ind)))
                s = ind
            else:
                s = slice(*self.inds[name])

            if not self._open:
                self.open()
                close = True
            else:
                close = False

            for ti in range(self.nt)[slicet]:
                el = self.h5file[self.dname][ti, s]
                if postprocess:
                    el = postprocess(el)
                yield el

            if close:
                self.close()

        data_generator.__doc__ = self.__doc_template__.format(name,
                                                              self.h5path)
        return data_generator

# --------------------------------------------------------------------------- #

Data = HDFData

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
