#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 15 15:13:21 2017

@author: Falaize
"""

from .moves import moveCoreMcolnrow


def port2connector(core, i):
    """
==============
port2connector
==============

Define the port i as a connector. That is, the port with index i is removed
from the list of ports and is appended to the end of the list of connectors.

Parameters
----------

core: Core

i: int
    index of the port to be defined as a connector. The index value must
    be in the range [0, ..., core.dims.y()]

Output
------

No output (inplace change of the Core)
    """
    moveCoreMcolnrow(core, core.dims.x()+core.dims.w()+i, core.dims.tot())

    # append port symbols to the list of connectors symbols
    core.cu += [core.u[i], ]
    core.cy += [core.y[i], ]

    # remove symbols from the list of port symbols
    for name in ['u', 'y']:
        attr = getattr(core, name)
        symb = attr[i]
        attr.remove(symb)
