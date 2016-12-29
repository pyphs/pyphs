# -*- coding: utf-8 -*-
"""
Created on Tue May 24 11:20:26 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function
from pyphs.numerics.methods import dic_of_numerical_methods
from pyphs.numerics import PHSNumericalCore
from pyphs.config import standard_simulations
from .data import Data
from pyphs.misc.io import open_files, close_files, dump_files
import progressbar
import time
import os
import numpy as np


class PHSSimulation:
    """
    object that stores data and methods for simulation of PortHamiltonianObject
    """
    def __init__(self, core, config=None):
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
        self.config = standard_simulations.copy()

        # update with provided opts
        if config is None:
            config = {}
        self.config.update(config)

        if self.config['path'] is None:
            self.config['path'] = os.getcwd()

        # store PHSCore
        setattr(self, 'core', core.__deepcopy__())

        self.fs = 0

        if self.config['language'] == 'python':
            self.init_numericalcore()
        else:
            assert False

###############################################################################

    def init_numericalmethod(self):
        if not self.fs == self.config['fs']:
            Method = dic_of_numerical_methods[self.config['method']]
            self.method = Method(self.core, config=self.config)
            self.fs = self.config['fs']

    def init_numericalcore(self):
        self.init_numericalmethod()
        setattr(self, 'nums', PHSNumericalCore(self.method,
                                               config=self.config))

    def init(self, sequ=None, seqp=None, x0=None, nt=None, config=None):
        if config is None:
            config = {}
        self.config.update(config)
        setattr(self, 'data', Data(self.core, self.config))
        self.data.init_data(sequ, seqp, x0, nt)
        if self.config['language'] == 'python':
            self.init_numericalcore()

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
            self.process_py()

        if self.config['timer']:
            tstop = time.time()

        if self.config['timer']:
            time_it = ((tstop-tstart)/float(self.config['nt']))
            print('time per iteration: {0!s} s'.format(format(time_it, 'f')))
            time_ratio = time_it*self.config['fs']
            print('ratio compared to real-time: {0!s}'.format(format(
                time_ratio, 'f')))

    def process_py(self):

        # get generators of u and p
        data = self.data
        seq_u = data.u()
        seq_p = data.p()

        files = open_files(self.config['path'], self.config['files_to_save'])

        if self.config['progressbar']:
            pb_widgets = ['\n', 'Simulation: ', progressbar.Percentage(), ' ',
                          progressbar.Bar(), ' ', progressbar.ETA()]
            pbar = progressbar.ProgressBar(widgets=pb_widgets,
                                           maxval=self.config['nt'])
            pbar.start()
        else:
            print("\n*** Simulation... ***\n")

        # init time step
        n = 0
        for (u, p) in zip(seq_u, seq_p):
            self.nums.update(u=np.array(u), p=np.array(p))
            dump_files(self.nums, files)
            n += 1
            if self.config['progressbar']:
                pbar.update(n)
        if self.config['progressbar']:
            pbar.finish()
        time.sleep(0.5)
        close_files(files)
