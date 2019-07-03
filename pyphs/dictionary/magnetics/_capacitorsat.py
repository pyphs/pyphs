# -*- coding: utf-8 -*-
"""
Created on Sat May 21 16:24:12 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

import sympy as sp
from ..edges import StorageNonLinear
from pyphs.dictionary.tools import symbols
from ..tools import componentDoc, parametersDefault
from ..magnetics import metadata as dicmetadata
from pyphs.misc.rst import equation


class Capacitorsat(StorageNonLinear):

    def __init__(self, label, nodes, **kwargs):
        parameters = parametersDefault(self.metadata['parameters'])
        parameters.update(kwargs)
        # parameters
        pars = ['C0', 'Csat', 'phisat']
        C_0, C_sat, phi_sat = symbols(pars)
        # state  variable
        x = symbols("x"+label)
        # storage funcion
        Hlin = x**2/2
        t1 = sp.pi*x/(2*phi_sat)
        c1 = (8*phi_sat/(sp.pi*(4-sp.pi)))
        Hsat = c1 * (sp.log(sp.cos(t1)) + (t1**2)/2.)
        H = (Hlin - C_sat*Hsat)/C_0
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

    metadata = {'title': 'Saturating magnetic capacitor',
                'component': 'Capacitorsat',
                'label': 'capa',
                'dico': 'magnetics',
                'desc': (r'Saturating magnetic capacity from [1]_ (chap 7) with state :math:`\phi\in [-\phi_{sat}, \phi_{sat}]` and parameters described below. The energy is' +
                         equation('H(\\phi) = \\frac{1}{C_{0}} \, \\left( \\frac{\\phi^2}{2} +  C_{sat} H_{sat}(\\phi)\\right),') +
                         'with' +
                         equation('H_{sat}(\\phi) = -  \\frac{8 \\phi_{sat}}{\\pi \\left(4-\\pi\\right)} \, \\left(\\frac{\\pi^{2} \\phi^{2}}{8\\phi_{sat}^{2}} + \\log{\\left (\\cos{\\left (\\frac{\\pi \\phi}{2 \\phi_{sat}} \\right)} \\right)}\\right).') +
                         'The resulting magnetomotive force is:' +
                         equation('\\psi(\\phi)= \\frac{d\\,H(\\phi)}{d \\phi} = \\frac{ 1}{C_{0}} \\left(\\phi + C_{sat} \\frac{d\\,H_{sat}(\\phi)}{d \\phi}\\right),') +
                         'with' +
                         equation('\\frac{d\\,H_{sat}(\\phi)}{d \\phi}= \\frac{4}{4- \\pi} \\left(\\tan{\\left (\\frac{\\pi \\phi}{2 \\phi_{sat}} \\right )} - \\frac{\\pi \\phi}{2\\phi_{sat}} \\right).')) ,
                'nodesdesc': "Component terminals with positive flux N1->N2.",
                'nodes': ('N1', 'N2'),
                'parametersdesc': 'Component parameters',
                'parameters': [['C0', "Magnetic capacitance around zero", 'H', 1e3],
                               ['Csat', "Nonlinearity parameter", 'd.u.', 1e3],
                               ['phisat', "Magnetic capacitance", 'Wb', 1e-1]],
                'refs': {1: "Antoine Falaize. Modelisation, simulation, generation de code et correction de systemes multi-physiques audios: Approche par reseau de composants et formulation hamiltonienne a ports. PhD thesis, ecole Doctorale d'Informatique, Telecommunication et electronique de Paris, Universite Pierre et Marie Curie, Paris 6, EDITE UPMC ED130, july 2016."},
                'nnodes': 2,
                'nedges': 1,
                'flux': dicmetadata['flux'],
                'effort': dicmetadata['effort'],
                }

    # Write documentation
    __doc__ = componentDoc(metadata)
