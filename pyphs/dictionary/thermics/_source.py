#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 12:14:22 2017

@author: Falaize
"""

from ..edges import Port
from ..tools import symbols
from pyphs.graphs import datum
from ..tools import componentDoc, parametersDefault
from ..mechanics import metadata as dicmetadata
from pyphs.misc.rst import equation


class Source(Port):

    def __init__(self, label, nodes, **kwargs):

        # parameters
        parameters = parametersDefault(self.metadata['parameters'])
        parameters.update(kwargs)

        type_ = parameters['type']
        type_ = type_.lower()

        if not label == nodes[0]:
            text = "The node label associated with a heat source must be the\
 same as the component label:\n{}\nis not \n{}".format(label, nodes[0])
            raise NameError(text)

        assert type_ in ('temperature', 'entropyvar')

        if type_ == 'entropyvar':
            ctrl = 'e'
            obs = {}
        elif type_ == 'temperature':
            ctrl = 'f'
            obs = {symbols('gx'+label): symbols('u'+label)}

        kwargs.update({'ctrl': ctrl})
        Port.__init__(self, label,
                         (datum, nodes[0]), **kwargs)
        self.core.observers.update(obs)

    metadata = {'title': 'Mechanical Source',
                'component': 'Source',
                'label': 'T',
                'dico': 'thermics',
                'desc': r"Thermal source, i.e. imposed temperature delta (type='temp') or entropy variation (type='ev') between points.",
                'nodesdesc': "Thermal point associated with the source with positive flux #->temp. The node label must be the same as the component label.",
                'nodes': ('T', ),
                'parametersdesc': 'Component parameter.',
                'parameters': [['type', "Source type in {'entropyvar', 'temperature'}", 'string', 'temperature']],
                'refs': {},
                'nnodes': 2,
                'nedges': 1,
                'flux': dicmetadata['flux'],
                'effort': dicmetadata['effort'],
                }

    __doc__ = componentDoc(metadata)
