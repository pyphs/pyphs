#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 23:55:44 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

from ..common import Port
from ..tools import componentDoc
from . import metadata as dicmetadata


class Source(Port):
    def __init__(self, label, nodes, **kwargs):
        assert kwargs["ctrl"] in ("f", "e")
        Port.__init__(self, label, nodes, **kwargs)

    metadata = {
        "title": "Electrical source",
        "component": "Source",
        "label": "sourc",
        "dico": "electronics",
        "desc": 'Controlled flux (ctrl="e") or effort (ctrl="f") source.',
        "nodesdesc": "source terminals with positive flux N1->N2.",
        "nodes": ("N1", "N2"),
        "parameters": [["ctrl", "Source type in {'f', 'e'}", "string", "f"]],
        "refs": {},
        "nnodes": 2,
        "nedges": 1,
        "flux": dicmetadata["flux"],
        "effort": dicmetadata["effort"],
    }

    # Write documentation
    __doc__ = componentDoc(metadata)
