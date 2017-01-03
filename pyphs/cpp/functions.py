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
            files['h']['private'] += '\n%s _%s;' % (mtype, name)
        else:
            files['h']['private'] += '\ndouble _%s;' % name


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
    get_h = '\n%s %s() const;' % (mtype, name)
    get_cpp = '\n%s %s::%s() const {\n    return _%s;\n}' % (mtype, objlabel,
                                                             name, name)
    return get_h, get_cpp


def _str_scal_func_get(name, objlabel):
    get_h = '\ndouble %s();' % name
    get_cpp = '\ndouble %s::%s() const {\n    return _%s;\n}' % (objlabel,
                                                                 name, name)
    return get_h, get_cpp


def _str_mat_func_get_vector(method, name, objlabel):
    mat = sympy.Matrix(getattr(method, name + '_expr'))
    mtype = 'vector<double>'
    get_h = '\n%s %s_vector() const;' % (mtype, name)
    get_cpp = '\n%s %s::%s_vector() const {' % (mtype, objlabel, name)
    dim = mat.shape[0]
    get_cpp += indent("\nvector<double> v = vector<double>(%i);" % dim)
    for i in range(dim):
        get_cpp += indent("\nv[%i] = _%s(%i, 0);" % (i, name, i))
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
    update_h = '\nvoid %s_update();' % name
    update_cpp = '\nvoid %s::%s_update(){' % (objlabel, name)
    for n in range(mat.shape[1]):
        for m in range(mat.shape[0]):
            expr = mat[m, n]
            symbs = expr.free_symbols
            if any(symb in method.args for symb in symbs):
                c = ccode(expr, dereference=dereference(method))
                update_cpp += '\n_%s(%i, %i) = %s;' % (name, m, n, c)
    update_cpp += '\n};'
    return update_h, update_cpp


def _str_scal_func_update(method, name, objlabel):
    expr = getattr(method, name + '_expr')
    update_h = '\nvoid %s_update();' % name
    update_cpp = '\nvoid %s::%s_update(){' % (objlabel, name)
    symbs = expr.free_symbols
    if any(symb in method.args for symb in symbs):
        c = ccode(expr, dereference=dereference(method))
        update_cpp += '\n_%s = %s;' % (name, c)
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
    init_data = 'double %s_data[] = {' % name
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
                init_data += '%s, ' % c
                crop = True
    if crop:
        init_data = init_data[:-2]
    init_data += '};'
    return init_data


def _str_scal_func_init_data(method, name):
    expr = getattr(method, name + '_expr')
    init_data = 'double %s_data = ' % name
    symbs = expr.free_symbols
    if any(symb in method.args for symb in symbs):
        init_data += "0.;"
    else:
        c = ccode(expr, dereference=dereference(method))
        init_data += '%s;' % c
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
    return '\n_%s = Map<%s> (%s_data);' % (name, mtype, name)


def _str_scal_func_init_cpp(name):
    return '\n_%s = %s_data;' % (name, name)
