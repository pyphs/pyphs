# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 11:46:11 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function
import sympy
from .calculus import hessian, jacobian
from .symbs_tools import simplify, free_symbols
from .misc_tools import myrange, geteval


def movesquarematrixcolnrow(matrix, indi, indf):
    n = matrix.shape[0]
    new_indices = myrange(n, indi, indf)
    return matrix[new_indices, new_indices]


def moveMcolnrow(core, indi, indf):
    core.M = movesquarematrixcolnrow(core.M, indi, indf)


def move_stor(core, indi, indf):
    new_indices = myrange(core.dims.x(), indi, indf)
    core.x = [core.x[el] for el in new_indices]
    if core._dxH is not None:
        core._dxH = [core._dxH[el] for el in new_indices]
    moveMcolnrow(core, indi, indf)


def move_diss(core, indi, indf):
    new_indices = myrange(core.dims.w(), indi, indf)
    core.w = [core.w[el] for el in new_indices]
    core.z = [core.z[el] for el in new_indices]
    moveMcolnrow(core, core.dims.x()+indi, core.dims.x()+indf)


def move_port(core, indi, indf):
    new_indices = myrange(core.dims.y(), indi, indf)
    core.u = [core.u[el] for el in new_indices]
    core.y = [core.y[el] for el in new_indices]
    moveMcolnrow(core, core.dims.x()+core.dims.w()+indi,
                 core.dims.x()+core.dims.w()+indf)


def move_connector(core, indi, indf):
    new_indices = myrange(core.dims.cy(), indi, indf)
    core.cu = [core.cu[el] for el in new_indices]
    core.cy = [core.cy[el] for el in new_indices]
    moveMcolnrow(core, core.dims.x()+core.dims.w()+core.dims.y()+indi,
                 core.dims.x()+core.dims.w()+core.dims.y()+indf)


def split_monovariate(core):
    """
    """

    from utils.structure import move_stor, move_diss
    # split storage part
    i = 0
    for _ in range(core.dims.x()):
        hess = hessian(core.H, core.x)
        hess_line = list(hess[i, :].T)
        # remove i-th element
        hess_line.pop(i)
        # if other elements are all 0
        if all(el is sympy.sympify(0) for el in hess_line):
            # do nothing and increment counter
            i += 1
        else:
            # move the element at the end of states vector
            move_stor(core, i, core.dims.x())
    # number of separate components
    core.dims.xs = i
    # number of non-separate components
    core.dims.xns = core.dims.x()-i
    # split dissipative part
    i = 0
    for _ in range(core.dims.w()):
        Jacz_line = list(core.Jacz[i, :].T)
        # remove i-th element
        Jacz_line.pop(i)
        # if other elements are all 0
        if all(el is sympy.sympify(0) for el in Jacz_line):
            # do nothing and increment counter
            i += 1
        else:
            # move the element at the end of variables vector
            move_diss(core, i, core.dims.w())
    # number of separate components
    core.dims.ws = i
    # number of non-separate components
    core.dims.wns = core.dims.w()-i


def split_linear(core, criterion=None):
    """
    """
    if criterion is None:
        args = (core.x + core.dx() + core.w, core.dx() + core.w)
        mats = (hessian(core.H, core.x), jacobian(core.z, core.w))
        criterion = zip(mats, args)

    # split storage part
    nxl = 0
    hess = criterion[0][0]
    arg = criterion[0][1]
    for _ in range(hess.shape[0]):
        # hess_row = list(hess[nxl, :].T)
        hess_col = list(hess[:, nxl])
        # collect line symbols
        symbs = free_symbols(hess_col)
        # if symbols are not states
        if symbs.isdisjoint(arg):
            # do nothing and increment counter
            nxl += 1
        else:
            # move the element at the end of states vector
            move_stor(core, nxl, core.dims.x()-1)
            hess = movesquarematrixcolnrow(hess, nxl, core.dims.x()-1)
    # number of linear components
    setattr(core.dims, '_xl', nxl)
    setattr(core, 'Q', hessian(core.H, core.xl()))

    # split dissipative part
    nwl = 0
    jacz = criterion[1][0]
    arg = criterion[1][1]
    for _ in range(jacz.shape[0]):
        # jacz_row = list(jacz[nwl, :].T)
        jacz_col = list(jacz[:, nwl])
        # collect line symbols
        symbs = free_symbols(jacz_col)
        # if symbols are not dissipation variables
        if symbs.isdisjoint(arg):
            # do nothing and increment counter
            nwl += 1
        else:
            # move the element to end of dissipation variables vector
            move_diss(core, nwl, core.dims.w()-1)
            jacz = movesquarematrixcolnrow(jacz, nwl, core.dims.w()-1)
    # number of linear components
    setattr(core.dims, '_wl', nwl)
    core.setexpr('Zl', jacobian(core.zl(), core.wl()))


def reduce_linear_dissipations(core):

    core.split_linear()
    iDwl = sympy.eye(core.dims.wl())-core.Mwlwl()*core.Zl
    Dwl = iDwl.inv()

    Mwlnl = sympy.Matrix.hstack(core.Mwlxl(),
                                core.Mwlxnl(),
                                core.Mwlwnl(),
                                core.Mwly())
    Mnlwl = sympy.Matrix.vstack(core.Mxlwl(),
                                core.Mxnlwl(),
                                core.Mwnlwl(),
                                core.Mywl())

    names = ('xl', 'xnl', 'wnl', 'y')
    mat = []
    for namei in names:
        mati = []
        for namej in names:
            mati.append(geteval(core, 'M'+namei+namej))
        mat.append(sympy.Matrix.hstack(*mati))
    Mnl = sympy.Matrix.vstack(*mat)
    core.w = core.w[core.dims.wl():]
    core.z = core.z[core.dims.wl():]
    core.dims._wl = 0
    core.M = Mnlwl*core.Zl*Dwl*Mwlnl + Mnl


def output_function(core):
    """
    Returns the expression of the continuous output vector function y, and the\
expression of the discrete output vector function yd.

    Input:

        - core: pyphs.PHSCore

    Output:

        - y: list of sympy expressions associated with output vector \
components, considering the continuous version of storage function gradient
        - yd: list of sympy expressions associated with output vector \
components, considering the discrete version of storage function gradient
    """
    if core.dims.y() > 0:  # Check if system has external ports

        # contribution of inputs to the output
        Vyu = core.Myy()*sympy.Matrix(core.u)

        if core.dims.x() > 0:  # Check if system has storage parts
            Vyx = core.Myx()*sympy.Matrix(core.dxH())
        else:
            Vyx = sympy.zeros(core.dims.y(), 1)

        if core.dims.w() > 0:  # Check if system has dissipative parts
            Vyw = core.Myw()*sympy.Matrix(core.z)
        else:
            Vyw = sympy.zeros(core.dims.y(), 1)

        out = list(Vyx + Vyw + Vyu)
        out = simplify(out)

    else:
        out = sympy.Matrix(list(list()))

    return list(out)
