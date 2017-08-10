# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 16:01:13 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function
import os
from pyphs.config import CONFIG_CPP

linesplit = '\n//' + '='*74

def make_executable(path):
    """
    """
    os.chmod(path, 0b111101101)

def formatPath(path):
    r"""
return a string representation of the path with:
    - doubling of escape characters \\;
    - strip of the side ' characters.
    """
    return repr(path).strip("'")


# formated OS dependent path separator
SEP = formatPath(os.sep)


def main_path(simu):
    """
Return a formated string associated with the path in simu.config['path']
    """
    return formatPath(simu.config['path'])


def dereference(method):
    return method.args() + [k for k in method.subscpp]


def matrix_type(dim1, dim2):
    return "Matrix<{0},{1}, {2}>".format(CONFIG_CPP['float'], str(dim1), str(dim2))


def indent(string):
    return "\n".join(['    ' + el for el in string.split('\n')])
