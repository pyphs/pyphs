#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 23:23:08 2017

@author: Falaize
"""


from __future__ import absolute_import, division, print_function

from ..magnetics import metadata as magnetics
from ..edges import StorageLinear
from ..tools import componentDoc, parametersDefault
from ..magnetics import metadata as dicmetadata
from pyphs.misc.rst import equation


class Capacitor(StorageLinear):

    def __init__(self, label, nodes, **kwargs):
        parameters = parametersDefault(self.metadata['parameters'])
        parameters.update(kwargs)
        par_name = 'C'
        par_val = parameters[par_name]
        kwargs = {'name': par_name,
                  'value': par_val,
                  'inv_coeff': True,
                  'ctrl': 'f'}
        StorageLinear.__init__(self, label, nodes, **kwargs)

    metadata = {'title': 'Magnetic capacitor',
                'component': 'Capacitor',
                'label': 'capa',
                'dico': 'magnetics',
                'desc': r'Magnetic capacity from [1]_ (chap 7). In Laplace domain with :math:`s\in\mathbb C`:' + equation(r'e(s) = \frac{1}{C s} \, f(s).'),
                'nodesdesc': "Component terminals with positive flux N1->N2.",
                'nodes': ('N1', 'N2'),
                'parametersdesc': 'Component parameters',
                'parameters': [['C', "Magnetic capacitance", 'H', 1e-9]],
                'refs': {1: "Antoine Falaize. Modelisation, simulation, generation de code et correction de systemes multi-physiques audios: Approche par reseau de composants et formulation hamiltonienne a ports. PhD thesis, ecole Doctorale d'Informatique, Telecommunication et electronique de Paris, Universite Pierre et Marie Curie, Paris 6, EDITE UPMC ED130, july 2016."},
                'nnodes': 2,
                'nedges': 1,
                'flux': dicmetadata['flux'],
                'effort': dicmetadata['effort'],
                }
    # Write documentation
    __doc__ = componentDoc(metadata)
