# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 13:54:48 2016

@author: Falaize
"""

from tools import name2dim, str_matblk, \
    str_dims, cppobj_name, indent
from preamble import str_preamble


def data(phs):
    files = {'h': str_preamble(phs),
             'cpp': str_preamble(phs)}
    files['h'] += """
#ifndef DATA_H
#define DATA_H"""
    _append_include(phs, files)
    _append_subs(phs, files)
    files['h'] += """\n
#endif /* defined(DATA_H) */
"""
    return files


def _append_include(phs, files):
    files['cpp'] += """
# include "data.h"\
"""


def _append_subs(phs, files):
    dim = phs.simu.exprs.nsubs
    if dim > 0:
        files['h'] += """\n
extern const double subs[1][""" + str(dim) + """];"""
        files['cpp'] += """\n
const double subs[1][""" + str(dim) + """] = {
    {"""
        for el in phs.simu.exprs.subs:
            files['cpp'] += str(phs.symbs.subs[el]) + ', '
        files['cpp'] = files['cpp'][:-2] + """},
};"""
