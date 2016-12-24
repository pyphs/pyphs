# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 00:24:35 2016

@author: Falaize
"""
from sympy.printing import latex
import sympy
from pyphs.config import authors, affiliations, \
    fold_short_frac, mat_delim, mat_str, mul_symbol
from pyphs.misc.tools import geteval
from .tools import obj2tex, cr

special_chars = ['#']


def symbol_names(core):
    sn = {}
    for var in [r'x', r'w', r'u', r'y', r'p']:
        for symb in getattr(core, var):
            string = str(symb)
            lab = string[1:]
            sn.update({symb: var+r'_{\mathrm{'+lab+r'}}'})
    return sn


def coredims2tex(core):
    """
    latexize dimensions nx, nx, ny and np
    """
    sm = symbol_names(core)
    str_variables = cr(2)
    str_dimensions += r"\section{System dimensions}"
    for dim in [r'x', r'w', r'y', r'p']:
        val = getattr(core.dims, dim)()
        label = r"n_\mathbf{"+dim+r"}"
        desc = r"$\dim(\mathbf{"+dim+r"})=$"
        str_dimensions += self.obj2tex(val, label, desc, toMatrix=False, sm)
    return str_dimensions


def coresyms2tex(core):
    sm = symbol_names(core)
    str_variables = cr(2)
    str_variables += r"\section{System variables}"
    if core.dims.x() > 0:
        str_variables += obj2tex(core.x, r'\mathbf{x}',
                                 'State variable', sm)
    if core.dims.w() > 0:
        str_variables += obj2tex(core.w, r'\mathbf{w}',
                                 'Dissipation variable', sm)
    if core.dims.y() > 0:
        str_variables += obj2tex(core.u, r'\mathbf{u}',
                                 'Input', sm)
        str_variables += obj2tex(core.y, r'\mathbf{y}',
                                 'Output', sm)
    return str_variables


def coreexprs2tex(core):
    sm = symbol_names(core)
    str_relations = cr(2)
    str_relations += r"\section{Constitutive relations}"
    if core.dims.x() > 0:
        str_relations += obj2tex(core.H, r'\mathtt{H}(\mathbf{x})',
                                 'Hamiltonian', sm,
                                 toMatrix=False)
        str_relations += obj2tex(core.dxH,
                                 r'\nabla \mathtt{H}(\mathbf{x})',
                                 'Hamiltonian gradient', sm)
    if core.dims.w() > 0:
        str_relations += obj2tex(core.z, r'\mathbf{z}(\mathbf{w})',
                                 'Dissipation function', sm)
        str_relations += obj2tex(core.jacz,
                                 r'\mathcal{J}_{\mathbf{z}}(\mathbf{w})',
                                 'Jacobian of dissipation function', sm)
    return str_relations


def corepars2tex(core):
    sm = symbol_names(core)
    str_parameters = ""
    if len(core.subs) > 0:
        str_parameters += cr(2)
        str_parameters += r"\section{System parameters}" + cr(2)
        str_parameters += r"\subsection{Constant}" + cr(1)
        str_parameters += dic2table(['parameter', 'value (SI)'], core.subs)
    if core.dims.p() > 0:
        str_parameters += cr(2)
        str_parameters += r"\subsection{Controled}" + cr(1)
        str_parameters += obj2tex(core.p, r'\mathbf{p}',
                                  'Control parameters', sm)
    return str_parameters


def corestruc2tex(core, which='all'):
    """
    return latex code for system structure matrices.
    """
    str_structure = cr(1)
    str_structure += r"\section{System structure}"
    if which == 'all' or which == 'M':
        str_structure += corestructureM2tex(core)
    if which == 'all' or which == 'J':
        str_structure += corestructureJ2tex(core)
    if which == 'all' or which == 'R':
        str_structure += corestructureR2tex(core)
    return str_structure


def corestrucM2tex(core):
    """
    return latex code for matrix M.
    """
    sm = symbol_names(core)
    str_structure = cr(1)
    str_structure += obj2tex(core.M, r"\mathbf{M}", "", sm)
    if core.dims.x() > 0:
        str_structure += obj2tex(core.Mxx(), r"\mathbf{M_{xx}}", "", sm)
        if core.dims.w() > 0:
            str_structure += obj2tex(core.Mxw(), r"\mathbf{M_{xw}}", "", sm)
        if core.dims.y() > 0:
            str_structure += obj2tex(core.Mxy(), r"\mathbf{M_{xy}}", "", sm)
    if core.dims.w() > 0:
        if core.dims.x() > 0:
            str_structure += obj2tex(core.Mwx(), r"\mathbf{M_{wx}}", "", sm)
        str_structure += obj2tex(core.Mww(), r"\mathbf{M_{ww}}", "", sm)
        if core.dims.y() > 0:
            str_structure += obj2tex(core.Mwy(), r"\mathbf{M_{wy}}", "", sm)
    if core.dims.y() > 0:
        if core.dims.x() > 0:
            str_structure += obj2tex(core.Myx(), r"\mathbf{M_{yx}}", "", sm)
        if core.dims.w() > 0:
            str_structure += obj2tex(core.Myw(), r"\mathbf{M_{yw}}", "", sm)
        str_structure += obj2tex(core.Myy(), r"\mathbf{M_{yy}}", "", sm)
    return str_structure


def corestrucJ2tex(core):
    """
    return latex code for matrix M.
    """
    sm = symbol_names(core)
    str_structure = cr(1)
    str_structure += obj2tex(core.J(), r"\mathbf{J}", "", sm)
    if core.dims.x() > 0:
        str_structure += obj2tex(core.Jxx(), r"\mathbf{J_{xx}}", "", sm)
        if core.dims.w() > 0:
            str_structure += obj2tex(core.Jxw(), r"\mathbf{J_{xw}}", "", sm)
        if core.dims.y() > 0:
            str_structure += obj2tex(core.Jxy(), r"\mathbf{J_{xy}}", "", sm)
    if core.dims.w() > 0:
        str_structure += obj2tex(core.Jww(), r"\mathbf{J_{ww}}", "", sm)
        if core.dims.y() > 0:
            str_structure += obj2tex(core.Jwy(), r"\mathbf{J_{wy}}", "", sm)
    if core.dims.y() > 0:
        str_structure += obj2tex(core.Jyy(), r"\mathbf{J_{yy}}", "", sm)
    return str_structure


def corestrucR2tex(core):
    """
    return latex code for matrix M.
    """
    sm = symbol_names(core)
    str_structure = cr(1)
    str_structure += obj2tex(core.R(), r"\mathbf{R}", "", sm)
    if core.dims.x() > 0:
        str_structure += obj2tex(core.Rxx(), r"\mathbf{R_{xx}}", "", sm)
        if core.dims.w() > 0:
            str_structure += obj2tex(core.Rxw(), r"\mathbf{R_{xw}}", "", sm)
        if core.dims.y() > 0:
            str_structure += obj2tex(core.Rxy(), r"\mathbf{R_{xy}}", "", sm)
    if core.dims.w() > 0:
        str_structure += obj2tex(core.Rww(), r"\mathbf{R_{ww}}", "", sm)
        if core.dims.y() > 0:
            str_structure += obj2tex(core.Rwy(), r"\mathbf{R_{wy}}", "", sm)
    if core.dims.y() > 0:
        str_structure += obj2tex(core.Ryy(), r"\mathbf{R_{yy}}", "", sm)
#        str_J = str_J.replace('begin{matrix}', 'begin{array}{' +
#                              r'c'*self.nx +
#                              r'|' + r'c'*self.nw +
#                              r'|' + r'c'*self.nw + r'}')
#        str_J += str_J.replace('end{matrix}', 'end{array}')
    return str_structure


def netlist2tex(netlist):
    str_netlist = cr(2)
    if netlist.nlines() > 0:
        str_netlist += r"\section{System netlist}" + cr(2)
        str_netlist += r"\begin{center}" + cr(1)
        str_netlist += r"\texttt{" + cr(0)
        str_netlist += r"\begin{tabular}{llllll}" + cr(0)
        str_netlist += r"\hline" + cr(0)
        str_netlist += "line & label & dictionary.component & nodes & \
parameters " + r"\\ \hline" + cr(1)
        l = 0
        for comp in netlist:
            l += 1
            latex_line = r"$\ell_" + str(l) + r"$"
            latex_dic = str(comp['dictionary'])
            latex_comp = str(comp['component'])
            latex_label = str(comp['label'])
            latex_nodes = str(comp['nodes'])
            latex_args = r'$\left\{ ' + dic2array(comp['arguments']) +\
                r'\right.$'
            str_table = r'{} & {} & {}.{} & {} & {}'.format(latex_line,
                                                            latex_label,
                                                            latex_dic,
                                                            latex_comp,
                                                            latex_nodes,
                                                            latex_args)
            str_netlist += str_table + cr(0) + r" \\" + cr(0)
        str_netlist += r"\hline" + cr(0)
        str_netlist += r"\end{tabular}" + cr(1)
        str_netlist += r"}" + cr(1)
    return str_netlist


def graphplot2tex(graph, name=None, path=None):
    """
    associate the plot of the graph to a latex figure
    """
    import os
    from pyphs.config import plot_format
    if name is None:
        if hasattr(graph, 'label'):
            name = graph.label
        else:
            name = 'graph'
    if path is None:
        path = os.getcwd()
    filename = path + os.sep + name + '.' + plot_format
    graph.plot(filename=filename)
    string = cr(2) + r"""\begin{figure}[!h]
\begin{center}
\includegraphics[width=\linewidth]{""" + filename + r"""}
%
\caption{\label{fig:graph""" + name +\
        r"""} Graph of system \texttt{""" + name + r"""}. }
\end{center}
\end{figure}
%"""
    return string



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
\title{""" + title + r"""}}
%
\usepackage{authblk}
\usepackage{hyperref}
%\renewcommand\Authands{ and }
%"""
    return str_preamble + latex_authors + latex_affiliations


def document(self):
    """
    return latex code as plain string for global phs description
    """
    title = r"\title{Structure of the port-Hamiltonian system\\\texttt{" + sys_label + r"}}"
    str_tex = ""
    str_tex += self.preamble()
    str_tex += cr(1) + r"\begin{document}" + cr(1)
    str_tex += r"\maketitle"
    str_tex += self.netlist()
    str_tex += self.dimensions()
    str_tex += self.symbols()
    str_tex += self.expressions()
    str_tex += self.parameters()
    str_tex += self.structure()
    str_tex += cr(1)
    str_tex += r"\end{document}"
    for special_char in special_chars:
        latex_char = "\\" + special_char
        str_tex = str_tex.replace(special_char, latex_char)
    import os
    filename = self.path + os.sep + self.sys_label + r'.tex'
    if not os.path.exists(self.path):
        os.makedirs(self.path)
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
