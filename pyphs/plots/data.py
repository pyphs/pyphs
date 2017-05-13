# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 13:12:43 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function
from .multiplots import multiplot
from .singleplots import singleplot
from pyphs.latex.tools import nice_label
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
        from pyphs.plots.singleplots import singleplot
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
        from pyphs.plots.multiplots import multiplot
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


def plot(data, var_list, imin=0, imax=None, decim=1, show=True):
    # Absci
    datax = list(data.t(imin=imin, imax=imax, decim=decim))
    datay = list()
    labels = list()
    path = data.config['path'] + os.sep + 'figures'
    if not os.path.exists(path):
        os.makedirs(path)
    filelabel = path + os.sep
    for tup in var_list:
        generator = getattr(data, tup[0])
        sig = [el for el in generator(ind=tup[1], imin=imin,
                                      imax=imax, decim=decim)]
        datay.append(sig)
        labels.append(nice_label(data.core, tup))
        filelabel += '_'+tup[0]+str(tup[1])
    plotopts = {'unitx': 'time $t$ (s)',
                'unity': labels,
                'filelabel': filelabel}
    if len(datay) > 1:
        multiplot(datax, datay, show=show, **plotopts)
    else:
        singleplot(datax, datay, show=show, **plotopts)
