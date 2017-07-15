# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 18:57:18 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

from ..core.core import Core
from ..core.tools import types

symbols = Core.symbols


class Argument:

    def __init__(self, name, obj):
        self.symb, self.sub, self.par = form(name, obj)


def form(name, obj):
    """
    Pyphs formating of argument format 'obj' to a symbol

    Parameters
    ----------
    argname : str
    argobj : {str, float, (str, float)}

    Outputs
    -------
    symb : Core.symbol
    subs : Core.subs
    """
    if isinstance(obj, tuple):
        if not isinstance(obj[0], str):
            raise TypeError('For tupple parameter, \
        first element should be a str, got {0}'.format(type(obj[0])))
        try:
            if not isinstance(obj[1], types.scalar_types):
                raise TypeError('For tupple parameter, \
                    second element should be numeric, got\
                    {0}'.format(type(obj[1])))
        except AssertionError:
            types.scalar_test(obj[1])
        string = obj[0]
        symb = Core.symbols(string)
        sub = {symb: obj[1]}
        par = None
    elif isinstance(obj, (float, int)):
        string = name
        symb = Core.symbols(string)
        sub = {symb: obj}
        par = None
    elif isinstance(obj, str):
        string = obj
        symb = Core.symbols(string)
        sub = {}
        par = symb
    else:
        types.scalar_test(obj)
        string = name
        symb = Core.symbols(string)
        sub = {symb: obj}
        par = None

    return symb, sub, par


def mappars(graph, **kwargs):
    """
    map dictionary of 'par':('label', value) to dictionary of substitutions \
for parameters in component expression 'dicpars' and for parameters in phs \
'subs'.
    """
    dicpars = {}
    subs = {}
    for key in kwargs.keys():
        symb, sub, par = form(graph.label + '_' + str(key), kwargs[key])
        dicpars.update({Core.symbols(key): symb})
        subs.update(sub)
        if par is not None:
            graph.core.add_parameters(par)
    return dicpars, subs


def nicevarlabel(var, label):
    """
    return a formated string eg. xcapa if 'var' is 'x' and label is 'capa'.
    """
    return var + label
