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

import datetime
__copyright__ = "Copyright 2012-" + str(datetime.date.today().year)
__author__ = "Antoine Falaize"
__licence__ = "CeCILL-B"
__version__ = "0.1.5"
__maintainer__ = "Antoine Falaize"

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
        Path used for export. If None, current directory is \
used (the default is 'None').
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
        from attributes import paths
        paths._init_paths(self, path)

        from symbolics.symbols import Symbols
        setattr(self, 'symbs', Symbols())

        from symbolics.expressions import Expressions
        setattr(self, 'exprs', Expressions())

        from symbolics.structures.structure import Structure
        setattr(self, 'struc', Structure(self))

        from graphs.graph import Graph
        setattr(self, 'graph', Graph())

    ###########################################################################

    def __getitem__(self, n):
        """
        Return 'n'-th element in structure 'a=J.b', ie. a[n], b[n] and J[n,:].
        """
        if n < self.struc.indx()[1]:
            name = 'x'
            func = 'dxH'
        elif n < self.struc.indw()[1]:
            name = 'w'
            func = 'z'
        elif n < self.struc.indy()[1]:
            name = 'y'
            func = 'u'
        else:
            name = 'cy'
            func = 'cu'
        symb = getattr(self.symbs, name)
        if func in ('u', 'cu'):
            expr = getattr(self.symbs, func)
        else:
            expr = getattr(self.exprs, func)
        return symb, expr, self._struc_item(n)

    def _struc_item(self, n):
        """
        Return n'th row of structure matrix J
        """
        return self.struc.J[n, :]

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

    def __add__(phs1, phs2):
        label = phs1.label
        path = phs1.path
        phs = PortHamiltonianObject(label=label, path=path)
        for attr in ['symbs', 'exprs', 'struc', 'graph']:
            sumattrs = getattr(phs1, attr) + getattr(phs2, attr)
            setattr(phs, attr, sumattrs)
        return phs

    ###########################################################################

    def symbols(self, obj):
        """
        Standard symbols in pyphs are REAL sympy.Symbol instances.
        """
        from symbolics.tools import symbols
        return symbols(obj)

    ###########################################################################

    def build_exprs(self):
        """
        set attributes 'dxH', 'hessH' and 'jacz'
        """
        self.exprs.build(self)

    def build_nums(self):
        """
        set module for numerical evaluations
        """
        from numerics.numeric import Numeric
        setattr(self, 'nums', Numeric(self))

    def build_from_netlist(self, filename):
        """
        read and stor data from netlist 'filename'
        """
        self.graph.netlist.read(filename)
        self.graph.build_from_netlist(self)
        self.graph._perform_analysis()
        self.graph.analysis.build_phs(self)

    def build_simulation(self, config=None, sequ=None, seqp=None,
                         nt=None, x0=None):
        """
        Parameters
        -----------

        config : dic of configuraiton options, including sample rate 'fs' and\
'language' ('c++' or 'python').

        sequ : iterable of tuples of inputs values.

        seqp : iterable of tuples of parameters values.

        nt : number of time steps (x goes to x[nt+1]).
        """
        from simulations.simulation import Simulation
        self.simulation = Simulation(self, config=config, sequ=sequ, seqp=seqp,
                                     nt=nt, x0=x0)

    def run_simulation(self):
        """
        run the simulation. to set parameters (inputs, sampling rate, etc.), \
refer to function 'buil_simulation' of your 'PortHamiltonianObject'
        """
        self.simulation.process()

    def apply_subs(self, subs=None):
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
                for i in range(len(attr)):
                    try:
                        attr[i] = attr[i].subs(subs)
                    except:
                        pass
            else:
                attr = attr.subs(subs)
            setattr(self.exprs, name, attr)
        self.struc.J = self.struc.J.subs(subs)

    def apply_connectors(phs):
        """
        Effectively connect inputs and outputs defined in phs.connectors.
        """
        import sympy as sp
        J = phs.J
        nxwy = phs.nx() + phs.nw() + phs.ny()
        switch_list = [connector['alpha'] * sp.Matrix([[0, 1], [-1, 0]])
                       for connector in phs.connectors]
        Mswitch = sp.diag(*switch_list)
        G_connectors = sp.Matrix(J[:nxwy, nxwy:])
        J_connectors = G_connectors * Mswitch * G_connectors.T
        J = J[:nxwy, :nxwy] + J_connectors
        phs.addStructure(J=J)

    def add_storages(self, x, H):
        """
        Add a storage component with state x and energy H.

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
        self.symbs.x = tuple(list(self.symbs.x) + list(x))
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
        self.symbs.w = tuple(list(self.symbs.w) + list(w))
        self.exprs.z = tuple(list(self.exprs.z) + list(z))

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
        self.symbs.u = tuple(list(self.symbs.u) + list(u))
        self.symbs.y = tuple(list(self.symbs.y) + list(y))

    def add_connectors(self, connectors):
        """
        add a connector (gyrator or transformer)
        """
        self.connectors += [connectors]
        self.struc.connectors = tuple(list(self.struc.connectors) +
                                      list(connectors))
        self.symbs.cu = tuple(list(self.symbs.cu) +
                              list(connectors['u']))
        self.symbs.cy = tuple(list(self.symbs.cy) +
                              list(connectors['y']))

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
        self.symbs.p = tuple(list(self.symbs.p) + list(p))

#######################################################################

    def plot_graph(self):
        """
        Plot the graph of the system (networkx.plot method).
        """
        from utils.graphs import ShowGraph
        from pyphs_config import plot_format
        import os
        self.paths['plots'] = self.path + os.sep + 'plots'
        if not os.path.exists(self.paths['plots']):
            os.makedirs(self.paths['plots'])
        fig_name = self.paths['plots'] + os.sep + self.label + \
            '_graph.' + plot_format
        ShowGraph(self, save=fig_name)

    def plot_powerBal(self, plot_properties=None,
                      imin=0, imax=None):
        """
        Plot the power balance between imin and imax
        """
        from plots.plots import singleplot, plotprops
        import os
        if plot_properties is None:
            plot_properties = {}
        datax = [el for el in self.simulation.data.t(imin=imin, imax=imax)]
        datay = list()
        datay.append([el for el in self.simulation.data.dtE(imin=imin,
                                                            imax=imax)])
        Psd = map(lambda x, y: float(x) - float(y),
                  self.simulation.data.ps(imin=imin,
                                          imax=imax),
                  self.simulation.data.pd(imin=imin,
                                          imax=imax))
        datay.append(Psd)
        if not os.path.exists(self.paths['figures']):
            os.makedirs(self.paths['figures'])
        pp = plotprops(which='single')
        pp.update({'unitx': 'time $t$ (s)',
                   'unity': r'Power (W)',
                   'labels': [r'$\frac{\mathtt{d} \mathrm{E}}{\mathtt{d} t}$',
                              r'$\mathrm{P_S}-\mathrm{P_D}$'],
                   'filelabel':
                       self.paths['figures']+os.path.sep+'power_balance',
                   'maintitle': r'Power balance',
                   'linestyles': ['-b', '--r'],
                   'linewidth': 3,
                   'loc': 0})
        pp.update(plot_properties)
        singleplot(datax, datay, **pp)

        #######################################################################

    def plot_variables(self, var_list,
                       imin=0, imax=None, plot_properties=None):
        """
        Plot each phs.seq_'var'['ind'] in var_list = [(var1, ind1), (...)]
        """
        from plots.plots import multiplot, plotprops
        import os
        if plot_properties is None:
            plot_properties = {}
        datax = [el for el in self.simulation.data.t(imin=imin, imax=imax)]
        datay = list()
        labels = list()

        if not os.path.exists(self.paths['figures']):
            os.makedirs(self.paths['figures'])
        filelabel = self.paths['figures']+os.path.sep
        for tup in var_list:
            generator = getattr(self.simulation.data, tup[0])
            sig = [el for el in generator(ind=tup[1], imin=imin, imax=imax)]
            datay.append(sig)
            labels.append(nice_label(tup[0], tup[1]))
            filelabel += '_'+tup[0]+str(tup[1])
        pp = plotprops(which='multi')

        pp.update({'unitx': 'time $t$ (s)',
                   'unity': labels,
                   'labels': None,
                   'maintitle': None,
                   'filelabel': filelabel,
                   'limits': 'extend',
                   'log': None})
        pp.update(plot_properties)
        multiplot(datax, datay, **pp)

###############################################################################


def nice_label(var, ind):
    if var in ('dxHd', 'dxH'):
        return r'$\overline{\nabla}\mathtt{H}_'+str(ind)+r'$'
    elif var == 'dtx':
        return r'$\mathrm D_t \,{x}_'+str(ind)+'$'
    else:
        return r'$'+var+'_'+str(ind)+r'$'
