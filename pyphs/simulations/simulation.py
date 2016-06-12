# -*- coding: utf-8 -*-
"""
Created on Tue May 24 11:20:26 2016

@author: Falaize
"""
from pyphs.misc.io import write_data
from pyphs.configs.simulations import standard_config
from data import Data
import time
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
                * 'fs': 48e3,
                * 'numtol': EPS,
                * 'maxit': 100,
                * 'split': True
                * 'solver': 'standard',
                * 'timer': True,
                * 'load_options': {'decim': 1,
                                   'imin': 0,
                                   'imax': None},

        sequ : iterable of tuples of inputs values

        seqp : iterable of tuples of parameters values

        nt : number of time steps (state x goes to x[nt+1])
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
                from pyphs.symbolics.structures.tools import split_linear
                split_linear(phs)
        else:
            # set all components as nonlinear
            phs.dims.xl = phs.dims.wl = 0

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
                if phs.dims.y() > 0:
                    yield [0, ]*phs.dims.y()
                else:
                    yield ""
        sequ = generator_u()
    # if seqp is not provided, a sequence of [[0]*np]*nt is assumed
    if seqp is None:
        def generator_p():
            for _ in range(simulation.nt):
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

    # build data i/o structure
    simulation.data = Data(simulation, phs)
    # write input sequence
    write_data(phs, sequ, 'u')
    # write parameters sequence
    write_data(phs, seqp, 'p')
    # write initial state
    write_data(phs, [x0, ], 'x0')
