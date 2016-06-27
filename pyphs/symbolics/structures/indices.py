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

        self.phs = phs
        self._set_inds(phs.dims._names)

    def _set_inds(self, names):
        """
        Add indices from list of list of names in dims with \
sum(dims.name())=dims.tot()
        """
        for name in names:
            inds = _inds_in_all(self.phs, names, name)
            setattr(self, name, inds)



def _inds_in_all(phs, names, name):
    """
    return position of deb and end of name in structure
    """
    def inds():
        """
        get indices deb and end of a block"""
        deb = 0
        for current_name in names:
            if current_name != name:
                deb += geteval(phs.dims, current_name)
            else:
                end = deb + geteval(phs.dims, current_name)
                break
        return (deb, end)
    return inds

##############################################################################
