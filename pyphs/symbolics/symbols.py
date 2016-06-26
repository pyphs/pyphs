# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 14:22:39 2016

@author: Falaize
"""

from pyphs.misc.tools import geteval

##############################################################################


class Symbols:
    """
    Class that serves as a container for all symbols:
    * x: list of state variable symbols
    * w: list of dissipation variable symbols
    * u: list of input symbols
    * y: list of output symbols
    * p: list of parameter symbols
    * subs: dictionary with symbols as keys and substitution exprs as values
    * cu: list of connectors input symbols
    * cy: list of connectors outputs symbols
    * _names: set of names for all the lists
    """
    def __init__(self):
        # init subs with empty dictionary
        setattr(self, 'subs', dict())
        setattr(self, '_names', set())
        # init symbols with empty lists
        for name in {'x', 'w', 'u', 'y', 'cu', 'cy', 'p'}:
            self._setsymb(name, tuple())

    def __add__(symbs1, symbs2):
        """
        method to concatenates (add) two pHs objects.
        """
        symbs = symbs1
        for name in symbs._names:
            symbs._setsymb(name, list(getattr(symbs, name)) +
                           list(getattr(symbs2, name)))
        symbs.subs.update(symbs2.subs)
        return symbs

    def dx(self):
        """
        returns the states increment symbols "dxi" associated with state \
symbol "xi" for "xi" in state vector "x".
        """
        from tools import symbols
        symbs = tuple()
        for x in self.x:
            symbs += (symbols('d'+str(x)), )
        return symbs

    def args(self):
        """
        return list of symbols associated with arguments of numerical functions
        """
        # names of arguments for functions evaluation
        _args_names = ('x', 'dx', 'w', 'u', 'p')
        args = []
        for name in _args_names:
            symbs = geteval(self, name)
            args += symbs
        return args

    def _setsymb(self, name, list_symbs):
        """
        define list of symbol "name" (eg "x", "w" or "y") and add "name" \
to list of names.
        """
        if name not in self._names:
            self._names.add(name)
        setattr(self, name, tuple(list_symbs))

    def _allsymbs(self):
        """
        return all symbols in lists with name in Symbols._names
        """
        symbs = set()
        for attr in self._names:
            symbs_attr = getattr(self, attr)
            for symb in symbs_attr:
                symbs.add(symb)
        return symbs
