# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 14:23:19 2016

@author: Falaize
"""

##############################################################################


class Expressions:
    """
    Class that serves as a container for all symbolic expressions
    * H: Hamiltonian function expressions
    * z: tuple of dissipation functions expressions
    * g: tuple of input/output gains functions expressions
    """
    def __init__(self):
        import sympy
        setattr(self, '_names', set())
        self.setexpr('H', sympy.sympify(0))
        self.setexpr('z', tuple())
        self.setexpr('g', tuple())

    def __add__(exprs1, exprs2):
        exprs = exprs1
        exprs.setexpr('H', exprs.H + exprs2.H)
        exprs.setexpr('z', list(exprs.z)+list(exprs2.z))
        exprs.setexpr('g', list(exprs.g)+list(exprs2.g))
        return exprs

    def build(self, symbs):
        from symbolics.calculus import gradient, jacobian, hessian
        self.setexpr('gradH', gradient(self.H, symbs.x))
        self.setexpr('hessH', hessian(self.H, symbs.x))
        self.setexpr('jacz', jacobian(self.z, symbs.w))

    def setexpr(self, name, expr):
        if name not in self._names:
            self._names.add(name)
        if name is 'H':
            import sympy
            expr = sympy.sympify(expr)
        setattr(self, name, expr)

    def freesymbols(self):
        symbs = set()
        for name in self._names:
            attr = getattr(self, name)
            if hasattr(attr, "__len__"):
                for expr in attr:
                    symbs.union(expr.free_symbols)
            else:
                symbs.union(attr.free_symbols)
        return symbs
