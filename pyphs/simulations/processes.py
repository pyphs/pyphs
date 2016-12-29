# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 16:10:47 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function
from builtins import input

import numpy as np
import progressbar
import time

from .tools import update, build_args, build_funcs
from pyphs.misc.io import open_files, close_files, dump_files


def process_cpp(simu):

    simu._phs.cppbuild()

    from pyphs.conf import cpp_build_and_run_script
    if cpp_build_and_run_script is None:
        import os
        print("\no==========================================================\
        ==o\n")
        print(" Please, execute:\n" + simu._phs.paths['cpp'] +
              os.path.sep + "/main.cpp")
        print("\no==========================================================\
        ==o\n")
        input("Press a key when done.\nWaiting....\n")
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
            print(line),
