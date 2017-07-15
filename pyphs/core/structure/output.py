#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 15 15:18:03 2017

@author: Falaize
"""
import sympy
from ..tools import types


# =============================== Output function =========================== #
def output_function(core):
    """
Returns the expression of the continuous output vector function y.
.. math:: \\mathbf{y} = \\mathbf{M}_{\\mathtt{yx}}\\cdot\\nabla \\mathrm{H} + \
\\mathbf{M}_{\\mathtt{yw}}\\cdot \\mathbf{z} + \
\\mathbf{M}_{\\mathtt{yy}}\\cdot\\mathrm{u} + \
\\mathbf{M}_{\\mathtt{ycy}}\\cdot\\mathrm{c_u}.

Input
------

core: pyphs.Core

Output
------
y: list
    of sympy expressions associated with output vector components.
    """
    if core.dims.y() > 0:  # Check if system has external ports

        # contribution of inputs to the output
        Vyu = core.Myy()*types.matrix_types[0](core.u)

        if core.dims.x() > 0:  # Check if system has storage parts
            Vyx = core.Myx()*types.matrix_types[0](core.dxH())
        else:
            Vyx = types.matrix_types[0](sympy.zeros(core.dims.y(), 1))

        if core.dims.w() > 0:  # Check if system has dissipative parts
            Vyw = types.matrix_types[0](core.Myw()*types.matrix_types[0](core.z))
        else:
            Vyw = types.matrix_types[0](sympy.zeros(core.dims.y(), 1))

        out = list(Vyx + Vyw + Vyu)

    else:
        out = types.matrix_types[0](list(list()))

    return list(out)
