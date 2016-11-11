# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 13:12:43 2016

@author: Falaize
"""


def plot_powerbal(phs, mode='single', opts=None):
    """
    Plot the power balance. mode is 'single' or 'multi' for single figure or \
multifigure
    """
    import os
    if not os.path.exists(phs.paths['figures']):
        os.makedirs(phs.paths['figures'])
    filelabel = phs.paths['figures'] + os.sep+'power_balance'
    conf = {'figsize': (6., 4.),
            'fontsize': 20,
            'axedef': (0.13, 0.1, 0.95, 0.9, 0.2, 0.3),
            'unitx': r'time $t$ (s)',
            'filelabel': filelabel,
            'loc': 0,
            'minor': False,
            'maintitle': r'Power balance'}
    if opts is not None:
        conf.update(opts)
    opts = conf

    labdtE = r'$\frac{\mathtt{d}\mathrm{E}}{\mathtt{d}t}$'
    labPs = r'$\mathrm{P_S}$'
    labPd = r'$\mathrm{P_D}$'

    datax = [el for el in phs.data.t()]

    if mode == 'single':
        from pyphs.plots.singleplots import singleplot
        datay = list()
        datay.append([el for el in phs.data.dtE()])
        Psd = map(lambda x, y: - float(x) - float(y),
                  phs.data.ps(),
                  phs.data.pd())
        datay.append(Psd)
        opts.update({'unity': r'Power (W)',
                     'labels': [labdtE, r'$-$('+labPs+r'$+$'+labPd + r')']})
        singleplot(datax, datay, **opts)
    else:
        assert mode == 'multi'
        from pyphs.plots.multiplots import multiplot
        datay = list()
        datay.append([el for el in phs.data.dtE()])
        datay.append([el for el in phs.data.pd()])
        datay.append([el for el in phs.data.ps()])
        deltaP = map(lambda dte, d, s: float(dte) + float(d) + float(s),
                     phs.data.dtE(),
                     phs.data.pd(),
                     phs.data.ps())
        datay.append(deltaP)
        opts.update({'figsize': (6., 4.),
                     'unity': [r'(W)']*4,
                     'fontsize': 16,
                     'labels': [labdtE,
                                labPd,
                                labPs,
                                labdtE+r'$+$'+labPd+r'$+$'+labPs]})
        multiplot(datax, datay, **opts)
