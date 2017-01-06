# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 19:28:12 2016

@author: Falaize
"""
from pyphs.plots.tools import (activate_latex, annotate, whichplot,
                               setlims, setticks, dec, standard)
from .fonts import globalfonts


def singleplot(datax, datay, **kwargs):
    """
    Plot multiple y-axis and possible multiple curves in each. Result is saved\
 as a '.png' document.

    Parameters
    ----------

    datax : list of numerics
        x-axis values.

    datay : list of lists of numerics
        y-axis values for each curves curve.

    labels : list, optional
        list of curve labels (the default is None).

    unitx : str, optional
        x-axis label (the default is None).

    unity : list of str, optional
        y-axis labels (the default is None).

    ylims : tuple of float, optional
        (ymin, ymax) values. If None then (ymin, ymax) is set automatically \
(the default is None).
        If extend the y-axis is extended by 5% on both sides (the default is \
'extend').

    linewidth : float, optional
        The default is 2.

    figsize : tuple of float, optional
        The default is (5., 5.).

    filelabel : str, optional
        Figure is saved in 'filelabel.png' (the default is 'multiplot').

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

    fontsize : int, optional
        the default is figsize[0]*4.

    legendfontsize : int, optional
        Figure legend font size. If None then set to 4/5 of fontsize (the \
default is None).

    maintitle : str, optional
        Figure main title. If set to None, the desactivated (the default is \
None).

    axedef : tuple of floats, optional
        Figure geometry (left, botom, right, top).
        The default is (.15, .15, .85, .85).

    nbinsx, nbinsy : int, optional
        number of x-axis and y-axis ticks (the default is 4).

    minor : bool
        Activate the minor grid.

    markersize : float
        Default is 6.

    markeredgewidth : float
        Width of line around markers (the default is 0.5).

    """
    opts = standard.copy()
    opts.update(kwargs)
    if opts['axedef'] is None:
        opts['axedef'] = [.15, .15, .75, .75]
    if opts['linestyles'] is None:
        opts['linestyles'] = ['-b', '--r', '-.g', ':m']
    nplots = int(datay.__len__())
    if opts['fontsize'] is None:
        opts['fontsize'] = int(4*opts['figsize'][0])
    if opts['legendfontsize'] is None:
        opts['legendfontsize'] = int(0.8*opts['fontsize'])
    if opts['labels'] is None:
        opts['labels'] = [None, ]*nplots
    if opts['log'] is None:
        opts['log'] = ''

    activate_latex(opts)

    from matplotlib.pyplot import rc
    rc('font', size=opts['fontsize'], **globalfonts())

    from matplotlib.pyplot import close
    close('all')

    from matplotlib.pyplot import figure
    fig = figure(1, figsize=opts['figsize'])
    nplots = datay.__len__()

    if isinstance(datax[0], (float, int)):
        datax = [datax, ]*nplots

    from matplotlib.pyplot import axes
    if opts['axedef'] is not None:
        geometry = opts['axedef'][:4]
    else:
        geometry = None
    ax = axes(geometry)

    miny = float('Inf')
    maxy = -float('Inf')

    for n in range(nplots):

        x = dec(datax[n], opts)
        y = dec(datay[n], opts)
        maxy = max([maxy, max(y)])
        miny = min([miny, min(y)])

        if isinstance(opts['labels'][n], (list, tuple)):
            annotate(x, y, opts['labels'][n][0], opts['labels'][n][1],
                     opts['legendfontsize'])
            l = None
        else:
            l = opts['labels'][n]

        plotn = whichplot(opts['log'], ax)
        plotn(x, y, opts['linestyles'][n], linewidth=opts['linewidth'],
              markeredgewidth=opts['markeredgewidth'],
              markersize=opts['markersize'], label=l)

    setlims(ax, x, miny, maxy, opts['ylims'])
    setticks(ax, opts)

    from matplotlib.pyplot import legend
    legend(loc=opts['loc'], fontsize=opts['legendfontsize'])

    if opts['unitx'] is not None:
        from matplotlib.pyplot import xlabel
        xlabel(opts['unitx'])

    if opts['unity'] is not None:
        from matplotlib.pyplot import ylabel
        ylabel(opts['unity'])

    if opts['maintitle'] is not None:
        from matplotlib.pyplot import title
        title(opts['maintitle'])

    if opts['axedef'] is None:
        fig.tight_layout()

    if opts['filelabel'] is not None:
        from matplotlib.pyplot import savefig
        savefig(opts['filelabel'] + '.' + opts['format'])

    from matplotlib.pyplot import show
    show()
