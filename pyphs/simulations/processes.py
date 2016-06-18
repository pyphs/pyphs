# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 16:10:47 2016

@author: Falaize
"""
from pyphs.misc.tools import progressbar
import time


def process_py(simulation):
    # get generators of u and p
    seq_u = simulation.data.u()
    seq_p = simulation.data.p()

    from pyphs.misc.io import open_files, close_files, dump_files
    files_to_open = ['x', 'dx', 'dxHd', 'w', 'z', 'yd']
    files = open_files(simulation.data.path, files_to_open)

    # init time step
    n = 0
    print "\n*** Simulation ***\n"
    for (u, p) in zip(seq_u, seq_p):
        simulation.internal.update(u=u, p=p)
        dump_files(simulation.internal, files)
        n += 1
        progressbar(n/float(simulation.nt))
    time.sleep(0.5)
    close_files(files)


def process_cpp(phs):

    phs.cppwrite()

    from pyphs.configs.cpp import cpp_build_and_run_script
    if cpp_build_and_run_script is None:
        import os
        print"\no==========================================================\
        ==o\n"
        print " Please, execute:\n" + phs.paths['cpp'] + \
            os.path.sep + \
            "/main.cpp"
        print"\no==========================================================\
        ==o\nWaiting....\n"
        raw_input()
    elif type(cpp_build_and_run_script) is str:
        import subprocess
        # Replace generic term 'phobj_path' by actual object path
        script = cpp_build_and_run_script.replace('phobj_path',
                                                  phs.path)
        # exec Build and Run script
        p = subprocess.Popen(script, shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        for line in iter(p.stdout.readline, ''):
            print line,
