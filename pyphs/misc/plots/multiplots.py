# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 20:06:50 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

from .tools import annotate, whichplot, standard
import numpy


def multiplot(x, y, show=True, **kwargs):
    """
    Plot multiple y-axis and possible multiple curves in each. Result can be
    saved as a '.png' document.

    Parameters
    ----------

    x : list of floats
        x-axis values.

    y : list of floats or of tuples of list of floats
        y-axis values per axis and per curve in each axis, if tuple.

    xlabel : str, optional
        x-axis label (the default is None).

    ylabels : list of str, optional
        y-axis label for each axe (the default is None).

    title : str, optional
        Figure main title. Desactivated if set to None (default).

    labels : list, optional
        list of curve labels (the default is None). Textboxes can be used with_files
        the elements syntax ['label', (xrel, yrel)] where xrel and yrel are
        relative x and y position.

    path : str, optional
        Figure is saved in 'path.ext' if provided (the default is None).
        Extension from pyphs config.py.

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
        List of line styles; the default is None.

    xpos_ylabel : float, optional
        If provided, set the x-position of the ylabels so that they align (the
        default is None). You probably want it to be negative.

    grid : bool
        Indicate whether to show the grid or not.

    """

    # ------------------------------------------------------------
    # Number of axes
    nplots = len(y)

    # ------------------------------------------------------------
    # Recover standard options
    opts = standard.copy()

    # Update with new options
    opts.update(kwargs)

    # ------------------------------------------------------------
    # Check fo options length
    if opts['ylabels'] is None:
        opts['ylabels'] = ['', ]*nplots
    elif not len(opts['ylabels']) == nplots:
        raise AttributeError('wrong number of y labels')

    if opts['labels'] is None:
        opts['labels'] = [None, ]*nplots
    elif not len(opts['ylabels']) == nplots:
        raise AttributeError('wrong number of curves labels')

    if opts['log'] is None:
        opts['log'] = ['', ] * nplots
    elif not len(opts['log']) == nplots:
        raise AttributeError('wrong number of log options')

    # ------------------------------------------------------------
    # Init figure and axes
    from matplotlib.pyplot import subplots, fignum_exists

    i = 1
    while fignum_exists(i):
        i += 1
    fig, axs = subplots(nplots, 1, sharex=True, num=i)

    # ------------------------------------------------------------
    # Iterate over y data
    for n, yn in enumerate(y):

        # --------------------------------------------------------
        # get axe
        if nplots > 1:
            axe = axs[n]
        else:
            axe = axs

        axe.ticklabel_format(style='sci', scilimits=(-2, 2))

        # --------------------------------------------------------
        # flag
        print_legend = False

        # --------------------------------------------------------
        # if yn is a list of values
        if (isinstance(yn[0], (float, int)) or
            (isinstance(yn[0], numpy.ndarray) and len(yn[0].shape) == 0)):

            # get plot in {plot, semilogx, semilogy, loglog}
            plotn = whichplot(opts['log'][n], axe)

            # Add label or annotation
            if isinstance(opts['labels'][n], (list, tuple)):
                annotate(*opts['labels'][n], ax=axe)
                l = None
            else:
                l = opts['labels'][n]
            print_legend = l is not None or print_legend

            # Plot
            if opts['linestyles'] is not None:
                plotn(x, yn, opts['linestyles'][n][0],
                      label=l)
            else:
                plotn(x, yn, label=l)

        # --------------------------------------------------------
        # if yn is a list of signals
        else:

            # get number of signals in yn
            len_yn = len(yn)

            # Set appropriate len of labels
            if opts['labels'][n] is None:
                opts['labels'][n] = (None, )*len_yn
            elif not len(opts['labels'][n]) == len_yn:
                raise AttributeError('wrong number of labels')

            # iterate over yn  data
            for m, ynm in enumerate(yn):

                # Add label or annotation
                if isinstance(opts['labels'][n][m], (list, tuple)):
                    annotate(*opts['labels'][n][m], ax=axe)
                    l = None
                else:
                    l = opts['labels'][n][m]
                print_legend = l is not None or print_legend

                # get plot in {plot, semilogx, semilogy, loglog}
                plotn = whichplot(opts['log'][n], axe)

                # Plot
                if opts['linestyles'] is not None:
                    plotn(x, ynm, opts['linestyles'][n][m], label=l)
                else:
                    plotn(x, ynm, label=l)

        # --------------------------------------------------------
        # Print legend
        if print_legend:
            axs[n].legend(loc=opts['loc'])

        # --------------------------------------------------------
        # Set y label
        if opts['ylabels'][n] is not None:
            axs[n].set_ylabel(opts['ylabels'][n])
            if opts['xpos_ylabel'] is not None:
                axs[n].yaxis.set_label_coords(opts['xpos_ylabel'], 0.5)

        # --------------------------------------------------------
        # Set x label if last plot
        if n == nplots-1:
            axs[n].set_xlabel(opts['xlabel'])
        else:
            from matplotlib.pyplot import setp
            setp(axs[n].get_xticklabels(), visible=False)

        # --------------------------------------------------------
        # Show grid
        axs[n].grid(opts['grid'])
        axs[n].minorticks_on()

    # ------------------------------------------------------------
    # Set title
    if opts['title'] is not None:
        from matplotlib.pyplot import suptitle
        suptitle(opts['title'])

    # ------------------------------------------------------------
    # Save file
    if opts['path'] is not None:
        from matplotlib.pyplot import savefig
        savefig(opts['path'] + '.' + opts['format'])

    # ------------------------------------------------------------
    # Show
    if show:
        from matplotlib.pyplot import show as pltshow
        pltshow()

    return fig, axs
