# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 20:06:50 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

from .tools import activate_latex, annotate, whichplot, setlims, \
    setticks, dec, standard
from .fonts import globalfonts


def multiplot(datax, datay, **kwargs):
    """
    Plot multiple y-axis and possible multiple curves in each. Result is saved\
 as a '.png' document.

    Parameters
    ----------

    datax : list of floats
        x-axis values.

    datay : list of floats or list of tuples of list of floats
        y-axis values per axis and per curve in each axis, if tuple.

    labels : list, optional
        list of or tupple of list of curve labels (the default is None).

    unitx : str, optional
        x-axis label (the default is None).

    unity : list of str, optional
        y-axis labels per axis (the default is None).

    limits= : list of tuples, optional
        List of (ymin, ymax) values. If None then (ymin, ymax) is set \
automatically.
        If 'extend', the y-axis is extend by 5% on both ends (the default is \
'extend').

    linewidth : float, optional
        The default is 2.

    figsize : tuple of float, optional
        The default is (5., 5.).

    filelabel : str, optional
        Figure is saved in 'filelabel.png' if provided (the default is None).

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

    log : list of str, optional
        Log-scale activation for each axis according to
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
        the default is figsize[0]*4

    legendfontsize : int, optional
        Figure legend font size. If None then set to 4/5 of fontsize (the \
default is None).

    maintitle : str, optional
        Figure main title. If set to None, the desactivated (the default is \
None).

    axedef : tuple of floats, optional
        Figure geometry (left, botom, right, top, height, width).
        The default is (.15, .15, .85, .85, .1, .3).

        ======  \
===============================================================
        Value    Description
        ======  \
===============================================================
        left     the left side of the subplots of the figure.
        bottom   the bottom of the subplots of the figure.
        right    the right side of the subplots of the figure.
        top      the top of the subplots of the figure.
        wspace   the amount of width reserved for blank space between subplots.
        hspace   the amount of height reserved for white space between \
subplots.
        ======  \
===============================================================

    markersize : float
        Default is 6.

    markeredgewidth : float
        Width of line around markers (the default is 0.5).

    nbinsx, nbinsy : int, optional
        number of x-axis and y-axis ticks (the default is 4).

    minor : bool
        Activate the minor grid.

    xpos_ylabel : float, optional
        If provided, set the x-position of the ylabels so that they align (the\
 default is None).
        You probably want it to be negative.

    """
    opts = standard.copy()
    opts.update(kwargs)
    nplots = len(datay)

    if opts['fontsize'] is None:
        opts['fontsize'] = int(6*opts['figsize'][0])
    if opts['legendfontsize'] is None:
        opts['legendfontsize'] = int(0.8*opts['fontsize'])
    if opts['unity'] is None:
        opts['unity'] = ['', ]*nplots
    if opts['limits'] is None:
        opts['limits'] = [None, ]*nplots
    elif opts['limits'] == 'extend':
        opts['limits'] = ['extend', ]*nplots
    if opts['labels'] is None:
        opts['labels'] = [None, ] * nplots
    if opts['log'] is None:
        opts['log'] = ['', ] * nplots
    from matplotlib.pyplot import subplots, close
    close('all')
    fig, axs = subplots(nplots, 1, sharex=True, figsize=opts['figsize'])

    activate_latex(opts)

    # Dic of font properties
    from matplotlib.pyplot import rc
    rc('font', size=opts['fontsize'], **globalfonts())

    x = dec(datax, opts)
    for n in range(nplots):

        miny = float('Inf')
        maxy = -float('Inf')

        if type(datay[n]) is list:
            y = dec(datay[n], opts)
            maxy = max([maxy, max(y)])
            miny = min([miny, min(y)])
            if nplots > 1:
                plotn = whichplot(opts['log'][n], axs[n])
            else:
                whichplot(opts['log'][n], axs)
            plotn(x, y, opts['linestyles'][0], label=opts['labels'][n],
                  linewidth=opts['linewidth'],
                  markeredgewidth=opts['markeredgewidth'],
                  markersize=opts['markersize'])

        elif isinstance(datay[n], tuple):
            len_yn = len(datay[n])
            if opts['labels'][n] is None:
                opts['labels'][n] = (None, )*len_yn
            for m in range(len_yn):
                if isinstance(opts['labels'][n][m], (list, tuple)):
                    annotate(x, y, opts['labels'][n][m][0],
                             opts['labels'][n][m][1],
                             opts['legendfontsize'])
                    l = None
                else:
                    l = opts['labels'][n][m]

                y = dec(datay[n][m])
                maxy = max([maxy, max(y)])
                miny = min([miny, min(y)])
                plotn = whichplot(opts['log'][n], axs[n])
                plotn(x, y, opts['linestyles'][m], label=l,
                      linewidth=opts['linewidth'],
                      markersize=opts['markersize'],
                      markeredgewidth=opts['markeredgewidth'])

        setlims(axs[n], x, miny, maxy, opts['limits'][n])
        setticks(axs[n], opts, n)

        axs[n].legend(loc=opts['loc'], fontsize=opts['legendfontsize'])
        if opts['unity'][n] is not None:
            axs[n].set_ylabel(opts['unity'][n], fontsize=opts['fontsize'])
            if opts['xpos_ylabel'] is not None:
                axs[n].yaxis.set_label_coords(opts['xpos_ylabel'], 0.5)
        if n == nplots-1:
            axs[n].set_xlabel(opts['unitx'], fontsize=opts['fontsize'])
        else:
            from matplotlib.pyplot import setp
            setp(axs[n].get_xticklabels(), visible=False)

    if opts['maintitle'] is not None:
        from matplotlib.pyplot import suptitle
        suptitle(opts['maintitle'])

    if opts['axedef'] is not None:
        print(opts['axedef'])
        left, right = opts['axedef'][0], opts['axedef'][2]
        bottom, top = opts['axedef'][1], opts['axedef'][3]
        wspace, hspace = opts['axedef'][4], opts['axedef'][5]
        fig.subplots_adjust(left=left, right=right,
                            bottom=bottom, top=top,
                            wspace=wspace, hspace=hspace)
    else:
        fig.tight_layout(pad=0.6, w_pad=0.5, h_pad=.0)

    if opts['filelabel'] is not None:
        from matplotlib.pyplot import savefig
        savefig(opts['filelabel'] + '.' + opts['format'])

    from matplotlib.pyplot import show
    show()
