# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 16:01:13 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function


def dereference(method):
    return method.core.args() + [k for k in method.core.subs]


def matrix_type(dim1, dim2):
    return "Matrix<double, " + str(dim1) + ', ' + str(dim2) + '>'


def indent(string):
    return "\n".join(['    ' + el for el in string.split('\n')])


def name2dim(name):
    """
    return dim label associated with variable 'name' (eg. 'nx' if name='dxH').
    """
    parser = {'x': 'nx',
              'dx': 'nx',
              'dxH': 'nx',
              'xl': 'nxl',
              'dxl': 'nxl',
              'dxHl': 'nxl',
              'xnl': 'nxnl',
              'dxnl': 'nxnl',
              'dxHnl': 'nxnl',
              'x0': 'nx',
              'w': 'nw',
              'z': 'nw',
              'wl': 'nwl',
              'zl': 'nwl',
              'wnl': 'nwnl',
              'znl': 'nwnl',
              'u': 'ny',
              'y': 'ny',
              'p': 'np',
              'subs': 'nsubs',
              'vl': 'nl',
              'vnl': 'nnl',
              'fl': 'nl',
              'fnl': 'nnl'}
    return parser[name]


def str_matblk(mat_name, blck_name, blck_dims, blck_pos):
    string_h = "\ndouble * ptr_" + blck_name + " = "
    str_dims = "<" + str(blck_dims[0]) + ', ' + str(blck_dims[1]) + ">"
    str_pos = "(" + str(blck_pos[0]) + ', ' + str(blck_pos[1]) + ")"
    string_h += " & " + mat_name + ".block" + str_dims + str_pos + "(0);"
    string_cpp = "\nMap<Matrix<double, " + str_dims[1:-1] + ">> "
    string_cpp += blck_name + '(ptr_' + blck_name + ', ' + \
        str_dims[1:-1] + ');'
    return string_h, string_cpp


def str_get_int(class_ref, name):
    strget = "const unsigned int " + class_ref + "get_" + name \
        + "() const {\n    return " + name + ";\n}\n"
    return strget


def str_get_vec(class_ref, name, dim):
    strget = ""
    strget += "\nvector<double> "
    strget += class_ref
    strget += "get_" + name + "() const { \n"
    strget += "    vector<double> v = vector<double>(get_" + dim + "());\n"
    strget += "    for (int i=0; i<get_" + dim + "(); i++) {\n"
    strget += "        v[i] = " + name + "[i];\n"
    strget += "    }\n"
    strget += "    return v;\n"
    strget += "    }"
    return strget
