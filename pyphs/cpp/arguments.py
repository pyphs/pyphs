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
    title = "\n\n// Arguments"
    files['h'] += indent(title)
    files['h'] += indent('\n%s args;\n' % matrix_type(len(method.args), 1))
    for i, arg in enumerate(method.args):
        files['h'] += indent(
            '\ndouble * %s = & args(%i, 0);' % (str(arg), i))

def _append_args_accessors_vector(method, files, objlabel):
    title = "\n\n// Acessors to Arguments, return vector<double>."
    files['h'] += indent(title)
    files['cpp'] += title
    for name in method.args_names:
        arg = getattr(method, name+'_expr')
        dim = len(arg)
        files['h'] += indent('\nvector<double> %s() const;' % name)
        files['cpp'] += "\n\nvector<double> %s::%s() const {" % (objlabel, name)
        files['cpp'] += indent("\nvector<double> v = vector<double>(%i);" % dim)
        for i, symb in enumerate(arg):
            files['cpp'] += indent("\nv[%i] = *%s;" % (i, str(symb)))
        files['cpp'] += indent("\nreturn v;")
        files['cpp'] += "\n}"
        

def _append_args_accessors_matrix(method, files, objlabel):
    title = "\n\n// Acessors to Arguments, return Matrix<double, n, m>."
    files['h'] += indent(title)
    files['cpp'] += title
    for name in method.args_names:
        arg = getattr(method, name+'_expr')
        dim = len(arg)
        files['h'] += indent('\nMatrix<double, %i, 1> %s() const;' % (dim, name))
        files['cpp'] += "\nMatrix<double, %i, 1> %s::%s() const {" % (dim, objlabel, name)
        files['cpp'] += indent('\nMatrix<double, %i, 1> m;' % dim)
        for i, symb in enumerate(arg):
            files['cpp'] += indent("\nm(%i, 0) = *%s;" % (i, str(symb)))
        files['cpp'] += indent("\nreturn m;")
        files['cpp'] += "\n}"


def _append_args_mutators_matrix(method, files, objlabel):
    title = "\n\n// Mutators for Arguments, type = Matrix<double, n, m>"
    files['h'] += indent(title)
    files['cpp'] += title
    for name in method.args_names:
        arg = getattr(method, name+'_expr')
        dim = len(arg)
        files['h'] += indent('\nvoid set_' + name + '(Matrix<double, ' + str(dim) + ', 1> &);')
        files['cpp'] += """\n
void """ + objlabel + '::set_' + name + """(Matrix<double, """ + str(dim) + ", 1> & m) {"
        for i, symb in enumerate(arg):
            files['cpp'] += """
    *"""+ str(symb) + " = m(" + str(i) + ", 0);"
        files['cpp'] += """
}"""


def _append_args_mutators_vectors(method, files, objlabel):
    title = "\n\n// Mutators for Arguments, type = vector<double>"
    files['h'] += indent(title)
    files['cpp'] += title
    for name in method.args_names:
        arg = getattr(method, name+'_expr')
        files['h'] += indent('\nvoid set_' + name + '(vector<double> &);')
        files['cpp'] += """\n
void """ + objlabel + '::set_' + name + """(vector<double> & v) {"""
        for i, symb in enumerate(arg):
            files['cpp'] += """
    *"""+ str(symb) + " = v[" + str(i) + "];"
        files['cpp'] += """
}"""

if __name__ == '__main__':
    files = {'h':'', 'cpp':''}
    objlabel = 'test'.upper()
#    _append_includes(files)
#    _append_namespaces(files)
    append_args(method, files, objlabel)
#    _append_args_accessors_matrix(method, files, objlabel)
#    _append_funcs(method, files, objlabel)
#    _append_vecs_args(method, files)
#    _append_blocks_accessors(method, files, objlabel)
#    _append_args_mutators_matrix(method, files, objlabel)
#    _append_args_mutators_vectors(method, files, objlabel)    
    print(files['h'])

