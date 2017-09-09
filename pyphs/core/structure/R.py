# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 11:46:11 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function
import sympy
from pyphs.misc.tools import geteval
from pyphs.core.tools import types
from pyphs.core.maths import inverse


def reduce_z(core):
    """
Incorporate the linear dissipative elements in the interconnection by \
redefining the structure matrix \
:math:`\\mathbf{M}_{\\mathrm{new}}\\in\\mathbb{R}^{N\\times N}` \
with \
:math:`N=\\mathrm{dim}(\\mathbf{x})+\\mathrm{dim}(\\mathbf{w}_{\\mathtt{nl}})+\\mathrm{dim}(\\mathbf{y})+\\mathrm{dim}(\\mathbf{c_y})`:

.. math:: \\mathbf{M}_{\\mathrm{new}} = \\mathbf{M}_{\\mathtt{nlwl}}\\cdot\\mathbf{Z}_{\\mathtt{l}}\\cdot\\mathbf{D}_{\\mathtt{l}}\\cdot\\mathbf{M}_{\\mathtt{wlnl}} +\\mathbf{M}_{\\mathtt{nl}}

where

* :math:`\\mathbf{z}_{\\mathtt{l}}(\\mathbf{w}_{\\mathtt{l}})=\\mathbf{Z}_{\\mathtt{l}}\\cdot\\mathbf{w}_{\\mathtt{l}}`;
* :math:`\\mathbf{D}_{\\mathtt{l}} = \\left(\\mathbf{I_d}-\
\\mathbf{M}_{\\mathtt{wlwl}}\\cdot\\mathbf{Z}_{\\mathtt{l}}\\right)^{-1}`,
* :math:`\\mathbf{M}_{\\mathtt{wlnl}} = \\left(\\mathbf{M}_{\\mathtt{wlxl}}, \
\\mathbf{M}_{\\mathtt{wlxnl}}, \\mathbf{M}_{\\mathtt{wlwnl}}, \
\\mathbf{M}_{\\mathtt{wly}}, \\mathbf{M}_{\\mathtt{wlcy}}\\right)`,
* :math:`\\mathbf{M}_{\\mathtt{nlwl}} = \\left(\\begin{array}{c}\
\\mathbf{M}_{\\mathtt{xlwl}} \\\\ \\mathbf{M}_{\\mathtt{xnlwl}}\\\\ \
\\mathbf{M}_{\\mathtt{wnlwl}}\\\\ \\mathbf{M}_{\\mathtt{ywl}}\\\\ \
\\mathbf{M}_{\\mathtt{cywl}}\\end{array}\\right)`.

Warning
-------
The linear dissipative variables :code:`core.wl()` are not accessible \
after this operation, and :code:`core.z()=core.znl()`.

"""
    # identify the linear components
    core.linear_nonlinear()
    # identify the number of components excluded from the linear part
    nforced = len(core.force_wnl)
    # move linear and excluded components at the top of linear components list
    if not nforced == 0:
        i = 0
        for _ in range(core.dims.wl()):
            if core.w[i] in core.force_wnl:
                core.move_dissipative(i, core.dims.wl())
            else:
                i += 1
        # reduce number of linear components
        core.dims._wl -= nforced
        # reduce Zl
        core.Zl = core.Zl[:-nforced, :-nforced]
    # build inverse of Dl
    iDl = types.matrix_types[0](sympy.eye(core.dims.wl())-core.Mwlwl()*core.Zl)
    # build Dl
    Dl = inverse(iDl)
    # build Mwlnl
    Mwlnl = types.matrix_types[0].hstack(core.Mwlxl(),
                                         core.Mwlxnl(),
                                         core.Mwlwnl(),
                                         core.Mwly(),
                                         core.Mwlcy())
    # build Mnlwl
    Mnlwl = types.matrix_types[0].vstack(core.Mxlwl(),
                                         core.Mxnlwl(),
                                         core.Mwnlwl(),
                                         core.Mywl(),
                                         core.Mcywl())
            # build Mnl
    names = ('xl', 'xnl', 'wnl', 'y', 'cy')
    mat = []
    for namei in names:
        mati = []
        for namej in names:
            Mij = geteval(core, 'M'+namei+namej)
            mati.append(Mij)
        Mi = types.matrix_types[0].hstack(*mati)
        mat.append(Mi)
    Mnl = types.matrix_types[0].vstack(*mat)
    # Set M to Mnew
    core.M = Mnlwl*core.Zl*Dl*Mwlnl + Mnl
    # Reduce w
    core.w = core.w[core.dims.wl():]
    # Reduce z
    core.z = core.z[core.dims.wl():]
    # Set dim(wl) to 0
    core.dims._wl = 0
