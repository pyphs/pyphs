# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 19:19:36 2016

@author: Falaize
"""

from sympy.printing import latex
from pyphs.config import fold_short_frac, mat_delim, mat_str, mul_symbol
from pyphs.misc.tools import geteval
from pyphs.core.tools import types
from sympy import simplify, Abs


def symbol_names(core):
    sn = {}
    for var in [r'x', 'dx', r'w', r'u', r'y', r'cy', r'p', r'o', r'g', r'z_symbols']:
        for symb in geteval(core, var):
            string = str(symb)
            lab = string[1:]
            sn.update({symb: string[0]+r'_{\mathrm{'+lab+r'}}'})
    for symb in core.subs.keys():
        string = str(symb)
        lab = string[1:]
        sn.update({symb: string[0]+r'_{\mathrm{'+lab+r'}}'})
    return sn


def nice_label(core, tup):
    var, ind = tup
    if var in ['x', 'w', 'u', 'y']:
        label = str(geteval(core, var)[ind])
        content = label[0] + '_{\mathrm{' + label[1:] + '}}'
        return r'$' + content + r'$'
    if var in ['dx']:
        label = str(geteval(core, 'x')[ind])
        content = label[0] + '_{\mathrm{' + label[1:] + '}}'
        return r'$\mathrm{d} ' + content + r'$'
    elif var == 'dxH':
        label = str(geteval(core, 'x')[ind])
        content = label[0] + '_{\mathrm{' + label[1:] + '}}'
        return r'$\frac{\mathrm{d} \mathtt{H}}{\mathrm{d} ' + content+r'}$'
    elif var == 'dtx':
        label = str(geteval(core, 'x')[ind])
        content = label[0] + '_{\mathrm{' + label[1:] + '}}'
        return r'$\frac{\mathrm{d}' + content + r'}{\mathrm{d} t}$'
    elif var == 'z':
        label = str(geteval(core, 'w')[ind])
        content = '_{\mathrm{' + label[1:] + '}}'
        return r'$z' + content+r'$'


def sympy2latex(sp_object, symbol_names):
    """
    print latex code from sympy object
    """
    if isinstance(sp_object, types.matrix_types) and any(el == 0
                                                   for el in
                                                   sp_object.shape):
        return r'\left(\right)'
    else:
        return latex(sp_object, fold_short_frac=fold_short_frac,
                     mat_str=mat_str, mat_delim=mat_delim,
                     mul_symbol=mul_symbol, symbol_names=symbol_names)


def obj2tex(obj, label, description, symbol_names, toMatrix=True):
    r"""
    Return "\ndescription $label = obj$"
    Parameters
    -----------
    obj : sympy object
    label : latex compliant string
    description : string

    Return
    ------
    string
    """
    obj = simplify(obj)
    if toMatrix:
        obj = types.matrix_types[0](obj)
        if obj.shape[0] * obj.shape[1] == 0:
            texobj = r'\mathrm{Empty}'
        elif sum(Abs(obj)) == 0:
            texobj = r'\mathrm{Zeros}'
        else:
            texobj = sympy2latex(obj, symbol_names)
    else:
        texobj = sympy2latex(obj, symbol_names)
    str_out = ''
    description = description + " " if len(description) > 0 \
        else description
    str_out += description +\
        r"$ " + label + r" = " +\
        texobj + r"$"
    return str_out


def cr(n):
    """
    Latex cariage return with insertion of n "%"
    """
    assert isinstance(n, int), 'n should be an int, got {0!s}'.format(type(n))
    string = ('\n' + r'%')*n + '\n'
    return string


def dic2table(labels, dic, sn, centering=True):
    """
    Return a latex table with two columns. Columns labels are labels[0] and
    labels[1], then each line is made of columns key and dic[key] for each
    key in dic.keys.
    """
    l_keys, l_vals = labels
    string = ""
    if centering:
        string += r"\begin{center}" + cr(1)
    string += r"\begin{tabular}{ll}" + cr(1)
    string += r"\hline" + cr(0)
    string += l_keys + r" & " + l_vals + cr(0) + r"\\ \hline" + cr(0)
    for k in dic.keys():
        v = dic[k]
        strk = str(k)
        label = strk[0]
        if len(strk[1:]) > 0:
            label += r'_{\mathrm{'+strk[1:]+r'}}'
        if not isinstance(v, (int, float, str)):
            value = sympy2latex(v, sn)
        else:
            value = str(v)
        string += r"$" + label + r"$ & " + value + cr(0) + r"\\" + cr(0)
    string += r"\hline" + cr(0)
    string += r"\end{tabular}" + cr(1)
    if centering:
        string += r"\end{center}"
    return string


def dic2array(dic):
    """
    """
    string = cr(1)
    string += r"\begin{tabular}{ll}" + cr(1)
    for k in dic.keys():
        v = dic[k]
        string += str(k) + r" & " + str(v) + cr(0) + r"\\" + cr(0)
    string += r"\end{tabular}"
    return string


def comment(s):
    out = str()
    for line in s.splitlines():
        out += '% ' + line + '\n'
    return out
