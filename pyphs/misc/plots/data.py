# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 13:12:43 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function
from .multiplots import multiplot
from .singleplots import singleplot
from ..latex.tools import nice_label
import os


def plot_powerbal(data, mode='single', DtE='DxhDtx', imin=0, imax=None,
                  decim=1, show=True):
    """
    Plot the power balance. mode is 'single' or 'multi' for single figure or \
multifigure
    """
    path = data.config['path'] + os.sep + 'figures'
    if not os.path.exists(path):
        os.makedirs(path)
    filelabel = path + os.sep + 'power_balance'
    config = {'figsize': (6., 4.),
              'unitx': r'time $t$ (s)',
              'filelabel': filelabel,
              'maintitle': r'Power balance'}

    labdtE = r'$\frac{\mathtt{d}\mathrm{E}}{\mathtt{d}t}$'
    labPs = r'$\mathrm{P_S}$'
    labPd = r'$\mathrm{P_D}$'

    datax = [el for el in data.t(imin=imin, imax=imax, decim=decim)]

    if mode == 'single':
        datay = list()
        datay.append([el for el in data.dtE(imin=imin, imax=imax,
                                            decim=decim, DtE=DtE)])
        Psd = map(lambda x, y: - float(x) - float(y),
                  data.ps(imin=imin, imax=imax, decim=decim),
                  data.pd(imin=imin, imax=imax, decim=decim))
        datay.append(Psd)
        config.update({'unity': r'Power (W)',
                       'labels': [labdtE, r'$-$('+labPs+r'$+$'+labPd + r')']})
        singleplot(datax, datay, show=show, **config)
    else:
        assert mode == 'multi'
        datay = list()
        datay.append([el for el in data.dtE(imin=imin, imax=imax,
                                            decim=decim, DtE=DtE)])
        datay.append([el for el in data.pd(imin=imin, imax=imax, decim=decim)])
        datay.append([el for el in data.ps(imin=imin, imax=imax, decim=decim)])
        deltaP = [sum(el) for el in zip(data.dtE(imin=imin, imax=imax,
                                                 decim=decim, DtE=DtE),
                                        data.pd(imin=imin,
                                                imax=imax, decim=decim),
                                        data.ps(imin=imin, imax=imax,
                                                decim=decim))]
        datay.append(deltaP)
        config.update({'figsize': (6., 4.),
                       'unity': [r'(W)']*4,
                       'fontsize': 16,
                       'labels': [labdtE,
                                  labPd,
                                  labPs,
                                  labdtE+r'$+$'+labPd+r'$+$'+labPs]})
        multiplot(datax, datay, show=show, **config)


def plot(data, vars, imin=0, imax=None, decim=1, show=True, label=None):
    """
    Plot simulation data

    Parameters
    ----------

    data : Data
        Simulation data.

    vars : list
        List of variables to plot. Elements can be a single string name or a
        tuples of strings (name, index). For each string element, every indices
        of variable name are ploted. For each tuple element, the element index
        of variable name is ploted.

    imin, imax : starting and toping indices

    decim : decimation integer > 0

    show : bool
        Activate matplotlib.pyplot.show().

    label : str
        Plot label.
    """

    if label is None:
        label = data.method.label

    datax = list(data.t(imin=imin, imax=imax, decim=decim))
    datay = list()
    labels = list()

    path = data.config['path'] + os.sep + 'figures'
    if not os.path.exists(path):
        os.makedirs(path)
    filelabel = path + os.sep + label

    def append_sig(name, index):
        generator = getattr(data, name)
        sig = [el for el in generator(ind=index, imin=imin,
                                      imax=imax, decim=decim)]
        datay.append(sig)
        labels.append(nice_label(data.method, (name, index)))
    dimsmap = {'x': 'x',
               'dx': 'x',
               'dtx': 'x',
               'dxH': 'x',
               'w': 'w',
               'z': 'w',
               'u': 'y',
               'y': 'y'
               }
    for var in vars:
        if isinstance(var, (tuple, list)):
            append_sig(*var)
            filelabel += '_'+var[0]+str(var[1])
        elif isinstance(var, str):
            dim = dimsmap[var]
            for i in range(getattr(data.method.dims, dim)()):
                append_sig(var, i)
                filelabel += '_'+var+str(i)
        else:
            raise TypeError('variable {} not understood'.format(var))

    if len(datay) > 1:
        plotopts = {'unitx': 'time $t$ (s)',
                    'unity': labels,
                    'filelabel': filelabel}
        multiplot(datax, datay, show=show, **plotopts)

    else:
        plotopts = {'unitx': 'time $t$ (s)',
                    'unity': labels[0],
                    'filelabel': filelabel}
        singleplot(datax, datay, show=show, **plotopts)
