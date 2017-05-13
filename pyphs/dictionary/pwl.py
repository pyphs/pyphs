# -*- coding: utf-8 -*-
"""
Created on Thu May  4 18:59:02 2017

@author: tristan
"""

import numpy as np
import sympy as sp
from pyphs.numerics.tools import lambdify
from pyphs.dictionary import edges
from pyphs import PHSGraph
from pyphs.misc.io import data_generator
from pyphs.core.core import symbols
from pyphs.core.symbs_tools import simplify as simplify_func


class Storage(PHSGraph):
    def __init__(self, label, nodes, **kwargs):

        # instanciate a PHSGraph object
        PHSGraph.__init__(self, label=label)

        assert 'file' in kwargs, "pwl.storage component need 'file' argument"
        path = kwargs.pop('file')
        vals = np.vstack(map(np.array, data_generator(path)))
        x_vals = vals[0, :]
        h_vals = vals[1, :]

        assert all(h_vals[np.nonzero(x_vals >= 0)] >= 0), 'All values h(x) for\
 x>=0 must be non-negative (component {})'.format(label)

        if kwargs['integ']:
            assert all(h_vals[np.nonzero(x_vals < 0)] < 0), 'All values dxh(x)\
 for x<0 must be negative (component {})'.format(label)
        else:
            assert all(h_vals[np.nonzero(x_vals < 0)] >= 0), 'All values h(x)\
 for x<0 must be non-negative (component {})'.format(label)

        assert h_vals[np.nonzero(x_vals == 0)] == 0, 'dxh(0) and h(0) must be \
zero (component {})'.format(label)

        ctrl = kwargs.pop('ctrl')

        # state  variable
        x = symbols("x"+label)
        # storage funcion
        h = pwl_func(x_vals, h_vals, x, **kwargs)

        # edge data
        data = {'label': x,
                'type': 'storage',
                'ctrl': ctrl,
                'link': None}
        N1, N2 = nodes

        # edge
        edge = (N1, N2, data)

        # init component
        self += edges.PHSStorageNonLinear(label, [edge], x, h, **kwargs)

    @staticmethod
    def metadata():
        return {'nodes': ('N1', 'N2'),
                'arguments': {'integ': False}}


class Dissipative(PHSGraph):
    def __init__(self, label, nodes, **kwargs):

        # instanciate a PHSGraph object
        PHSGraph.__init__(self, label=label)

        assert 'file' in kwargs, "pwl.dissipative component need 'file' argument"
        path = kwargs.pop('file')
        data = np.vstack(map(np.array, data_generator(path)))
        w_vals = data[0, :]
        z_vals = data[1, :]

        assert all(z_vals[np.nonzero(w_vals >= 0)] >= 0), 'All values z(w) for\
 w>=0 must be non-negative (component {})'.format(label)

        assert all(z_vals[np.nonzero(w_vals >= 0)] >= 0), 'All values z(w) for\
 w<0 must be negative (component {})'.format(label)

        assert all(z_vals[np.nonzero(w_vals == 0)] == 0), 'z(0) must be zero \
(component {})'.format(label)

        ctrl = kwargs.pop('ctrl')

        # state  variable
        w = symbols("w"+label)
        # storage funcion
        z = pwl_func(w_vals, z_vals, w, **kwargs)

        # edge data
        data = {'label': w,
                'type': 'dissipative',
                'ctrl': ctrl,
                'link': None}
        N1, N2 = nodes

        # edge
        edge = (N1, N2, data)

        # init component
        self += edges.PHSDissipativeNonLinear(label, [edge, ], w, z, **kwargs)

    @staticmethod
    def metadata():
        return {'nodes': ('N1', 'N2'),
                'arguments': {}}

        
                                
def pwl_func(X_lst, Y_lst, symbol=sp.symbols('x'),
             integ=False, y0=0., intconst=0.):
    """
Returns a piecewise linear interpolation of the set (X_lst, Y_lst), based on
the following explicit form a + b.x + sum(c_i*abs(x - X_i)), where i denote the
ith component of the list and a, b and c are defined in [Chua and Ying, eq (2)].
[Chua and Ying, eq (2)] : Chua, L., & Ying, R. (1983). Canonical \
piecewise-linear analysis. IEEE Transactions on Circuits and Systems, \
30(3), 125-140.
    """

    # Numerical values
    assert len(X_lst) == len(Y_lst), "X and Y must have the same length"
    X = np.array(X_lst)
    Y = np.array(Y_lst)

    # State sympy symbol
    x = symbol

    # in [Chua and Ying, fig. 1], indices for x and y = f(x) range from 1 to P
    P = len(X)
    # delta_x[i] = x[x+1] - x[i] for i in [1, ..., P-1]
    delta_x = np.diff(X)
    # delta_f[i] = f(x[x+1]) - f(x[i]) for i in [1, ..., P-1]
    delta_y = np.diff(Y)
    # m[i] = delta_y[i]/delta_x[i]
    m = delta_y/delta_x
    # m <= (m[0], m, m[P-2]
    m = np.concatenate((m[np.newaxis, 0], m, m[np.newaxis, -1]))
    # in [Chua and Ying, eq (2.2)]: 0.5*(m[0] + m[-1])
    b = 0.5*(m[0] + m[-1])
    # in [Chua and Ying, eq (2.3)]: c[i] = 0.5*(m[i] - m[i-1]) for i in [1, ... P]
    c = 0.5*(m[1:] - m[:P])
    # in [Chua and Ying, eq (2.3)]: a = f(0) - sum_i(c[i]*abs(x[i]))
    # here we force f(0) = y0
    a = y0 - np.sum(c*np.abs(X))

    if integ:
        # integral of a + b.x + sum(c[i]*abs(x - X[i]))
        expr = (intconst + a*x + (b/2)*x**2 +
                sum(c*0.5*abs(x - X)*(x - X)) +
                sum(c*0.5*abs(X)*X))
    else:
        expr = a + b*x + sum(c*abs(x - X))

    return expr
    