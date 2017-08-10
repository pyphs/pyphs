#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 12:56:16 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

from sympy.printing import ccode
from .tools import matrix_type, dereference, indent, linesplit
from pyphs.core.tools import types
from pyphs.config import VERBOSE, CONFIG_CPP


def append_funcs(method, files, objlabel):
    if VERBOSE >= 2:
        print('    Definitions...')
    _append_funcs_defs(method, files)
    if VERBOSE >= 2:
        print('    Accessors (matrix)...')
    _append_funcs_get(method, files, objlabel)
    if VERBOSE >= 2:
        print('    Accessors (vector)...')
    _append_funcs_get_vector(method, files, objlabel)
    if VERBOSE >= 2:
        print('    Accessors (element)...')
    _append_funcs_get_element(method, files, objlabel)
    if VERBOSE >= 2:
        print('    Update...')
    _append_funcs_updates(method, files, objlabel)
    if VERBOSE >= 2:
        print('    Data...')
    _append_funcs_data(method, files, objlabel)
    if VERBOSE >= 2:
        print('    Initialisation...')
    _append_funcs_init(method, files, objlabel)


###############################################################################
# DEFs

def _append_funcs_defs(method, files):
    title = linesplit + "\n// Functions Results Definitions"
    files['h']['private'] += title
    for name in method.update_actions_deps():
        if name in method.funcs_names:
            expr = getattr(method, name + '_expr')
            if isinstance(expr, types.scalar_types):
                files['h']['private'] += '\n{1} _{0};'.format(name, CONFIG_CPP['float'])
            else:
                mtype = matrix_type(*types.matrix_types[0](expr).shape)
                files['h']['private'] += '\n{0} _{1};'.format(mtype, name)


###############################################################################
# GET

def _append_funcs_get(method, files, objlabel):
    title = linesplit + "\n// Functions Results Accessors (matrix)"
    files['h']['public'] += title
    files['cpp']['public'] += title
    for name in method.update_actions_deps():
        if name in method.funcs_names:
            expr = getattr(method, name + '_expr')
            if isinstance(expr, types.scalar_types):
                h, cpp = _str_scal_func_get(name, objlabel)
            else:
                h, cpp = _str_mat_func_get(method, name, objlabel)
            files['h']['public'] += h
            files['cpp']['public'] += cpp


def _append_funcs_get_vector(method, files, objlabel):
    title = linesplit + "\n// Functions Results Accessors (vector)"
    files['h']['public'] += title
    files['cpp']['public'] += title
    for name in method.update_actions_deps():
        if name in method.funcs_names:
            expr = getattr(method, name + '_expr')
            if isinstance(expr, types.scalar_types):
                pass
            else:
                getvec = _str_mat_func_get_vector(method, name, objlabel)
                h = getvec[0]
                cpp = getvec[1]
                files['h']['public'] += h
                files['cpp']['public'] += cpp


def _append_funcs_get_element(method, files, objlabel):
    title = linesplit + "\n// Functions Results Accessors (element)"
    files['h']['public'] += title
    files['cpp']['public'] += title
    for name in method.update_actions_deps():
        if name in method.funcs_names:
            expr = getattr(method, name + '_expr')
            if isinstance(expr, types.scalar_types):
                pass
            else:
                getvec = _str_mat_func_get_element(method,
                                                   name, objlabel)
                h = getvec[0]
                cpp = getvec[1]
                files['h']['public'] += h
                files['cpp']['public'] += cpp


def _str_mat_func_get(method, name, objlabel):
    mat = types.matrix_types[0](getattr(method, name + '_expr'))
    mtype = matrix_type(mat.shape[0], mat.shape[1])
    get_h = '\n{0} {1}() const;'.format(mtype, name)
    get_cpp = '\n{0} {1}::{2}() const'.format(mtype, objlabel, name)
    get_cpp += ' {\n'
    get_cpp += indent("return _{0};".format(name))
    get_cpp += '\n}'
    return get_h, get_cpp


def _str_scal_func_get(name, objlabel):
    get_h = '\n{1} {0}();'.format(name, CONFIG_CPP['float'])
    get_cpp = \
        '\n{2} {0}::{1}() const '.format(objlabel, name, CONFIG_CPP['float']) + '{\n'
    get_cpp += indent('return _{0};'.format(name)) + '\n}'
    return get_h, get_cpp


def _str_mat_func_get_vector(method, name, objlabel):
    mat = types.matrix_types[0](getattr(method, name + '_expr'))
    mtype = 'vector<{0}>'.format(CONFIG_CPP['float'])
    get_h = '\n{0} {1}_vector() const;'.format(mtype, name)
    get_cpp = '\n{0} {1}::{2}_vector() const'.format(mtype, objlabel, name) + \
        ' {'
    dim = mat.shape[0]
    get_cpp += indent("\nvector<{1}> v = vector<{1}>({0});".format(dim, CONFIG_CPP['float']))
    for i in range(dim):
        get_cpp += indent("\nv[{0}] = _{1}({0}, 0);".format(i, name))
    get_cpp += indent("\nreturn v;")+"\n}"
    return get_h, get_cpp


def _str_mat_func_get_element(method, name, objlabel):
    mtype = CONFIG_CPP['float']
    get_h = '\n{0} {1}(unsigned int &) const;'.format(mtype, name)
    get_cpp = '\n{0} {1}::{2}(unsigned int & index) const'.format(mtype, objlabel, name) + \
        ' {'
    get_cpp += indent("\nreturn _{0}(index, 0);".format(name))+"\n}"
    return get_h, get_cpp


###############################################################################
# Updates

def _append_funcs_updates(method, files, objlabel):
    title = linesplit + "\n// Functions Results Updates"
    files['h']['private'] += title
    files['cpp']['private'] += title
    for name in method.update_actions_deps():
        if VERBOSE >= 3:
            print('        Build {}...'.format(name))
        if name in method.funcs_names:
            expr = getattr(method, name + '_expr')
            if isinstance(expr, types.scalar_types):
                h, cpp = _str_scal_func_update(method, name, objlabel)
            else:
                h, cpp = _str_mat_func_update(method, name, objlabel)

            files['h']['private'] += h
            files['cpp']['private'] += cpp


def _str_mat_func_update(method, name, objlabel):
    mat = types.matrix_types[0](getattr(method, name + '_expr'))
    update_h = '\nvoid {0}_update();'.format(name)
    update_cpp = '\nvoid {0}::{1}_update()'.format(objlabel, name) + '{'
    for m, n, expr in mat.row_list():
            symbs = expr.free_symbols
            if any(symb in method.args() for symb in symbs):
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

def _append_funcs_data(method, files, objlabel):
    title = linesplit + "\n// Functions Results Initialisation Data"
    files['cpp']['data'] += title
    for name in method.update_actions_deps():
        if name in method.funcs_names:
            expr = getattr(method, name + '_expr')
            if isinstance(expr, types.scalar_types):
                h = _str_scal_func_init_data(method, name)
            else:
                h = _str_mat_func_init_data(method, name)
            files['cpp']['data'] += '\n' + h


def _str_mat_func_init_data(method, name):
    mat = types.matrix_types[0](getattr(method, name + '_expr'))
    mat_dic = dict((((i, j), e) for i, j, e in mat.row_list()))
    init_data = '{1} {0}_data[] ='.format(name, CONFIG_CPP['float']) + ' {'
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
#                    data = 'float({0}), '.format(c)
                    data = '{0}, '.format(c)
            init_data += data
    if crop:
        init_data = init_data[:-2]
    init_data += '};'
    return init_data


def _str_scal_func_init_data(method, name):
    expr = getattr(method, name + '_expr')
    init_data = '{1} {0}_data = '.format(name, CONFIG_CPP['float'])
    symbs = expr.free_symbols
    if any(symb in method.args for symb in symbs):
        init_data += "0.;"
    else:
        c = ccode(expr, dereference=dereference(method))
        init_data += '{};'.format(c)
    return init_data


###############################################################################
# INIT

def _append_funcs_init(method, files, objlabel):
    title = linesplit + "\n// Functions Results Initialisation"
    files['cpp']['init'] += title
    for name in method.update_actions_deps():
        if name in method.funcs_names:
            cpp = _str_func_init_cpp(name)
            files['cpp']['init'] += cpp


def _str_func_init_cpp(name):
    return '\n{0}_update();'.format(name)

###############################################################################
# Constructtor

def append_funcs_constructors(method, files, objlabel):
    title = indent(linesplit + "\n// Functions Results Initialisation")
    files['cpp']['public'] += title
    for name in method.update_actions_deps():
        if name in method.funcs_names:
            expr = getattr(method, name + '_expr')
            if isinstance(expr, types.scalar_types):
                cpp = _str_scal_func_constructors(name)
            else:
                cpp = _str_mat_func_constructors(method, name)
            files['cpp']['public'] += indent(cpp)


def _str_mat_func_constructors(method, name):
    mat = types.matrix_types[0](getattr(method, name + '_expr'))
    mtype = matrix_type(mat.shape[0], mat.shape[1])
    string = '\n_{0} = Map<{1}> ({0}_data);'.format(name, mtype)
    return string


def _str_scal_func_constructors(name):
    return '\n_{0} = {0}_data;'.format(name)
