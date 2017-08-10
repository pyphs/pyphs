#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 12:03:17 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

from .tools import indent, matrix_type
from sympy.printing import ccode
from pyphs.core.tools import types
from pyphs.config import CONFIG_CPP
from .tools import dereference, linesplit


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
    _append_args_mutators_elements(method, files, objlabel)
    _append_args_data(method, files, objlabel)
    _append_args_init(method, files, objlabel)


def _append_args_pointers(method, files):
    """
    add all pointers for arguments from method.args_names to the cpp files for
    object with name objlabel. pointers to 'args(i, 0)' for i in range(nargs)
    """
    title = linesplit + "\n// Arguments"
    files['h']['private'] += title
    files['h']['private'] += \
        '\n{0} args;'.format(matrix_type(len(method.args()), 1))
    for i, arg in enumerate(method.args()):
        files['h']['private'] += \
            '\n{2} * {0} = & args({1}, 0);'.format(str(arg), i, CONFIG_CPP['float'])


def _append_args_accessors_vector(method, files, objlabel):
    """
    add all accessors for arguments from method.args_names to the cpp files for
    object with name objlabel. return vector<{0}>
    """.format(CONFIG_CPP['float'])
    title = linesplit + "\n// Acessors to Arguments, return vector<{0}>".format(CONFIG_CPP['float'])
    files['h']['public'] += title
    files['cpp']['public'] += title
    for name in method.args_names:
        arg = getattr(method, name+'_expr')
        dim = len(arg)
        files['h']['public'] += \
            '\nvector<{1}> {0}_vector() const;'.format(name, CONFIG_CPP['float'])
        files['cpp']['public'] += \
            "\nvector<{0}> ".format(CONFIG_CPP['float']) + \
            "{0}::{1}".format(objlabel, name) + \
            "_vector() const {"
        files['cpp']['public'] += \
            indent("\nvector<{1}> v = vector<{1}>({0});".format(dim, CONFIG_CPP['float']))
        for i, symb in enumerate(arg):
            files['cpp']['public'] += \
                indent("\nv[{0}] = *{1};".format(i, str(symb)))
        files['cpp']['public'] += indent("\nreturn v;")
        files['cpp']['public'] += "\n}"


def _append_args_accessors_matrix(method, files, objlabel):
    """
    add all accessors for arguments from method.args_names to the cpp files for
    object with name objlabel. return Matrix<{0}, n, m>
    """.format(CONFIG_CPP['float'])
    title = linesplit + "\n// Acessors to Arguments, return Matrix<{0}, n, m>".format(CONFIG_CPP['float'])
    files['h']['public'] += title
    files['cpp']['public'] += title
    for name in method.args_names:
        arg = getattr(method, name+'_expr')
        dim0 = len(arg)
        if dim0 == 0:
            dim1 = 0
        else:
            dim1 = 1
        files['h']['public'] += \
            '\n{0} {1}() const;'.format(matrix_type(dim0, dim1), name)
        files['cpp']['public'] += \
            "\n{0} {1}::{2}() const".format(matrix_type(dim0, dim1),
                                            objlabel, name) + ' {'
        files['cpp']['public'] += \
            indent('\n{0} m;'.format(matrix_type(dim0, dim1)))
        for i, symb in enumerate(arg):
            files['cpp']['public'] += \
                indent("\nm({0}, 0) = *{1};".format(i, str(symb)))
        files['cpp']['public'] += indent("\nreturn m;")
        files['cpp']['public'] += "\n}"


def _append_args_mutators_matrix(method, files, objlabel):
    """
    add all mutators for arguments from method.args_names to the cpp files for
    object with name objlabel. input is Matrix<{0}, n, m>
    """.format(CONFIG_CPP['float'])
    title = linesplit + "\n// Mutators for Arguments, type = Matrix<{0}, n, m>".format(CONFIG_CPP['float'])
    files['h']['public'] += title
    files['cpp']['public'] += title
    for name in method.args_names:
        arg = getattr(method, name+'_expr')
        dim0 = len(arg)
        if dim0 == 0:
            dim1 = 0
        else:
            dim1 = 1
        files['h']['public'] += '\nvoid set_' + name + \
            '(Matrix<{2}, {0}, {1}> &);'.format(dim0, dim1, CONFIG_CPP['float'])
        files['cpp']['public'] += \
            "\nvoid {0}::set_{1}".format(objlabel, name) + \
            "(Matrix<{2}, {0}, {1}> & m)".format(dim0, dim1, CONFIG_CPP['float']) + " {"
        for i, symb in enumerate(arg):
            files['cpp']['public'] += \
                '\n'+indent("*{0} = m({1}, 0);".format(str(symb), i))
        files['cpp']['public'] += "\n}"


def _append_args_mutators_vectors(method, files, objlabel):
    """
    add all mutators for arguments from method.args_names to the cpp files for
    object with name objlabel. input is vector<{0}>
    """.format(CONFIG_CPP['float'])
    title = linesplit + "\n// Mutators for Arguments, type = vector<{0}>".format(CONFIG_CPP['float'])
    files['h']['public'] += title
    files['cpp']['public'] += title
    for name in method.args_names:
        arg = getattr(method, name+'_expr')
        files['h']['public'] += \
            '\nvoid set_{0}(vector<{1}> &);'.format(name, CONFIG_CPP['float'])
        files['cpp']['public'] += \
            "\nvoid {0}::set_{1}(vector<{2}> & v)".format(objlabel, name, CONFIG_CPP['float']) +\
            " {"
        for i, symb in enumerate(arg):
            files['cpp']['public'] += "\n" + \
                indent("*{0} = v[{1}];".format(str(symb), i))
        files['cpp']['public'] += "\n}"


def _append_args_mutators_elements(method, files, objlabel):
    """
    add all mutators for arguments from method.args_names to the cpp files for
    object with name objlabel. input is {0} and int index.
    """.format(CONFIG_CPP['float'])
    title = linesplit + "\n// Mutators for a single argument, types are {0} with int index".format(CONFIG_CPP['float'])
    files['h']['public'] += title
    files['cpp']['public'] += title
    for name in method.args_names:
        arg = getattr(method, name+'_expr')
        files['h']['public'] += \
            '\nvoid set_{0}({1} &, unsigned int &);'.format(name, CONFIG_CPP['float'])
        files['cpp']['public'] += \
            "\nvoid {0}::set_{1}({2} & value, unsigned int & index)".format(objlabel, name, CONFIG_CPP['float']) +\
            " {"
        for i, symb in enumerate(arg):
            if i == 0:
                files['cpp']['public'] += "\n" + \
                    indent("if(index == {0})".format(i)) + ' {' + \
                    "\n" + \
                    indent(indent("*{0} = value;".format(str(symb)))) + \
                    "\n" + \
                    indent('}')
            else:
                files['cpp']['public'] += "\n" + \
                    indent("else if(index == {0})".format(i)) + ' {' + \
                    "\n" + \
                    indent(indent("*{0} = value;".format(str(symb)))) + \
                    "\n" + \
                    indent('}')
        files['cpp']['public'] += "\n}"

###############################################################################
# DATA

def _append_args_data(method, files, objlabel):
    title = linesplit + "\n// Arguments Initialisation Data"
    files['cpp']['init'] += title
    for name in method.inits.keys():
        cpp = _str_args_init_data(method, name)
        files['cpp']['init'] += '\n' + cpp


def _str_args_init_data(method, name):
    mat = types.matrix_types[0](method.inits[name])
    mat_dic = dict((((i, j), e) for i, j, e in mat.row_list()))
    init_data = 'vector<{1}> {0}_data ='.format(name, CONFIG_CPP['float']) + ' {'
    crop = False
    for n in range(mat.shape[1]):
        for m in range(mat.shape[0]):
            crop = True
            data = "0., "
            if (m, n) in mat_dic.keys():
                expr = mat[m, n]
                symbs = expr.free_symbols
                if not any(symb in method.args() for symb in symbs):
                    c = ccode(expr, dereference=dereference(method))
                    data = 'float({0}), '.format(c)
            init_data += data
    if crop:
        init_data = init_data[:-2]
    init_data += '};'
    return init_data

###############################################################################
# INIT

def _append_args_init(method, files, objlabel):
    title = linesplit + "\n// Arguments Initialisation"
    files['cpp']['init'] += title
    for name in method.inits.keys():
        cpp = '\nset_{0}({0}_data);'.format(name)
        files['cpp']['init'] += cpp
