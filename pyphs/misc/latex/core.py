#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 14:53:41 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

from pyphs.misc.tools import geteval
from .tools import obj2tex, cr, symbol_names, dic2table
from .latexcore import LatexCore
import os
import string


def core2tex(core):

    latexcore = LatexCore(core)

    from pyphs import path_to_templates
    with open(os.path.join(path_to_templates,
                           'latex', 'core.template'), 'r') as f:
        template = string.Template(f.read())
    subs = {}

    # --------------------------------------------------------------------------
    subs['dims'] = ""
    for key in latexcore.dims.keys():
        val = latexcore.dims[key]
        if ((len(key) > 1 and key.endswith('l')) or
                (len(key) > 1 and key.endswith('nl'))):
            label = r"n_\mathbf{"+key[0] + '_{' + key[1:] + r"}}"
            desc = r" $\dim(\mathbf{"+key[0] + '_{' + key[1:] + r"}})=$"
        else:
            label = r"n_\mathbf{"+key+r"}"
            desc = r" $\dim(\mathbf{"+key+r"})=$"
        subs['dims'] += '\par ' + obj2tex(val, label, desc, latexcore.sn,
                                         toMatrix=False)
    # --------------------------------------------------------------------------
    for name in ['x', 'w', 'y', 'o', 'p', 'cy', ]:
        subs['n'+name] = latexcore.dims[name]
    # --------------------------------------------------------------------------
    for name in ['x', 'dx', 'dxH', 'H', 'hessH', 'Q', 'bl',
                 'w', 'z', 'jacz', 'Zl',
                 'u', 'y',
                 'cu', 'cy',
                 'p', 'o', 'subs']:
        subs[name] = getattr(latexcore, name)
    # --------------------------------------------------------------------------
    for name in ['z', 'dxH', 'o', 'y', 'connectors']:
        elts = getattr(latexcore, name+'_elements')
        s = ''
        if len(elts) > 0:
            for t in elts:
                s += r"\par\Resize{" + t + ".}\n" + cr(1)
        subs[name+'_elements'] = s
    # --------------------------------------------------------------------------
    for name in 'MJR':
        struc = ""
        struc += r'\par\Resize{' + getattr(latexcore, name) + r'}' + cr(1)
        for i in ['x', 'w', 'y', 'cy']:
            for j in ['x', 'w', 'y', 'cy']:
                key = name + i + j
                t = getattr(latexcore, key)
                struc += r'\par\Resize{' + t + r'}' + cr(1)
        subs[name] = struc
    # --------------------------------------------------------------------------

    return template.substitute(subs)
