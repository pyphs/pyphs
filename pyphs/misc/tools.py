# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 13:53:43 2016

@author: Falaize
"""
from datetime import datetime


# =========================================================================== #

def get_date():
    " Return current date and time "
    now = datetime.now()
    dt_format = '%Y/%m/%d %H:%M:%S'
    return now.strftime(dt_format)


# =========================================================================== #

def pause():
    """
Pause compatible with Python 2 and Python 3, wait for user to press return.
    """
    try:
        raw_input()
    except NameError:
        input()


# =========================================================================== #

def geteval(obj, attr):
    """
    if getattr(obj, attr) is function, return evaluation with no arguments, \
else return value.
    """
    elt = getattr(obj, attr)
    if hasattr(elt, '__call__'):
        return elt()
    else:
        return elt


# =========================================================================== #

def myrange(N, indi, indf):
    """
Return 'range(N)' with index 'indi' at position 'indf'
    """
    lis = list(range(N))
    if indi < indf:
        deb = lis[:indi] + lis[indi+1:indf+1]
        end = lis[indf+1:]
        eli = [lis[indi], ]
        lis = deb + eli + end
    elif indi > indf:
        deb = lis[:indf]
        end = lis[indf:indi] + lis[indi+1:]
        eli = [lis[indi], ]
        lis = deb + eli + end
    return lis


# =========================================================================== #

def decimate(it, nd=10):
    """
    Return first then each 'nd' elements from iterable 'it'.

    Parameters
    -----------

    it : iterable
        Input data.

    nd : int
        Decimation factor

    Returns
    -------

    l : list
        One in 'nd' values from 'it'.

    """
    assert isinstance(nd, int), "'nd' is not an integer: {0!r}".format(nd)
    assert nd > 0, "'nd' is not a positive integer: {0!r}".format(nd)
    l = list()
    n = 0
    for el in it:
        if not n % nd:
            l.append(el)
        n += 1
    return l


# =========================================================================== #

def remove_duplicates(lis):
    """
    Remove duplicate entries from a given list, preserving ordering.
    """
    out_list = []
    for el in lis:
        if el not in out_list:
            out_list.append(el)
    return out_list


# =========================================================================== #

def get_strings(obj, remove=None):
    """
Get strings in obj recursively.

Example
-------
>>> from pyphs.misc.tools import get_strings
>>> l = ['jkl', ['llm', ['o']], 'r', ['k', ['l']]]
>>> get_strings(l)
['jkl', 'llm', 'o', 'r', 'k', 'l']
    """
    if remove is None:
        remove = list()
    strings = []
    if not isinstance(obj, str):
        for el in obj:
            strings += get_strings(el, remove=remove)
    else:
        if obj not in remove:
            strings.append(obj)
    return strings


# =========================================================================== #

def find(symbs, allsymbs):
    """
Sort elements in symbs according to allsymbs to form and return (args, inds)
with list of ordered arguments as args and corresponding list of indices in
allsymbs as inds.
    """
    args = []
    inds = []
    n = 0
    for symb in allsymbs:
        if symb in symbs:
            args.append(symb)
            inds.append(n)
        n += 1
    return tuple(args), tuple(inds)


# =========================================================================== #

def interleave(l1, l2):
    """
    Interleave the elements in lists l1 and l2 (same length).
    """
    return [val for pair in zip(l1, l2) for val in pair]
