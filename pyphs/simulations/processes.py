# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 16:10:47 2016

@author: Falaize
"""

import progressbar
import time


def process_py(simulation):
    # get generators of u and p
    data = simulation.phs.data
    seq_u = data.u()
    seq_p = data.p()

    from pyphs.misc.io import open_files, close_files, dump_files
    data_path = simulation.phs.paths['data']
    files_to_open = ['x', 'dx', 'dxHd', 'w', 'z', 'yd']
    files = open_files(data_path, files_to_open)

    pb_widgets = ['\n', 'Simulation: ', progressbar.Percentage(), ' ',
                  progressbar.Bar(), ' ', progressbar.ETA()]
    pbar = progressbar.ProgressBar(widgets=pb_widgets,
                                   maxval=simulation.config['nt'])
    pbar.start()

    # init time step
    n = 0
    print "\n*** Simulation ***\n"
    for (u, p) in zip(seq_u, seq_p):
        simulation.update(u=u, p=p)
        dump_files(simulation, files)
        n += 1
        pbar.update(n)
    pbar.finish()
#        progressbar(n/float(simulation.nt))
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
