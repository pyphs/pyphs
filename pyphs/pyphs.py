# -*- coding: utf-8 -*-
"""
Copyright or © or Copr. Project-Team S3 (Sound Signals and Systems) and
Analysis/Synthesis team, Laboratory of Sciences and Technologies of Music and
Sound (UMR 9912), IRCAM-CNRS-UPMC, 1 place Igor Stravinsky, F-75004 Paris
contributor(s) : Antoine Falaize, Thomas Hélie, Thu Jul 9 23:11:37 2015
corresponding contributor: antoine.falaize@ircam.fr

This software (pypHs) is a computer program whose purpose is to generate C++
code for the simulation of multiphysics system described by graph structures.
It is composed of a library (pypHs.py) and a dictionnary (Dictionnary.py)

This software is governed by the CeCILL-B license under French law and
abiding by the rules of distribution of free software.  You can  use,
modify and/ or redistribute the software under the terms of the CeCILL-B
license as circulated by CEA, CNRS and INRIA at the following URL
"http://www.cecill.info".

As a counterpart to the access to the source code and  rights to copy,
modify and redistribute granted by the license, users are provided only
with a limited warranty  and the software's author,  the holder of the
economic rights, and the successive licensors  have only  limited liability.

In this respect, the user's attention is drawn to the risks associated
with loading,  using,  modifying and/or developing or reproducing the
software by the user in light of its specific status of free software,
that may mean  that it is complicated to manipulate,  and  that  also
therefore means  that it is reserved for developers  and  experienced
professionals having in-depth computer knowledge. Users are therefore
encouraged to load and test the software's suitability as regards their
requirements in conditions enabling the security of their systems and/or
data to be ensured and,  more generally, to use and operate it in the
same conditions as regards security.

The fact that you are presently reading this means that you have had
knowledge of the CeCILL-B license and that you accept its terms.

Created on Thu Jun  2 21:33:07 2016

@author: Antoine Falaize
"""

###############################################################################


__licence__ = "CEA CNRS Inria Logiciel Libre License, version 2.1 (CeCILL-2.1)"
__author__ = "Antoine Falaize"
__maintainer__ = "Antoine Falaize"
__copyright__ = "Copyright 2012-2016"
__version__ = '0.1.9c3_DEV'
__author_email__ = 'antoine.falaize@gmail.com'


###############################################################################


class PortHamiltonianObject:
    """ Object oriented sympy (symbolic) representation of a port-Hamiltonian \
system with methods that allow:

    * in-place python simulation,
    * c++ simulation-code generation,
    * LaTeX code generation with system's description.

    Parameters
    -----------
    label : str or 'None'
        System label. If 'None', "dummy_phs" is used (the default is 'None').
    path : str or 'None'
        * if path is None, no path is used (default);
        * if path is 'cwd', current working directory is used;
        * if path is 'label', a new folder with phs label is created in \
current working directory;
        * if path is a str, it is used for the system's path.
    """

    ###########################################################################

    def __init__(self, label=None, path=None):
        # object label
        if label is None:
            label = 'dummy_phs'
        else:
            assert isinstance(label, str), 'label argument should be a str, \
got %s' % type(label)
        self.label = label

        # object path
        import paths
        paths._init_paths(self, path)

        # Include the pyphs.symbolics tools
        from symbolics.symbols import Symbols
        setattr(self, 'symbs', Symbols())

        # Include the pyphs.structures.dimensions tools
        from symbolics.structures.dimensions import Dimensions
        setattr(self, 'dims', Dimensions(self))

        # Include the pyphs.structures.indices tools
        from symbolics.structures.indices import Indices
        setattr(self, 'inds', Indices(self))

        # Include the pyphs.structures.indices tools
        from symbolics.structures.structure import Structure
        setattr(self, 'struc', Structure(self))

        # Include the pyphs.expressions tools
        from symbolics.expressions import Expressions
        setattr(self, 'exprs', Expressions(self))

        # Include the pyphs.expressions tools
        from numerics.numeric import Functions
        setattr(self, 'funcs', Functions(self))

        # Include the pyphs.simulation tools
        from simulations.simulation import Simulation
        setattr(self, 'simu', Simulation(self))

        # Include the pyphs.data tools
        from data.data import Data
        setattr(self, 'data', Data(self))

        # Include the pyphs.graphs tools
        from graphs.graph import Graph
        setattr(self, 'graph', Graph())
        
        from misc.signals.synthesis import signalgenerator
        self.signalgenerator = signalgenerator
        
    ###########################################################################

    def __add__(phs1, phs2):
        label = phs1.label
        if hasattr(phs1, 'path'):
            path = phs1.path
        else:
            path = None
        phs = PortHamiltonianObject(label=label, path=path)
        for attr in ['symbs', 'exprs', 'struc', 'graph']:
            sumattrs = getattr(phs1, attr) + getattr(phs2, attr)
            setattr(phs, attr, sumattrs)
        return phs

    ###########################################################################

    def __getitem__(self, n):
        """
        Return 'n'-th element in structure 'a=J.b', ie. a[n], b[n] and J[n,:].
        """
        if n < self.inds.x()[1]:
            name = 'x'
            func = 'dxH'
            deb = self.inds.x()[0]
        elif n < self.inds.w()[1]:
            name = 'w'
            func = 'z'
            deb = self.inds.w()[0]
        elif n < self.inds.y()[1]:
            name = 'y'
            func = 'u'
            deb = self.inds.y()[0]
        else:
            name = 'cy'
            func = 'cu'
            deb = self.inds.cy()[0]
        symb = getattr(self.symbs, name)[n-deb]
        if func in ('u', 'cu'):
            expr = getattr(self.symbs, func)[n-deb]
        else:
            expr = getattr(self.exprs, func)[n-deb]
        mat = self._struc_item(n)
        return symb, expr, mat

    def _struc_item(self, n):
        """
        Return n'th row of structure matrix J
        """
        return self.struc.M[n, :]

    def _getblock(self, indices):
        import sympy
        symbs = tuple()
        exprs = tuple()
        mats = sympy.zeros(0, self.dims.tot())
        for n in indices:
            symb, expr, mat = self.__getitem__(n)
            symbs += (symb, )
            exprs += (expr, )
            mats = sympy.Matrix.vstack(mats, mat)
        return symbs, exprs, mats
    ###########################################################################

    def symbols(self, obj):
        """
        Standard symbols in PyPHS are REAL sympy.Symbol instances.
        """
        from symbolics.tools import symbols
        return symbols(obj)

    ###########################################################################

    def build_from_netlist(self, filename):
        """
        build phs structure from netlist 'filename'
        """
        self.graph.netlist.read(filename)
        self.graph.build_from_netlist(self)
        self.graph._perform_analysis()
        self.graph.analysis.build_phs(self)
        self.apply_connectors()

    ###########################################################################

    def is_nl(self):
        return bool(self.dims.xnl() + self.dims.wnl())

    ###########################################################################

    def apply_subs(self, subs=None):
        """
        replace all instances of key by value for each key:value in self.subs
        """
        if subs is None:
            subs = {}
        subs.update(self.symbs.subs)
        for name in self.symbs._names:
            attr = getattr(self.symbs, name)
            attr = list(attr)
            for i in range(len(attr)):
                try:
                    attr[i] = attr[i].subs(subs)
                except:
                    pass
            setattr(self.symbs, name, attr)
        for name in self.exprs._names:
            attr = getattr(self.exprs, name)
            if hasattr(attr, "__len__"):
                attr = list(attr)
                for i, at in enumerate(attr):
                    try:
                        attr[i] = at.subs(subs)
                    except:
                        pass
            else:
                attr = attr.subs(subs)
            setattr(self.exprs, name, attr)
        self.struc.M = self.struc.M.subs(subs)
        self.symbs.subs = {}

    ###########################################################################

    def add_storages(self, x, H):
        """
        Add a storage component with state x and energy H.
        * State x is append to the current list of states symbols,
        * Expression H is added to the current expression of Hamiltonian.

        Parameters
        ----------

        x : str, symbol, or list of
        H : sympy.Expr
        """
        from symbolics.tools import _assert_expr, _assert_vec
        try:
            hasattr(x, 'index')
            x = _assert_vec(x)
        except:
            _assert_expr(x)
            x = (x, )
        self.symbs.x = self.symbs.x + list(x)
        self.exprs.H += H

    def add_dissipations(self, w, z):
        """
        Add a dissipative component with dissipation variable w and \
dissipation function z.

        Parameters
        ----------

        w : str, symbol, or list of
        z : sympy.Expr or list of
        """
        from symbolics.tools import _assert_expr, _assert_vec
        try:
            hasattr(w, 'index')
            w = _assert_vec(w)
            z = _assert_vec(z)
            assert len(w) == len(z), 'w and z should be have same\
 dimension.'
        except:
            _assert_expr(w)
            _assert_expr(w)
            w = (w, )
            z = (z, )
        self.symbs.w = self.symbs.w + list(w)
        self.exprs.z = self.exprs.z + list(z)

    def add_ports(self, u, y):
        """
        Add one or several ports with input u and output y.

        Parameters
        ----------

        u : str, symbol, or list of
        y : str, symbol, or list of
        """
        from symbolics.tools import _assert_expr, _assert_vec
        if hasattr(u, '__len__'):
            u = _assert_vec(u)
            y = _assert_vec(y)
            assert len(u) == len(y), 'u and y should be have same\
 dimension.'
        else:
            _assert_expr(u)
            _assert_expr(y)
            u = (u, )
            y = (y, )
        self.symbs.u = self.symbs.u + list(u)
        self.symbs.y = self.symbs.y + list(y)

    def add_connectors(self, connectors):
        """
        add a connector (gyrator or transformer)
        """
        self.struc.connectors += [connectors, ]
        self.symbs.cu = list(connectors['u'])
        self.symbs.cy = list(connectors['y'])

    def add_parameters(self, p):
        """
        add a continuously varying parameter
        """
        from symbolics.tools import _assert_expr, _assert_vec
        try:
            hasattr(p, '__len__')
            p = _assert_vec(p)
        except:
            _assert_expr(p)
            p = (p, )
        self.symbs.p = self.symbs.p + list(p)

    ###########################################################################

    def build_resistive_structure(self):
        """
        Build resistsive structure matrix R in PHS structure (J-R) associated \
with the linear dissipative components. Notice the associated \
dissipative variables w are no more accessible.
        """
        from symbolics.structures.tools import reduce_linear_dissipations
        reduce_linear_dissipations(self)

    def split_linear(self):
        """
        Split the system into linear and nonlinear parts.
        """
        from symbolics.structures.tools import split_linear
        split_linear(self)

    ###########################################################################

    def plot_graph(self):
        """
        Plot the graph of the system (networkx.plot method).
        """
        from graphs.tools import plot
        import os
        if not os.path.exists(self.paths['figures']):
            os.makedirs(self.paths['figures'])
        fig_name = self.paths['figures'] + os.sep + self.label + \
            '_graph'
        plot(self.graph, save=fig_name)

    def plot_powerbal(self, mode='single', opts=None):
        """
        Plot the power balance. mode is 'single' or 'multi' for single figure \
or multifigure (default is 'single').
        """
        from plots.phs import plot_powerbal
        plot_powerbal(self, mode=mode, opts=opts)

    def plot_data(self, var_list, imin=0, imax=None):
        """
        Plot each phs.seq_'var'['ind'] in var_list = [(var1, ind1), (...)]
        """
        from plots.multiplots import multiplot
        from generation.codelatex.tools import nice_label
        import os

        datax = [el for el in self.data.t(imin=imin, imax=imax)]
        datay = list()
        labels = list()

        if not os.path.exists(self.paths['figures']):
            os.makedirs(self.paths['figures'])

        filelabel = self.paths['figures']+os.path.sep
        for tup in var_list:
            generator = getattr(self.data, tup[0])
            sig = [el for el in generator(ind=tup[1], imin=imin, imax=imax)]
            datay.append(sig)
            labels.append(nice_label(tup[0], tup[1]))
            filelabel += '_'+tup[0]+str(tup[1])

        plotopts = {'unitx': 'time $t$ (s)',
                    'unity': labels,
                    'filelabel': filelabel}

        multiplot(datax, datay, **plotopts)

    ###########################################################################

    def texwrite(self):
        """
        Export latex description of the system in the folder pointed by \
phs.paths['latex'].
        """
        from generation.codelatex.latex import Latex
        latex = Latex(self)
        latex.export()

    def cppbuild(self):
        """
        Build the module for c++ code generation.
        """
        from generation.codecpp.phs2cpp import CppCode
        import os
        path = self.paths['cpp']
        if not os.path.exists(path):
            os.makedirs(path)
        self.cpp = CppCode(self)

    def cppwrite(self):
        """
        Export system's simulation code (c++) in the folder pointed by \
phs.paths['cpp'].
        """
        self.cpp.gen_main()
        self.cpp.gen_phobj()
        self.cpp.gen_data()

    def wavwrite(self, name, index, fs_in, filename=None, gain=1, fs_out=None):
        """
        write phs.simulation.data.name[index] in the folder pointed by \
phs.paths['wav'].
        """
        from misc.signals.waves import wavwrite
        import os
        if fs_out is None:
            fs_out = fs_in
        if filename is None:
            filename = name
        path = self.path + os.sep + 'wav'
        if not os.path.exists(path):
            os.makedirs(path)
        data = getattr(self.data, name)
        sig = []
        for el in data():
            s = gain*el[index]
            if abs(s) >= 1:
                s = 0.
            sig.append(s)
        wavwrite(sig, fs_in, path + os.sep + filename, fs_out=fs_out)

    ###########################################################################

    def labels(self):
        """
        Return a list of edges labels
        """
        labels = list(self.symbs.x) + \
            list(self.symbs.w) + \
            list(self.symbs.y) + \
            +list(self.symbs.cy)
        return [str(el) for el in labels]

    def get_label(self, n):
        """
        return label of edge n
        """
        return self.labels[n]

    ###########################################################################

    def apply_connectors(phs):
        """
        Effectively connect inputs and outputs defined in phs.connectors.
        """
        import sympy as sp
        nxwy = phs.dims.x() + phs.dims.w() + phs.dims.y()
        switch_list = [connector['alpha'] * sp.Matrix([[0, 1], [-1, 0]])
                       for connector in phs.struc.connectors]
        Mswitch = sp.diag(*switch_list)
        M = phs.struc.M
        G_connectors = sp.Matrix(M[:nxwy, nxwy:])
        J_connectors = G_connectors * Mswitch * G_connectors.T
        M = M[:nxwy, :nxwy] + J_connectors
        phs.struc.M = M
        phs.symbs.cy = []
        phs.symbs.cu =[]
        phs.struc.connectors = []
        