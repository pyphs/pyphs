# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 19:41:09 2016

@author: Falaize
"""


def dec(li, opts):
    """
    decimate liste li so that number of ploted points is no mode than \
opts['maxnplot'].
    """
    from pyphs.misc.tools import decimate
    ndecim = max((1, int(len(li)/opts['maxnplot'])))
    return [el for el in decimate(li, ndecim)]


def activate_latex(opts):
    """
    activate latex for plot texts
    """
    # Path for latex compiler
    import os
    from pyphs.generation.codelatex.config import compiler_path
    os.environ['PATH'] = os.environ['PATH'] + compiler_path
    # Activate use of latex expressions
    from matplotlib.pyplot import rc
    rc('text', usetex=opts['latex'])
    # Add Latex Preamble
    from pyphs.plots.config import latex_preamble
    from matplotlib import rcParams
    rcParams['text.latex.preamble'] = latex_preamble


def annotate(x, y, pos, annote, legendfontsize):
    """
    function for plot annotation
    """
    from matplotlib.pyplot import text
    nbin = int(pos*len(x))
    binx = x[nbin]
    biny = y[nbin]
    text(binx, biny, annote, fontdict={'fontsize': legendfontsize},
         bbox=dict(facecolor='white', alpha=1.),
         horizontalalignment='center', verticalalignment='center')


def setticks(ax, properties):
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

    if properties['log'] == '':
        locatorxMaj = MaxNLocator(nbins=nbinsx)
        locatoryMaj = MaxNLocator(nbins=nbinsy)
        locatorxMin = AutoMinorLocator()
        locatoryMin = AutoMinorLocator()

    elif properties['log'] == 'x':
        locatorxMaj = AutoLocator()
        locatoryMaj = MaxNLocator(nbins=nbinsy)
        locatorxMin = locatorxMaj
        locatoryMin = AutoMinorLocator()

    elif properties['log'] == 'y':
        locatorxMaj = MaxNLocator(nbins=nbinsx)
        locatoryMaj = AutoLocator()
        locatorxMin = AutoMinorLocator()
        locatoryMin = locatoryMaj

    elif properties['log'] == 'xy':
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
