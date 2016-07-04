# -*- coding: utf-8 -*-
"""
Created on Tue May 24 11:20:26 2016

@author: Falaize
"""

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

        # init config with standard configuration options
        self.config = config.standard
        # update with provided opts
        if opts is None:
            opts = {}
        self.config.update(opts)
        # store phs
        self._phs = phs

###############################################################################

    def init_expressions(self):
        """
        Init the phs.simu.exprs module that contains all expressions for \
simulation.
        """

        if self.config['presubs']:
            self._phs.apply_subs()

        # split system into linear and nonlinear parts
        force_nolin = not self.config['split']

        from pyphs.symbolics.structures.tools import split_linear
        split_linear(self._phs, force_nolin=force_nolin)

        from expressions import SimulationExpressions
        self.exprs = SimulationExpressions(self._phs)

###############################################################################

    def init(self, sequ=None, seqp=None, x0=None, nt=None, opts=None):
        if opts is not None:
            self.config.update(opts)

        self.init_expressions()
        self._phs.data.init_data(sequ, seqp, x0, nt)

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
            time_it = ((tstop-tstart)/float(self.config['nt']))
            print 'time per iteration: {0!s} s'.format(format(time_it, 'f'))
            time_ratio = time_it*self.config['fs']
            print 'ratio compared to real-time: {0!s}'.format(format(
                time_ratio, 'f'))
