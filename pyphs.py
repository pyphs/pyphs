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

@author: Falaize
"""

from symbolics.tools import _assert_expr, _assert_vec, symbols


##########################################################################
# Current version
__version__ = 0.5


class PortHamiltonianObject:
    """ Object oriented sympy (symbolic) representation of a port-Hamiltonian \
system with methods that allow:

    * in-place python simulation,
    * c++ simulation code generation,
    * LaTeX  code generation with system's description.

    Parameters
    -----------

    label : str or 'None'
        System label. If 'None', "dummy_phs" is used (the default is 'None').

    path : str or 'None'
        Path used for export. \
If None, current directory is used (the default is 'None').

    netlist : str or 'None'
        Label of the netlist 'netlist.net' used to construct the \
port-Hamiltonian structure. If 'None', the structure is empty \
(the default is 'None').

    """
    def __init__(self, label=None, path=None):
        # object label
        if label is None:
            label = 'dummy_phs'
        else:
            assert isinstance(label, str), 'label argument should be a str, \
got %s' % type(label)
        self.label = label

        # object path
        from misc.paths import _init_paths
        _init_paths(self, path)

        from symbolics.symbols import Symbols
        setattr(self, 'symbs', Symbols())

        from symbolics.expressions import Expressions
        setattr(self, 'exprs', Expressions())

        from symbolics.structure import Structure
        setattr(self, 'struc', Structure(self))

        from graphs.graph import Graph
        setattr(self, 'graph', Graph())

    def __getitem__(self, n):
        """
        Return data associated to 'n'-th element in structure 'a=J.b'
        """
        if n < self.struc.indx()[1]:
            name = 'x'
            func = 'gradH'
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
        return symb, expr, self.get_structure(n)

    def __add__(phs1, phs2):
        label = phs1.label
        path = phs1.path
        phs = PortHamiltonianObject(label=label, path=path)
        for attr in ['symbs', 'exprs', 'struc', 'graph']:
            sumattrs = getattr(phs1, attr) + getattr(phs2, attr)
            setattr(phs, attr, sumattrs)
        return phs

    def symbols(self, obj):
        return symbols(obj)

    def labels(self):
        labels = list(self.symbs.x) + \
            list(self.symbs.w) + \
            list(self.symbs.y) + \
            +list(self.symbs.cy)
        return tuple(str(el) for el in labels)

    def get_label(self, n):
        return self.labels[n]

    def get_structure(self, n):
        return self.struc.J[n, :]

    def build_exprs(self):
        """
        set attributes 'gradH', 'hessH' and 'jacz'
        """
        self.exprs.build(self.symbs)

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

    def build_simulation(self, fs, sequ=None, seqp=None, language='python',
                         nt=None, x0=None):
        """
        Parameters
        -----------

        fs : float, sample rate

        sequ : iterable of tuples of inputs values

        seqp : iterable of tuples of parameters values

        language : 'c++' or 'python'

        nt : number of time steps (x goes to x[nt+1])
        """
        from simulations.simulation import Simulation
        self.simulation = Simulation(self, fs, sequ=sequ, seqp=seqp,
                                     language=language, nt=nt, x0=x0)

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
        try:
            hasattr(x, '__len__')
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
        try:
            hasattr(w, '__len__')
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
        from symbolics.tools import symbols
        self.connectors += [connectors]
        self.struc.connectors = tuple(list(self.struc.connectors) +
                                      list(connectors))
        self.symbs.cu = tuple(list(self.symbs.cu) +
                              list(symbols(connectors['u'])))
        self.symbs.cy = tuple(list(self.symbs.cy) +
                              list(symbols(connectors['y'])))

    def add_parameters(self, p):
        try:
            hasattr(p, '__len__')
            p = _assert_vec(p)
        except:
            _assert_expr(p)
            p = (p, )
        self.symbs.p = tuple(list(self.symbs.p) + list(p))

#######################################################################

    def writeCppCode(self):
        from utils.phs2cpp import phs2mainfile, phs2cppfile, phs2headerfile
        for fold in ['data', 'cpp']:
            self.folders[fold] = safe_mkdir(self.path, fold)
        phs2cppfile(self)
        phs2headerfile(self)
        phs2mainfile(self)

#######################################################################

    def generator_data(self, var, ind=None, decim=1, postprocess=None,
                       imin=0, imax=None):
        from utils.io import data_generator
        import os
        file_to_read = self.folders['data'] + os.sep + var + '.txt'
        generator = data_generator(file_to_read, ind=None, decim=1,
                                   postprocess=None, imin=0, imax=None)
        return generator

#######################################################################

    def applySubs(self, subs=None):
        """
        apply 'sympy.subs(pHobj.subs)' to every variables, functions and \
        matrices in the object.
        """
        import sympy
        if subs is None:
            subs = {}

        def sublist(subs, lis):
            """
            apply sympy.subs(subs) to each element in lis (subs a dictionary)
            """
            return [sympy.sympify(el).subs(subs) for el in lis]
        self.subs.update(subs)
        for k in self.subs.keys():
            assert isinstance(k, sympy.Symbol)

        self.x = sublist(self.subs, self.x)
        self.w = sublist(self.subs, self.w)
        self.z = sublist(self.subs, self.z)
        self.u = sublist(self.subs, self.u)
        self.y = sublist(self.subs, self.y)
        self.H = sympy.sympify(self.H).subs(self.subs)
        J = self.J.subs(self.subs)
        self.addStructure(J=J)

        # remove parameter from list of modulated parameters
        for symb in self.subs.keys():
            if symb in self.p:
                self.p.pop(self.p.index(symb))

        self.build(print_latex=False)

    def TransferFunction(self, tupin, tupout, nfft=None,
                         filtering=None, limits=None):
        """
        Return frequencies and modulus of transfer function with

            * input s_in = phs.seq_'tupin[0]'['tupin[1]']
            * output s_out = phs.seq_'tupout[0]'['tupout[1]']

        Parameters
        ----------

        tupin, tupout : (var_label, var_index)
            If tuples, pointer to the phs.seq_'var_label'['var_index'].
            If listes, consider as direct time signas.

        fs : float
            Sampling frequency

        nfft : int, optional
            Length of the FFT used, if a zero padded FFT is desired. If None,
            the FFT length is nperseg. Defaults to None.

        filtering : float, optional
            If provided, apply a lowpass filter on sigin and sigout before
            computing fft (the default is None). Then filtering is the cutoff
            frequency as a fraction of the sampling rate (in (0, 0.5)).

        limits : (fmin, fmax), optional
            If provided, truncates the output between fmin and fmax (the
            default is None).

        Return
        ------

        f : list
            frequency point in Hertz.

        TF : list
            Modulus of transfer function.

        """
        fs = self.fs
        from numpy import ceil, log2
        nfft = 2**ceil(log2(fs)) if nfft is None else nfft
        sigin = get_sequence(self, tupin)
        sigout = get_sequence(self, tupout)
        from utils.signal import frequencyresponse
        return frequencyresponse(sigin, sigout, fs, nfft=nfft,
                                 filtering=filtering, limits=limits)

    def plot_graph(self):
        from utils.graphs import ShowGraph
        from pyphs_config import plot_format
        import os
        fold = 'plots'
        self.folders[fold] = safe_mkdir(self.path, fold)
        fig_name = self.folders[fold] + os.sep + self.label + \
            '_graph.' + plot_format
        ShowGraph(self, save=fig_name)

    def print_latex(self):
        """
        Print a latex description of the system in 'phs.folder/phs.label.tex'
        """
        fold = 'tex'
        self.folders[fold] = safe_mkdir(self.path, fold)

        from utils.latex import phs2tex
        str_latex = phs2tex(self)
        file_name = self.label + r".tex"
        import os
        latex_file = open(self.folders['tex'] + os.path.sep + file_name, 'w')
        latex_file.write(str_latex)
        latex_file.close()

    def plot_powerBal(self, nmin=0, nmax=None, plot_properties=None):

        if plot_properties is None:
            plot_properties = {}
        datax = self.numerics.seq_t[nmin: nmax]
        datay = list()
        datay.append(self.numerics.seq_dtE[nmin: nmax])
        Psd = map(lambda x, y: float(x) - float(y),
                  self.numerics.seq_ps[nmin: nmax],
                  self.numerics.seq_pd[nmin: nmax])
        datay.append(Psd)
        from utils.plots import singleplot
        from utils.plots import plotprops
        pp = plotprops(which='single')
        import os
        fold = 'plots'
        self.folders[fold] = safe_mkdir(self.path, fold)

        pp.update({'unitx': 'time $t$ (s)',
                   'unity': r'Power (W)',
                   'labels': [r'$\frac{\mathtt{d} \mathrm{E}}{\mathtt{d} t}$',
                              r'$\mathrm{P_S}-\mathrm{P_D}$'],
                   'filelabel':
                       self.folders['plots']+os.path.sep+'power_balance',
                   'maintitle': r'Power balance',
                   'linestyles': ['-b', '--r'],
                   'linewidth': 3,
                   'loc': 0})
        pp.update(plot_properties)
        singleplot(datax, datay, **pp)

        #######################################################################

    def plot_variables(self, var_list,
                       nmin=0, nmax=None, plot_properties=None):
        """
        Plot each phs.seq_'var'['ind'] in var_list = [(var1, ind1), (...)]
        """
        if plot_properties is None:
            plot_properties = {}
        datax = self.numerics.seq_t[nmin:nmax]
        datay = list()
        labels = list()

        import os
        fold = 'plots'
        self.folders[fold] = safe_mkdir(self.path, fold)
        filelabel = self.folders['plots']+os.path.sep
        for tup in var_list:
            sig = get_sequence(self, tup)
            datay.append(sig[nmin:nmax])
            labels.append(nice_label(tup[0], tup[1]))
            filelabel += '_'+tup[0]+str(tup[1])
        from utils.plots import plotprops
        pp = plotprops(which='multi')
        pp.update({'unitx': 'time $t$ (s)',
                   'unity': labels,
                   'labels': None,
                   'maintitle': None,
                   'filelabel': filelabel,
                   'limits': 'extend',
                   'log': None})
        pp.update(plot_properties)
        from utils.plots import multiplot
        multiplot(datax, datay, **pp)

###############################################################################


def get_sequence(phs, tup):
    if isinstance(tup, list):
        sig = tup
    else:
        if isinstance(tup, tuple):
            var, ind = tup
        else:
            assert isinstance(tup, str), 'Signal label not understood: \
            expected string, got {0!s}'.format(type(tup))
            var, ind = tup, 0
        sig = [e[ind] for e in getattr(phs.numerics, "seq_"+var)]
    return sig


def nice_label(var, ind):
    if var in ('dxHd', 'dxH'):
        return r'$\overline{\nabla}\mathtt{H}_'+str(ind)+r'$'
    elif var == 'dtx':
        return r'$\mathrm D_t \,{x}_'+str(ind)+'$'
    else:
        return r'$'+var+'_'+str(ind)+r'$'


def safe_mkdir(main_folder, new_folder):
    import os
    newpath = main_folder + os.path.sep + new_folder
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath
