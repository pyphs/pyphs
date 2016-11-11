# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 11:46:11 2016

@author: Falaize
"""
import sympy
from pyphs.symbolics.calculus import hessian, jacobian
from pyphs.symbolics.tools import simplify
from pyphs.misc.tools import myrange, geteval


def moveJcolnrow(phs, indi, indf):
    new_indices = myrange(phs.dims.tot(), indi, indf)
    phs.struc.M = phs.struc.M[new_indices, new_indices]


def move_stor(phs, indi, indf):
    new_indices = myrange(phs.dims.x(), indi, indf)
    phs.symbs.x = [phs.symbs.x[el] for el in new_indices]
    moveJcolnrow(phs, indi, indf)


def move_diss(phs, indi, indf):
    new_indices = myrange(phs.dims.w(), indi, indf)
    phs.symbs.w = [phs.symbs.w[el] for el in new_indices]
    phs.exprs.z = [phs.exprs.z[el] for el in new_indices]
    moveJcolnrow(phs, phs.dims.x()+indi, phs.dims.x()+indf)


def move_port(phs, indi, indf):
    new_indices = myrange(phs.dims.y(), indi, indf)
    phs.symbs.u = [phs.symbs.u[el] for el in new_indices]
    phs.symbs.y = [phs.symbs.y[el] for el in new_indices]
    moveJcolnrow(phs, phs.dims.x()+phs.dims.w()+indi,
                 phs.dims.x()+phs.dims.w()+indf)


def split_separate(phs):
    """
    """

    from utils.structure import move_stor, move_diss
    # split storage part
    i = 0
    for _ in range(phs.dims.x()):
        hess = hessian(phs.exprs.H, phs.symbs.x)
        hess_line = list(hess[i, :].T)
        # remove i-th element
        hess_line.pop(i)
        # if other elements are all 0
        if all(el is sympy.sympify(0) for el in hess_line):
            # do nothing and increment counter
            i += 1
        else:
            # move the element at the end of states vector
            move_stor(phs, i, phs.dims.x())
    # number of separate components
    phs.dims.xs = i
    # number of non-separate components
    phs.dims.xns = phs.dims.x()-i
    # split dissipative part
    i = 0
    for _ in range(phs.dims.w()):
        Jacz_line = list(phs.Jacz[i, :].T)
        # remove i-th element
        Jacz_line.pop(i)
        # if other elements are all 0
        if all(el is sympy.sympify(0) for el in Jacz_line):
            # do nothing and increment counter
            i += 1
        else:
            # move the element at the end of variables vector
            move_diss(phs, i, phs.dims.w())
    # number of separate components
    phs.dims.ws = i
    # number of non-separate components
    phs.dims.wns = phs.dims.w()-i


def split_linear(phs, force_nolin=False):
    """
    """
    # split storage part
    nxl = 0
    if not force_nolin:
        for _ in range(phs.dims.x()):
            hess = hessian(phs.exprs.H, phs.symbs.x)
            hess_line = list(hess[nxl, :].T)
            # init line symbols
            line_symbols = set()
            # collect line symbols
            for el in hess_line:
                line_symbols = line_symbols.union(el.free_symbols)
            # if symbols are not states
            if not any(el in line_symbols for el in phs.symbs.x):
                # do nothing and increment counter
                nxl += 1
            else:
                # move the element at the end of states vector
                print(str(nxl)+" "+str(phs.dims.x()-1))
                move_stor(phs, nxl, phs.dims.x()-1)

    hess = hessian(phs.exprs.H, phs.symbs.x)
    phs.exprs.setexpr('Q', hess[:nxl, :nxl])
    # number of linear components
    setattr(phs.dims, 'xl', nxl)

    # split dissipative part
    nwl = 0
    if not force_nolin:
        for _ in range(phs.dims.w()):
            jacz = jacobian(phs.exprs.z, phs.symbs.w)
            jacz_line = list(jacz[nwl, :].T)
            # init line symbols
            line_symbols = set()
            # collect line symbols
            for el in jacz_line:
                line_symbols = line_symbols.union(el.free_symbols)
            # if symbols are not dissipation variables
            if not any(el in line_symbols for el in phs.symbs.w):
                # do nothing and increment counter
                nwl += 1
            else:
                # move the element to end of dissipation variables vector
                move_diss(phs, nwl, phs.dims.w()-1)
    jacz = jacobian(phs.exprs.z, phs.symbs.w)
    phs.exprs.setexpr('Zl', jacz[:nwl, :nwl])
    # number of linear components
    setattr(phs.dims, 'wl', nwl)
    phs.exprs.build()

    names = ('xl', 'xnl', 'wl', 'wnl', 'y')
    phs.inds._set_inds(names)

    # get() and set() for structure matrices
    phs.struc._build_getset(phs, dims_names=names)


def reduce_linear_dissipations(phs):
    if not hasattr(phs, 'nwl'):
        split_linear(phs)
    iDwl = sympy.eye(phs.dims.wl)-phs.struc.Mwlwl()*phs.exprs.Zl
    Dwl = iDwl.inv()
    Mwlnl = sympy.Matrix.hstack(phs.struc.Mwlxl(),
                                phs.struc.Mwlxnl(),
                                phs.struc.Mwlwnl(),
                                phs.struc.Mwly())
    Mnlwl = sympy.Matrix.vstack(phs.struc.Mxlwl(),
                                phs.struc.Mxnlwl(),
                                phs.struc.Mwnlwl(),
                                phs.struc.Mywl())

    names = ('xl', 'xnl', 'wnl', 'y')
    mat = []
    for namei in names:
        mati = []
        for namej in names:
            mati.append(geteval(phs.struc, 'M'+namei+namej))
        mat.append(sympy.Matrix.hstack(*mati))
    Mnl = sympy.Matrix.vstack(*mat)

    phs.symbs.w = phs.symbs.w[phs.dims.wl:]
    phs.exprs.z = phs.exprs.z[phs.dims.wl:]
    phs.dims.wl = 0
    phs.struc.M = Mnlwl*phs.exprs.Zl*Dwl*Mwlnl + Mnl
    phs.exprs.build()


def output_function(phs):
    """
    Returns the expression of the continuous output vector function y, and the\
expression of the discrete output vector function yd.

    Input:

        - phs: pyphs.PortHamiltonianObject

    Output:

        - y: list of sympy expressions associated with output vector \
components, considering the continuous version of storage function gradient
        - y: list of sympy expressions associated with output vector \
components, considering the discrete version of storage function gradient
    """

    if phs.dims.y() > 0:  # Check if system has external ports

        # contribution of inputs to the output
        Vyu = phs.struc.Myy()*sympy.Matrix(phs.symbs.u)

        if phs.dims.x() > 0:  # Check if system has storage parts
            Vyx = phs.struc.Myx()*sympy.Matrix(phs.exprs.dxH)
            Vyxd = phs.struc.Myx()*sympy.Matrix(phs.exprs.dxHd)
        else:
            Vyx = Vyxd = sympy.zeros(phs.dims.y(), 1)

        if phs.dims.w() > 0:  # Check if system has dissipative parts
            Vyw = phs.struc.Myw()*sympy.Matrix(phs.exprs.z)
        else:
            Vyw = sympy.zeros(phs.dims.y(), 1)

        out = list(Vyx + Vyw + Vyu)
        out = simplify(out)

        outd = list(Vyxd + Vyw + Vyu)
        outd = simplify(outd)

    else:
        out = sympy.Matrix(list(list()))
        outd = sympy.Matrix(list(list()))

    return list(out), list(outd)
