#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 12:03:17 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

from pyphs.cpp.tools import indent, matrix_type


def append_args(method, files, objlabel):
    """
    add all pointers, accessors_vector, accessors_matrix, mutators_vectors,
    mutators_matrix for arguments from method.args_names to the cpp files for
    object with name objlabel.
    """
    _append_args_pointers(method, files)
    _append_args_accessors_vector(method, files, objlabel)
    _append_args_accessors_matrix(method, files, objlabel)
    _append_args_mutators_vectors(method, files, objlabel)
    _append_args_mutators_matrix(method, files, objlabel)


def _append_args_pointers(method, files):
    """
    add all pointers for arguments from method.args_names to the cpp files for
    object with name objlabel. pointers to 'args(i, 0)' for i in range(nargs)
    """
    title = "\n\n// Arguments\n"
    files['h']['private'] += title
    files['h']['private'] += \
        '\n{0} args;\n'.format(matrix_type(len(method.args), 1))
    for i, arg in enumerate(method.args):
        files['h']['private'] += \
            '\ndouble * {0} = & args({1}, 0);'.format(str(arg), i)


def _append_args_accessors_vector(method, files, objlabel):
    """
    add all accessors for arguments from method.args_names to the cpp files for
    object with name objlabel. return vector<double>
    """
    title = "\n\n// Acessors to Arguments, return vector<double>\n"
    files['h']['public'] += title
    files['cpp']['public'] += title
    for name in method.args_names:
        arg = getattr(method, name+'_expr')
        dim = len(arg)
        files['h']['public'] += \
            '\nvector<double> {0}_vector() const;'.format(name)
        files['cpp']['public'] += \
            "\n\nvector<double> " + \
            "{0}::{1}".format(objlabel, name) + \
            "_vector() const {"
        files['cpp']['public'] += \
            indent("\nvector<double> v = vector<double>({0});".format(dim))
        for i, symb in enumerate(arg):
            files['cpp']['public'] += \
                indent("\nv[{0}] = *{1};".format(i, str(symb)))
        files['cpp']['public'] += indent("\nreturn v;")
        files['cpp']['public'] += "\n}"


def _append_args_accessors_matrix(method, files, objlabel):
    """
    add all accessors for arguments from method.args_names to the cpp files for
    object with name objlabel. return Matrix<double, n, m>
    """
    title = "\n\n// Acessors to Arguments, return Matrix<double, n, m>\n"
    files['h']['public'] += title
    files['cpp']['public'] += title
    for name in method.args_names:
        arg = getattr(method, name+'_expr')
        dim = len(arg)
        files['h']['public'] += \
            '\n{0} {1}() const;'.format(matrix_type(dim, 1), name)
        files['cpp']['public'] += \
            "\n{0} {1}::{2}() const".format(matrix_type(dim, 1),
                                            objlabel, name) + ' {'
        files['cpp']['public'] += \
            indent('\n{0} m;'.format(matrix_type(dim, 1)))
        for i, symb in enumerate(arg):
            files['cpp']['public'] += \
                indent("\nm({0}, 0) = *{1};".format(i, str(symb)))
        files['cpp']['public'] += indent("\nreturn m;")
        files['cpp']['public'] += "\n}"


def _append_args_mutators_matrix(method, files, objlabel):
    """
    add all mutators for arguments from method.args_names to the cpp files for
    object with name objlabel. input is Matrix<double, n, m>
    """
    title = "\n\n// Mutators for Arguments, type = Matrix<double, n, m>\n"
    files['h']['public'] += title
    files['cpp']['public'] += title
    for name in method.args_names:
        arg = getattr(method, name+'_expr')
        dim = len(arg)
        files['h']['public'] += '\nvoid set_' + name + \
            '(Matrix<double, ' + str(dim) + ', 1> &);'
        files['cpp']['public'] += \
            "\nvoid {0}::set_{1}".format(objlabel, name) + \
            "(Matrix<double, {0}, 1> & m)".format(dim) + " {"
        for i, symb in enumerate(arg):
            files['cpp']['public'] += \
                '\n'+indent("*{0} = m({1}, 0);".format(str(symb), i))
        files['cpp']['public'] += "\n}"


def _append_args_mutators_vectors(method, files, objlabel):
    """
    add all mutators for arguments from method.args_names to the cpp files for
    object with name objlabel. input is vector<double>
    """
    title = "\n\n// Mutators for Arguments, type = vector<double>\n"
    files['h']['public'] += title
    files['cpp']['public'] += title
    for name in method.args_names:
        arg = getattr(method, name+'_expr')
        files['h']['public'] += \
            '\nvoid set_{0}(vector<double> &);'.format(name)
        files['cpp']['public'] += \
            "\nvoid {0}::set_{1}(vector<double> & v)".format(objlabel, name) +\
            " {"
        for i, symb in enumerate(arg):
            files['cpp']['public'] += "\n" + \
                indent("*{0} = v[{1}];".format(str(symb), i))
        files['cpp']['public'] += "\n}"
