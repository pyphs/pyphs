#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 14:53:41 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

from pyphs.latex.tools import obj2tex, cr
from pyphs.latex.latex import dic2table


def symbol_names(core):
    sn = {}
    for var in [r'x', r'w', r'u', r'y', r'p']:
        for symb in getattr(core, var):
            string = str(symb)
            lab = string[1:]
            sn.update({symb: var+r'_{\mathrm{'+lab+r'}}'})
    return sn


def core2tex(core):
    string = r""
    string += coredims2tex(core)
    string += coresyms2tex(core)
    string += coreexprs2tex(core)
    string += corepars2tex(core)
    string += corestruc2tex(core)
    return string


def coredims2tex(core):
    """
    latexize dimensions nx, nx, ny and np
    """
    sm = symbol_names(core)
    str_dimensions = cr(2)
    str_dimensions += r"\section{System dimensions}"
    for dim in [r'x', r'w', r'y', r'p']:
        val = getattr(core.dims, dim)()
        label = r"n_\mathbf{"+dim+r"}"
        desc = r"$\dim(\mathbf{"+dim+r"})=$"
        str_dimensions += obj2tex(val, label, desc, sm, toMatrix=False)
    return str_dimensions


def coresyms2tex(core):
    sm = symbol_names(core)
    str_variables = cr(2)
    str_variables += r"\section{System variables}"
    if core.dims.x() > 0:
        str_variables += obj2tex(core.x, r'\mathbf{x}',
                                 'State variable', sm)
    if core.dims.w() > 0:
        str_variables += obj2tex(core.w, r'\mathbf{w}',
                                 'Dissipation variable', sm)
    if core.dims.y() > 0:
        str_variables += obj2tex(core.u, r'\mathbf{u}',
                                 'Input', sm)
        str_variables += obj2tex(core.y, r'\mathbf{y}',
                                 'Output', sm)
    return str_variables


def coreexprs2tex(core):
    sm = symbol_names(core)
    str_relations = cr(2)
    str_relations += r"\section{Constitutive relations}"
    if core.dims.x() > 0:
        str_relations += obj2tex(core.H, r'\mathtt{H}(\mathbf{x})',
                                 'Hamiltonian', sm,
                                 toMatrix=False)
        str_relations += obj2tex(core.dxH(),
                                 r'\nabla \mathtt{H}(\mathbf{x})',
                                 'Hamiltonian gradient', sm)
    if core.dims.w() > 0:
        str_relations += obj2tex(core.z, r'\mathbf{z}(\mathbf{w})',
                                 'Dissipation function', sm)
        str_relations += obj2tex(core.jacz,
                                 r'\mathcal{J}_{\mathbf{z}}(\mathbf{w})',
                                 'Jacobian of dissipation function', sm)
    return str_relations


def corepars2tex(core):
    sm = symbol_names(core)
    str_parameters = ""
    if len(core.subs) > 0:
        str_parameters += cr(2)
        str_parameters += r"\section{System parameters}" + cr(2)
        str_parameters += r"\subsection{Constant}" + cr(1)
        str_parameters += dic2table(['parameter', 'value (SI)'], core.subs)
    if core.dims.p() > 0:
        str_parameters += cr(2)
        str_parameters += r"\subsection{Controled}" + cr(1)
        str_parameters += obj2tex(core.p, r'\mathbf{p}',
                                  'Control parameters', sm)
    return str_parameters


def corestruc2tex(core, which='all'):
    """
    return latex code for system structure matrices.
    """
    str_structure = cr(1)
    str_structure += r"\section{System structure}"
    if which in ['all', 'M']:
        str_structure += corestrucM2tex(core)
    if which in ['all', 'J']:
        str_structure += corestrucJ2tex(core)
    if which in ['all', 'R']:
        str_structure += corestrucR2tex(core)
    return str_structure


def corestrucM2tex(core):
    """
    return latex code for matrix M.
    """
    sm = symbol_names(core)
    str_structure = cr(1)
    str_structure += obj2tex(core.M, r"\mathbf{M}", "", sm)
    if core.dims.x() > 0:
        str_structure += obj2tex(core.Mxx(), r"\mathbf{M_{xx}}", "", sm)
        if core.dims.w() > 0:
            str_structure += obj2tex(core.Mxw(), r"\mathbf{M_{xw}}", "", sm)
        if core.dims.y() > 0:
            str_structure += obj2tex(core.Mxy(), r"\mathbf{M_{xy}}", "", sm)
    if core.dims.w() > 0:
        if core.dims.x() > 0:
            str_structure += obj2tex(core.Mwx(), r"\mathbf{M_{wx}}", "", sm)
        str_structure += obj2tex(core.Mww(), r"\mathbf{M_{ww}}", "", sm)
        if core.dims.y() > 0:
            str_structure += obj2tex(core.Mwy(), r"\mathbf{M_{wy}}", "", sm)
    if core.dims.y() > 0:
        if core.dims.x() > 0:
            str_structure += obj2tex(core.Myx(), r"\mathbf{M_{yx}}", "", sm)
        if core.dims.w() > 0:
            str_structure += obj2tex(core.Myw(), r"\mathbf{M_{yw}}", "", sm)
        str_structure += obj2tex(core.Myy(), r"\mathbf{M_{yy}}", "", sm)
    return str_structure


def corestrucJ2tex(core):
    """
    return latex code for matrix M.
    """
    sm = symbol_names(core)
    str_structure = cr(1)
    str_structure += obj2tex(core.J(), r"\mathbf{J}", "", sm)
    if core.dims.x() > 0:
        str_structure += obj2tex(core.Jxx(), r"\mathbf{J_{xx}}", "", sm)
        if core.dims.w() > 0:
            str_structure += obj2tex(core.Jxw(), r"\mathbf{J_{xw}}", "", sm)
        if core.dims.y() > 0:
            str_structure += obj2tex(core.Jxy(), r"\mathbf{J_{xy}}", "", sm)
    if core.dims.w() > 0:
        str_structure += obj2tex(core.Jww(), r"\mathbf{J_{ww}}", "", sm)
        if core.dims.y() > 0:
            str_structure += obj2tex(core.Jwy(), r"\mathbf{J_{wy}}", "", sm)
    if core.dims.y() > 0:
        str_structure += obj2tex(core.Jyy(), r"\mathbf{J_{yy}}", "", sm)
    return str_structure


def corestrucR2tex(core):
    """
    return latex code for matrix M.
    """
    sm = symbol_names(core)
    str_structure = cr(1)
    str_structure += obj2tex(core.R(), r"\mathbf{R}", "", sm)
    if core.dims.x() > 0:
        str_structure += obj2tex(core.Rxx(), r"\mathbf{R_{xx}}", "", sm)
        if core.dims.w() > 0:
            str_structure += obj2tex(core.Rxw(), r"\mathbf{R_{xw}}", "", sm)
        if core.dims.y() > 0:
            str_structure += obj2tex(core.Rxy(), r"\mathbf{R_{xy}}", "", sm)
    if core.dims.w() > 0:
        str_structure += obj2tex(core.Rww(), r"\mathbf{R_{ww}}", "", sm)
        if core.dims.y() > 0:
            str_structure += obj2tex(core.Rwy(), r"\mathbf{R_{wy}}", "", sm)
    if core.dims.y() > 0:
        str_structure += obj2tex(core.Ryy(), r"\mathbf{R_{yy}}", "", sm)
    return str_structure
