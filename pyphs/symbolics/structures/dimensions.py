# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 23:08:40 2016

@author: Falaize
"""
from pyphs.misc.tools import geteval

dims_names = ('x', 'w', 'y', 'cy')


class Dimensions:
    """
    Class that serves as a container for system's dimensions
    """
    def __init__(self, phs):
        """
        define accessors to len of var 'phs.symbs.nvar' for var in x, w, y, cy
        """
        setattr(self, '_names', dims_names)

        for name in self._names:
            dimvar = _dimvar_generator(phs, name)
            setattr(self, name, dimvar)

        dimp = _dimvar_generator(phs, 'p')
        setattr(self, 'p', dimp)

        dimargs = _dimvar_generator(phs, 'args')
        setattr(self, 'args', dimargs)

        # init number of linear components to 0
        self.xl = 0
        self.wl = 0

    def tot(self):
        """
        total dimension ntot = dim(x)+dim(w)+dim(y)+dim(cy)
        """
        return sum(geteval(self, var) for var in self._names)

    def xnl(self):
        """
        number of states associated to nonlinear components
        """
        return self.x() - self.xl

    def wnl(self):
        """
        number of dissiaptive variables to nonlinear components
        """
        return self.w() - self.wl


def _dimvar_generator(phs, var):
    """
    return length of 'pho.symbs.var'
    """
    def dimvar():
        return len(geteval(phs.symbs, var))
    return dimvar
