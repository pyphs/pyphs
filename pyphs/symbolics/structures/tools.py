# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 11:46:11 2016

@author: Falaize
"""
import sympy
from pyphs.symbolics.calculus import hessian, jacobian
from pyphs.symbolics.tools import simplify
from pyphs.misc.tools import myrange


def moveJcolnrow(phs, indi, indf):
    new_indices = myrange(phs.dims.tot(), indi, indf)
    phs.struc.J = phs.struc.J[new_indices, new_indices]


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


def split_linear(phs):
    """
    """
    # split storage part
    nxl = 0
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
            move_stor(phs, nxl, phs.dims.x()-1)
    # number of linear components
    setattr(phs.dims, 'xl', nxl)

    # split dissipative part
    nwl = 0
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

    # number of linear components
    setattr(phs.dims, 'wl', nwl)


def reduce_linear_dissipations(phs):
    if not hasattr(phs, 'nwl'):
        split_linear(phs)
    from utils.calculus import compute_jacobian
    phs.zl = compute_jacobian(phs.z[:phs.dims.wl], phs.w[:phs.dims.wl])
    Kl = phs.K[:, :phs.dims.wl]
    Knl = phs.K[:, phs.dims.wl:]
    Gl = phs.Gw[:phs.dims.wl, :]
    Gnl = phs.Gw[phs.dims.wl:, :]
    Jll = phs.Jw[:phs.dims.wl, :phs.dims.wl]
    Jlnl = phs.Jw[:phs.dims.wl, phs.dims.wl:]
    Jnlnl = phs.Jw[phs.dims.wl:, phs.dims.wl:]
    iDw = sympy.eye(phs.dims.wl)-Jll*phs.zl
    Dw = iDw.inv()
    Ktot = sympy.Matrix.vstack(-Kl, -Jlnl.T, -Gl.T)
    Rtot = Ktot*phs.zl*Dw*Ktot.T
    phs.w = phs.w[phs.dims.wl:]
    phs.z = phs.z[phs.dims.wl:]
    if phs.dims.x() > 0:
        hstack1 = sympy.Matrix.hstack(phs.Jx, -Knl, phs.Gx)
    else:
        hstack1 = sympy.zeros(phs.dims.x(), phs.dims.tot())
    if phs.dims.w() > 0:
        hstack2 = sympy.Matrix.hstack(Knl.T, Jnlnl, Gnl)
    else:
        hstack2 = sympy.zeros(phs.dims.w(), phs.dims.tot())
    if phs.dims.y() > 0:
        hstack3 = sympy.Matrix.hstack(-phs.Gx.T, -Gnl.T, phs.Jy)
    else:
        hstack3 = sympy.zeros(phs.dims.y(), phs.dims.tot())
    phs.dims.wl = 0
    J = sympy.Matrix.vstack(hstack1, hstack2, hstack3)
    phs.addStructure(J=J-Rtot)
    phs.build()


def output_function(phs):
    """
    creates funtion phs.output_function
    """
    if phs.dims.y() > 0:

        Vyu = phs.struc.Jyy()*sympy.Matrix(phs.symbs.u)

        if phs.dims.x() > 0:
            Vyx = phs.struc.Jyx()*sympy.Matrix(phs.exprs.dxH)
            Vyxd = phs.struc.Jyx()*sympy.Matrix(phs.exprs.dxHd)
        else:
            Vyx = Vyxd = sympy.zeros(phs.dims.y(), 1)

        if phs.dims.w() > 0:
            Vyw = phs.struc.Jyw()*sympy.Matrix(phs.exprs.z)
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
