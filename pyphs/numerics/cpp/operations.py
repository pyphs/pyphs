#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 14:37:48 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

from .tools import matrix_type, indent, linesplit
from pyphs.config import CONFIG_CPP
import numpy


def append_ops(method, files, objlabel):
    _append_ops_defs(method, files)
    _append_ops_get(method, files, objlabel)
    _append_ops_get_vector(method, files, objlabel)
    _append_ops_updates(method, files, objlabel)
    _append_ops_init(method, files, objlabel)


###############################################################################
# DEF

def op2cpp(op):  # used in place of lambda s: '({0}) + ({1})'.format
    parser = {'add': '({0}) + ({1})'.format,
              'prod': '({0})*({1})'.format,
              'dot': '({0})*({1})'.format,
              'inv': '({0}).inverse()'.format,
              'norm': lambda s: 'sqrt(({0}).dot({1}))'.format(s, s),
              'copy': '{0}'.format,
              'none': lambda: ''
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

def _append_ops_defs(method, files):
    title = linesplit + "\n// Operations Results Definition"
    files['h']['private'] += title
    for name in method.ops_names:
        attr = method.inits_evals[name]
        if len(attr.shape) > 0:
            h = _str_mat_op_def(method, name, attr)
        else:
            h = _str_scal_op_def(name)
        files['h']['private'] += h


def _str_mat_op_def(method, name, mat):
    if len(mat.shape) == 1:
        mat = numpy.matrix(mat).T
    if not bool(numpy.prod(mat.shape)):
        shape = (0, 0)
    else:
        shape = mat.shape
    mtype = matrix_type(shape[0], shape[1])
    return '\n{0} _{1};'.format(mtype, name)


def _str_scal_op_def(name):
    return '\n{1} _{0};'.format(name, CONFIG_CPP['float'])


###############################################################################
# UPDATE

def _append_ops_updates(method, files, objlabel):
    title = linesplit + "\n// Oprations Results Updates"
    files['h']['private'] += title
    files['cpp']['private'] += title
    for name in method.ops_names:
        h, cpp = _str_op_update(method, name, objlabel)
        files['h']['private'] += h
        files['cpp']['private'] += cpp


def _str_op_update(method, name, objlabel):
    op = getattr(method, name + '_op')
    update_h = '\nvoid {0}_update();'.format(name)
    update_cpp = '\nvoid {0}::{1}_update()'.format(objlabel, name) + '{'
    update_cpp += '\n'+indent('_{0} = {1};'.format(name, op2cpp(op)))
    update_cpp += '\n};'
    return update_h, update_cpp


###############################################################################
# GET

def _append_ops_get(method, files, objlabel):
    title = linesplit + "\n// Oprations Results Accessors"
    files['h']['public'] += title
    files['cpp']['public'] += title
    for name in method.ops_names:
        attr = method.inits_evals[name]
        if len(attr.shape) > 0:
            h, cpp = _str_mat_op_get(method, name, objlabel)
        else:
            h, cpp = _str_scal_op_get(name, objlabel)
        files['h']['public'] += h
        files['cpp']['public'] += cpp


def _append_ops_get_vector(method, files, objlabel):
    title = linesplit + "\n// Oprations Results Accessors"
    files['h']['public'] += title
    files['cpp']['public'] += title
    for name in method.ops_names:
        attr = method.inits_evals[name]
        if len(attr.shape) == 1:
            getvec = _str_mat_op_get_vector(method, name, objlabel)
            h = getvec[0]
            cpp = getvec[1]
            files['h']['public'] += h
            files['cpp']['public'] += cpp


def _str_mat_op_get(method, name, objlabel):
    mat = method.inits_evals[name]
    if len(mat.shape) == 1:
        mat = numpy.matrix(mat).T
    if not bool(numpy.prod(mat.shape)):
        shape = (0, 0)
    else:
        shape = mat.shape
    mtype = matrix_type(shape[0], shape[1])
    get_h = '\n{0} {1}() const;'.format(mtype, name)
    get_cpp = \
        '\n{0} {1}::{2}() const'.format(mtype, objlabel, name)
    get_cpp += ' {\n' + indent('return _{0};'.format(name)) + '\n}'
    return get_h, get_cpp


def _str_mat_op_get_vector(method, name, objlabel):
    mat = method.inits_evals[name]
    if len(mat.shape) == 1:
        mat = numpy.matrix(mat).T
    mtype = 'vector<{0}>'.format(CONFIG_CPP['float'])
    get_h = '\n{0} {1}_vector() const;'.format(mtype, name)
    get_cpp = \
        '\n{0} {1}::{2}_vector() const'.format(mtype, objlabel, name) + ' {'
    dim = mat.shape[0]
    get_cpp += indent("\nvector<{1}> v = vector<{1}>({0});".format(dim, CONFIG_CPP['float']))
    for i in range(dim):
        get_cpp += indent("\nv[{0}] = _{1}({0}, 0);".format(i, name))
    get_cpp += indent("\nreturn v;")+"\n}"
    return get_h, get_cpp


def _str_scal_op_get(name, objlabel):
    get_h = '\n{1} {0}() const;'.format(name, CONFIG_CPP['float'])
    get_cpp = \
        '\n{2} {0}::{1}() const'.format(objlabel, name, CONFIG_CPP['float'])
    get_cpp += ' {\n' + indent('return _{0};'.format(name)) + '\n}'
    return get_h, get_cpp


###############################################################################
# INIT

def _append_ops_init(method, files, objlabel):
    title = linesplit + "\n// Operations Results Initialisation"
    files['cpp']['init'] += title
    for name in method.update_actions_deps():
        if name in method.ops_names:
            files['cpp']['init'] += '\n' + '{0}_update();'.format(name)

