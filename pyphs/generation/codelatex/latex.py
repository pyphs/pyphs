# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 00:24:35 2016

@author: Falaize
"""
from pyphs.misc.tools import geteval
special_chars = ['#']


class Latex:
    """
    object that generates latex description of PortHamiltonianObject
    """
    def __init__(self, phs):

        self.sys_label = phs.label

        
        self.netlist_dic = phs.graph.netlist

        self.path_figs = phs.paths['figures']
        self.path = phs.paths['tex']

        for dim in list(phs.dims._names) + ['p']:
            obj = getattr(phs.dims, dim)
            setattr(self, 'n'+dim, obj())

        for var in [r'x', r'w', r'u', r'y', r'p', 'subs']:
            obj = getattr(phs.symbs, var)
            setattr(self, var, obj)

        self.symbol_names = {}
        for var in [r'x', r'w', r'u', r'y', r'p']:
            for symb in getattr(self, var):
                string = str(symb)
                lab = string[1:]
                self.symbol_names.update({symb: var+r'_{\mathrm{'+lab+r'}}'})
        for key in self.subs.keys():
            self.symbol_names.update({key: r'\mathrm{'+str(key)+r'}'})

        if self.netlist_dic.nlines() > 0:
            phs.plot_graph()

        if not hasattr(phs.exprs, 'dxH'):
            phs.exprs.build()

        for expr in [r'H', r'z', r'jacz', r'dxH']:
            obj = getattr(phs.exprs, expr)
            setattr(self, expr, obj)

        for mat in ['M', 'J', 'R']:
            M = geteval(phs.struc, mat)
            setattr(self, mat, M)
            for parti in ['x', 'w', 'y']:
                for partj in ['x', 'w', 'y']:
                    obj = geteval(phs.struc, mat+parti+partj)
                    setattr(self, mat+parti+partj, obj)

    def sympy2latex(self, sp_object):
        """
        print latex code from sympy object
        """
        from sympy.printing import latex
        import sympy
        from config import fold_short_frac, mat_delim,\
            mat_str, mul_symbol
        if isinstance(sp_object, sympy.Matrix) and any(el == 0
                                                       for el in
                                                       sp_object.shape):
            return r'\left(\right)'
        else:
            return latex(sp_object, fold_short_frac=fold_short_frac,
                         mat_str=mat_str, mat_delim=mat_delim,
                         mul_symbol=mul_symbol, symbol_names=self.symbol_names)

    def obj2tex(self, obj, label, description, toMatrix=True):
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
            self.sympy2latex(obj) + r" ; $ " + cr(1) + r'\\'
        return str_out

    def export(self):
        """
        return latex code as plain string for global phs description
        """
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

    def preamble(self):
        from config import authors, affiliations
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
\title{Structure of the port-Hamiltonian system\\\texttt{""" + self.sys_label + r"""}}
%
\usepackage{authblk}
\usepackage{hyperref}
%\renewcommand\Authands{ and }
%"""
        return str_preamble + latex_authors + latex_affiliations

    def dimensions(self):
        """
        latexize dimensions nx, nx, ny and np
        """
        str_dimensions = ""
        str_dimensions += r"\section{System dimensions}"
        for dim in [r'x', r'w', r'y', r'p']:
            val = getattr(self, 'n'+dim)
            label = r"n_\mathbf{"+dim+r"}"
            desc = r"$\dim(\mathbf{"+dim+r"})=$"
            str_dimensions += self.obj2tex(val, label, desc, toMatrix=False)
        return str_dimensions

    def graph(self):
        """
        associate the plot of the graph to a latex figure
        """
        import os
        from pyphs.plots.config import plot_format
        fig_name = self.path_figs + os.sep + \
            self.sys_label + '_graph.' + plot_format
        string = r"""%
    %
    \begin{figure}[!h]
    \begin{center}
    \includegraphics[width=\linewidth]{""" + fig_name + r"""}
    %
    \caption{\label{fig:graph_""" + self.sys_label +\
            r"""} Graph of system \texttt{""" + self.sys_label + r"""}. }
    \end{center}
    \end{figure}
    %"""
        return string

    def netlist(self):
        str_netlist = cr(2)
        if self.netlist_dic.nlines()>0:
            str_netlist += r"\section{System netlist}" + cr(2)
            str_netlist += r"\begin{center}" + cr(1)
            str_netlist += r"\texttt{" + cr(0)
            str_netlist += r"\begin{tabular}{llllll}" + cr(0)
            str_netlist += r"\hline" + cr(0)
            str_netlist += "line & label & dictionary.component & nodes & \
    parameters " + r"\\ \hline" + cr(1)
            l = 0
            for comp in self.netlist_dic:
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
            str_netlist += r"\end{center}"+'\n'
            str_netlist += self.graph()
        return str_netlist

    def symbols(self):
        str_variables = cr(2)
        str_variables += r"\section{System variables}"
        if self.nx > 0:
            str_variables += self.obj2tex(self.x, r'\mathbf{x}',
                                          'State variable')
        if self.nw > 0:
            str_variables += self.obj2tex(self.w, r'\mathbf{w}',
                                          'Dissipation variable')
        if self.ny > 0:
            str_variables += self.obj2tex(self.u, r'\mathbf{u}',
                                          'Input')
            str_variables += self.obj2tex(self.y, r'\mathbf{y}',
                                          'Output')
        return str_variables

    def expressions(self):
        str_relations = cr(2)
        str_relations += r"\section{Constitutive relations}"
        if self.nx > 0:
            str_relations += self.obj2tex(self.H, r'\mathtt{H}(\mathbf{x})',
                                          'Hamiltonian',
                                          toMatrix=False)
            str_relations += self.obj2tex(self.dxH,
                                          r'\nabla \mathtt{H}(\mathbf{x})',
                                          'Hamiltonian gradient')
        if self.nw > 0:
            str_relations += self.obj2tex(self.z, r'\mathbf{z}(\mathbf{w})',
                                          'Dissipation function')
            str_relations += self.obj2tex(self.jacz,
                                          r'\mathcal{J}_{\mathbf{z}}(\mathbf{w})',
                                          'Jacobian of dissipation function')
        return str_relations

    def parameters(self):
        str_parameters = ""
        if len(self.subs) > 0:
            str_parameters += cr(2)
            str_parameters += r"\section{System parameters}" + cr(2)
            str_parameters += r"\subsection{Constant}" + cr(1)
            str_parameters += dic2table(['parameter', 'value (SI)'], self.subs)
        if self.np > 0:
            str_parameters += cr(2)
            str_parameters += r"\subsection{Controled}" + cr(1)
            str_parameters += self.obj2tex(self.p, r'\mathbf{p}',
                                           'Control parameters')
        return str_parameters

    def structure(self):
        """
        return latex code for system structure matrices.
        """
        str_structure = cr(1)
        str_structure += r"\section{System structure}" + cr(1)
        str_structure += self.obj2tex(self.M, r"\mathbf{M}", "")
        if self.nx > 0:
            str_structure += self.obj2tex(self.Mxx, r"\mathbf{M_{xx}}", "")
            if self.nw > 0:
                str_structure += self.obj2tex(self.Mxw, r"\mathbf{M_{xw}}", "")
            if self.ny > 0:
                str_structure += self.obj2tex(self.Mxy, r"\mathbf{M_{xy}}", "")
        if self.nw > 0:
            if self.nx > 0:
                str_structure += self.obj2tex(self.Mwx, r"\mathbf{M_{wx}}", "")
            str_structure += self.obj2tex(self.Mww, r"\mathbf{M_{ww}}", "")
            if self.ny > 0:
                str_structure += self.obj2tex(self.Mwy, r"\mathbf{M_{wy}}", "")
        if self.ny > 0:
            if self.nx > 0:
                str_structure += self.obj2tex(self.Myx, r"\mathbf{M_{yx}}", "")
            if self.nw > 0:
                str_structure += self.obj2tex(self.Myw, r"\mathbf{M_{yw}}", "")
            str_structure += self.obj2tex(self.Myy, r"\mathbf{M_{yy}}", "")
        str_structure += self.obj2tex(self.J, r"\mathbf{J}", "")
        if self.nx > 0:
            str_structure += self.obj2tex(self.Jxx, r"\mathbf{J_{xx}}", "")
            if self.nw > 0:
                str_structure += self.obj2tex(self.Jxw, r"\mathbf{J_{xw}}", "")
            if self.ny > 0:
                str_structure += self.obj2tex(self.Jxy, r"\mathbf{J_{xy}}", "")
        if self.nw > 0:
            str_structure += self.obj2tex(self.Jww, r"\mathbf{J_{ww}}", "")
            if self.ny > 0:
                str_structure += self.obj2tex(self.Jwy, r"\mathbf{J_{wy}}", "")
        if self.ny > 0:
            str_structure += self.obj2tex(self.Jyy, r"\mathbf{J_{yy}}", "")
        str_structure += self.obj2tex(self.R, r"\mathbf{R}", "")
        if self.nx > 0:
            str_structure += self.obj2tex(self.Rxx, r"\mathbf{R_{xx}}", "")
            if self.nw > 0:
                str_structure += self.obj2tex(self.Rxw, r"\mathbf{R_{xw}}", "")
            if self.ny > 0:
                str_structure += self.obj2tex(self.Rxy, r"\mathbf{R_{xy}}", "")
        if self.nw > 0:
            str_structure += self.obj2tex(self.Rww, r"\mathbf{R_{ww}}", "")
            if self.ny > 0:
                str_structure += self.obj2tex(self.Rwy, r"\mathbf{R_{wy}}", "")
        if self.ny > 0:
            str_structure += self.obj2tex(self.Ryy, r"\mathbf{R_{yy}}", "")
#        str_J = str_J.replace('begin{matrix}', 'begin{array}{' +
#                              r'c'*self.nx +
#                              r'|' + r'c'*self.nw +
#                              r'|' + r'c'*self.nw + r'}')
#        str_J += str_J.replace('end{matrix}', 'end{array}')
        return str_structure


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


def cr(n):
    """
    Latex cariage return with insertion of n "%"
    """
    assert isinstance(n, int), 'n should be an int, got {0!s}'.format(type(n))
    string = ('\n' + r'%')*n + '\n'
    return string
