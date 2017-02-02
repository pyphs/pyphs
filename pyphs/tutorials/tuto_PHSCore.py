# -*- coding: utf-8 -*-
"""
This is the tutorial 0 for pyphs.

Details can be found at: https://afalaize.github.io/pyphs/posts/tuto_phscore/

author: afalaize
date: 01. February 2017
"""

# Support for Python 2.x and Python 3.x
from __future__ import division, print_function, absolute_import

# import of external packages
import numpy  # numerical tools
import sympy  # symbolic tools

# load the pyphs.PHSCore class in the current namespace
from pyphs import PHSCore

# instantiate a pyphs.PHSCore object
core = PHSCore()

xL, L = core.symbols(['xL', 'L'])   # define sympy symbols
HL = xL**2/(2*L)                    # define sympy expression
core.add_storages(xL, HL)           # add storage function to the `core` object

xC, C = core.symbols(['xC', 'C'])   # define sympy symbols
HC = xC**2/(2*C)                    # define sympy expression
core.add_storages(xC, HC)           # add storage function to the `core` object

wR, R = core.symbols(['wR', 'R'])   # define sympy symbols
zR = R*wR                           # define sympy expression
core.add_dissipations(wR, zR)       # add dissipation to the `core` object

u, y = core.symbols(['vout', 'iout'])  # define sympy symbols
core.add_ports(u, y)                   # add the port to the `core` object


# The structure matrices can be numpy.array...
Jxx = numpy.array([[0., -1.],
                   [1., 0.]])
core.set_Jxx(Jxx)

# ... or list()...
Jxw = [[-1.],
       [0.]]
core.set_Jxw(Jxw)

# ... or sympy.Matrix.
Jxy = sympy.Matrix([[-1.],
                   [0.]])
core.set_Jxy(Jxy)

# Physical parameters
L_value = 50e-3     # 50mH
C_value = 2e-9      # 2nF
R_value = 1e3       # 1 kOhm

# Dictionary with core.symbols as keys and parameters value as values
subs = {L: L_value,
        C: C_value,
        R: R_value}
core.subs.update(subs)

# Build of the resistive structure R in M = J-R
core.build_R()

# change R to R(xC) = r * abs(xC) with r = 1e2Ohms/Coulomb
r = core.symbols('r')
core.apply_subs(subs={R: r*sympy.Abs(core.x[1])},
                selfsubs=False)

# save value for symbol r
core.subs.update({r: R_value})

# not executed if import from an other module
if __name__ == '__main__':
    # Export latex description
    core.texwrite(filename='dlc_core.tex', title='PHSCore of a DLC')
