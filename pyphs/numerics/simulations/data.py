# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 10:22:56 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

from pyphs.misc.io import data_generator, write_data
from pyphs.misc.signals.waves import wavwrite
from pyphs.misc.plots.data import plot, plot_powerbal
import os
import numpy
from pyphs.numerics.tools import lambdify
from pyphs.misc.tools import find
from pyphs.core.tools import free_symbols
from pyphs.config import VERBOSE


try:
    import itertools.izip as zip
except ImportError:
    pass


class Data:
    """
=======
Data
=======

Interface for pyphs.Simulation data files.

Generators
-----------
t:
    Generator of simulation time values computed from simulation configuration.
x, dx, dxH, w, z, u, y, p:
    Read from files in the folder specified by the simulation configuration.
dtE, ps, pd:
    Compute the discrete energy's time variation, dissipated power, and sources
    power (respectively).
wavewrite:
    Export data to wave file.
plot:
    Plot selected data.
plot_powerbal:
    Plot the power balance.
    """
    def __init__(self, method, config):

        if VERBOSE >= 1:
            print('Build data i/o...')

        # init configuration options
        self.config = config

        # init method
        self.method = method

        self._build_generators()

    def subs(self):
        d = self.method.subs.copy()
        d[self.method.fs] = self.config['fs']
        return d

    def _build_generators(self):
        def build_generator(name):
            "Build data_generator from data name."

            def data_generator(ind=None, postprocess=None,
                               imin=self.config['load']['imin'],
                               imax=self.config['load']['imax'],
                               decim=self.config['load']['decim']):
                "Doc string overwritten below"
                return self._data_generator(name, ind=ind, imin=imin,
                                            imax=imax, decim=decim,
                                            postprocess=postprocess)

            doc_template = """
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
    from index imin to index imax with decimation factor decim (i.e. the value
    is generated if i-imin % decim == 0).
"""
            filename = '{0}{1}data{1}{2}.txt'.format(self.config['path'],
                                                     os.sep,
                                                     name)
            doc = doc_template.format(name, filename)
            setattr(data_generator, 'func_doc', doc)
            return data_generator

        for name in ['x', 'dx', 'w', 'u', 'p', 'y', 'dxH', 'z']:
            setattr(self, name, build_generator(name))

    def _data_generator(self, name, ind=None, postprocess=None,
                        imin=None, imax=None, decim=None):
        opts = self.config['load']
        options = {'imin': opts['imin'] if imin is None else imin,
                   'imax': opts['imax'] if imax is None else imax,
                   'decim': opts['decim'] if decim is None else decim}

        path = self.config['path'] + os.sep + 'data'
        filename = path + os.sep + name + '.txt'
        generator = data_generator(filename, ind=ind, postprocess=postprocess,
                                   **options)
        return generator

    def t(self, imin=None, imax=None, decim=None):
        """
t
=

Generator of simulation times values.

Parameters
-----------
imin: int or None, optional
    Starting index. If None, imin=0 (default).
imax: int or None,
    Stoping index. If None, imax=simu.config['nt'] (default).
decim: int or None,
    decimation factor

Returns
-------

t_generator: generator
    A python generator of scalar time value t[i] for each time step i starting
    from index imin to index imax with decimation factor decim (i.e. the value
    is generated if i-imin % decim == 0).
"""
        options = self.config['load']
        if imin is None:
            imin = options['imin']
        if imax is None:
            imax = options['imax']
            if imax is None:
                imax = float('Inf')
        if decim is None:
            decim = options['decim']

        def generator():
            for n in range(self.config['nt']):
                yield n/self.config['fs']
        i = 0
        for el in generator():
            if imin <= i < imax and not bool(i % decim):
                yield el
            i += 1

    def dtE(self, imin=None, imax=None, decim=None, DtE='DxhDtx'):
        """
dtE
===

Generator of discrete energy's time variation values.

Parameters
-----------
imin: int or None, optional
    Starting index. If None, imin=0 (default).
imax: int or None,
    Stoping index. If None, imax=simu.config['nt'] (default).
decim: int or None,
    decimation factor. If None, decim = int(simu.config['nt']/1000) (default)
DtE: str in {'deltaH', 'DxhDtx'}, optional
    Method for the computation of discrete energy's time variation. If DtE is
    'deltaH', the output with index i is (H[t[i+1]]-H[t[i]]) * samplerate. If
    DtE is 'DxhDtx', the output with index i is (dxH[i] dot dtx[i]).

Returns
-------

dtE_generator: generator
    A python generator of scalar discrete energy's time variation value DtE[i]
    for each time step i starting from index imin to index imax with decimation
    factor decim (i.e. the value is generated if i-imin % decim == 0).
        """
        options = self.config['load']
        options = {'imin': options['imin'] if imin is None else imin,
                   'imax': options['imax'] if imax is None else imax,
                   'decim': options['decim'] if decim is None else decim}

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
                       H(*H_args(*a)))*self.config['fs']

        elif DtE == 'DxhDtx':
            for dtx, dxh in zip(self.dtx(**options), self.dxH(**options)):
                yield scalar_product(dtx, dxh)

    def E(self, imin=None, imax=None, decim=None):
        """
E
===

Generator of discrete energy's values.

Parameters
-----------
imin: int or None, optional
    Starting index. If None, imin=0 (default).
imax: int or None,
    Stoping index. If None, imax=simu.config['nt'] (default).
decim: int or None,
    decimation factor. If None, decim = int(simu.config['nt']/1000) (default)

Returns
-------

E_generator: generator
    A python generator of scalar discrete energy's value E[i] for each time
    step i starting from index imin to index imax with decimation factor decim
    (i.e. the value is generated if i-imin % decim == 0).
        """
        options = self.config['load']
        options = {'imin': options['imin'] if imin is None else imin,
                   'imax': options['imax'] if imax is None else imax,
                   'decim': options['decim'] if decim is None else decim}

        H_expr = self.method.H.subs(self.method.subs)
        H_symbs = free_symbols(H_expr)
        H_args, H_inds = find(H_symbs, self.method.args())
        H = lambdify(H_args, H_expr, theano=self.config['theano'])
        H_args = lambdify(self.method.args(), H_args,
                          theano=self.config['theano'])

        for args, o in zip(self.args(**options), self.o(**options)):
            a = (list(args)+list(o))
            yield H(*H_args(*a))

    def pd(self, imin=None, imax=None, decim=None):
        """
pd
==

Generator of discrete dissipated power values.

Parameters
-----------
imin: int or None, optional
    Starting index. If None, imin=0 (default).
imax: int or None,
    Stoping index. If None, imax=simu.config['nt'] (default).
decim: int or None,
    decimation factor. If None, decim = int(simu.config['nt']/1000) (default)

Returns
-------

pd_generator: generator
    A python generator of scalar discrete dissipated power value pd[i] for each
    time step i starting from index imin to index imax with decimation
    factor decim (i.e. the value is generated if i-imin % decim == 0), with
    pd[i] = w[i] dot z[i].

        """
        options = self.config['load']
        options = {'imin': options['imin'] if imin is None else imin,
                   'imax': options['imax'] if imax is None else imax,
                   'decim': options['decim'] if decim is None else decim}

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

    def ps(self, imin=None, imax=None, decim=None):
        """
ps
==

Generator of discrete sources power values.

Parameters
-----------
imin: int or None, optional
    Starting index. If None, imin=0 (default).
imax: int or None,
    Stoping index. If None, imax=simu.config['nt'] (default).
decim: int or None,
    decimation factor. If None, decim = int(simu.config['nt']/1000) (default)

Returns
-------

ps_generator: generator
    A python generator of scalar discrete sources power value ps[i] for each
    time step i starting from index imin to index imax with decimation
    factor decim (i.e. the value is generated if i-imin % decim == 0), with
    ps[i] = u[i] dot y[i].

        """
        options = self.config['load']
        options = {'imin': options['imin'] if imin is None else imin,
                   'imax': options['imax'] if imax is None else imax,
                   'decim': options['decim'] if decim is None else decim}
        for u, y in zip(self.u(**options),
                        self.y(**options)):
            yield scalar_product(u, y)

    def o(self, ind=None, imin=None, imax=None, decim=None):
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
    Stoping index. If None, imax=simu.config['nt'] (default).
decim: int or None,
    decimation factor. If None, decim = int(simu.config['nt']/1000) (default)

Returns
-------

ps_generator: generator
    A python generator of scalar discrete sources power value ps[i] for each
    time step i starting from index imin to index imax with decimation
    factor decim (i.e. the value is generated if i-imin % decim == 0), with
    ps[i] = u[i] dot y[i].

        """
        options = self.config['load']
        options = {'imin': options['imin'] if imin is None else imin,
                   'imax': options['imax'] if imax is None else imax,
                   'decim': options['decim'] if decim is None else decim}
        obs_expr = [e.subs(self.subs()) for e in self.method.observers.values()]

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


    def args(self, ind=None, imin=None, imax=None, decim=None):
        """
args
====

Generator of values for arguments of numerical functions args=(x, dx, w, u, p).

Parameters
-----------
ind: int or None, optional
    Index for the returned value args[ind]. If None, the full arguments vector
    is returned (default).
imin: int or None, optional
    Starting index. If None, imin=0 (default).
imax: int or None,
    Stoping index. If None, imax=simu.config['nt'] (default).
decim: int or None,
    decimation factor. If None, decim = int(simu.config['nt']/1000) (default)

Returns
-------

args_generator: generator
    A python generator of arguments of numerical functions value args[ind][i]
    for each time step i starting from index imin to index imax with decimation
    factor decim (i.e. the value is generated if i-imin % decim == 0).
        """
        options = self.config['load']
        options = {'imin': options['imin'] if imin is None else imin,
                   'imax': options['imax'] if imax is None else imax,
                   'decim': options['decim'] if decim is None else decim}
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

    def dtx(self, ind=None, imin=None, imax=None, decim=None):
        """
dtx
====

Generator of state vector time variation values dtx ~ dx * samplerate.

Parameters
-----------
ind: int or None, optional
    Index for the returned value dx[ind] * samplerate. If None, the full state
    vector variation dx[:] * samplerate is returned (default).
imin: int or None, optional
    Starting index. If None, imin=0 (default).
imax: int or None,
    Stoping index. If None, imax=simu.config['nt'] (default).
decim: int or None,
    decimation factor. If None, decim = int(simu.config['nt']/1000) (default)

Returns
-------

dtx_generator: generator
    A python generator of state vector time variation dx[ind][i] * samplerate
    for each time step i starting from index imin to index imax with decimation
    factor decim (i.e. the value is generated if i-imin % decim == 0).

See Also
---------
x, dx
"""
        for dtx in self.dx(postprocess=self._dxtodtx, ind=ind, imin=imin,
                           imax=imax, decim=decim):
            yield dtx

    def _dxtodtx(self, dx):
        return numpy.asfarray(dx)*self.config['fs']

    def a(self, ind=None, imin=None, imax=None, decim=None):
        """
a
====

Generator of values for components of vector a in the core port-Hamiltonian
structure b = J dot a, i.e. a = (dxH, z, u).

Parameters
-----------
ind: int or None, optional
    Index for the returned value a[ind]. If None, the full vector is
    returned (default).
imin: int or None, optional
    Starting index. If None, imin=0 (default).
imax: int or None,
    Stoping index. If None, imax=simu.config['nt'] (default).
decim: int or None,
    decimation factor. If None, decim = int(simu.config['nt']/1000) (default)

Returns
-------

a_generator: generator
    A python generator of arguments of numerical functions value a[ind][i]
    for each time step i starting from index imin to index imax with decimation
    factor decim (i.e. the value is generated if i-imin % decim == 0).
        """
        options = self.config['load']
        options = {'imin': options['imin'] if imin is None else imin,
                   'imax': options['imax'] if imax is None else imax,
                   'decim': options['decim'] if decim is None else decim}
        for dxH, z, u in zip(self.dxH(**options),
                             self.z(**options),
                             self.u(**options)):
            if ind is None:
                yield dxH + z + u
            else:
                yield (dxH + z + u)[ind]

    def b(self, ind=None, imin=None, imax=None, decim=None):
        """
a
====

Generator of values for components of vector b in the core port-Hamiltonian
structure b = J dot a, i.e. b = (dtx, w, y).

Parameters
-----------
ind: int or None, optional
    Index for the returned value b[ind]. If None, the full vector is
    returned (default).
imin: int or None, optional
    Starting index. If None, imin=0 (default).
imax: int or None,
    Stoping index. If None, imax=simu.config['nt'] (default).
decim: int or None,
    decimation factor. If None, decim = int(simu.config['nt']/1000) (default)

Returns
-------

b_generator: generator
    A python generator of arguments of numerical functions value b[ind][i]
    for each time step i starting from index imin to index imax with decimation
    factor decim (i.e. the value is generated if i-imin % decim == 0).
        """
        options = self.config['load']
        options = {'imin': options['imin'] if imin is None else imin,
                   'imax': options['imax'] if imax is None else imax,
                   'decim': options['decim'] if decim is None else decim}

        for dtx, w, y in zip(self.dtx(**options),
                             self.w(**options),
                             self.y(**options)):
            if ind is None:
                yield list(dtx) + list(w) + list(y)
            else:
                yield [list(dtx) + list(w) + list(y)][ind]

    def init_data(self, sequ=None, seqp=None, nt=None):
        """
Initialize the object and save the sequences for input u, parameters p and
state initialisation x0 to files in the folder specified by the simulation
configuration.

Parameters
----------

sequ: iterable or None, optional
    Input sequence wich elements are arrays with shape (method.dims.y(), ). If
    the lenght nt of the sequence is known (e.g. sequ is a list), the number of
    simulation time steps is set to nt. If None, a sequence with length nt of
    zeros with appropriate shape is used (default).

seqp: iterable or None, optional
    Input sequence wich elements are arrays with shape (method.dims.p(), ). If
    (i) the lenght of sequ is not known, and (ii) the length nt of seqp is
    known (e.g. seqp is a list), the number of simulation time steps is set to
    nt=len(seqp). If None, a sequence with length nt of zeros with appropriate
    shape is used (default).

nt: int or None:
    Number of time steps. If None, the lenght of either sequ or seqp must be
    known (default).

        """
        # get number of time-steps
        if nt is not None:
            pass
        elif hasattr(sequ, 'index'):
            nt = len(sequ)
        elif hasattr(seqp, 'index'):
            nt = len(seqp)
        else:
            assert nt is not None, 'Unknown number of \
    iterations. Please tell either a list sequ (input sequence), a list seqp \
    (sequence of parameters) or an int nt (number of time steps).'
            assert isinstance(nt, int), 'number of time steps is not integer, \
    got {0!s} '.format(nt)

        # if sequ is not provided, a sequence of [[0]*ny]*nt is assumed
        if sequ is None:
            def generator_u():
                for _ in range(nt):
                    if self.method.dims.y() > 0:
                        yield [0, ]*self.method.dims.y()
                    else:
                        yield ""
            sequ = generator_u()
        # if seqp is not provided, a sequence of [[0]*np]*nt is assumed
        if seqp is None:
            def generator_p():
                for _ in range(nt):
                    if self.method.dims.p() > 0:
                        yield [0, ]*self.method.dims.p()
                    else:
                        yield ""
            seqp = generator_p()

        # write input sequence
        write_data(self.config['path']+os.sep+'data', sequ, 'u')
        # write parameters sequence
        write_data(self.config['path']+os.sep+'data', seqp, 'p')

        self.config['nt'] = nt

        if self.config['load']['imin'] is None:
            self.config['load']['imin'] = 0
        if self.config['load']['imax'] is None:
            self.config['load']['imax'] = self.config['nt']-1
        if self.config['load']['decim'] is None:
            nt = self.config['load']['imax']-self.config['load']['imin']
            decim = max(1, int(nt/1e3))
            self.config['load']['decim'] = decim

        self._build_generators()

    def wavwrite(self, name, index, path=None, gain=1.,
                 fs=None, normalize=True, timefades=0.):
        """
========
wavwrite
========

Write data to wave file.

Parameters
----------
name: str
    Name of the data generator to export (e.g. 'x', 'y', 'dxH').

index: int
    Index of the component of the data generator to read (e.g. if name is 'x'
    and index is 0, the signal is x[index]).

path: str or None, optional
    Raw path to the generated wave file. Notice '.wav' is appended by default.
    If None, the simulation path and the data generator name is used (default).

gain: float, optional
    Gain applied to the signal before writing to file. Default is 1.

fs: float or None, optional
    Sample rate for the generated wave file. Resampling is performed with
    scipy.signal.resample. If None, the simulation samplerate is use (default).

normalize: Bool
    If True, the signal is normalised by the maximum absolute value. Default is
    False.

timefades: float, optional
    Fade-in and fade-out time to avoid clics. Default is 0.

See also
---------
pyphs.misc.signals.waves.wavwrite
        """
        if fs is None:
            fs = self.config['fs']
        if path is None:
            path = self.config['path'] + os.sep + name + str(index)
        print(path)
        args = {'ind': index,
                'imin': 0, 'imax': None, 'decim': 1,
                'postprocess': lambda e: gain*e}
        sig = getattr(self, name)(**args)
        wavwrite(sig, self.config['fs'], path,
                 fs_out=fs, normalize=normalize, timefades=timefades)

    def plot_powerbal(self, mode='single', DtE='deltaH', load=None, show=True):
        """
        Plot the power balance. mode is 'single' or 'multi' for single figure \
or multifigure (default is 'single').
        """
        if load is None:
            load = self.config['load']
        plot_powerbal(self, mode=mode, DtE=DtE, show=show, **load)

    def plot(self, vars, load=None, show=True, label=None):
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
        if load is None:
            load = self.config['load']
        plot(self, vars, show=show, label=label, **load)

###########################################################################


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
