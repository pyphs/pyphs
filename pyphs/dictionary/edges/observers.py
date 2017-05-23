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


class Nodeobs(PHSGraph):

    def __init__(self, label, nodes):
        PHSGraph.__init__(self, label=label)

        Nend, = nodes
        comp = PHSDissipativeLinear(label, (self.datum, Nend),
                                    coeff=PHSArgument('R'+label, 1e-16),
                                    ctrl='e', inv_coeff=False)
        self += comp
        # force nl so that it the flux observer is not
        self.core.force_wnl += [self.core.w[0], ]
        comp = PHSStorageLinear(label,
                                (self.datum, Nend),
                                value=PHSArgument('C'+label, 1e-16),
                                inv_coeff=False,
                                ctrl='e')
        self += comp
