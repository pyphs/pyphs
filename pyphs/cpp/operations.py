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

def op2cpp(op):  # used in place of lambda s: '({0}) + ({1})'.format
    parser = {'add': '({0}) + ({1})'.format,
              'prod': '({0})*({1})'.format,
              'dot': '({0})*({1})'.format,
              'inv': '({0}).inverse()'.format,
              'norm': lambda s: 'sqrt(({0}).dot({1}))'.format(s, s),
              'copy': '{0}'.format
              }
    args = []
    for arg in op.args:
        if isinstance(arg, str):
            args.append('{0}()'.format(arg))
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
    return '\n{0} _{1};'.format(mtype, name)


def _str_scal_op_def(name):
    return '\ndouble _{0};'.format(name)


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
    update_h = '\nvoid {0}_update();'.format(name)
    update_cpp = '\nvoid {0}::{1}_update()'.format(objlabel, name) + '{'
    update_cpp += '\n'+indent('_{0} = {1};'.format(name, op2cpp(op)))
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
    get_h = '\n{0} {1}() const;'.format(mtype, name)
    get_cpp = \
        '\n{0} {1}::{2}() const'.format(mtype, objlabel, name)
    get_cpp += ' {\n' + indent('return _{0};'.format(name)) + '\n}'
    return get_h, get_cpp


def _str_mat_op_get_vector(nums, name, objlabel):
    mat = getattr(nums, name)()
    if len(mat.shape) == 1:
        mat = numpy.matrix(mat).T
    mtype = 'vector<double>'
    get_h = '\n{0} {1}_vector() const;'.format(mtype, name)
    get_cpp = \
        '\n{0} {1}::{2}_vector() const'.format(mtype, objlabel, name) + ' {'
    dim = mat.shape[0]
    get_cpp += indent("\nvector<double> v = vector<double>({0});".format(dim))
    for i in range(dim):
        get_cpp += indent("\nv[{0}] = _{1}({0}, 0);".format(i, name))
    get_cpp += indent("\nreturn v;")+"\n}"
    return get_h, get_cpp


def _str_scal_op_get(name, objlabel):
    get_h = '\ndouble {0}() const;'.format(name)
    get_cpp = \
        '\ndouble {0}::{1}() const'.format(objlabel, name)
    get_cpp += ' {\n' + indent('return _{0};'.format(name)) + '\n}'
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
    init_data = 'double {0}_data[] = '.format(name) + '{'
    for n in range(mat.shape[1]):
        for m in range(mat.shape[0]):
            init_data += '{0}, '.format(mat[m, n])
    init_data = '{0}'.format(init_data[:-2]) + '};'
    return init_data


def _str_scal_op_init_data(nums, name):
    init_data = 'double {0}_data = 0.;'.format(name)
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
    return '_{0} = Map<{1}> ({0}_data);'.format(name, mtype)


def _str_scal_op_init_cpp(name):
    return '_{0} = {0}_data;'.format(name)
