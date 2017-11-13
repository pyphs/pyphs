#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 10:33:44 2017

@author: afalaize
"""

from pyphs.misc.latex.tools import obj2tex, symbol_names, sympy2latex
from pyphs.misc.latex.latex import dic2table


from pyphs.misc.tools import geteval

matrices = r"""
$$
\underbrace{\left(
\begin{array}{lll}
\mathbf{M_{xx}} & \mathbf{M_{xw}} & \mathbf{M_{xy}} \\
\mathbf{M_{wx}} & \mathbf{M_{ww}} & \mathbf{M_{wy}} \\
\mathbf{M_{yx}} & \mathbf{M_{yw}} &  \mathbf{M_{yy}} \\
\end{array}
\right)}_{\mathbf M}
=
\underbrace{\left(
\begin{array}{lll}
\mathbf{J_{xx}} & \mathbf{J_{xw}} & \mathbf{J_{xy}} \\
-^\intercal\mathbf{J_{xw}} & \mathbf{J_{ww}} & \mathbf{J_{wy}} \\
-^\intercal\mathbf{J_{xy}} & -^\intercal\mathbf{J_{wy}} &  \mathbf{J_{yy}} \\
\end{array}
\right)}_{\mathbf J}
-
\underbrace{\left(
\begin{array}{lll}
\mathbf{R_{xx}} & \mathbf{R_{xw}} & \mathbf{R_{xy}} \\
^\intercal\mathbf{R_{xw}} & \mathbf{R_{ww}} & \mathbf{R_{wy}} \\
^\intercal\mathbf{R_{xy}} & ^\intercal\mathbf{R_{wy}} &  \mathbf{R_{yy}} \\
\end{array}
\right)}_{\mathbf R}
$$
"""

core_tex = r"""
$$
\left(
\begin{array}{c}
\frac{\mathrm d\, \mathbf x}{\mathrm d t} \\
\mathbf w \\
\mathbf y \\
\end{array}
\right)
=
\left(
\begin{array}{lll}
\mathbf{M_{xx}} & \mathbf{M_{xw}} & \mathbf{M_{xy}} \\
\mathbf{M_{wx}} & \mathbf{M_{ww}} & \mathbf{M_{wy}} \\
\mathbf{M_{yx}} & \mathbf{M_{yw}} &  \mathbf{M_{yy}} \\
\end{array}
\right)
\cdot
\left(
\begin{array}{c}
\\nnabla \mathrm H\\
\mathbf z \\
\mathbf u \\
\end{array}
\right)
$$
""".replace(r'\n', '')


class LatexCore(object):

    phs = core_tex
    matrices = matrices

    def __init__(self, core):

        self.dims = {}
        for name in ['', 'x', 'w', 'y', 'p', 'o', 'cy']:
            for dim in ['', 'l', 'nl']:
                key = name+dim
                try:
                    self.dims[key] = geteval(core.dims, key)
                except AttributeError:
                    pass

        self.core = core
        self.sn = symbol_names(core)

        self.x = obj2tex(self.core.x, r'\mathbf{x}', '', self.sn)

        self.dx = obj2tex(self.core.dx(), r'\mathbf{d_x}', '', self.sn)

        self.H = obj2tex(self.core.H, r'\mathrm H(\mathbf{x})', '', self.sn,
                         toMatrix=False)

        self.dxH = obj2tex(self.core.g(), r'\nabla\mathrm H(\mathbf{x})',
                           '', self.sn)

        self.dxH_elements = list(map(lambda a: obj2tex(a[0], sympy2latex(a[1], self.sn),
                                                     '', self.sn, toMatrix=False),
                                   zip(core.dxH(), self.core.g())))

        self.Q = obj2tex(self.core.Q, r'\mathbf{Q}',
                         '', self.sn)

        self.Zl = obj2tex(self.core.Zl, r'\mathbf{Z_l}',
                          '', self.sn)

        self.w = obj2tex(self.core.w, r'\mathbf{w}', '', self.sn)

        self.z = obj2tex(core.z_symbols(),
                         r'\mathbf z(\mathbf{w})', '', self.sn)

        self.z_elements = list(map(lambda a: obj2tex(a[0], sympy2latex(a[1], self.sn),
                                                     '', self.sn, toMatrix=False),
                                   zip(core.z, core.z_symbols())))

        self.u = obj2tex(self.core.u, r'\mathbf{u}', '', self.sn)

        self.y = obj2tex(self.core.y, r'\mathbf y', '', self.sn)
        self.cy = obj2tex(self.core.cy, r'\mathbf y_c', '', self.sn)
        self.cu = obj2tex(self.core.cu, r'\mathbf u_c', '', self.sn)

        self.y_elements = list(map(lambda a: obj2tex(a[0], sympy2latex(a[1], self.sn),
                                                     '', self.sn, toMatrix=False),
                                   zip(core.output(), core.y)))

        self.o = obj2tex(self.core.o(), r'\mathbf o', '', self.sn)

        self.o_elements = list(map(lambda a: obj2tex(a[0], sympy2latex(a[1], self.sn),
                                                     '', self.sn, toMatrix=False),
                                   zip(core.observers.values(),
                                       core.observers.keys())))

        self.p = obj2tex(self.core.p, r'\mathbf p', '', self.sn)

        for mat in 'MJR':
            M = obj2tex(geteval(core, mat), r'\mathbf{%s}' % mat,
                        '', self.sn)
            setattr(self, mat, M)

            for i in ['x', 'w', 'y', 'cy']:
                for j in ['x', 'w', 'y', 'cy']:
                    M = obj2tex(geteval(core, mat + i + j),
                                r'\mathbf{' + mat + '_{' + i + j + '}}',
                        '', self.sn)
                    setattr(self, mat + i + j, M)

        self.subs = dic2table(['parameter', 'value (SI)'], core.subs, self.sn,
                              centering=True)

        self.jacz = obj2tex(self.core.jacz(), r'\mathcal J_{\mathbf z}(\mathbf w)', '', self.sn)
        self.hessH = obj2tex(self.core.hessH(), r'\triangle\mathrm H(\mathbf x)', '', self.sn)

if __name__ == '__main__':
    from pyphs.examples.rlc.rlc import core
    l = LatexCore(core)
