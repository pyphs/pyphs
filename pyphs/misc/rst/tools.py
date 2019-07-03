#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 16:50:23 2018

@author: afalaize
"""

from pyphs.config import RST
from pyphs.numerics.cpp.tools import indent


def equation(text):
    if RST['equations'] == 'mathjax':
        return '\n\n.. math::\n\n    ' + text + '\n\n'
    elif RST['equations'] == 'latex':
        return '\n$' + text + '$\n'
    else:
        raise AttributeError('unknown rst equation format {}'.format(RST['equations']))


def title(text, level=1):

    seps = {0: '=',
            1: '-',
            2: '=',
            3: '-',
            4: '`',
            5: "'",
            }

    lt = len(text)
    if level < 2:
        text = ' {} \n'.format(text)
        bottom = top = (lt+2)*seps[level] + '\n'
    else:
        top = ''
        text = '{}\n'.format(text)
        bottom = lt*seps[level] + '\n'

    return top + text + bottom


def rstTableV2(header, content):
    """
    Return a restructured-text table.

    Parameters
    ----------

    header : list of strings
        List of table headers.

    content : list of list of strings
        List of table lines, with each line a list of line columns content.

    Return
    ------

    table : string
        Restructured-text table.

    """

    dim = []
    for i, h in enumerate(header):
        dim.append(max(map(len, [h, ] + [c[i] for c in content])))

    def line(l, center=False):
        string = ''
        for i, e in enumerate(l):
            nb = dim[i] + 2 - len(e)
            if center:
                pre = int(nb/2.)
            else:
                pre = 1
            post = nb-pre
            string += '{}{}{} '.format(pre*' ', e, post*' ')
        string += '\n'
        return string

    def delimiters():
        string = ''
        for i, d in enumerate(dim):
            string += '='*(d+2) + ' '
        string = string[:-1] + '\n'
        return string

    string = ''
    string += delimiters()
    string += line(header, center=True)
    string += delimiters()
    for l in content:
        string += line(l)
        string += delimiters()

    return string


def rstTableV1(header, content):
    """
    Return a restructured-text table.

    Parameters
    ----------

    header : list of strings
        List of table headers.

    content : list of list of strings
        List of table lines, with each line a list of line columns content.

    Return
    ------

    table : string
        Restructured-text table.

    """

    dim = []
    for i, h in enumerate(header):

        dim.append(max(map(len, [h, ] + [str(c[i]) for c in content])))

    def line(l):
        string = '|'
        for i, e in enumerate(l):
            nb = dim[i]+1-len(str(e))
            string += ' {}{}|'.format(e, ' '*nb)
        string += '\n'
        return string

    def delimiters(marker='-'):
        string = '+'
        for i, d in enumerate(dim):
            string += marker*(d+2) + '+'
        string += '\n'
        return string

    string = ''
    string += delimiters()
    string += line(header)
    string += delimiters('=')
    for l in content:
        string += line(l)
        string += delimiters()

    return string
