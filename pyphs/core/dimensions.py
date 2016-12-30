# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 23:08:40 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function
from pyphs.core.misc_tools import geteval


class Dimensions:
    """
    Class that serves as a container for system's dimensions
    """
    def __init__(self, core):
        """
        Defines accessors to len of var 'phs.symbs.nvar' for var in x, w, y, cy
        """
        setattr(self, 'names', ('x', 'w', 'y', 'cy'))

        for name in self.names:
            dimvar = _dimvar_generator(core, name)
            setattr(self, name, dimvar)

        dimp = _dimvar_generator(core, 'p')
        setattr(self, 'p', dimp)

        dimargs = _dimvar_generator(core, 'args')
        setattr(self, 'args', dimargs)

        # init number of linear components to 0
        self._xl = 0
        self._wl = 0

    def tot(self):
        """
        Total dimension ntot = dim(x)+dim(w)+dim(y)+dim(cy)
        """
        return sum(geteval(self, var) for var in self.names)

    def xl(self):
        """
        Number of states associated to linear storage components
        """
        return self._xl

    def xnl(self):
        """
        Number of states associated to nonlinear storage components
        """
        return self.x() - self.xl()

    def wl(self):
        """
        Number of linear dissiaptive variables
        """
        return self._wl

    def wnl(self):
        """
        Number of nonlinear dissiaptive variables
        """
        return self.w() - self.wl()

    def l(self):
        """
        Total number of inear variables
        """
        return self.xl() + self.wl()

    def nl(self):
        """
        Total number of nonlinear variables
        """
        return self.xnl() + self.wnl()

###############################################################################
###############################################################################
###############################################################################


def _dimvar_generator(core, var):
    """
    return length of 'pho.symbs.var'
    """
    def dimvar():
        return len(geteval(core, var))
    return dimvar
