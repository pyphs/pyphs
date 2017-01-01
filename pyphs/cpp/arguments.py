#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 12:03:17 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

from pyphs.cpp.tools import indent, matrix_type


def append_args(method, files, objlabel):
    _append_args_pointers(method, files)
    _append_args_accessors_vector(method, files, objlabel)
    _append_args_accessors_matrix(method, files, objlabel)
    _append_args_mutators_vectors(method, files, objlabel)
    _append_args_mutators_matrix(method, files, objlabel)


def _append_args_pointers(method, files):
    title = "\n\n// Arguments\n"
    files['h']['private'] += title
    files['h']['private'] += '\n%s args;\n' % matrix_type(len(method.args), 1)
    for i, arg in enumerate(method.args):
        files['h']['private'] += '\ndouble * %s = & args(%i, 0);' \
            % (str(arg), i)


def _append_args_accessors_vector(method, files, objlabel):
    title = "\n\n// Acessors to Arguments, return vector<double>\n"
    files['h']['public'] += title
    files['cpp']['public'] += title
    for name in method.args_names:
        arg = getattr(method, name+'_expr')
        dim = len(arg)
        files['h']['public'] += '\nvector<double> %s_vector() const;' % name
        files['cpp']['public'] += \
            "\n\nvector<double> %s::%s_vector() const {" \
            % (objlabel, name)
        files['cpp']['public'] += \
            indent("\nvector<double> v = vector<double>(%i);" % dim)
        for i, symb in enumerate(arg):
            files['cpp']['public'] += indent("\nv[%i] = *%s;" % (i, str(symb)))
        files['cpp']['public'] += indent("\nreturn v;")
        files['cpp']['public'] += "\n}"


def _append_args_accessors_matrix(method, files, objlabel):
    title = "\n\n// Acessors to Arguments, return Matrix<double, n, m>\n"
    files['h']['public'] += title
    files['cpp']['public'] += title
    for name in method.args_names:
        arg = getattr(method, name+'_expr')
        dim = len(arg)
        files['h']['public'] += '\nMatrix<double, %i, 1> %s() const;' \
            % (dim, name)
        files['cpp']['public'] += "\nMatrix<double, %i, 1> %s::%s() const {" \
            % (dim, objlabel, name)
        files['cpp']['public'] += indent('\nMatrix<double, %i, 1> m;' % dim)
        for i, symb in enumerate(arg):
            files['cpp']['public'] += indent("\nm(%i, 0) = *%s;"
                                             % (i, str(symb)))
        files['cpp']['public'] += indent("\nreturn m;")
        files['cpp']['public'] += "\n}"


def _append_args_mutators_matrix(method, files, objlabel):
    title = "\n\n// Mutators for Arguments, type = Matrix<double, n, m>\n"
    files['h']['public'] += title
    files['cpp']['public'] += title
    for name in method.args_names:
        arg = getattr(method, name+'_expr')
        dim = len(arg)
        files['h']['public'] += '\nvoid set_' + name + \
            '(Matrix<double, ' + str(dim) + ', 1> &);'
        files['cpp']['public'] += \
            "\nvoid %s::set_%s(Matrix<double, %i, 1> & m) {" \
            % (objlabel, name, dim)
        for i, symb in enumerate(arg):
            files['cpp']['public'] += '\n'+indent("*%s = m(%i, 0);"
                                                  % (str(symb), i))
        files['cpp']['public'] += "\n}"


def _append_args_mutators_vectors(method, files, objlabel):
    title = "\n\n// Mutators for Arguments, type = vector<double>\n"
    files['h']['public'] += title
    files['cpp']['public'] += title
    for name in method.args_names:
        arg = getattr(method, name+'_expr')
        files['h']['public'] += '\nvoid set_%s(vector<double> &);' \
            % name
        files['cpp']['public'] += "\nvoid %s::set_%s(vector<double> & v) {" \
            % (objlabel, name)
        for i, symb in enumerate(arg):
            files['cpp']['public'] += "\n" + \
                indent("*%s = v[%i];" % (str(symb), i))
        files['cpp']['public'] += "\n}"
