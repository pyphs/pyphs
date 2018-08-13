#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 12:14:04 2017

@author: Falaize
"""

from ..edges import StorageNonLinear
from ..tools import symbols
from pyphs.graphs import datum
import sympy as sp
from ..tools import componentDoc, parametersDefault
from ..thermics import metadata as dicmetadata
from pyphs.misc.rst import equation


class Capacitor(StorageNonLinear):

    def __init__(self, label, nodes, **kwargs):

        # parameters
        parameters = parametersDefault(self.metadata['parameters'])
        parameters.update(kwargs)

        if not label == nodes[0]:
            text = "The node label associated with a heat capacitor must be the\
 same as the component label:\n{}\nis not \n{}".format(label, nodes[0])
            raise NameError(text)

        pars = ['C', 'T0']
        C, T0 = symbols(pars)

        # state  variable
        x = symbols("x"+label)
        # storage funcion
        H = C*T0*sp.exp(x/C)
        N1, N2 = datum, nodes[0]

        # edge data
        data = {'label': x,
                'type': 'storage',
                'ctrl': 'f',
                'link': None}

        # edge
        edge = (N1, N2, data)

        # init component
        StorageNonLinear.__init__(self, label, [edge],
                                  x, H, **parameters)

    metadata = {'title': 'Thermal Capacitor',
                'component': 'Capacitor',
                'label': 'T',
                'dico': 'thermics',
                'desc': (r'Heat capacity (or mass) with entropy :math:`\sigma\in\mathbb R`, energy (exponential law):' +
                equation(r'H(\sigma)= C\,T_0\,\exp{\left(\frac{\sigma}{C}\right)},') +
                'and temperature:' +
                equation(r'\theta(\sigma) = \frac{d H}{d \sigma}(\sigma) = T_0\,\exp{\left(\frac{\sigma}{C}\right)}.')),
                'nodesdesc': "Thermal point associated with the heat mass. The node label must be the same as the component label. The capacity temperature is measured from the reference node (datum).",
                'nodes': ('T', ),
                'parametersdesc': 'Component parameter.',
                'parameters': [['C', "Thermal capacity", 'J/K', 1e3],
                               ['T0', "Initial temperature", 'K', 273.16]],
                'refs': {},
                'nnodes': 2,
                'nedges': 1,
                'flux': dicmetadata['flux'],
                'effort': dicmetadata['effort'],
                }

    __doc__ = componentDoc(metadata)
