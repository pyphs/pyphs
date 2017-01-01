#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 18:35:17 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

def geteval(obj, attr):
    """
    If getattr(obj, attr) is a function, returns the evaluation of this \
function with no arguments; else returns the value from getattr.
    """
    elt = getattr(obj, attr)
    if hasattr(elt, '__call__'):
        return elt()
    else:
        return elt


def myrange(N, indi, indf):
    """
    return 'range(N)' with index 'indi' at position 'indf'
    """
    lis = list(range(N))
    if indi < indf:
        deb = lis[:indi] + lis[indi+1:indf+1]
        end = lis[indf+1:]
        eli = [lis[indi], ]
        lis = deb + eli + end
    elif indi > indf:
        deb = lis[:indf]
        end = lis[indf:indi] + lis[indi+1:]
        eli = [lis[indi], ]
        lis = deb + eli + end
    return lis
