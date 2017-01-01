#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 14:37:48 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

from pyphs.cpp.tools import matrix_type, indent
import numpy


def append_ops(nums, files, objlabel):
    _append_ops_defs(nums, files)
    _append_ops_get(nums, files, objlabel)
    _append_ops_get_vector(nums, files, objlabel)
    _append_ops_updates(nums, files, objlabel)
    _append_ops_data(nums, files, objlabel)
    _append_ops_init(nums, files, objlabel)


###############################################################################
# DEF

def op2cpp(op):
    parser = {'add': lambda s1, s2: '(%s) + (%s)' % (s1, s2),
              'prod': lambda s1, s2: '(%s)*(%s)' % (s1, s2),
              'dot': lambda s1, s2: '(%s)*(%s)' % (s1, s2), #lambda s1, s2: '(%s).dot(%s)' % (s1, s2),
              'inv': lambda s: '(%s).inverse()' % s,
              'norm': lambda s: 'sqrt((%s).dot(%s))' % (s, s),
              'copy': lambda s: '%s' % s
              }
    args = []
    for arg in op.args:
        if isinstance(arg, str):
            args.append('%s()' % arg)
        elif isinstance(arg, (float, int)):
            args.append(str(arg))
        else:
            args.append(op2cpp(arg))
    return parser[op.operation](*args)


###############################################################################
# DEF

def _append_ops_defs(nums, files):
    title = "\n\n// Operations Results Definition\n"
    files['h']['private'] += title
    for name in nums.method.ops_names:
        attr = getattr(nums, name)()
        if len(attr.shape) > 0:
            h = _str_mat_op_def(nums, name)
        else:
            h = _str_scal_op_def(name)
        files['h']['private'] += h


def _str_mat_op_def(nums, name):
    mat = getattr(nums, name)()
    if len(mat.shape) == 1:
        mat = numpy.matrix(mat).T
    mtype = matrix_type(mat.shape[0], mat.shape[1])
    return '\n%s _%s;' % (mtype, name)


def _str_scal_op_def(name):
    return '\ndouble _%s;' % name


###############################################################################
# UPDATE

def _append_ops_updates(nums, files, objlabel):
    title = "\n\n// Oprations Results Updates\n"
    files['h']['private'] += title
    files['cpp']['private'] += title
    for name in nums.method.ops_names:
        h, cpp = _str_op_update(nums, name, objlabel)
        files['h']['private'] += h
        files['cpp']['private'] += cpp


def _str_op_update(nums, name, objlabel):
    op = getattr(nums.method, name + '_op')
    update_h = '\nvoid %s_update();' % name
    update_cpp = '\nvoid %s::%s_update(){' % (objlabel, name)
    update_cpp += '\n'+indent('_%s = %s;' % (name, op2cpp(op)))
    update_cpp += '\n};'
    return update_h, update_cpp


###############################################################################
# GET

def _append_ops_get(nums, files, objlabel):
    title = "\n\n// Oprations Results Accessors\n"
    files['h']['public'] += title
    files['cpp']['public'] += title
    for name in nums.method.ops_names:
        attr = getattr(nums, name)()
        if len(attr.shape) > 0:
            h, cpp = _str_mat_op_get(nums, name, objlabel)
        else:
            h, cpp = _str_scal_op_get(name, objlabel)
        files['h']['public'] += h
        files['cpp']['public'] += cpp


def _append_ops_get_vector(nums, files, objlabel):
    title = "\n\n// Oprations Results Accessors\n"
    files['h']['public'] += title
    files['cpp']['public'] += title
    for name in nums.method.ops_names:
        attr = getattr(nums, name)()
        if len(attr.shape) == 1:
            getvec = _str_mat_op_get_vector(nums, name, objlabel)
            h = getvec[0]
            cpp = getvec[1]
            files['h']['public'] += h
            files['cpp']['public'] += cpp


def _str_mat_op_get(nums, name, objlabel):
    mat = getattr(nums, name)()
    if len(mat.shape) == 1:
        mat = numpy.matrix(mat).T
    mtype = matrix_type(mat.shape[0], mat.shape[1])
    get_h = '\n%s %s() const;' % (mtype, name)
    get_cpp = '\n%s %s::%s() const {\n    return _%s;\n}' % (mtype, objlabel,
                                                             name, name)
    return get_h, get_cpp


def _str_mat_op_get_vector(nums, name, objlabel):
    mat = getattr(nums, name)()
    if len(mat.shape) == 1:
        mat = numpy.matrix(mat).T
    mtype = 'vector<double>'
    get_h = '\n%s %s_vector() const;' % (mtype, name)
    get_cpp = '\n%s %s::%s_vector() const {' % (mtype, objlabel, name)
    dim = mat.shape[0]
    get_cpp += indent("\nvector<double> v = vector<double>(%i);" % dim)
    for i in range(dim):
        get_cpp += indent("\nv[%i] = _%s(%i, 0);" % (i, name, i))
    get_cpp += indent("\nreturn v;")+"\n}"
    return get_h, get_cpp


def _str_scal_op_get(name, objlabel):
    get_h = '\ndouble %s() const;' % name
    get_cpp = '\ndouble %s::%s() const {\n    return _%s;\n}' % (objlabel,
                                                                 name, name)
    return get_h, get_cpp


###############################################################################
# DATA

def _append_ops_data(nums, files, objlabel):
    title = "\n\n// Oprations Results Initialisation Data"
    files['cpp']['data'] += title
    for name in nums.method.ops_names:
        attr = getattr(nums, name)()
        if len(attr.shape) > 0:
            h = _str_mat_op_init_data(nums, name)
        else:
            h = _str_scal_op_init_data(nums, name)
        files['cpp']['data'] += '\n' + h


def _str_mat_op_init_data(nums, name):
    mat = getattr(nums, name)()
    if len(mat.shape) == 1:
        mat = numpy.matrix(mat).T
    init_data = 'double %s_data[] = {' % name
    for n in range(mat.shape[1]):
        for m in range(mat.shape[0]):
            init_data += '%f, ' % mat[m, n]
    init_data = '%s};' % init_data[:-2]
    return init_data


def _str_scal_op_init_data(nums, name):
    init_data = 'double %s_data = 0.;' % name
    return init_data


###############################################################################
# INIT

def _append_ops_init(nums, files, objlabel):
    title = "\n\n// Operations Results Initialisation\n"
    files['cpp']['init'] += title
    for name in nums.method.ops_names:
        attr = getattr(nums, name)()
        if len(attr.shape) > 0:
            cpp = _str_mat_op_init_cpp(nums, name)
        else:
            cpp = _str_scal_op_init_cpp(name)
        files['cpp']['init'] += '\n' + cpp


def _str_mat_op_init_cpp(nums, name):
    mat = getattr(nums, name)()
    if len(mat.shape) == 1:
        mat = numpy.matrix(mat).T
    mtype = matrix_type(mat.shape[0], mat.shape[1])
    return '_%s = Map<%s> (%s_data);' % (name, mtype, name)


def _str_scal_op_init_cpp(name):
    return '_%s = %s_data;' % (name, name)
