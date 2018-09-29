#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 23:24:06 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

from ..edges import DissipativeLinear
from ..tools import componentDoc, parametersDefault
from ..magnetics import metadata as dicmetadata
from pyphs.misc.rst import equation


class Resistor(DissipativeLinear):

    def __init__(self, label, nodes, **kwargs):
        parameters = parametersDefault(self.metadata['parameters'])
        parameters.update(kwargs)
        if parameters['R'] is None:
            coeff = 0
        else:
            coeff = parameters['R']
        DissipativeLinear.__init__(self, label, nodes, coeff=coeff)

    metadata = {'title': 'Magnetic resistor',
                'component': 'Resistor',
                'label': 'res',
                'dico': 'magnetics',
                'desc': r'Magnetic resistance from [1]_ (chap 7). In Laplace domain with :math:`s\in\mathbb C`:' + equation(r'e(s) = R \, f(s).'),
                'nodesdesc': "Component terminals with positive flux N1->N2.",
                'nodes': ('N1', 'N2'),
                'parametersdesc': 'Component parameters',
                'parameters': [['R', "Magnetic resistance", '1/Ohm', 1e-3]],
                'refs': {1: "Antoine Falaize. Modelisation, simulation, generation de code et correction de systemes multi-physiques audios: Approche par reseau de composants et formulation hamiltonienne a ports. PhD thesis, ecole Doctorale d'Informatique, Telecommunication et electronique de Paris, Universite Pierre et Marie Curie, Paris 6, EDITE UPMC ED130, july 2016."},
                'nnodes': 2,
                'nedges': 1,
                'flux': dicmetadata['flux'],
                'effort': dicmetadata['effort'],
                }

    # Write documentation
    __doc__ = componentDoc(metadata)
