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
import numpy

def _str_mat_func_def(method, name):
    mat = sympy.Matrix(getattr(method, name + '_expr'))
    mtype = matrix_type(mat.shape[0], mat.shape[1])
    return '\n%s _%s;' % (mtype, name)


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

    
def _str_mat_func_get(method, name, objlabel):
    mat = sympy.Matrix(getattr(method, name + '_expr'))
    mtype = matrix_type(mat.shape[0], mat.shape[1])
    get_h = '\n%s %s() const;' % (mtype, name)
    get_cpp = '\n%s %s::%s() const {\n    return _%s;\n}' % (mtype, objlabel, name, name)
    return get_h, get_cpp

    
def _str_mat_func_get_vector(method, name, objlabel):
    mat = sympy.Matrix(getattr(method, name + '_expr'))
    mtype = 'vector(double)'
    get_h = '\n%s %s();' % (mtype, name)
    get_cpp = '\n%s %s::%s() const {' % (mtype, objlabel, name)
    dim = mat.shape[0]
    get_cpp += indent("\nvector<double> v = vector<double>(%i);" % dim)
    for i in range(dim):
        get_cpp += indent("\nv[%i] = %s(%i, 1);" % (name, i))
    get_cpp += indent("\nreturn v;")+"\n}"
    return get_h, get_cpp

    
def _str_mat_func_init_data(method, name):
    mat = sympy.Matrix(getattr(method, name + '_expr'))
    init_data = '\ndouble %s_data[] = {' % name
    for n in range(mat.shape[1]):
        for m in range(mat.shape[0]):
            expr = mat[m, n]
            symbs = expr.free_symbols
            if any(symb in method.args for symb in symbs):
                init_data += "0, "
            else:
                c = ccode(expr, dereference=dereference(method))
                init_data += '%s, ' % c                                          
    init_data = '%s};' % init_data[:-2]
    return init_data
    

def _str_mat_func_init_cpp(method, name):
    mat = sympy.Matrix(getattr(method, name + '_expr'))
    mtype = matrix_type(mat.shape[0], mat.shape[1])
    return '\n_%s = Map<%s> (%s_data);' % (name, mtype, name)
    

def _append_mat_funcs(method, files, objlabel, names):
    defs, udhs, udcpps, icpps, datas, ghs, gcpps= ["", ]*7
    for name in names:
        def_ = _str_mat_func_def(method, name)
        defs += def_
        update_h, update_cpp = _str_mat_func_update(method, name, objlabel)
        udhs += update_h
        udcpps += update_cpp
        get_h, get_cpp  = _str_mat_func_get(method, name, objlabel)
        ghs += get_h
        gcpps += get_cpp
        init_data = _str_mat_func_init_data(method, name)
        datas += init_data
    files['h'] += defs + ghs + udhs +  datas
    files['cpp'] += gcpps + udcpps + icpps
        

def _str_scal_func_def(name):
    return '\ndouble _%s;' % name


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

    
def _str_scal_func_init_data(method, name):
    expr = getattr(method, name + '_expr')
    init_data = '\ndouble %s_data = ' % name
    symbs = expr.free_symbols
    if any(symb in method.args for symb in symbs):
        init_data += "0.;"
    else:
        c = ccode(expr, dereference=dereference(method))
        init_data += '%s;' % c                                          
    return init_data
    

def _str_scal_func_init_cpp(name):
    return '\n_%s = %s_data;' % (name, name)
    

def _str_scal_func_get(name, objlabel):
    get_h = '\ndouble %s();' % name
    get_cpp = '\ndouble %s::%s() const {\n    return _%s;\n}' % (objlabel, name, name)
    return get_h, get_cpp

    
def _append_scal_funcs(method, files, objlabel, names):
    defs, udhs, udcpps, icpps, datas = ["", ]*5
    for name in names:
        def_ = _str_scal_func_def(name)
        defs += def_
        update_h, update_cpp = _str_scal_func_update(method, name, objlabel)
        udhs += update_h
        udcpps += update_cpp
        get_h, get_cpp = _str_scal_func_get(name, objlabel)
        udhs += get_h
        udcpps += get_cpp        
        init_data = _str_scal_func_init_data(method, name)
        datas += init_data
    files['h'] += defs + udhs +  datas
    files['cpp'] += udcpps + icpps
        

def append_funcs(nums, files, objlabel):
    scal_funcs_names = []
    mat_funcs_names = []
    for name in nums.method.funcs_names:
        attr = getattr(nums, name)()
        if len(attr.shape) > 0:
            mat_funcs_names.append(name)
        else:
            scal_funcs_names.append(name)
    _append_scal_funcs(nums.method, files, objlabel, scal_funcs_names)
    _append_mat_funcs(nums.method, files, objlabel, mat_funcs_names)
if __name__ == '__main__':
    files = {'h':'', 'cpp':''}
    objlabel = 'test'.upper()
    append_funcs(nums, files, objlabel)
    print(files['cpp'])
    
