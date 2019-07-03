#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 10:02:31 2018

@author: afalaize
"""

from __future__ import absolute_import, division, print_function

from pyphs.misc.signals.waves import wavwrite
from pyphs.misc.plots.data import plot, plot_powerbal
import os
import numpy
from pyphs.misc.tools import geteval
from pyphs.config import VERBOSE
import h5py
import warnings


class H5Data(object):
    """
    =======
    HDFData
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

    # global data name
    dname = 'global'

    # ----------------------------------------------------------------------- #

    def __init__(self, method, config, h5name='results.h5', erase=False):

        if VERBOSE >= 1:
            print('Build data i/o...')

        # init configuration options
        self.config = config

        # init method
        self.method = method

        # HDF5 file name and path
        self.h5name = h5name
        self.h5path = os.path.join(self.folder, self.h5name)

        # data names
        self.names = ['u', 'p'] + list(self.config['dnames'])

        if erase or not os.path.exists(self.h5path):
            # new hdf5 file
            self._h5new()
        else:
            # read hdf5
            self._read_h5infos()

        self._build_readers()

        # init load options
        self.start = None
        self.stop = None
        self.step = None

    # ----------------------------------------------------------------------- #
    # fs
    @property
    def fs(self):
        return self.config['fs']

    # nt
    @property
    def nt(self):
        return self.config['nt']

    # ntplot: number of points selected in arrays for plot (stepation)
    ntplot = 1000

    # ----------------------------------------------------------------------- #
    # start and stop

    def _get_start(self):
        i = self.config['load']['start']
        if i is None:
            return 0
        else:
            return i

    def _set_start(self, i):
        if i is None:
            self.config['load']['start'] = i
        else:
            if not 0 <= i < self.stop:
                text = 'start must be in [0, {0}].'
                raise ValueError(text.format(self.stop-1))
            if not isinstance(i, (int, float)):
                text = 'start must be a positive integer: %s.' % str(i)
                raise ValueError(text)
            self.config['load']['start'] = int(i)

    start = property(_get_start, _set_start)

    def _get_stop(self):
        i = self.config['load']['stop']
        if i is None:
            return self.nt
        else:
            return i

    def _set_stop(self, i):
        if i is None:
            self.config['load']['stop'] = i
        else:
            if not self.start < i <= self.nt:
                text = 'stop must be in [{0}, {1}].'
                raise ValueError(text.format(self.start+1, self.nt))
            if not isinstance(i, (int, float)):
                text = 'stop must be a positive integer: %s.' % str(i)
                raise ValueError(text)
            self.config['load']['stop'] = int(i)

    stop = property(_get_stop, _set_stop)

    # ----------------------------------------------------------------------- #
    # tstart and tstop

    def _time2index(self, t, m='min'):
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

    def _index2time(self, i, m='min'):
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

    def _get_tstart(self):
        return self._index2time(self.start, m='min')

    def _set_tstart(self, t):
        if t is None:
            self.start = t
        else:
            tstart = 0.
            tstop = self.tstop
            if not tstart <= t <= tstop:
                text = 'tstart must be in [{0}, {1}].'
                raise ValueError(text.format(tstart, tstop))
            if not isinstance(t, (int, float)):
                text = 'tstart must be a positive value: %s.' % str(t)
                raise ValueError(text)
        self.start = self._time2index(t, m='min')

    # tstart: start = tstart*fs and slice for t is slice(start, stop, step)
    tstart = property(_get_tstart, _set_tstart)

    def _get_tstop(self):
        return self._index2time(self.stop, m='max')

    def _set_tstop(self, t):
        if t is None:
            self.stop = t
        else:
            tstart = self.tstart
            tstop = (self.nt-1)/self.fs
            if not tstart <= t <= tstop:
                text = 'tstop must be in [{0}, {1}].'
                raise ValueError(text.format(tstart, tstop))
            if not isinstance(t, (int, float)):
                text = 'tstop must be a positive value: %s.' % str(t)
                raise ValueError(text)
            self.stop = self._time2index(t, m='max')

    # tstop: stop = tstop*fs + 1 and slice for t is slice(start, stop, step)
    tstop = property(_get_tstop, _set_tstop)

    # ----------------------------------------------------------------------- #
    # step: slice for t is slice(start, stop, step)

    def _get_step(self):
        return self.config['load']['step']

    def _set_step(self, i):
        if i is None:
            self.config['load']['step'] = 1
        else:
            if not 1 <= i or not isinstance(i, (int, float)):
                text = 'step must be an integer >= 1.'
                raise ValueError(text)
            self.config['load']['step'] = int(i)

    step = property(_get_step, _set_step)

    # ----------------------------------------------------------------------- #
    @property
    def subs(self):
        """
        Return substitution dictionary from method object and update samplerate
        """
        d = self.method.subs.copy()
        d[self.method.fs] = self.fs
        return d

    # ----------------------------------------------------------------------- #
    @property
    def h5data(self):
        """
        Return substitution dictionary from method object and update samplerate
        """
        return self.h5file[self.dname]

    # ----------------------------------------------------------------------- #

    @property
    def dtype(self):
        return numpy.float64
#        return numpy.dtype({'names': list(map(str, range(self.dim))),
#                            'formats': [numpy.float64] * self.dim})

    # ----------------------------------------------------------------------- #

    def init_data(self, nt=None, sequ=None, seqp=None):
        """
        Initialize the object and save the sequences for input u, parameters p
        and state initialisation x0 to files in the folder specified by the
        simulation configuration.

        Parameters
        ----------

        nt: int or None, optional
            Number of time steps. If None, it is extracted from sequ or seqp
            dimensions.

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

        """
        # get number of time-steps
        if nt is None:
            if hasattr(sequ, '__len__'):
                nt = len(sequ)
            elif hasattr(sequ, 'shape'):
                nt = sequ.shape[0]
            elif hasattr(seqp, '__len__'):
                nt = len(seqp)
            elif hasattr(seqp, 'shape'):
                nt = seqp.shape[0]
            else:
                raise ValueError("""Unknown number of iterations.
Please give either a list u (input sequence), a list p (sequence of parameters)
or an integer nt (number of time steps).'
    """)

        # store number of time steps
        self.config['nt'] = nt = int(nt)

        self._h5new()

        # if sequ is not provided, a sequence of [[0]*ny]*nt is assumed
        ny = self.method.dims.y()
        if isinstance(sequ, list):
            sequ = numpy.array(sequ)
        elif hasattr(sequ, '__next__'):
            sequ = numpy.array(list(sequ))
            # TODO: remoce warnings
            warnings.warn('Use of generator as inputs to simulation objects is deprecated. Use lists or arrays instead.')
        if sequ is None:
            sequ = [[0]*ny for _ in range(nt)]
        elif len(sequ.shape) == 1:
            if not ny == 1:
                text = 'Input shape should be ({}, {}).'
                raise AttributeError(text.format(nt, ny))
            else:
                sequ = sequ[:, numpy.newaxis]

        # if seqp is not provided, a sequence of [[0]*np]*nt is assumed
        np = self.method.dims.p()
        if seqp is None:
            seqp = [[0]*np for _ in range(nt)]
        if isinstance(seqp, list):
            seqp = numpy.array(seqp)
        elif len(seqp.shape) == 1:
            if not np == 1:
                text = 'Parameters shape should be ({}, {}).'
                raise AttributeError(text.format(nt, np))
            else:
                seqp = seqp[:, numpy.newaxis]

        # data to store in h5 dataset
        seqs = {'u': sequ, 'p': seqp}

        # Open h5 file
        self.h5open()

        # Init h5 dataset shape
        self.h5file[self.dname].resize((nt, self.dim))

        # dump seqs on times [0:nt-1]
        self.h5dump_seqs(seqs, slice(0, nt))

        # Close h5 file
        self.h5close()

    # ----------------------------------------------------------------------- #

    def _dimsinit(self):
        """
        Init the object attributes dims and inds
        """

        # dictionary {'var': dim}
        self.dims = dict(self._method_dims)

        # dictionary {'var': (start, stop)}
        self.inds = dict()

        # start in global
        start = 0

        for name in self.names:

            # stop in global
            stop = start + self.dims[name]

            # save indices
            self.inds[name] = (start, stop)

            # start in global
            start = stop

    # ----------------------------------------------------------------------- #

    def _h5new(self):
        """
        Clear and init the hdf5 file.
        """

        self._dimsinit()

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

            maxshape = (None, self.dim)

            data = numpy.zeros((1, self.dim)).astype(self.dtype)

            # Create a global dataset
            f.create_dataset(self.dname, data=data, dtype=self.dtype,
                             maxshape=maxshape)

    # ----------------------------------------------------------------------- #

    def _read_h5infos(self):
        """
        Read the hdf5 file and inits dimensions.
        """

        file_dims = list()

        # Read HDF5 file and extract dimensions
        with h5py.File(self.h5path, 'r') as f:
            names = [n.decode() for n in f['names'][:, 0]]
            for name in names:
                file_dims.append((name, f[name].attrs['dim']))

        if not file_dims == self._method_dims:
            text = 'hdf5 dims do not coincide with method dims: \n{0} != {1}'
            raise AttributeError(text.format(file_dims, self._method_dims))

        self._dimsinit()

        self._open = False

        self.config['nt'] = self._h5shape[0]

    # ----------------------------------------------------------------------- #

    @property
    def _h5shape(self):
        """
        return the number of timesteps in the timeserie
        """
        # close flag
        if not self._open:
            self.h5open()
            close = True
        else:
            close = False
        shape = self.h5file[self.dname].shape
        if close:
            self.h5close()

        return shape

    # ----------------------------------------------------------------------- #

    @property
    def _method_dims(self):
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
                dim = geteval(self.method.dims, name)

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

    def h5open(self):
        """
        open hdf5 file
        """
        self.h5file = h5py.File(self.h5path, 'a')
        self._open = True

    def h5close(self):
        """
        close hdf5 file
        """
        self.h5file.close()
        self._open = False

    # ----------------------------------------------------------------------- #
    def h5dump_vecs(self, t, data):
        """
        Write vectors to h5 file, with data a dictionary structured as:

        data = {k1: vec1,
                k2: vec2,
                ...}

        where dim(veci) = (dim(ki),).

        """
        # close flag
        if not self._open:
            self.h5open()
            close = True
        else:
            close = False

        # single array for every data
        v = numpy.zeros(self.dim)

        for name in self.names:
            if name not in data:
                data[name] = self[name, t, :]

        # update array with data values
        for i, name in enumerate(data):
            v[slice(*self.inds[name])] = data[name]

        # write array in h5 file at time t
        self.h5file[self.dname][t] = numpy.asarray(v, dtype=self.dtype)

        if close:
            self.h5close()

    # ----------------------------------------------------------------------- #
    def h5dump_seqs(self, data, tslice):
        """
        Write sequences to h5 file, with data a dictionary structured as:

        data = {k1: seq1,
                k2: seq2,
                ...}

        where dim(seqi) = (nt, dim(ki)).

        """

        # close flag
        if not self._open:
            self.h5open()
            close = True
        else:
            close = False

        dtype = self.dtype
        # update array with data values
        for name in data:
            # write array in h5 file at time t
            vslice = slice(*self.inds[name])
            self.h5data[tslice, vslice] = numpy.asarray(data[name],
                                                        dtype=dtype)

        if close:
            self.h5close()

    # ----------------------------------------------------------------------- #

    def _tslice(self, tslice):

        # Set time slice

        if tslice is None:
            tslice = slice(self.start,
                           self.stop,
                           self.step)

        elif isinstance(tslice, int):
            tslice = slice(tslice, tslice+1, None)

        if tslice.start is None:
            start = self.start
        else:
            start = tslice.start
        if tslice.stop is None:
            stop = self.stop
        else:
            stop = tslice.stop
        if tslice.step is None:
            step = self.step
        else:
            step = tslice.step
        return slice(start, stop, step)

    def _tuple2slice(self, vname, vslice):
        """
        return slice in the data from item spicifier
        """

        # read variable slice from data object indices
        if vslice is None:
            vslice = slice(*self.inds[vname])

        # convert index in var to index in global dataset
        elif isinstance(vslice, int):
            vslice += self.inds[vname][0]

        # custom variable slice
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

        return vslice

    def _read_data(self, vname, tslice, vslice):
        """

        """
        # open h5 file
        if not self._open:
            self.h5open()
            close = True
        else:
            close = False

        # open h5 file
        output = self.h5data[self._tslice(tslice),
                             self._tuple2slice(vname, vslice)]

        # close h5 file
        if close:
            self.h5close()

        return output

    def _build_reader(self, name):
        "Build data_generator from data name."

        def data_reader(tslice=None, vslice=None, postprocess=None):

            if postprocess is None:
                return self._read_data(name, tslice, vslice)
            else:
                return postprocess(self._read_data(name,
                                                   tslice,
                                                   vslice))

        data_reader.__doc__ = self.__doc_template__.format(name, self.h5path)
        return data_reader

    def _build_readers(self):
        """
        Build most readers to h5 file.
        """

        # ------------------------------------------------------------------- #

        for name in self.names:
            setattr(self, name, self._build_reader(name))

    # ----------------------------------------------------------------------- #

    def _process_data(self, pname, tslice, vslice):

        # open h5 file
        if not self._open:
            self.h5open()
            close = True
        else:
            close = False

        # open h5 file
        output = getattr(self, pname)(tslice=tslice, vslice=vslice)

        # close h5 file
        if close:
            self.h5close()

        return output

    # ----------------------------------------------------------------------- #

    def __getitem__(self, value):
        """
        Read from g5file[global].
        """

        # vname: variable name
        # vslice: slice in [0:dim(variable)]
        # tslice: slice in [0:nt]

        # value contains var name and var slice
        if isinstance(value, tuple) and len(value) == 2:
            vname, tslice = value
            vslice = None
        # value contains var name, var slice, and time slice
        elif isinstance(value, tuple) and len(value) == 3:
            vname, tslice, vslice = value
        # value contains var name only
        else:
            vname = value
            tslice = None
            vslice = None

        if not isinstance(vname, str):
            text = """
                    data getitem call attributes are:
                        data[var_str],
                        data[var_str, time_slice] or
                        data[var_str, time_slice, var_slice].""".format()
            raise TypeError(text)

        if vname not in self.inds:
            return self._process_data(vname, tslice, vslice)
        else:
            return self._read_data(vname, tslice, vslice)

    # ----------------------------------------------------------------------- #

    def t(self, tslice=None, vslice=None, postprocess=None):
        """
        t
        =

        Generator of simulation times values.

        Parameters
        -----------

        vslice : slice or None, optional
            Slice in the returned value {0}[tslice, vslice]. If None, the full
            vector is returned (default).

        tslice : slice or None, optional
            Slice in time {0}[tslice, vslice]. The default can be set with
            data.start, data.stop and data.step.

        Returns
        -------

        t_generator : generator
            A python generator of scalar time value t[i] for each time step i
            starting from index start to index stop with stepation factor step
            (i.e. the value is generated if i-start % step == 0).

        See also
        --------

        self.tstart, self.tstop

        """
        tslice = self._tslice(tslice)
        output = numpy.arange(tslice.start, tslice.stop, tslice.step)/self.fs
        if postprocess is None:
            return output
        else:
            return postprocess(output)

    # ----------------------------------------------------------------------- #

    def _hstack(self, names, tslice=None, vslice=None, postprocess=None):
        """

        """

        if not self._open:
            self.h5open()
            close = True
        else:
            close = False

        if vslice is None:
            vslice = slice(None, None, None)

        tslice = self._tslice(tslice)
        arrays = []
        for name in names:
            array = self[name, tslice]
            if len(array.shape) < 2:
                array = array[:, numpy.newaxis]
            arrays.append(array)
        output = numpy.hstack(arrays)[vslice]

        if postprocess is None:
            return output
        else:
            return postprocess(output)

        if close:
            self.h5close()

    def _expression(self, name, tslice=None, vslice=None, postprocess=None):

        tslice = self._tslice(tslice)

        if not self._open:
            self.h5open()
            close = True
        else:
            close = False

        if vslice is None:
            vslice = slice(None, None, None)

        expectedNt = (tslice.stop-tslice.start)//tslice.step

        evalobj = self.method.to_evaluation(names=[name])

        # cope with functions that have no arguments (see Evaluation object)
        if name == 'o':
            argsname = 'args'
        else:
            argsname = 'args_o'

        if len(getattr(evalobj, name+'_inds')) > 0:
            vs = getattr(evalobj, name+'_inds')
            args = getattr(self, argsname)(tslice=tslice)[:, vs]
        else:
            args = numpy.zeros((expectedNt, 1))

        # Try to slice the output
        try:
            output = getattr(evalobj, name)(*args.T)[:, vslice]
        except IndexError:
            output = getattr(evalobj, name)(*args.T)

        # Reshape if output is 0 dimensional
        if not numpy.prod(output.shape):
            output = numpy.zeros((expectedNt, 0))

        # Apply postprocess
        if postprocess is None:
            return output
        else:
            return postprocess(output)

        if close:
            self.h5close()

    def args(self, tslice=None, vslice=None, postprocess=None):
        """
        args
        ====

        Array of values for arguments of numerical functions
        args=(x, dx, w, u, p).

        Parameters
        -----------
        ind: int or None, optional
            Index for the returned value args[ind]. If None, the full arguments
            vector is returned (default).
        start: int or None, optional
            Starting index. If None, start=0 (default).
        stop: int or None,
            Stoping index. If None, stop=data.nt (default).
        step: int or None,
            stepation factor. If None, step = 1 (default)

        Returns
        -------

        args_generator: generator
            A python generator of arguments of numerical functions value
            args[ind][i] for each time step i starting from index start to
            index stop with stepation factor step (i.e. the value is generated
            if i-start % step == 0).
        """
        names = ['x', 'dx', 'w', 'u', 'p']
        return self._hstack(names,
                            tslice=tslice, vslice=vslice,
                            postprocess=postprocess)

    # ----------------------------------------------------------------------- #

    def o(self, tslice=None, vslice=None, postprocess=None):
        """
        o
        ==

        Generator of values for observers.

        Parameters
        -----------
        ind: int or None, optional
            Index of the observer. If None, values for every observers are
            returned (default).
        start: int or None, optional
            Starting index. If None, start=0 (default).
        stop: int or None,
            Stoping index. If None, stop=data.nt (default).
        step: int or None,
            stepation factor. If None, step = 1 (default).

        Returns
        -------

        o_generator: generator
            A python generator of observed quantites.
        """

        return self._expression('o', tslice=tslice, vslice=vslice,
                                postprocess=postprocess)

    # ----------------------------------------------------------------------- #

    def args_o(self, tslice=None, vslice=None, postprocess=None):
        """
        args_o
        ==

        Generator of values for arguments incuding observers.

        Parameters
        -----------
        ind: int or None, optional
            Index of the observer. If None, values for every observers are
            returned (default).
        start: int or None, optional
            Starting index. If None, start=0 (default).
        stop: int or None,
            Stoping index. If None, stop=data.nt (default).
        step: int or None,
            stepation factor. If None, step = 1 (default).

        Returns
        -------

        o_generator: generator
            A python generator of observed quantites.
        """

        names = ['args', 'o']
        return self._hstack(names,
                            tslice=tslice, vslice=vslice,
                            postprocess=postprocess)

    # ----------------------------------------------------------------------- #

    def dtx(self, tslice=None, vslice=None, postprocess=None):
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
        start: int or None, optional
            Starting index. If None, start=0 (default).
        stop: int or None,
            Stoping index. If None, stop=data.nt (default).
        step: int or None,
            stepation factor. If None, step = 1 (default).

        Returns
        -------

        dtx_generator: generator
            A python generator of state vector time variation
            dx[ind][i] * samplerate for each time step i starting from index
            start to index stop with stepation factor step (i.e. the value is
            generated if i-start % step == 0).

        See Also
        ---------
        x, dx
        """

        if not self._open:
            self.h5open()
            close = True
        else:
            close = False

        output = self.dx(tslice=tslice, vslice=vslice,
                         postprocess=lambda dx: dx*self.fs)

        if postprocess is None:
            return output
        else:
            return postprocess(output)

        if close:
            self.h5close()

    # ----------------------------------------------------------------------- #

    def a(self, tslice=None, vslice=None, postprocess=None):
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
        start: int or None, optional
            Starting index. If None, start=0 (default).
        stop: int or None,
            Stoping index. If None, stop=data.nt (default).
        step: int or None,
            stepation factor. If None, step = 1 (default).

        Returns
        -------

        a_generator: generator
            A python generator of arguments of numerical functions value
            a[ind][i] for each time step i starting from index start to index
            stop with stepation factor step (i.e. the value is generated if
            i-start % step == 0).

        See also
        --------

        b

        """

        names = ['dxH', 'z', 'u']
        return self._hstack(names,
                            tslice=tslice, vslice=vslice,
                            postprocess=postprocess)

    # ----------------------------------------------------------------------- #

    def b(self, tslice=None, vslice=None, postprocess=None):
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
        start: int or None, optional
            Starting index. If None, start=0 (default).
        stop: int or None,
            Stoping index. If None, stop=data.nt (default).
        step: int or None,
            stepation factor. If None, step = 1 (default).

        Returns
        -------

        b_generator: generator
            A python generator of arguments of numerical functions value
            b[ind][i] for each time step i starting from index start to index
            stop with stepation factor step (i.e. the value is generated if
            i-start % step == 0).

        See also
        --------

        a

        """
        names = ['dtx', 'w', 'y']
        return self._hstack(names,
                            tslice=tslice, vslice=vslice,
                            postprocess=postprocess)

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
        # close flag
        if not self._open:
            self.h5open()
            close = True
        else:
            close = False

        # samplerate
        if fs is None:
            fs = self.fs
        if path is None:
            path = self.config['path'] + os.sep + name + str(index)

        # recover signal
        sig = getattr(self, name)(vslice=index,
                                  tslice=slice(self.start, self.stop, 1),
                                  postprocess=lambda e: gain*e)

        # write .wav file
        wavwrite(sig, self.fs, path,
                 fs_out=fs, normalize=normalize, timefades=timefades)

        # close flag
        if close:
            self.h5close()

    # ----------------------------------------------------------------------- #

    def plot_powerbal(self, mode='single', DtE='deltaH',
                      show=True, tslice=None):
        """
        Plot the power balance. mode is 'single' or 'multi' for single figure
        or multifigure (default is 'single').

        Parameters
        -----------
        tslice : dict
            dictionary of signal load options, with keys
                * 'start': starting index,
                * 'stop': stoping index,
                * 'step': stepation factor.

        show : bool (optional)
            Acivate the call to matplotlib.pyplot.show

        DtE : str (optional)
            Method for evaluation the time variation of the total energy.

        label : str (optional)

        Returns
        -------

        fig : matplotlib figure
            The generated figure for post-rendering.

        ax : matplotlib axe or list of axes
            The axe (or axes) of the plot for post-rendering.


        """

        tslice = self._tslice(tslice)

        if not self._open:
            self.h5open()
            close = True
        else:
            close = False

        if tslice.step is None:
            tslice.step = max((1, (self.stop-self.start)//self.ntplot))

        fig, ax = plot_powerbal(self, mode=mode, DtE=DtE,
                                show=show, tslice=tslice)

        if close:
            self.h5close()

        return fig, ax
    # ----------------------------------------------------------------------- #

    def plot(self, vars, tslice=None, show=True, label=None):
        """
        Plot simulation data

        Parameters
        ----------

        vars : list
            List of variables to plot. Elements can be a single string name or
            a tuples of strings (name, index). For each string element, every
            indices of variable name are ploted. For each tuple element, the
            element index of variable name is ploted.

        tslice : slice
            slice for signal: slice(start, stop, step)

        show : bool (optional)
            Acivate the call to matplotlib.pyplot.show

        label : str (optional)

        Returns
        -------

        fig : matplotlib figure
            The generated figure for post-rendering.

        ax : matplotlib axe or list of axes
            The axe (or axes) of the plot for post-rendering.

        """
        if not self._open:
            self.h5open()
            close = True
        else:
            close = False

        if tslice is None:
            tslice = self._tslice(tslice)

        if tslice.step is None:
            tslice = slice(
                tslice.start,
                tslice.stop,
                max((1, (self.stop-self.start)//self.ntplot)))

        fig, ax = plot(self, vars, show=show, label=label, tslice=tslice)

        if close:
            self.h5close()

        return fig, ax

    # ----------------------------------------------------------------------- #

    __doc_template__ = """
    {0}
    ====

    Reader for simulation data {0} from file:\n{1}

    Parameters
    -----------
    vslice: slice or None, optional
        Slice in the returned value {0}[tslice, vslice]. If None, the full
        vector is returned (default).
    tslice: slice or None, optional
        Slice in time {0}[tslice, vslice]. The default can be set with
        data.start, data.stop and data.step (see also data.tstart, data.tstop).
    postprocess: function or None:
        If not None, the function is applied to the ouput array.

    Returns
    -------

    {0}_generator: generator
        A numpy array of values postprocess({0}[tslice, vslice]).
    """

    # ----------------------------------------------------------------------- #

    def dtE(self, tslice=None, vslice=None, postprocess=None, DtE='DxhDtx'):
        """
        dtE
        ===

        Generator of discrete energy's time variation values.

        Parameters
        -----------
        start: int or None, optional
            Starting index. If None, start=0 (default).
        stop: int or None,
            Stoping index. If None, stop=data.nt (default).
        step: int or None,
            stepation factor. If None, step = 1 (default).
        DtE: str in {'deltaH', 'DxhDtx'}, optional
            Method for the computation of discrete energy's time variation. If
            DtE is 'deltaH', the output with index i is
            (H[t[i+1]]-H[t[i]]) * samplerate. If DtE is 'DxhDtx', the output
            with index i is (dxH[i] dot dtx[i]).

        Returns
        -------

        dtE_generator: generator
            A python generator of scalar discrete energy's time variation value
            DtE[i] for each time step i starting from index start to index stop
            with stepation factor step (i.e. the value is generated if
            i-start % step == 0).
        """

        if not self._open:
            self.h5open()
            close = True
        else:
            close = False

        tslice = self._tslice(tslice)

        # Compute DtE = (h[x[n+1]]-h[x[n]]) / dt
        if DtE == 'deltaH':
            last_dtH_value = numpy.einsum('ti,ti->t',
                                          self['dxH', tslice.stop-1],
                                          self['dtx', tslice.stop-1])/self.fs
            output = numpy.ediff1d(self.E(tslice=tslice),
                                   to_end=last_dtH_value)*self.fs/tslice.step

        # Compute DtE = dxh.T * dtx
        elif DtE == 'DxhDtx':
            output = numpy.einsum('ti,ti->t',
                                  self['dxH', tslice],
                                  self['dtx', tslice])

        if postprocess is None:
            return output
        else:
            return postprocess(output)

        if close:
            self.h5close()

    # ----------------------------------------------------------------------- #

    def E(self, tslice=None, vslice=None, postprocess=None):
        """
        E
        ===

        Generator of discrete energy's values.

        Parameters
        -----------
        start: int or None, optional
            Starting index. If None, start=0 (default).
        stop: int or None,
            Stoping index. If None, stop=data.nt (default).
        step: int or None,
            stepation factor. If None, step = 1 (default).

        Returns
        -------

        E_generator: generator
            A python generator of scalar discrete energy's value E[i] for each
            time step i starting from index start to index stop with stepation
            factor step (i.e. the value is generated if i-start % step == 0).
        """

        return self._expression('H', tslice=tslice, vslice=vslice,
                                postprocess=postprocess)

    # ----------------------------------------------------------------------- #

    def pd(self, tslice=None, vslice=None, postprocess=None):
        """
        pd
        ==

        Generator of discrete dissipated power values.

        Parameters
        -----------
        start: int or None, optional
            Starting index. If None, start=0 (default).
        stop: int or None,
            Stoping index. If None, stop=data.nt (default).
        step: int or None,
            stepation factor. If None, step = 1 (default).

        Returns
        -------

        pd_generator: generator
            A python generator of scalar discrete dissipated power value pd[i]
            for each time step i starting from index start to index stop with
            stepation factor step (i.e. the value is generated if
            i-start % step == 0), with pd[i] = w[i] dot z[i].
        """

        return self._expression('pd', tslice=tslice, vslice=vslice,
                                postprocess=postprocess)

    # ----------------------------------------------------------------------- #

    def ps(self, tslice=None, vslice=None, postprocess=None):
        """
        ps
        ==

        Generator of discrete sources power values from h5 dataset.

        Parameters
        -----------
        start: int or None, optional
            Starting index. If None, start=0 (default).
        stop: int or None,
            Stoping index. If None, stop=data.nt (default).
        step: int or None,
            stepation factor. If None, step = 1 (default).

        Returns
        -------

        ps_generator: generator
            A python generator of scalar discrete sources power value ps[i]
            for each time step i starting from index start to index stop with
            stepation factor step (i.e. the value is generated if
            i-start % step == 0), with ps[i] = u[i] dot y[i].
        """

        if not self._open:
            self.h5open()
            close = True
        else:
            close = False

        output = numpy.einsum('ti,ti->t',
                              self['u', tslice],
                              self['y', tslice])

        if postprocess is None:
            return output
        else:
            return postprocess(output)

        if close:
            self.h5close()
