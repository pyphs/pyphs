# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 19:41:09 2016

@author: Falaize
"""

import os
from matplotlib.pyplot import text
from pyphs.config import latex_compiler_path, plot_format
from pyphs.misc.tools import decimate


def dec(li, opts):
    """
    decimate liste li so that number of ploted points is no mode than \
opts['maxnplot'].
    """
    li = list(li)
    ndecim = max((1, int(len(li)/opts['maxnplot'])))
    return [el for el in decimate(li, ndecim)]


def activate_latex(opts):
    """
    activate latex for plot texts
    """
    # Path for latex compiler
    os.environ['PATH'] = os.environ['PATH'] + latex_compiler_path
    # Activate use of latex expressions
    from matplotlib.pyplot import rc
    rc('text', usetex=opts['latex'])
    # Add Latex Preamble
    from pyphs.config import latex_preamble
    from matplotlib import rcParams
    rcParams['text.latex.preamble'] = latex_preamble


def annotate(x, y, pos, annote, legendfontsize):
    """
    function for plot annotation
    """
    nbin = int(pos*len(x))
    binx = x[nbin]
    biny = y[nbin]
    text(binx, biny, annote, fontdict={'fontsize': legendfontsize},
         bbox=dict(facecolor='white', alpha=1.),
         horizontalalignment='center', verticalalignment='center')


def setticks(ax, properties, plotindex=None):
    """
    manage ticks and grids of a figure
    """

    major_linewidth = properties['linewidth']
    minor_linewidth = major_linewidth/4.

    from matplotlib.ticker import ScalarFormatter
    majorformatter = ScalarFormatter(useOffset=False)

    from matplotlib.ticker import MaxNLocator, AutoMinorLocator, AutoLocator

    nbinsx = properties['nbinsx'] + 1
    nbinsy = properties['nbinsy'] + 1
    if plotindex is None:
        log = properties['log']
    else:
        log = properties['log'][plotindex]
    if log == '' or properties['log'] is None:
        locatorxMaj = MaxNLocator(nbins=nbinsx)
        locatoryMaj = MaxNLocator(nbins=nbinsy)
        locatorxMin = AutoMinorLocator()
        locatoryMin = AutoMinorLocator()

    elif log == 'x':
        locatorxMaj = AutoLocator()
        locatoryMaj = MaxNLocator(nbins=nbinsy)
        locatorxMin = locatorxMaj
        locatoryMin = AutoMinorLocator()

    elif log == 'y':
        locatorxMaj = MaxNLocator(nbins=nbinsx)
        locatoryMaj = AutoLocator()
        locatorxMin = AutoMinorLocator()
        locatoryMin = locatoryMaj

    elif log == 'xy':
        locatorxMaj = AutoLocator()
        locatoryMaj = AutoLocator()
        locatorxMin = locatorxMaj
        locatoryMin = locatoryMaj

    locatorxMaj = MaxNLocator(nbins=nbinsx)
    locatoryMaj = MaxNLocator(nbins=nbinsy)

    # x-axis:
    ax.xaxis.set_major_formatter(majorformatter)
    ax.xaxis.set_major_locator(locatorxMaj)

    # y-axis
    ax.yaxis.set_major_formatter(majorformatter)
    ax.yaxis.set_major_locator(locatoryMaj)

    # grid
    ax.xaxis.grid(True, 'major', linewidth=major_linewidth)
    ax.yaxis.grid(True, 'major', linewidth=major_linewidth)
    if properties['minor']:
        ax.xaxis.set_minor_locator(locatorxMin)
        ax.yaxis.set_minor_locator(locatoryMin)
        ax.xaxis.grid(True, 'minor', linewidth=minor_linewidth)
        ax.yaxis.grid(True, 'minor', linewidth=minor_linewidth)

    ax.ticklabel_format(axis='both', style='sci', scilimits=(-2, 2))
    ax.tick_params(axis='both', labelsize=properties['legendfontsize'])
    t = ax.xaxis.get_offset_text()
    t.set_size(properties['legendfontsize'])
    t = ax.yaxis.get_offset_text()
    t.set_size(properties['legendfontsize'])


def setlims(ax, x, miny, maxy, limy):
    """
    manage limits of a plot
    """
    limx = (min(x), max(x))
    ax.set_xlim(limx)
    if limy is None:
        limy = (float(miny), float(maxy))
    elif limy == 'extend':
        extend = 0.05
        rangey = maxy-miny
        limy = (float(miny-rangey*extend), float(maxy+rangey*extend))
    ax.set_ylim(limy)


def whichplot(which, axe):
    """
    select plot function according to chosen log scale (if any).
    """
    if which == '':
        return axe.plot
    elif which == 'x':
        return axe.semilogx
    elif which == 'y':
        return axe.semilogy
    elif which == 'xy':
        return axe.loglog


standard = {'loc': 0,  # legend location
            'unitx': None,  # x axis label
            'unity': None,  # y axis label
            'linestyles': ('-b', '--r', '-.g', ':m'),  # styles (1->4 lines)
            #
            'axedef': None,  # left,bot,right,top (.15, .15, .75, .75, .1, .3)
            'fontsize': 20,                             #
            'log': None,  # logscale: 'x','y','xy'
            'legendfontsize': None,                     #
            'linewidth': 2.5,                           #
            'figsize': (7., 6.),                        #
            'nbinsx': 5,  # number of x axis ticks
            'nbinsy': 5,  # number of y axis ticks
            'minor': False,  # Show minor grid
            'markersize': 6,                            #
            'markeredgewidth': 0.5,  #
            'latex': False,  # Latex rendering
            'maxnplot': int(1e5),  # max number of line bins  before decimation
            'ylims': 'extend',
            'format': plot_format,
            'limits': None,
            'labels': None,
            'maintitle': None,
            'filelabel': None,
            'nfft': 2**12,
            'colormap': 'BuPu',
            'xpos_ylabel': -0.08,
            'cmap': 'BuPu',  # 'inferno', 'gnuplot2', 'CMRmap', 'PuBu',
            'dpi': 100,
            }
