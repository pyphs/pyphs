# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 18:57:18 2016

@author: Falaize
"""
from pyphs.symbolics.tools import symbols


def parsub(phs, obj, par_name):
    """
    format 'obj' to a symbol

    Parameters
    ----------
    phs : pypHs.PortHamiltonianObject

    obj : str, float or (str, float)

    par_name : str

    Outputs
    -------

    symb : sympy.symbols(real=True)

    subs : dic to be append on phs
    """
    if isinstance(obj, tuple):
        assert isinstance(obj[0], str), 'for tupple parameter, \
        first element should be a str, got {0!s}'.format(type(obj[0]))
        assert isinstance(obj[1], (float, int)), 'for tupple parameter, \
        second element should be numeric (foat or int), got\
{0!s}'.format(type(obj[1]))
        string = obj[0]
        symb = symbols(string)
        sub = {symb: obj[1]}
    elif isinstance(obj, (float, int)):
        string = par_name
        symb = symbols(string)
        sub = {symb: obj}
    elif isinstance(obj, str):
        string = obj
        symb = symbols(string)
        sub = {}
        phs.symbs.p += (symb, )
    return symb, sub


def mappars(phs, **kwargs):
    """
    map dictionary of 'par':('label', value) to dictionary of substitutions \
for parameters in component expression 'dicpars' and for parameters in phs \
'subs'.
    """
    dicpars = {}
    subs = {}
    for key in kwargs.keys():
        symb, sub = parsub(phs, kwargs[key], phs.label + '_' + str(key))
        dicpars.update({symbols(key): symb})
        subs.update(sub)
    return dicpars, subs
