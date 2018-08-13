# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 19:28:12 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

from pyphs.misc.plots.tools import (annotate, whichplot, standard)
import numpy


def singleplot(x, y, show=True, **kwargs):
    """
    Plot multiple y-axis and possible multiple curves in each. Result is saved\
 as a '.png' document.

    Parameters
    ----------

    x : list of numerics
        x-axis values.

    y : list of lists of numerics
        y-axis values for each curves curve.

    labels : list, optional
        list of curve labels (the default is None). The number of labels must
        be a divisor of the number of plots.

    xlabel : str, optional
        x-axis label (the default is None).

    ylabel : str, optional
        y-axis label (the default is None).

    path : str, optional
        Figure is saved in 'path.ext' if provided (the default is None). See
        'format' agument for extension.

    format : str, optional
        Extension in {'pdf', 'png'} for figure export. If not given, the
        extension from pyphs.config.py is used.

    loc : int or string or pair of floats, default: 0
        The location of the legend. Possible codes are:

            ===============   =============
            Location String   Location Code
            ===============   =============
            'best'            0
            'upper right'     1
            'upper left'      2
            'lower left'      3
            'lower right'     4
            'right'           5
            'center left'     6
            'center right'    7
            'lower center'    8
            'upper center'    9
            'center'          10
            ===============   =============

    log : str, optional
        Log-scale activation according to
            ===============   =============
            Plot type          Code
            ===============   =============
            'plot'            ''
            'semilogx'        'x'
            'semilogy'        'y'
            'loglog'          'xy'
            ===============   =============

    linestyles : iterable, otpional
        List of line styles; the default is ('-b', '--r', ':g', '-.m').

    title : str, optional
        Figure main title. If set to None, the desactivated (the default is \
None).

    grid = bool
        Indicate whether to show the grid or not (the default is False)
    """
    opts = standard.copy()
    opts['ylabel'] = opts.pop('ylabels')
    opts.update(kwargs)

    try:
        if (isinstance(y[0], (float, int)) or
           (isinstance(y[0], numpy.ndarray) and
           len(y[0].shape) == 0)):

            y = [y]
    except IndexError:
        pass

    nplots = int(y.__len__())

    if opts['labels'] is None:
        opts['labels'] = [None, ]*nplots
    elif len(opts['labels']) != nplots:
        nlabels = len(opts['labels'])
        if nplots % nlabels == 0:
            N = nplots - nlabels
            opts['labels'] = list(opts['labels']) + [None, ]*N

    if opts['log'] is None:
        opts['log'] = ''

    from matplotlib.pyplot import figure, fignum_exists
    i = 1
    while fignum_exists(i):
        i += 1

    fig = figure(i)

    from matplotlib.pyplot import axes

    ax = axes()
    ax.ticklabel_format(style='sci', scilimits=(-2, 2))

    print_legend = False

    for n, yn in enumerate(y):
        if len(yn) == 0:
            print('Skipping empty array: ', opts['labels'][n])
            continue

        if isinstance(opts['labels'][n], (list, tuple)):
            annotate(*opts['labels'][n], ax=ax)
            l = None
        else:
            l = opts['labels'][n]
        print_legend = l is not None or print_legend

        plot = whichplot(opts['log'], ax)
        if opts['linestyles'] is not None:
            plot(x, yn, opts['linestyles'][n], label=l)
        else:
            plot(x, yn, label=l)

    if print_legend:
        from matplotlib.pyplot import legend
        legend(loc=opts['loc'])

    if opts['xlabel'] is not None:
        from matplotlib.pyplot import xlabel
        xlabel(opts['xlabel'])

    if opts['ylabel'] is not None:
        from matplotlib.pyplot import ylabel
        ylabel(opts['ylabel'])

    if opts['title'] is not None:
        from matplotlib.pyplot import title
        title(opts['title'])

    # Show grid
    ax.grid(opts['grid'])
    ax.minorticks_on()

    if opts['path'] is not None:
        from matplotlib.pyplot import savefig
        savefig(opts['path'] + '.' + opts['format'])

    if show:
        from matplotlib.pyplot import show as pltshow
        pltshow()

    return fig, ax
