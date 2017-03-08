# -*- coding: utf-8 -*-
"""
Created on Tue May 24 11:20:26 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function
from pyphs.config import standard_simulations
from pyphs.cpp.simu2cpp import simu2cpp
from pyphs.numerics.method import PHSNumericalMethod
from pyphs.numerics.numeric import PHSNumericalCore
from .data import PHSData
from pyphs.misc.io import open_files, close_files, dump_files
import subprocess
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
        setattr(self, '_core', core.__deepcopy__())

        self.fs = 0
        self.it = list()

        self.init_numericalcore()
        assert self.config['language'] in ['c++', 'python']

###############################################################################

    def init_numericalmethod(self):
        if not self.fs == self.config['fs']:
            Method = PHSNumericalMethod
            self.method = Method(self._core, config=self.config)
            self.fs = self.config['fs']

    def init_numericalcore(self, x0=None):
        self.init_numericalmethod()
        setattr(self, 'nums', PHSNumericalCore(self.method,
                                               config=self.config))
        if x0 is not None:
            x0 = np.array(x0)
            assert len(x0.shape) == 1, \
                'x0 is not a 1D array, got x={}'.format(x0)
            self.nums.set_x(x0)

    def init(self, sequ=None, seqp=None, x0=None, nt=None, config=None):
        if config is None:
            config = {}
        self.config.update(config)
        self._core.M = self.nums.method.core.M
        setattr(self, 'data', PHSData(self._core, self.config))
        self.data.init_data(sequ, seqp, x0, nt)
        self.init_numericalcore(x0=x0)

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
            self.process_cpp()

        elif self.config['language'] == 'python':
            self.process_py()

        if self.config['timer']:
            tstop = time.time()

        if self.config['timer']:
            time_it = ((tstop-tstart)/float(self.data.config['nt']))
            print('time per iteration: {0!s} s'.format(format(time_it, 'f')))
            time_ratio = time_it*self.config['fs']
            print('ratio compared to real-time: {0!s}'.format(format(
                time_ratio, 'f')))


    def init_pb(self):
        pb_widgets = ['\n', 'Simulation: ',
                      progressbar.Percentage(), ' ',
                      progressbar.Bar(), ' ',
                      progressbar.ETA()
                      ]
        self.pbar = progressbar.ProgressBar(widgets=pb_widgets,
                                       maxval=self.data.config['nt'])
        self.pbar.start()

    def update_pb(self):
        self.pbar.update(self.n)

    def close_pb(self):
        self.pbar.finish()

    def process_py(self):

        self.config['files_to_save'] = map(str.lower,
                                           self.config['files_to_save'])

        # get generators of u and p
        data = self.data
        seq_u = data.u()
        seq_p = data.p()

        files = open_files(self.config['path'] + os.sep + 'data',
                           self.config['files_to_save'])

        if self.config['progressbar']:
            self.init_pb()

        # init time step
        self.n = 0
        for (u, p) in zip(seq_u, seq_p):
            self.nums.update(u=np.array(u), p=np.array(p))
            dump_files(self.nums, files)
            self.n += 1
            if self.config['progressbar']:
                self.update_pb()
        if self.config['progressbar']:
            self.close_pb()

        time.sleep(0.5)
        close_files(files)

    def process_cpp(self):

        simu2cpp(self)

        if self.config['cpp_build_and_run_script'] is None:
            print("\no==========================================================\
            ==o\n")
            print("Please, execute:\n" + self.config['path'] + os.sep + 'cpp' +
                  os.path.sep + "/main.cpp")
            print("\no==========================================================\
            ==o\n")
            input("Press a key when done.\nWaiting....\n")
        else:
            # Replace generic term 'phobj_path' by actual object path
            script = self.config['cpp_build_and_run_script']
            script = script.replace('pyphs_path', self.config['path'])
            # exec Build and Run script
            system_call(script)


def system_call(cmd):
    p = subprocess.Popen(cmd, shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    for line in iter(p.stdout.readline, b''):
        print(line.decode()),
