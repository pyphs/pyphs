#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 00:12:24 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import numpy as np
import sympy as sp
from .. import common
from pyphs import Graph
from ..tools import componentDoc, parametersDefault
from ..mechanics import metadata as dicmetadata
from pyphs.misc.rst import equation
from ..tools import symbols
from .tools import polynomial


class Storage(Graph):
    def __init__(self, label, nodes, **kwargs):

        # instanciate a Graph object
        Graph.__init__(self, label=label)

        ctrl = kwargs.pop("ctrl")

        max_degree = 0
        for c in kwargs:
            i = int(c[1:])
            max_degree = max((max_degree, i))

        coeffs = [sp.sympify(0.0) for _ in range(max_degree + 1)]
        for c in kwargs:
            i = int(c[1:])
            coeffs[i] = symbols(c)

        assert len(coeffs) > 0

        # state  variable
        x = symbols("x" + label)
        # storage funcion
        h = polynomial(x, coeffs)

        # edge data
        data = {"label": x, "type": "storage", "ctrl": ctrl, "link": None}
        N1, N2 = nodes

        # edge
        edge = (N1, N2, data)

        # init component
        self += common.StorageNonLinear(label, [edge], x, h, **kwargs)

    metadata = {
        "title": "Polynomial Storage",
        "component": "Storage",
        "label": "stor",
        "dico": "polynomial",
        "desc": r"Polynomial SISO storage component.",
        "nodesdesc": "Positive flux N1->N2.",
        "nodes": ("N1", "N2"),
        "parametersdesc": "Component parameter.",
        "parameters": [
            [
                "ctrl",
                "Controlled quantity in {'e', 'f'} (effort or flux).",
                "string",
                "e",
            ],
            ["c0", "Constant", "d.u.", 2.5],
            ["c1", "Coefficient of linear monomial", "d.u.", 3.0],
            ["c2", "Coefficient of linear monomial", "d.u.", 4.2],
        ],
        "refs": {},
        "nnodes": 2,
        "nedges": 1,
        "flux": dicmetadata["flux"],
        "effort": dicmetadata["effort"],
    }

    __doc__ = componentDoc(metadata)
