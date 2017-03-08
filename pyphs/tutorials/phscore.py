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

xC, C, Cnl = core.symbols(['xC', 'C', 'Cnl'])   # define sympy symbols
HC = (1./2.+Cnl*xC**2/4)*xC**2/(C)      # define sympy expression
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

# ... or list ...
Jxw = [[-1.],
       [0.]]
core.set_Jxw(Jxw)

# ... or sympy.Matrix.
Jxy = sympy.Matrix([[-1.],
                   [0.]])
core.set_Jxy(Jxy)

# Physical parameters with f0 ~ (2*pi*sqrt(L*C))**-1
F0 = 100.                               # 1 kH
L_value = 5e-1                          # 500 mH
C_value = (2*numpy.pi*F0)**-2/L_value   # 5.066 µF
Cnl_value = 1e8                         # dimensionless
R_value = 1e2                           # 0.1 kOhm

# Dictionary with core.symbols as keys and parameters value as values
subs = {L: L_value,
        C: C_value,
        Cnl: Cnl_value,
        R: R_value}
core.subs.update(subs)

# Build of the resistive structure R in M = J-R
core.build_R()

# change R to R(xL) = Rnl * xC^
Rnl = core.symbols('Rnl')
core.apply_subs(subs={R: Rnl*(1+core.x[0]**2)})

# save value for symbol Rnl = 0.1 kOhm/Coulomb
core.subs.update({Rnl: 1e2})

# not executed if this script is imported in an other module
if __name__ == '__main__':
    # Export latex description
    core.texwrite(filename='dummy_core.tex', title='a Dummy PHSCore')
