# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 00:24:35 2016

@author: Falaize
"""

forbiden_char = ['#']


def cr(n):
    """
    Latex cariage return with insertion of n "%"
    """
    assert isinstance(n, int), 'n should be an int, got {0!s}'.format(type(n))
    string = ('\n' + r'%')*n + '\n'
    return string


def print_latex(sp_object):
    from sympy.printing import latex
    import sympy as sp
    if isinstance(sp_object, sp.Matrix) and any(el == 0
                                                for el in sp_object.shape):
        return '\\left(\\right)'
    else:
        return latex(sp_object, fold_short_frac=True, mat_str="array")


def obj2tex(obj, label, description, toMatrix=True):
    """
    Return nicely latex formated string for "%\ndescription $label = obj$;"
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
    description = description + " " if len(description) > 0 else description
    str_out += description +\
        r"$ " + label + r" = " +\
        print_latex(obj) + r" ; $ " + cr(1) + r'\\'
    return str_out


def preamble(phs):
    str_preamble = \
        r"""
\documentclass[11pt, oneside]{article}  % use 'amsart' instead of \
'article' for AMSLaTeX format

\usepackage{geometry}                   % See geometry.pdf to learn the \
layout options. There are lots.
\geometry{letterpaper}                  % ... or a4paper or a5paper \
or ...
%\geometry{landscape}                   % Activate for for rotated page \
geometry

\usepackage[parfill]{parskip}           % Activate to begin paragraphs with \
an empty line rather than an indent

\usepackage{graphicx}                   % Use pdf, png, jpg, or eps with \
pdflatex; use eps in DVI mode
                                        % TeX will automatically convert \
eps --> pdf in pdflatex

\usepackage{amssymb}

%\date{}                                % Activate to display a given \
date or no date

\title{Structure of pHs \texttt{""" + phs.label + r"""}}

\usepackage{authblk}
\usepackage{hyperref}
\author[1]{Antoine Falaize}
\affil[1]{Project-team S3\footnote{\url{http://s3.ircam.fr}}, STMS, \
IRCAM-CNRS-UPMC (UMR 9912), 1 Place Igor-Stravinsky, 75004 Paris, France}
%\renewcommand\Authands{ and }



"""
    return str_preamble


def dimensions(phs):
    str_dimensions = ""
    str_dimensions += r"\section{System dimensions}"
    for dim in [r'x', r'w', r'y', r'p']:
        obj = eval(r'phs.n'+dim+r'()')
        label = r"n_\mathbf{"+dim+r"}"
        desc = r"$\dim(\mathbf{"+dim+r"})=$"
        str_dimensions += obj2tex(obj, label, desc, toMatrix=False)
    return str_dimensions


def str_figure_graph(phs):
    import os
    from pyphs_config import plot_format
    phs.plot_graph()
    fig_name = phs.folders['plots'] + os.sep + phs.label + \
        '_graph.' + plot_format
    string = r"""%
%
\begin{figure}[!h]
\begin{center}
\includegraphics[width=\linewidth]{""" + fig_name + r"""}
%
\caption{\label{fig:graph_""" + phs.label + r"""} Graph of system \texttt{""" + phs.label + r"""}. }
\end{center}
\end{figure}
%"""
    return string


def netlist(phs):
    str_netlist = cr(2)
    if len(phs.netlist) > 0:
        str_netlist += r"\section{System netlist}" + cr(2)
        str_netlist += r"\begin{center}" + cr(1)
        str_netlist += r"\texttt{" + cr(0)
        str_netlist += r"\begin{tabular}{llllll}" + cr(0)
        str_netlist += r"\hline" + cr(0)
        str_netlist += "line & dictionary.component & label & nodes & \
parameters " + r"\\ \hline" + cr(1)
        l = 0
        for line in phs.netlist.splitlines():
            l += 1
            str_table = ''
            columns = [r"$\ell_" + str(l) + r"$"]
            ind_bracket_1 = line.index('[')
            columns += line[:ind_bracket_1-1].split(' ')
            ind_bracket_2 = line.index(']')
            columns += [line[ind_bracket_1:ind_bracket_2+1], ]
            columns += [line[ind_bracket_2+2:], ]
            for el in columns:
                str_table += el + " & "
            str_netlist += str_table[:-2] + cr(0) + r"\\" + cr(0)
        str_netlist += r"\hline" + cr(0)
        str_netlist += r"\end{tabular}" + cr(1)
        str_netlist += r"}" + cr(1)
        str_netlist += r"\end{center}"+'\n'
        str_netlist += str_figure_graph(phs)
    return str_netlist


def variables(phs):
    str_variables = cr(2)
    str_variables += r"\section{System variables}"
    if phs.nx() > 0:
        str_variables += obj2tex(phs.x, r'\mathbf{x}', 'State variable')
    if phs.nw() > 0:
        str_variables += obj2tex(phs.w, r'\mathbf{w}', 'Dissipation variable')
    if phs.ny() > 0:
        str_variables += obj2tex(phs.u, r'\mathbf{u}', 'Input')
        str_variables += obj2tex(phs.y, r'\mathbf{y}', 'Output')
    return str_variables


def relations(phs):
    str_relations = cr(2)
    str_relations += r"\section{Constitutive relations}"
    if phs.nx() > 0:
        str_relations += obj2tex(phs.H, r'\mathtt{H}(\mathbf{x})',
                                 'Hamiltonian',
                                 toMatrix=False)
        str_relations += obj2tex(phs.dxH, r'\nabla \mathtt{H}(\mathbf{x})',
                                 'Hamiltonian gradient')
    if phs.nw() > 0:
        str_relations += obj2tex(phs.z, r'\mathbf{z}(\mathbf{w})',
                                 'Dissipation function')
        str_relations += obj2tex(phs.Jacz,
                                 r'\mathcal{J}_{\mathbf{z}}(\mathbf{w})',
                                 'Jacobian of dissipation function')
    return str_relations


def parameters(phs):
    str_parameters = ""
    if len(phs.subs) > 0:
        str_parameters += cr(2)
        str_parameters += r"\section{System parameters}" + cr(2)
        str_parameters += r"\subsection{Constant}" + cr(1)
        str_parameters += dic2table(['parameter', 'value (SI)'], phs.subs)
    if phs.np() > 0:
        str_parameters += cr(2)
        str_parameters += r"\subsection{Controled}" + cr(1)
        str_parameters += obj2tex(phs.params, r'\mathbf{p}',
                                  'Control parameters')
    return str_parameters


def structure(phs):
    str_structure = cr(1)
    str_structure += r"\section{System structure}" + cr(1)
    if phs.nx() > 0:
        str_structure += obj2tex(phs.Jx, r"\mathbf{J_x}", "")
        if phs.nw() > 0:
            str_structure += obj2tex(phs.K, r"\mathbf{K}", "")
        if phs.ny() > 0:
            str_structure += obj2tex(phs.Gx, r"\mathbf{G_x}", "")
    if phs.nw() > 0:
        str_structure += obj2tex(phs.Jw, r"\mathbf{J_w}", "")
        if phs.ny() > 0:
            str_structure += obj2tex(phs.Gw, r"\mathbf{G_w}", "")
    if phs.ny() > 0:
        str_structure += obj2tex(phs.Jy, r"\mathbf{J_y}", "")
    str_J = obj2tex(phs.J, r"\mathbf{J}", "")
    str_J = str_J.replace('begin{matrix}', 'begin{array}{' +
                          r'c'*phs.nx() +
                          r'|' + r'c'*phs.nw() +
                          r'|' + r'c'*phs.nw() + r'}')
    str_structure += str_J.replace('end{matrix}', 'end{array}')
    return str_structure


def dic2table(labels, dic):
    l_keys, l_vals = labels
    string = ""
    string += r"\begin{center}" + cr(1)
    string += r"\begin{tabular}{ll}" + cr(1)
    string += r"\hline" + cr(0)
    string += l_keys + r" & " + l_vals + cr(0) + r"\\ \hline" + cr(0)
    for k in dic.keys():
        v = dic[k]
        string += str(k) + r" & " + str(v) + cr(0) + r"\\" + cr(0)
    string += r"\hline" + cr(0)
    string += r"\end{tabular}" + cr(1)
    string += r"\end{center}"
    return string


def phs2tex(phs):
    str_tex = ""
    str_tex += preamble(phs)
    str_tex += r"\begin{document}" + cr(1)
    str_tex += r"\maketitle"
    str_tex += netlist(phs)
    str_tex += dimensions(phs)
    str_tex += variables(phs)
    str_tex += relations(phs)
    str_tex += parameters(phs)
    str_tex += structure(phs)
    str_tex += cr(1)
    str_tex += r"\end{document}"
    for char in forbiden_char:
        replacement_char = "\\" + char
        str_tex = str_tex.replace(char, replacement_char)
    str_tex = str_tex.replace('left[', 'left(')
    str_tex = str_tex.replace('right]', 'right)')
    return str_tex
