# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 14:23:19 2016

@author: Falaize
"""
import sympy
from calculus import gradient, jacobian, hessian
from structures.tools import output_function
from pyphs.numerics.discrete_calculus import discrete_gradient

##############################################################################


class Expressions:
    """
    Class that serves as a container for all symbolic expressions
    * H: Hamiltonian function expressions
    * z: tuple of dissipation functions expressions
    * g: tuple of input/output gains functions expressions
    """
    def __init__(self, phs):
        setattr(self, '_names', set())
        self.setexpr('H', sympy.sympify(0))
        self.setexpr('z', list())
        self.setexpr('g', list())
        self.phs = phs

    def __add__(exprs1, exprs2):
        """
        method to concatenates (add) two pHs objects.
        """
        exprs = exprs1
        exprs.setexpr('H', exprs.H + exprs2.H)
        exprs.setexpr('z', list(exprs.z)+list(exprs2.z))
        exprs.setexpr('g', list(exprs.g)+list(exprs2.g))
        return exprs

    def build(self):
        """
        Build the following system functions as sympy expressions and append \
them as attributes to the exprs module:
    - 'dxH' the continuous gradient vector of storage scalar function exprs.H,
    - 'dxHd' the discrete gradient vector of storage scalar function exprs.H,
    - 'hessH' the continuous hessian matrix of storage scalar function exprs.H,
    - 'jacz' the continuous jacobian matrix of dissipative vector function \
exprs.z,
    - 'y' the continuous output vector function,
    - 'yd' the discrete output vector function.
        """
        self.setexpr('dxH', gradient(self.H, self.phs.symbs.x))
        self.setexpr('dxHd', discrete_gradient(self.H,
                                               self.phs.symbs.x,
                                               self.phs.symbs.dx()))
        self.setexpr('hessH', hessian(self.H, self.phs.symbs.x))
        self.setexpr('jacz', jacobian(self.z, self.phs.symbs.w))
        y, yd = output_function(self.phs)
        self.setexpr('y', y)
        self.setexpr('yd', yd)

    def setexpr(self, name, expr):
        """
        Add the sympy expression 'expr' to the exprs module, with argument \
'name', and add 'name' to the set of _names
        """
        if name not in self._names:
            self._names.add(name)
        if name is 'H':
            import sympy
            expr = sympy.sympify(expr)
        setattr(self, name, expr)

    def freesymbols(self):
        """
        Retrun a set of freesymbols in all exprs in _names
        """
        symbs = set()
        for name in self._names:
            attr = getattr(self, name)
            if hasattr(attr, "__len__"):
                for expr in attr:
                    symbs.union(expr.free_symbols)
            else:
                symbs.union(attr.free_symbols)
        return symbs
