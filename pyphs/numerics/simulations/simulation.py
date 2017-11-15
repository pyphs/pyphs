# -*- coding: utf-8 -*-
"""
Created on Tue May 24 11:20:26 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function
from pyphs.config import (CONFIG_METHOD, CONFIG_SIMULATION,
                          CONFIG_NUMERIC, CONFIG_CPP, VERBOSE)
from ..cpp.simu2cpp import simu2cpp, main_path
from ..cpp.method2cpp import method2cpp, parameters
from .. import Numeric
from .data import Data
from pyphs.misc.io import dump_files, with_files
import subprocess
import progressbar
import time
import os
import sys


class Simulation:
    """
    object that stores data and methods for simulation of PortHamiltonianObject
    """
    def __init__(self, method, config=None, inits=None, label=None):
        """
        Parameters
        -----------

        config : dic of configuration options

            keys and default values are

              'fs': 48e3,           # Sample rate (Hz)
              'grad': 'discret',    # In {'discret', 'theta', 'trapez'}
              'theta': 0.,          # Theta-scheme for the structure
              'split': False,       # split implicit from explicit part
              'maxit': 10,          # Max number of iterations for NL solvers
              'eps': 1e-16,         # Global numerical tolerance
              'path': None,         # Path to the results folder
              'pbar': True,         # Display a progress bar
              'timer': False,       # Display minimal timing infos
              'lang': 'c++',        # Language in {'python', 'c++'}
              'script': None,       # Call to C++ compiler and exec binary
              # Options for the data reader. The data are read from index imin
              # to index imax, rendering one element out of the number decim
              'load': {'imin': None,
                       'imax': None,
                       'decim': None}
        inits : dict
            Dictionary with variable name as keys and initialization values
            as value. E.g: inits = {'x': [0, 0, 1]} to initalize state x
            with dim(x) = 3, x[0] = x[1] = 0 and x[2] = 1.
        """

        self.method = method
        if label is None:
            label = method.label
        self.label = label

        # init config with standard configuration options
        self.config = CONFIG_SIMULATION.copy()
        self.config.update(CONFIG_NUMERIC)
        self.config.update(CONFIG_METHOD)
        self.config.update(CONFIG_CPP)

        # Update with method config
        self.config.update(self.method.config)

        # update with config arguments
        if config is None:
            config = {}
        else:
            for k in config.keys():
                if not k in self.config.keys():
                    text = 'Configuration key "{0}" unknown.'.format(k)
                    raise AttributeError(text)
        self.config.update(config)

        # Rebuild method if parameters are differents
        self.init_method()

        if self.config['path'] is None:
            self.config['path'] = os.getcwd()

        if not os.path.exists(self.config['path']):
            os.mkdir(self.config['path'])

        # Define inits
        self.inits = {}
        if inits is not None:
            self.inits.update(inits)

        self.init_numericalCore()

    def config_numeric(self):
        dic = dict()
        for k in CONFIG_NUMERIC.keys():
            dic[k] = self.config[k]
        return dic

    def config_method(self):
        dic = dict()
        for k in CONFIG_METHOD.keys():
            dic[k] = self.config[k]
        return dic

    def config_simulation(self):
        dic = dict()
        for k in CONFIG_SIMULATION.keys():
            dic[k] = self.config[k]
        return dic

    def config_cpp(self):
        dic = dict()
        for k in CONFIG_CPP.keys():
            dic[k] = self.config[k]
        return dic

    def init_numericalCore(self):
        """
        Build the Numeric from the Core.
        Additionnally, generate the c++ code if config['lang'] == 'c++'.
        """
        if not self.config['lang'] in ['c++', 'python']:
            raise AttributeError('Unknows language {}'.format(self.config['lang']))

        elif self.config['lang'] == 'python':
            setattr(self, 'nums', Numeric(self.method,
                                          inits=self.inits,
                                          config=self.config_numeric()))
        elif self.config['lang'] == 'c++':
            objlabel = self.method.label.upper()
            self.work_path = os.getcwd()
            self.cpp_path = os.path.join(main_path(self), objlabel.lower())
            self.src_path = os.path.join(self.cpp_path, 'src')
            if not os.path.exists(self.cpp_path):
                os.mkdir(self.cpp_path)
            if not os.path.exists(self.src_path):
                os.mkdir(self.src_path)
            method2cpp(self.method, objlabel=objlabel, path=self.src_path,
                        inits=self.inits,
                        config=self.config_numeric())

        self.data = Data(self.method, self.config)

    def init_method(self):
        """
        Build the numerical method.
        """
        if self.config_method() != self.method.config:
            self.method.__init__(self.method._core, config=self.config_method())

###############################################################################


    def init(self, nt=None, u=None, p=None,  inits=None,
             config=None, subs=None):
        """
    init
    ****

    Initialize simulation data.

    Parameters
    ----------

    u: iterable or None, optional
        Input sequence wich elements are arrays with shape (core.dims.y(), ).
        If the lenght nt of the sequence is known (e.g. sequ is a list), the
        number of simulation time steps is set to nt. If None, a sequence with
        length nt of zeros with appropriate shape is used (default).

    p: iterable or None, optional
        Input sequence wich elements are arrays with shape (core.dims.p(), ).
        If (i) the lenght of sequ is not known, and (ii) the length nt of seqp
        is known (e.g. seqp is a list), the number of simulation time steps is
        set to nt=len(seqp). If None, a sequence with length nt of zeros with
        appropriate shape is used (default).

    nt: int or None:
        Number of time steps. If None, the lenght of either sequ or seqp must
        be known (i.e. they are not either generators or None).

    inits : dict
        Dictionary with variable name as keys and initialization values
        as value. E.g: inits = {'x': [0., 0., 1.]} to initalize state x
        with dim(x) = 3, x[0] = x[1] = 0 and x[2] = 1.
        """

        init_numeric = False
        init_parameters = False

        if config is None:
            config = {}

        if inits is None:
            inits = {}

        if subs is None:
            subs = {}
        else:
            for k in subs.keys():
                if not k in self.method.subs.keys():
                    init_numeric = True
            if not init_numeric:
                init_parameters = True
        self.method.subs.update(subs)
        if init_parameters:
            self.init_parameters()

        c = self.config_method()
        c.update(self.config_numeric())
        c.update(self.config_simulation())

        c.update(config)

        if inits is not None and any([any(v1!=v2 for (v1, v2) in zip(self.inits[k], inits[k])) for k in inits.keys()]):
            self.inits.update(inits)
            init_numeric = True

        if any([self.config[k] != c[k] for k in list(self.config_numeric().keys()) +
                                                list(self.config_method().keys())]):
            self.config.update(c)
            self.init_method()

        if init_numeric:
            self.init_numericalCore()

        self.data.init_data(u, p, nt)

    def process(self):
        """
        Process simulation for all time steps.

        Usage
        -----
        After initialization of a Simulation object `simu.init`:

        .. code:: simu.process()

        """
        if VERBOSE >= 1:
            print('Simulation: Process...')

        if self.config['timer']:
            tstart = time.time()

        # language is 'py' or 'cpp'
        if not self.config['lang'] in ('c++', 'python'):
            text = 'Unknown language {}.'.format(self.config['language'])
            raise NameError(text)

        if self.config['lang'] == 'c++':
            self._process_cpp()

        elif self.config['lang'] == 'python':
            self._process_py()

        if self.config['timer']:
            tstop = time.time()

        if self.config['timer']:

            t_total = tstop-tstart
            print('Total time: {}s'.format(tstop-tstart))

            string = 'Total time w.r.t number of time-steps: {}s'
            time_it = (t_total/float(self.data.config['nt']))
            print(string.format(time_it))

        if VERBOSE >= 1:
            print('Simulation: Done')

    def init_parameters(self, subs=None):
        """
        Generate a new parameters.cpp based on a given substitution dictionary.
        """
        if subs is None:
            subs = self.method.subs
        else:
            self.method.subs = subs
        path = self.src_path
        parameters_files = parameters(subs, 'rhodes'.upper())
        for e in ['cpp', 'h']:
            filename = path + os.sep + 'parameters.{0}'.format(e)
            string = parameters_files[e]
            _file = open(filename, 'w')
            _file.write(string)
            _file.close()
        print('Parameters Files generated in \n{}'.format(path))

    def _init_pb(self):
        pb_widgets = ['\n', 'Simulation: ',
                      progressbar.Percentage(), ' ',
                      progressbar.Bar(), ' ',
                      progressbar.ETA()
                      ]
        self._pbar = progressbar.ProgressBar(widgets=pb_widgets,
                                             max_value=self.data.config['nt'])
        self._pbar.start()

    def _update_pb(self):
        self._pbar.update(self.n)

    def _close_pb(self):
        self._pbar.finish()

    def _process_py(self):

        # get generators of u and p
        data = self.data
        load = {'imin': 0, 'imax': None, 'decim': 1}
        seq_u = data.u(**load)
        seq_p = data.p(**load)

        path = os.path.join(self.config['path'], 'data')
        list_of_files = list(self.config['files'])

        def process(files):
            if self.config['pbar']:
                self._init_pb()

            # init time step
            self.n = 0

            # process
            for (u, p) in zip(seq_u, seq_p):
                # update numerics
                self.nums.update(u=u, p=p)

                # write to files
                dump_files(self.nums, files)

                self.n += 1

                # update progressbar
                if self.config['pbar']:
                    self._update_pb()

            if self.config['pbar']:
                self._close_pb()

            time.sleep(0.1)

        with_files(path, list_of_files, process)
        # close_files(files)

    def _process_cpp(self):

        # build simu.cpp
        simu2cpp(self)

        # go to build folder
        os.chdir(self.cpp_path)

        # execute the bash script
        self.system_call('./run.sh')

        # go back to work folder
        os.chdir(self.work_path)

    @staticmethod
    def system_call(cmd):
        """
        Execute a system command.

        Parameter
        ---------

        cmd : list
            List of arguments.

        Example
        -------
        Change directory with
        cmd = ['cd', './my/folder']
        system_call(cmd)
        """
        system_call(cmd)

    @staticmethod
    def execute_bash(text):
        """
        Execute a bash script, ignoring lines starting with #

        Parameter
        ---------

        text : str
            Bash script content. Execution of each line iteratively.
        """
        execute_bash(text)


def system_call(cmd):
    """
    Execute a system command.

    Parameter
    ---------

    cmd : list
        List of arguments.

    Example
    -------

    Change directory with

    >>> cmd = ['cd', './my/folder']
    >>> system_call(cmd)

    """
    if sys.platform.startswith('win'):
        shell = True
    else:
        shell = True
    if VERBOSE >= 1:
        print(cmd)
    p = subprocess.Popen(cmd, shell=shell,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    for line in iter(p.stdout.readline, b''):
        l = line.decode()
        if VERBOSE >= 1:
            print(l)


def execute_bash(text):
    """
    Execute a bash script, ignoring lines starting with #

    Parameter
    ---------

    text : str
        Bash script content. Execution of each line iteratively.
    """
    for line in text.splitlines():
        if line.startswith('#') or len(line) == 0:
            pass
        else:
            system_call(line.split())
