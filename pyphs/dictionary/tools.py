# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 18:57:18 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

from pyphs.core.core import symbols


class PHSArgument:

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
    symb : PHSCore.symbol
    subs : PHSCore.subs
    """
    if isinstance(obj, tuple):
        assert isinstance(obj[0], str), 'for tupple parameter, \
        first element should be a str, got {0!s}'.format(type(obj[0]))
        assert isinstance(obj[1], (float, int)), 'for tupple parameter, \
        second element should be numeric, got\
{0!s}'.format(type(obj[1]))
        string = obj[0]
        symb = symbols(string)
        sub = {symb: obj[1]}
        par = None
    elif isinstance(obj, (float, int)):
        string = name
        symb = symbols(string)
        sub = {symb: obj}
        par = None
    elif isinstance(obj, str):
        string = obj
        symb = symbols(string)
        sub = {}
        par = symb
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
        dicpars.update({symbols(key): symb})
        subs.update(sub)
        if par is not None:
            graph.core.add_parameters(par)
    return dicpars, subs


def nicevarlabel(var, label):
    """
    return a formated string eg. xcapa if 'var' is 'x' and label is 'capa'.
    """
    return var + label
