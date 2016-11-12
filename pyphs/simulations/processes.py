# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 16:10:47 2016

@author: Falaize
"""

import progressbar
import time
from tools import update
import numpy as np


def process_py(simulation):

    # lambdify exprs and define get/set for args
    from tools import build_args, build_funcs
    build_args(simulation)
    build_funcs(simulation)

    # get generators of u and p
    data = simulation._phs.data
    seq_u = data.u()
    seq_p = data.p()

    from pyphs.misc.io import open_files, close_files, dump_files

    data_path = simulation._phs.paths['data']

    files_to_open = ['x', 'dx', 'dxH', 'w', 'z', 'y']

    files = open_files(data_path, files_to_open)

    if simulation.config['progressbar']:
        pb_widgets = ['\n', 'Simulation: ', progressbar.Percentage(), ' ',
                      progressbar.Bar(), ' ', progressbar.ETA()]
        pbar = progressbar.ProgressBar(widgets=pb_widgets,
                                       maxval=simulation.config['nt'])
        pbar.start()
    # init time step
    n = 0
    print "\n*** Simulation ***\n"
    for (u, p) in zip(seq_u, seq_p):
        update(simulation, u=np.array(u), p=np.array(p))
        dump_files(simulation, files)
        n += 1
        if simulation.config['progressbar']:
            pbar.update(n)
    if simulation.config['progressbar']:
        pbar.finish()
    time.sleep(0.5)
    close_files(files)


def process_cpp(simu):

    simu._phs.cppbuild()

    from pyphs.generation.codecpp.config import cpp_build_and_run_script
    if cpp_build_and_run_script is None:
        import os
        print"\no==========================================================\
        ==o\n"
        print " Please, execute:\n" + simu._phs.paths['cpp'] + \
            os.path.sep + \
            "/main.cpp"
        print"\no==========================================================\
        ==o\nWaiting....\n"
        raw_input()
    elif type(cpp_build_and_run_script) is str:
        import subprocess
        # Replace generic term 'phobj_path' by actual object path
        script = cpp_build_and_run_script.replace('phobj_path',
                                                  simu._phs.path)
        # exec Build and Run script
        p = subprocess.Popen(script, shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        for line in iter(p.stdout.readline, ''):
            print line,
