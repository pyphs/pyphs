# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 10:22:56 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

from pyphs.config import standard_simulations
from pyphs.misc.io import data_generator, write_data
from pyphs.misc.signals.waves import wavwrite
from pyphs.plots.data import plot, plot_powerbal
import os
import numpy

try:
    import itertools.izip as zip
except ImportError:
    pass

class PHSData:
    """
    container for simulation data
    """
    def __init__(self, core, config):

        # init config with standard configuration options
        self.config = standard_simulations.copy()
        self.config.update(config)
        self.core = core

        def dummy_func(name):
            def get_seq(ind=None, postprocess=None, imin=None, imax=None,
                        decim=None):
                return self.data_generator(name, ind=ind, imin=imin,
                                           imax=imax, decim=decim,
                                           postprocess=postprocess)
            return get_seq

        for name in list(self.core.args_names) + ['y', 'dxH', 'z', 'dx']:
            setattr(self, name, dummy_func(name))

    def t(self, imin=None, imax=None, decim=None):
        options = self.config['load_options']
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

    def dtE(self, imin=None, imax=None, decim=None):
        """
        Energy variation
        """
        options = self.config['load_options']
        options = {'imin': options['imin'] if imin is None else imin,
                   'imax': options['imax'] if imax is None else imax,
                   'decim': options['decim'] if decim is None else decim}

        if not hasattr(self.core, 'evals'):
            self.core.build_evals()
        H = self.core.evals.H
        for x, dx in zip(self.x(**options), self.dx(**options)):
            xpost = map(sum, zip(x, dx))
            yield (H(*xpost) - H(*x))*self.config['fs']
#        for dtx, dxh in zip(self.dtx(**options), self.dxH(**options)):
#            yield scalar_product(dtx, dxh)

    def pd(self, imin=None, imax=None, decim=None):
        """
        Dissipated power
        """
        options = self.config['load_options']
        options = {'imin': options['imin'] if imin is None else imin,
                   'imax': options['imax'] if imax is None else imax,
                   'decim': options['decim'] if decim is None else decim}
        if not hasattr(self.core, 'evals'):
            self.core.build_evals()
        R = self.core.evals.R
        for w, z, a, b, args in zip(self.w(**options),
                                    self.z(**options),
                                    self.a(**options),
                                    self.b(**options),
                                    self.args(**options)):
            yield scalar_product(w, z) + \
                scalar_product(a,
                               a,
                               R(*[args[i] for i in self.core.evals.R_inds]))

    def ps(self, imin=None, imax=None, decim=None):
        """
        Source power
        """
        options = self.config['load_options']
        options = {'imin': options['imin'] if imin is None else imin,
                   'imax': options['imax'] if imax is None else imax,
                   'decim': options['decim'] if decim is None else decim}
        for u, y in zip(self.u(**options),
                        self.y(**options)):
            yield scalar_product(u, y)

    def a(self, imin=None, imax=None, decim=None):
        """
        right-hand side
        """
        options = self.config['load_options']
        options = {'imin': options['imin'] if imin is None else imin,
                   'imax': options['imax'] if imax is None else imax,
                   'decim': options['decim'] if decim is None else decim}
        for dxH, z, u in zip(self.dxH(**options),
                             self.z(**options),
                             self.u(**options)):
            yield dxH + z + u

    def args(self, imin=None, imax=None, decim=None):
        """
        arguments of the system function in exprs
        """
        options = self.config['load_options']
        options = {'imin': options['imin'] if imin is None else imin,
                   'imax': options['imax'] if imax is None else imax,
                   'decim': options['decim'] if decim is None else decim}
        for x, dx, w, u, p in zip(self.x(**options),
                                  self.dx(**options),
                                  self.w(**options),
                                  self.u(**options),
                                  self.p(**options)):
            yield x + dx + w + u + p

    def dtx(self, ind=None, imin=None, imax=None, decim=None):
        for dtx in self.dx(postprocess=self.dxtodtx, ind=ind, imin=imin,
                           imax=imax, decim=decim):
            yield dtx

    def dxtodtx(self, dx):
        return numpy.asfarray(dx)*self.config['fs']

    def b(self, imin=None, imax=None, decim=None):
        """
        left-hand side
        """
        options = self.config['load_options']
        options = {'imin': options['imin'] if imin is None else imin,
                   'imax': options['imax'] if imax is None else imax,
                   'decim': options['decim'] if decim is None else decim}

        for dtx, w, y in zip(self.dx(postprocess=self.dxtodtx, **options),
                             self.w(**options),
                             self.y(**options)):
            yield list(dtx) + list(w) + list(y)

    def data_generator(self, name, ind=None, postprocess=None,
                       imin=None, imax=None, decim=None):
        opts = self.config['load_options']
        options = {'imin': opts['imin'] if imin is None else imin,
                   'imax': opts['imax'] if imax is None else imax,
                   'decim': opts['decim'] if decim is None else decim}

        path = self.config['path'] + os.sep + 'data'
        filename = path + os.sep + name.lower() + '.txt'
        generator = data_generator(filename, ind=ind, postprocess=postprocess,
                                   **options)
        return generator

    def init_data(self, sequ, seqp, x0, nt):
        # get number of time-steps
        if hasattr(sequ, 'index'):
            nt = len(sequ)
        elif hasattr(sequ, 'index'):
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
                    if self.core.dims.y() > 0:
                        yield [0, ]*self.core.dims.y()
                    else:
                        yield ""
            sequ = generator_u()
        # if seqp is not provided, a sequence of [[0]*np]*nt is assumed
        if seqp is None:
            def generator_p():
                for _ in range(nt):
                    if self.core.dims.p() > 0:
                        yield [0, ]*self.core.dims.p()
                    else:
                        yield ""
            seqp = generator_p()

        if x0 is None:
            x0 = [0, ]*self.core.dims.x()
        else:
            assert isinstance(x0, (list, tuple, numpy.array)), \
                'x0 not a list, tuple or numpy.array: got {}'.format(x0)
            assert len(x0) == self.core.dims.x(), 'len(x0) is len(x)'
            assert isinstance(x0[0], (float, int)), \
                'x0[0] not a number, got {0!s}'.format(type(x0[0]))
        # write input sequence
        write_data(self.config['path']+os.sep+'data', sequ, 'u')
        # write parameters sequence
        write_data(self.config['path']+os.sep+'data', seqp, 'p')
        # write initial state
        write_data(self.config['path']+os.sep+'data', [x0, ], 'x0')

        self.config['nt'] = nt

    def wavwrite(self, name, index, fs_in, filename=None, path=None, gain=1,
                 fs_out=None):
        """
        write phs.simulation.data.name[index] in the folder pointed by \
phs.paths['wav'].
        """
        if fs_out is None:
            fs_out = fs_in
        if filename is None:
            filename = name
        if path is None:
            path = os.getcwd()
        if not os.path.exists(path):
            os.makedirs(path)
        data = getattr(self, name)
        sig = []
        for el in data():
            s = gain*el[index]
            if abs(s) >= 1:
                s = 0.
            sig.append(s)
        wavwrite(sig, fs_in, path + os.sep + filename, fs_out=fs_out)

    def plot_powerbal(self, mode='single', opts=None):
        """
        Plot the power balance. mode is 'single' or 'multi' for single figure \
or multifigure (default is 'single').
        """
        plot_powerbal(self, mode=mode, opts=opts)

    def plot(self, var_list, imin=0, imax=None):
        """
        Plot each data.seq_'var'['ind'] in var_list = [(var1, ind1), (...)]
        """
        plot(self, var_list, imin=imin, imax=imax)

###########################################################################
def scalar_product(list1, list2, weight_matrix=None):
    list1, list2 = list(list1), list(list2)
    if weight_matrix is None:
        weight_matrix = numpy.eye(len(list1))
    return numpy.dot(numpy.array(list1),
                     numpy.dot(weight_matrix, numpy.array(list2)))
