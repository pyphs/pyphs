#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 23:21:59 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

from ..edges import Port
from ..tools import componentDoc, parametersDefault
from ..magnetics import metadata as dicmetadata
from pyphs.misc.rst import equation


class Source(Port):

    def __init__(self, label, nodes, **kwargs):
        parameters = parametersDefault(self.metadata['parameters'])
        parameters.update(kwargs)
        type_ = parameters['type']
        type_ = type_.lower()
        assert type_ in ('mmf', 'fluxvar')
        if type_ == 'mmf':
            ctrl = 'f'
        elif type_ == 'fluxvar':
            ctrl = 'e'
        parameters.update({'ctrl': ctrl})
        Port.__init__(self, label, nodes, **parameters)

    metadata = {'title': 'Magnetic source',
                'component': 'Source',
                'label': 'sourc',
                'dico': 'magnetics',
                'desc': r'Magnetic source from [1]_ (chap 7). Could be a source a magnetomotive force (mmf, e.g. a magnet) or a source of magnetic flux variation (mfv).',
                'nodesdesc': "Component terminals with positive flux N1->N2.",
                'nodes': ('N1', 'N2'),
                'parametersdesc': 'Component parameters',
                'parameters': [['type', "Source type in {'mmf', 'mfv'}", 'string', 'mmf']],
                'refs': {1: "Antoine Falaize. Modelisation, simulation, generation de code et correction de systemes multi-physiques audios: Approche par reseau de composants et formulation hamiltonienne a ports. PhD thesis, ecole Doctorale d'Informatique, Telecommunication et electronique de Paris, Universite Pierre et Marie Curie, Paris 6, EDITE UPMC ED130, july 2016."},
                'nnodes': 2,
                'nedges': 1,
                'flux': dicmetadata['flux'],
                'effort': dicmetadata['effort'],
                }

    # Write documentation
    __doc__ = componentDoc(metadata)
