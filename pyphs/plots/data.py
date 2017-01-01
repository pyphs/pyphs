# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 13:12:43 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function
from .multiplots import multiplot
from pyphs.latex.tools import nice_label
from pyphs.misc.tools import geteval
import os


def plot_powerbal(data, mode='single', opts=None):
    """
    Plot the power balance. mode is 'single' or 'multi' for single figure or \
multifigure
    """
    path = data.config['path'] + os.sep + 'figures'
    if not os.path.exists(path):
        os.makedirs(path)
    filelabel = path + os.sep + 'power_balance'
    conf = {'figsize': (6., 4.),
            'unitx': r'time $t$ (s)',
            'filelabel': filelabel,
            'maintitle': r'Power balance'}
    if opts is not None:
        conf.update(opts)
    opts = conf

    labdtE = r'$\frac{\mathtt{d}\mathrm{E}}{\mathtt{d}t}$'
    labPs = r'$\mathrm{P_S}$'
    labPd = r'$\mathrm{P_D}$'

    datax = [el for el in data.t()]

    if mode == 'single':
        from pyphs.plots.singleplots import singleplot
        datay = list()
        datay.append([el for el in data.dtE()])
        Psd = map(lambda x, y: - float(x) - float(y),
                  data.ps(),
                  data.pd())
        datay.append(Psd)
        opts.update({'unity': r'Power (W)',
                     'labels': [labdtE, r'$-$('+labPs+r'$+$'+labPd + r')']})
        singleplot(datax, datay, **opts)
    else:
        assert mode == 'multi'
        from pyphs.plots.multiplots import multiplot
        datay = list()
        datay.append([el for el in data.dtE()])
        datay.append([el for el in data.pd()])
        datay.append([el for el in data.ps()])
        deltaP = [sum(el) for el in zip(data.dtE(), data.pd(), data.ps())]
        datay.append(deltaP)
        opts.update({'figsize': (6., 4.),
                     'unity': [r'(W)']*4,
                     'fontsize': 16,
                     'labels': [labdtE,
                                labPd,
                                labPs,
                                labdtE+r'$+$'+labPd+r'$+$'+labPs]})
        multiplot(datax, datay, **opts)

def plot(data, var_list, imin=0, imax=None):
    datax = [el for el in data.t(imin=imin, imax=imax)]
    datay = list()
    labels = list()
    path = data.config['path'] + os.sep + 'figures'
    if not os.path.exists(path):
        os.makedirs(path)
    filelabel = path + os.sep
    for tup in var_list:
        generator = getattr(data, tup[0])
        sig = [el for el in generator(ind=tup[1], imin=imin, imax=imax)]
        datay.append(sig)
        labels.append(nice_label(data.core, tup))
        filelabel += '_'+tup[0]+str(tup[1])
    plotopts = {'unitx': 'time $t$ (s)',
                'unity': labels,
                'filelabel': filelabel}
    multiplot(datax, datay, **plotopts)
