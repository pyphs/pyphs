# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 00:24:35 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

from pyphs.config import special_chars
from pyphs.misc.tools import get_time
from .tools import comment

import string
import os


def texdocument(content, path, title=None, description=None):
    """
Build a LaTeX document and save it to path.

Parameters
-----------

content: str
    LaTeX content of the document.

path: str
    Path to the generated .tex file.

title: str or None
    Document title. Default is None.

    """

    subs = {}

    if title is None:
        title = ''
    subs['title'] = title

    if description is None:
        description = '%'
    subs['description'] = description

    from pyphs import path_to_templates
    with open(os.path.join(path_to_templates,
                           'latex', 'document.template'), 'r') as f:
        template = string.Template(f.read())

    with open(os.path.join(path_to_templates,
                           'licence.template'), 'r') as f:
        licence = string.Template(f.read())
    str_licence = licence.substitute({'time': get_time()})
    subs['licence'] = comment(str_licence)

    for special_char in special_chars:
        latex_char = "\\" + special_char
        content = content.replace(special_char, latex_char)
    subs['content'] = content
    subs['time'] = get_time()

    str_tex = template.substitute(subs)

    with open(path, 'w') as f:
        f.write(str_tex)
