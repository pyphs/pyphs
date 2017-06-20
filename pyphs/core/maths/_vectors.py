#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 15 21:18:38 2017

@author: Falaize
"""
from ..tools import types


def sumvecs(*args):
    """
sums vectors (list elements)
    """
    args = list(args)
    v0 = args.pop()
    types.vector_test(v0)
    l = len(v0)
    for v in args:
        types.vector_test(v)
        assert len(v) == l, '{} not equal to {}'.format(len(v), l)
        v0 = [e1 + e2 for e1, e2 in zip(v0, v)]
    return v0
