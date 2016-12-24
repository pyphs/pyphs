# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 19:19:36 2016

@author: Falaize
"""

import sympy
from sympy.printing import latex
from pyphs.config import fold_short_frac, mat_delim, mat_str, mul_symbol


def nice_label(var, ind):
    if var in ('dxHd', 'dxH'):
        return r'$\overline{\nabla}\mathtt{H}_'+str(ind)+r'$'
    elif var == 'dtx':
        return r'$\mathrm D_t \,{x}_'+str(ind)+'$'
    else:
        return r'$'+var+'_'+str(ind)+r'$'


def sympy2latex(sp_object, symbol_names):
    """
    print latex code from sympy object
    """
    if isinstance(sp_object, sympy.Matrix) and any(el == 0
                                                   for el in
                                                   sp_object.shape):
        return r'\left(\right)'
    else:
        return latex(sp_object, fold_short_frac=fold_short_frac,
                     mat_str=mat_str, mat_delim=mat_delim,
                     mul_symbol=mul_symbol, symbol_names=symbol_names)


def obj2tex(obj, label, description, symbol_names, toMatrix=True):
    """
    Return "%\ndescription $label = obj$;"
    Parameters
    -----------
    obj : sympy object
    label : latex compliant string
    description : string

    Return
    ------
    string
    """

    if toMatrix:
        import sympy as sp
        obj = sp.Matrix(obj)

    str_out = cr(1)
    description = description + " " if len(description) > 0 \
        else description
    str_out += description +\
        r"$ " + label + r" = " +\
        sympy2latex(obj, symbol_names) + r" ; $ " + cr(1) + r'\\'
    return str_out


def cr(n):
    """
    Latex cariage return with insertion of n "%"
    """
    assert isinstance(n, int), 'n should be an int, got {0!s}'.format(type(n))
    string = ('\n' + r'%')*n + '\n'
    return string
