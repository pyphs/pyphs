# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 23:28:36 2016

@author: Falaize
"""
from pyphs.misc.tools import geteval


class Indices:
    """
    Class that serves as a container for indices of arguments
    """
    def __init__(self, phs):
        for name in phs.dims._names:
            inds = _inds_in_all(phs, name)
            setattr(self, name, inds)
        setattr(self, name, inds)

def _inds_in_all(phs, name):
    """
    return position of deb and end of name in structure
    """

    def inds():
        """
        get indices deb and end of block """ + name
        names = list(phs.dims._names)
        iter_name = names.pop(0)
        deb = 0
        while iter_name != name:
            deb += geteval(phs.dims, iter_name)
            iter_name = names.pop(0)
        end = deb + geteval(phs.dims, iter_name)
        return (deb, end)

    return inds

##############################################################################
