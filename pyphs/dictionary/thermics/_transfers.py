#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 13:13:07 2017

@author: Falaize
"""

from pyphs.graphs import datum
from ..edges import DissipativeNonLinear
from ..tools import symbols
from ..tools import componentDoc, parametersDefault
from ..thermics import metadata as dicmetadata
from pyphs.misc.rst import equation


class Transfer(DissipativeNonLinear):

    def __init__(self, label, nodes, **kwargs):
        # parameters
        pars = ['R', ]
        for par in pars:
            assert par in kwargs.keys()
        R, = symbols(pars)

        # dissipation variable
        w = symbols('w{}_(:2)'.format(label))

        t1, t2 = symbols(['gx'+str(n) for n in nodes])

        # dissipation funcion
        zero = (w[0]-w[0]).simplify()
        z1 = R*(w[0]-w[1])/t1
        z2 = R*(w[1]-w[0])/t2

        N1, N2 = nodes
        # edge diode data
        data1 = {'label': w[0],
                 'z': {'e_ctrl': z1, 'f_ctrl': zero},
                 'type': 'dissipative',
                 'ctrl': 'e',
                 'link': None}
        # edge
        edge1 = (datum, N1, data1)

        # edge diode data
        data2 = {'label': w[1],
                 'z': {'e_ctrl': z2, 'f_ctrl': zero},
                 'type': 'dissipative',
                 'ctrl': 'e',
                 'link': None}
        # edge
        edge2 = (datum, N2, data2)

        # init component
        DissipativeNonLinear.__init__(self, label,
                                         [edge1,
                                          edge2],
                                         w, [z1, z2],
                                         **kwargs)

    metadata = {'title': 'Thermal transfer',
                'component': 'Transfer',
                'label': 'trans',
                'dico': 'thermics',
                'desc': (r'Irreversible heat transfer between two thermal nodes. It is made from two dissipative edges. The dissipation variables are temperatures (:math:`w_1=T_1` and :math:`w_2=T_2`). The dissipation functions are:' +
                         equation(r'\begin{array}{rcl} \dot \sigma _1 = z_1(w_1, w_2) & = & R\frac{w_1-w_2}{w_1}, \\ \dot \sigma _2 = z_2(w_1, w_2) & = & R\frac{w_2-w_1}{w_2}.  \end{array}')),
                'nodesdesc': "The thermal transfer occurs between thermal points 'T1' and 'T2'.",
                'nodes': ('T1', 'T2'),
                'parametersdesc': 'Component parameter.',
                'parameters': [['R', "Thermal transfer coefficient", 'W/K', 1e3]],
                'refs': {},
                'nnodes': 3,
                'nedges': 2,
                'flux': dicmetadata['flux'],
                'effort': dicmetadata['effort'],
                }

    __doc__ = componentDoc(metadata)
