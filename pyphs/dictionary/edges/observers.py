#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 14 19:07:37 2017

@author: Falaize
"""

from .storages import PHSStorageLinear
from .dissipatives import PHSDissipativeLinear
from ..tools import PHSArgument
from pyphs import PHSGraph


class Observerabs(PHSGraph):
    
    def __init__(self, label, nodes):
        PHSGraph.__init__(self, label=label)
        
        Nend = nodes[0]
        comp = PHSDissipativeLinear(label, (self.datum, Nend),
                                    coeff=PHSArgument('R'+label, 0), ctrl='e')
        self += comp

        comp = PHSStorageLinear(label, (self.datum, Nend),
                                    value=PHSArgument('K'+label, 0),
                                    inv_coeff=False,
                                    ctrl='e')
        self += comp

        
        
