# -*- coding: utf-8 -*-
"""
Created on Sat May 21 16:29:43 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function
from ..edges import StorageNonLinear
from pyphs.dictionary.tools import symbols
import sympy as sp
from ..tools import componentDoc, parametersDefault
from ..mechanics_dual import metadata as dicmetadata
from pyphs.misc.rst import equation


class Springsat(StorageNonLinear):

    def __init__(self, label, nodes, **kwargs):

        parameters = parametersDefault(self.metadata['parameters'])
        parameters.update(kwargs)

        # parameters
        pars = ['K0', 'Ksat', 'xsat']

        K0, Ksat, xsat = symbols(pars)
        # state  variable
        x = symbols("x"+label)
        # storage funcion
        Hlin = x**2/2
        t1 = sp.pi*x/(2*xsat)
        c1 = (8*xsat/(sp.pi*(4-sp.pi)))
        Hsat = c1 * (sp.log(sp.cos(t1)) + (t1**2)/2.)
        H = K0*(Hlin - Ksat*Hsat)
        N1, N2 = nodes

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

    metadata = {'title': 'Saturating spring',
                'component': 'Springsat',
                'label': 'spring',
                'dico': 'mechanics_dual',
                'desc': (r'Saturating spring from [1]_ (chap 7) with state :math:`q\in [-q_{sat}, q_{sat}]` and parameters described below. The energy is' +
                         equation('H(q) = K_0 \, \\left( \\frac{q^2}{2} +  K_{sat} H_{sat}(q)\\right),') +
                         'with' +
                         equation('H_{sat}(q) = -  \\frac{8 q_{sat}}{\\pi \\left(4-\\pi\\right)} \, \\left(\\frac{\\pi^{2} q^{2}}{8q_{sat}^{2}} + \\log{\\left (\\cos{\\left (\\frac{\\pi q}{2 q_{sat}} \\right)} \\right)}\\right).') +
                         'The resulting force is:' +
                         equation('f(q)= \\frac{d\\,H(q)}{d q} = K_{0} \\left(q + K_{sat} \\frac{d\\,H_{sat}(q)}{d q}\\right),') +
                         'with' +
                         equation('\\frac{d\\,H_{sat}(q)}{d q}= \\frac{4}{4- \\pi} \\left(\\tan{\\left (\\frac{\\pi q}{2 q_{sat}} \\right )} - \\frac{\\pi q}{2q_{sat}} \\right).')) ,
                'nodesdesc': "Nodes associated with the component terminals with positive flux N1->N2.",
                'nodes': ('N1', 'N2'),
                'parametersdesc': 'Component parameters.',
                'parameters': [['K0', "Stiffness around zero", 'H', 1e3],
                               ['Ksat', "Nonlinearity parameter", 'd.u.', 1e3],
                               ['xsat', "Saturating position", 'm', 1e-2]],
                'refs': {1: "Antoine Falaize. Modelisation, simulation, generation de code et correction de systemes multi-physiques audios: Approche par reseau de composants et formulation hamiltonienne a ports. PhD thesis, ecole Doctorale d'Informatique, Telecommunication et electronique de Paris, Universite Pierre et Marie Curie, Paris 6, EDITE UPMC ED130, july 2016."},
                'nnodes': 2,
                'nedges': 1,
                'flux': dicmetadata['flux'],
                'effort': dicmetadata['effort'],
                }
    # Write documentation
    __doc__ = componentDoc(metadata)
