"""
Created on Sat May 21 16:29:43 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function
from ..edges import Port
from ..tools import componentDoc, parametersDefault
from ..mechanics import metadata as dicmetadata


class Source(Port):

    def __init__(self, label, nodes, **kwargs):
        parameters = parametersDefault(self.metadata['parameters'])
        parameters.update(kwargs)
        type_ = parameters['type']
        type_ = type_.lower()
        assert type_ in ('force', 'velocity')
        if type_ == 'force':
            ctrl = 'e'
        elif type_ == 'velocity':
            ctrl = 'f'
        parameters.update({'ctrl': ctrl})
        Port.__init__(self, label, nodes, **parameters)

    metadata = {'title': 'Mechanical Source',
                'component': 'Source',
                'label': 'sourc',
                'dico': 'mechanics',
                'desc': r'Source of force or velocity imposed between two points.',
                'nodesdesc': "Mechanical points associated with the source with positive flux P1->P2",
                'nodes': ('P1', 'P2'),
                'parametersdesc': 'Component parameter.',
                'parameters': [['type', "Source type in {'velocity', 'force'}", 'string', 'force']],
                'refs': {},
                'nnodes': 2,
                'nedges': 1,
                'flux': dicmetadata['flux'],
                'effort': dicmetadata['effort'],
                }

    __doc__ = componentDoc(metadata)
