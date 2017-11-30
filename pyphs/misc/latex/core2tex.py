#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 14:53:41 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

from pyphs.misc.tools import geteval
from .tools import obj2tex, cr, symbol_names
from .latex import dic2table
from .latexcore import LatexCore

def core2tex(core):
    latexcore = LatexCore(core)
    string = coredims2tex(latexcore)
    string += coresyms2tex(latexcore)
    string += coreexprs2tex(latexcore)
    string += corestruc2tex(latexcore)
    return string

def coredims2tex(latexcore):
    """
    latexize dimensions nx, nx, ny and np
    """
    str_dimensions = cr(2)
    str_dimensions += r""""\section{Core dimensions}

The system

"""
    for key in latexcore.dims.keys():
        val = latexcore.dims[key]
        if (len(key) > 1 and key.endswith('l')) or (len(key) > 2 and key.endswith('nl')):
            label = r"n_\mathbf{"+key[0] + '_' + key[1:] +r"}"
            desc = r"$\dim(\mathbf{"+key[0] + '_' + key[1:]+r"})=$"
        else:
            label = r"n_\mathbf{"+key+r"}"
            desc = r"$\dim(\mathbf{"+key+r"})=$"
        str_dimensions += obj2tex(val, label, desc, latexcore.sn,
                                  toMatrix=False)
        str_dimensions += r' \par '
    return str_dimensions

def coresyms2tex(latexcore):
    str_variables = cr(2)
    str_variables += r"""\section{Core quantities}""" + cr(2)
    str_variables += r"\subsection{Core constants}" + cr(1)  + latexcore.subs + cr(1) + r"""

\subsection{Core variables}

The system variables are:
""" + cr(0) + r"""
\begin{itemize}
""" + cr(0) + r"""
\item the \emph{state} $\mathbf x: t\mapsto \mathbf x(t)\in \mathbb R ^{%i}$ associated with the system's energy storage:
""" % latexcore.dims['x'] + cr(0) + r"""
$""" + latexcore.x + r"""$
""" + cr(0) + r"""
\item the \emph{state increment} $\mathbf{d_x}: t\mapsto \mathbf{d_x}(t)\in \mathbb R ^{%i}$ that represents the numerical increment during a single simulation time-step:
""" % latexcore.dims['x'] + cr(0) + r"""
$""" + latexcore.dx + r"""$
""" + cr(0) + r"""
\item the \emph{dissipation variable} $\mathbf w: t\mapsto \mathbf w(t)\in \mathbb R^{%i}$ associated with the system's energy dissipation:
""" % latexcore.dims['w'] + cr(0) + r"""
$""" + latexcore.w + r"""$
""" + cr(0) + r"""
\end{itemize}
""" + cr(0) + r"""

\subsection{Core inputs}

The input (\textit{i.e.} controlled quantities) are:
""" + cr(0) + r"""
\begin{itemize}
""" + cr(0) + r"""
\item the \emph{input variable} $\mathbf u: t\mapsto \mathbf u(t)\in \mathbb R^{%i}$ associated with the system's energy supply (sources):
""" % latexcore.dims['y'] + cr(0) + r"""
$""" + latexcore.u + r"""$
""" + cr(0) + r"""
\item the \emph{parameters} $\mathbf p: t\mapsto \mathbf p(t)\in \mathbb R^{%i}$ associated with variable system parameters:
""" % latexcore.dims['p'] + cr(0) + r"""
$""" + latexcore.p + r"""$
""" + cr(0) + r"""
\end{itemize}
""" + cr(0) + r"""

\subsection{Core outputs}

The output (\textit{i.e.} observed quantities) are:
""" + cr(0) + r"""
\begin{itemize}
""" + cr(0) + r"""
\item the \emph{output variable} ${\mathbf y: t\mapsto \mathbf y(t)\in \mathbb R^{%i}}$ associated with the system's energy supply (sources):
""" % latexcore.dims['y'] + cr(0) + r"""
$""" + latexcore.y + r"""$
""" + cr(0) + r"""
\item the \emph{observer} ${\mathbf o: t\mapsto \mathbf o(t)\in \mathbb R^{%i}}$ associated with functions of the above quantities:
""" % latexcore.dims['o'] + cr(0) + r"""
$""" + latexcore.o + r"""$

\end{itemize}
""" + cr(0)
    if len(latexcore.o_elements) > 0:
        str_variables += r"""
The observed quantities are defined as follows:
"""
        for t in latexcore.o_elements:
            str_variables += r"$" + t + r"""$
""" + cr(1)
    str_variables += r"""
\subsection{Core connectors}

The connected quantities are:
""" + cr(0) + r"""
\begin{itemize}
""" + cr(0) + r"""
\item the \emph{connected inputs} ${\mathbf u_c: t\mapsto \mathbf u_c(t)\in \mathbb R^{%i}}$
""" % latexcore.dims['cy'] + cr(0) + r"""
$""" + latexcore.cu + r"""$
""" + cr(0) + r"""
\item the \emph{connected outputs} ${\mathbf y_c: t\mapsto \mathbf y_c(t)\in \mathbb R^{%i}}$
""" % latexcore.dims['cy'] + cr(0) + r"""
$""" + latexcore.cy + r"""$

\end{itemize}
""" + cr(1)

    return str_variables

def coreexprs2tex(latexcore):
    str_relations = cr(2)
    str_relations += r"""\section{Core constitutive relations}

\subsection{Core storage function}

The system's storage function is:
""" + cr(0) + r"""
$""" + latexcore.H + r"""$
""" + cr(0) + r"""
The gradient of the system's storage function is:
""" + cr(0) + r"""
$""" + latexcore.dxH + r"""$
""" + cr(0)
    if len(latexcore.dxH_elements) > 0:
        str_relations += r"""The elements of the storage function's gradient are given below:
"""
        for t in latexcore.dxH_elements:
            str_relations += r"$" + t + r"""$
    """ + cr(0)
        str_relations += r"""
The Hessian matrix of the storage function is:
""" + cr(0) + """
$""" + latexcore.hessH + r"""$
""" + cr(2)
    str_relations += r"""
The Hessian matrix of the linear part of the storage function is:
""" + cr(0) + """
$""" + latexcore.Q + r"""$
""" + cr(2)
    str_relations += r"""

\subsection{Core dissipation function}

The dissipative function is:
""" + cr(0) + """
$""" + latexcore.z + r"""$
""" + cr(2)
    if len(latexcore.z_elements) > 0:
        str_relations += r"""
The elements of the dissipation function are given below:
"""
        for t in latexcore.z_elements:
            str_relations += r"$" + t + r"""$
""" + cr(1)
        str_relations += r"""
The jacobian matrix of the dissipation function is:
""" + cr(1) + """
$""" + latexcore.jacz + r"""$
""" + cr(2)
        str_relations += r"""
The jacobian matrix of the linear part of the dissipation function is:
""" + cr(0) + """
$""" + latexcore.Zl + r"""$
""" + cr(2)
    return str_relations


def corestruc2tex(latexcore, which='all'):
    """
    return latex code for system structure matrices.
    """
    str_structure = cr(1)
    str_structure = r"""
\section{Core structure}

""" + latexcore.phs + cr(1) + latexcore.matrices + cr(1)

    for name in 'MJR':
        str_structure += r"""\subsection{Core %s-structure}""" % name + cr(1)
        str_structure += r'$' + getattr(latexcore, name) + r'$' + cr(1)
        for i in ['x', 'w', 'y', 'cy']:
            for j in ['x', 'w', 'y', 'cy']:
                key = name + i + j
                t = getattr(latexcore, key)
                str_structure += r'$' + t + r'$' + cr(1)

    return str_structure
