#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 12:56:16 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

from sympy.printing import ccode
from pyphs.cpp.tools import matrix_type, dereference, indent
import sympy


def append_funcs(nums, files, objlabel):
    _append_funcs_defs(nums, files)
    _append_funcs_get(nums, files, objlabel)
    _append_funcs_get_vector(nums, files, objlabel)
    _append_funcs_updates(nums, files, objlabel)
    _append_funcs_data(nums, files, objlabel)
    _append_funcs_init(nums, files, objlabel)


###############################################################################
# DEFs

def _append_funcs_defs(nums, files):
    title = "\n\n// Functions Results Definitions\n"
    files['h']['private'] += title
    for name in nums.method.funcs_names:
        attr = getattr(nums, name)()
        if len(attr.shape) > 0:
            mat = sympy.Matrix(getattr(nums.method, name + '_expr'))
            mtype = matrix_type(mat.shape[0], mat.shape[1])
            files['h']['private'] += '\n{0} _{1};'.format(mtype, name)
        else:
            files['h']['private'] += '\ndouble _{0};'.format(name)


###############################################################################
# GET

def _append_funcs_get(nums, files, objlabel):
    title = "\n\n// Functions Results Accessors\n"
    files['h']['public'] += title
    files['cpp']['public'] += title
    for name in nums.method.funcs_names:
        attr = getattr(nums, name)()
        if len(attr.shape) > 0:
            h, cpp = _str_mat_func_get(nums.method, name, objlabel)
        else:
            h, cpp = _str_scal_func_get(name, objlabel)
        files['h']['public'] += h
        files['cpp']['public'] += cpp


def _append_funcs_get_vector(nums, files, objlabel):
    title = "\n\n// Functions Results Accessors\n"
    files['h']['public'] += title
    files['cpp']['public'] += title
    for name in nums.method.funcs_names:
        attr = getattr(nums, name)()
        if len(attr.shape) == 1:
            getvec = _str_mat_func_get_vector(nums.method, name, objlabel)
            h = getvec[0]
            cpp = getvec[1]
            files['h']['public'] += h
            files['cpp']['public'] += cpp


def _str_mat_func_get(method, name, objlabel):
    mat = sympy.Matrix(getattr(method, name + '_expr'))
    mtype = matrix_type(mat.shape[0], mat.shape[1])
    get_h = '\n{0} {1}() const;'.format(mtype, name)
    get_cpp = '\n{0} {1}::{2}() const'.format(mtype, objlabel, name)
    get_cpp += ' {\n'
    get_cpp += indent("return _{0};".format(name))
    get_cpp += '\n}'
    return get_h, get_cpp


def _str_scal_func_get(name, objlabel):
    get_h = '\ndouble {0}();'.format(name)
    get_cpp = \
        '\ndouble {0}::{1}() const '.format(objlabel, name) + '{\n'
    get_cpp += indent('return _{0};'.format(name)) + '\n}'
    return get_h, get_cpp


def _str_mat_func_get_vector(method, name, objlabel):
    mat = sympy.Matrix(getattr(method, name + '_expr'))
    mtype = 'vector<double>'
    get_h = '\n{0} {1}_vector() const;'.format(mtype, name)
    get_cpp = '\n{0} {1}::{2}_vector() const'.format(mtype, objlabel, name) + \
        ' {'
    dim = mat.shape[0]
    get_cpp += indent("\nvector<double> v = vector<double>({0});".format(dim))
    for i in range(dim):
        get_cpp += indent("\nv[{0}] = _{1}({0}, 0);".format(i, name))
    get_cpp += indent("\nreturn v;")+"\n}"
    return get_h, get_cpp


###############################################################################
# Updates

def _append_funcs_updates(nums, files, objlabel):
    title = "\n\n// Functions Results Updates\n"
    files['h']['private'] += title
    files['cpp']['private'] += title
    for name in nums.method.funcs_names:
        attr = getattr(nums, name)()
        if len(attr.shape) > 0:
            h, cpp = _str_mat_func_update(nums.method, name, objlabel)
        else:
            h, cpp = _str_scal_func_update(nums.method, name, objlabel)
        files['h']['private'] += h
        files['cpp']['private'] += cpp


def _str_mat_func_update(method, name, objlabel):
    mat = sympy.Matrix(getattr(method, name + '_expr'))
    update_h = '\nvoid {0}_update();'.format(name)
    update_cpp = '\nvoid {0}::{1}_update()'.format(objlabel, name) + '{'
    for n in range(mat.shape[1]):
        for m in range(mat.shape[0]):
            expr = mat[m, n]
            symbs = expr.free_symbols
            if any(symb in method.args for symb in symbs):
                c = ccode(expr, dereference=dereference(method))
                update_cpp += '\n_{0}({1}, {2}) = {3};'.format(name, m, n, c)
    update_cpp += '\n};'
    return update_h, update_cpp


def _str_scal_func_update(method, name, objlabel):
    expr = getattr(method, name + '_expr')
    update_h = '\nvoid {0}_update();'.format(name)
    update_cpp = '\nvoid {0}::{1}_update()'.format(objlabel, name) + '{'
    symbs = expr.free_symbols
    if any(symb in method.args for symb in symbs):
        c = ccode(expr, dereference=dereference(method))
        update_cpp += '\n_{0} = {1};'.format(name, c)
    update_cpp += '\n};'
    return update_h, update_cpp


###############################################################################
# DATA

def _append_funcs_data(nums, files, objlabel):
    title = "\n\n// Functions Results Initialisation Data"
    files['cpp']['data'] += title
    for name in nums.method.funcs_names:
        attr = getattr(nums, name)()
        if len(attr.shape) > 0:
            h = _str_mat_func_init_data(nums.method, name)
        else:
            h = _str_scal_func_init_data(nums.method, name)
        files['cpp']['data'] += '\n' + h


def _str_mat_func_init_data(method, name):
    mat = sympy.Matrix(getattr(method, name + '_expr'))
    init_data = 'double {0}_data[] ='.format(name) + ' {'
    crop = False
    for n in range(mat.shape[1]):
        for m in range(mat.shape[0]):
            expr = mat[m, n]
            symbs = expr.free_symbols
            if any(symb in method.args for symb in symbs):
                init_data += "0, "
                crop = True
            else:
                c = ccode(expr, dereference=dereference(method))
                init_data += '{0}, '.format(c)
                crop = True
    if crop:
        init_data = init_data[:-2]
    init_data += '};'
    return init_data


def _str_scal_func_init_data(method, name):
    expr = getattr(method, name + '_expr')
    init_data = 'double {0}_data = '.format(name)
    symbs = expr.free_symbols
    if any(symb in method.args for symb in symbs):
        init_data += "0.;"
    else:
        c = ccode(expr, dereference=dereference(method))
        init_data += '{0};'.format(c)
    return init_data


###############################################################################
# INIT

def _append_funcs_init(nums, files, objlabel):
    title = "\n\n// Functions Results Initialisation\n"
    files['cpp']['init'] += title
    for name in nums.method.funcs_names:
        attr = getattr(nums, name)()
        if len(attr.shape) > 0:
            cpp = _str_mat_func_init_cpp(nums.method, name)
        else:
            cpp = _str_scal_func_init_cpp(name)
        files['cpp']['init'] += cpp


def _str_mat_func_init_cpp(method, name):
    mat = sympy.Matrix(getattr(method, name + '_expr'))
    mtype = matrix_type(mat.shape[0], mat.shape[1])
    return '\n_{0} = Map<{1}> ({0}_data);'.format(name, mtype)


def _str_scal_func_init_cpp(name):
    return '\n_{0} = {0}_data;'.format(name)
