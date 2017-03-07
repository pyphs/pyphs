# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 00:24:35 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

from pyphs.config import authors, affiliations, special_chars
from pyphs.latex.tools import cr


def docpreamble(title):
    nb_authors = len(authors)
    nb_affiliations = len(affiliations)
    latex_affiliations = ""
    if nb_affiliations > 1:
        assert nb_affiliations == nb_authors
        id_affiliations = list()
        i = 1
        for affiliation in affiliations:
            latex_affiliations += cr(1)
            latex_affiliations += r"\affil["+str(i)+r"]{"+affiliation+r"}"
            id_affiliations.append(i)
            i += 1
    else:
        latex_affiliations += cr(1)
        latex_affiliations += r"\affil["+str(1)+r"]{"+affiliations[0]+r"}"
        id_affiliations = [1, ]*nb_affiliations
    latex_authors = ""
    for author, id_aff in zip(authors, id_affiliations):
        latex_authors += cr(1)
        latex_authors += r'\author['+str(id_aff)+r']{'+author+'}'

    str_preamble = \
        r"""%
\documentclass[11pt, oneside]{article}      % use 'amsart' instead of """ + \
        r"""'article' for AMSLaTeX format
\usepackage{geometry}                       % See geometry.pdf to learn """ + \
        r"""the layout options. There are lots.
\geometry{letterpaper}                      % ... or a4paper or a5paper """ + \
        r"""or ...
%\geometry{landscape}                       % Activate for for rotated """ + \
        r"""page geometry
\usepackage[parfill]{parskip}               % Activate to begin """ + \
        r"""paragraphs with an empty line rather than an indent
\usepackage{graphicx}                       % Use pdf, png, jpg, or eps """ + \
        r"""with pdflatex; use eps in DVI mode
                                        % TeX will automatically """ + \
        r"""convert eps --> pdf in pdflatex
\usepackage{amssymb}
%\date{\today}                              % Activate to display a """ + \
        r"""given date or no date
\title{""" + title + r"""}
%
\usepackage{authblk}
\usepackage{hyperref}
%\renewcommand\Authands{ and }
%"""
    return str_preamble + latex_authors + latex_affiliations


def texdocument(content, title, filename=None):
    """
    return latex code as plain string for global phs description
    """
    str_tex = ""
    str_tex += docpreamble(title)
    str_tex += cr(1) + r"\begin{document}" + cr(1)
    str_tex += r"\maketitle"
    str_tex += content
    str_tex += cr(1)
    str_tex += r"\end{document}"
    for special_char in special_chars:
        latex_char = "\\" + special_char
        str_tex = str_tex.replace(special_char, latex_char)
    if filename is not None:
        file_ = open(filename, 'w')
        file_.write(str_tex)
        file_.close()


def dic2table(labels, dic):
    """
    Return a latex table with two columns. Columns labels are labels[0] and \
labels[1], then each line is made of columns key and dic[key] for each dic.keys
    """
    l_keys, l_vals = labels
    string = ""
    string += r"\begin{center}" + cr(1)
    string += r"\begin{tabular}{ll}" + cr(1)
    string += r"\hline" + cr(0)
    string += l_keys + r" & " + l_vals + cr(0) + r"\\ \hline" + cr(0)
    for k in dic.keys():
        v = dic[k]
        string += str(k) + r" :& " + str(v) + cr(0) + r"\\" + cr(0)
    string += r"\hline" + cr(0)
    string += r"\end{tabular}" + cr(1)
    string += r"\end{center}"
    return string


def dic2array(dic):
    """
    Return a latex table with two columns. Columns labels are labels[0] and \
labels[1], then each line is made of columns key and dic[key] for each dic.keys
    """
    string = cr(1)
    string += r"\begin{tabular}{ll}" + cr(1)
    for k in dic.keys():
        v = dic[k]
        string += str(k) + r" & " + str(v) + cr(0) + r"\\" + cr(0)
    string += r"\end{tabular}"
    return string
