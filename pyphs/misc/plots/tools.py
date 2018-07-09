# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 19:41:09 2016

@author: Falaize
"""

from pyphs.config import plot_format
from pyphs.misc.tools import decimate


def dec(li, opts):
    """
    decimate liste li so that number of ploted points is no mode than
    opts['maxnplot'].
    """
    li = list(li)
    ndecim = max((1, int(len(li)/opts['maxnplot'])))
    return [el for el in decimate(li, ndecim)]


def annotate(s, xy, ax=None):
    """
    function for plot annotation
    """
    binx = xy[0]
    biny = xy[1]
    ax.text(binx, biny, s,
            bbox=dict(facecolor='white', alpha=1.),
            horizontalalignment='center',
            verticalalignment='center',
            transform=ax.transAxes)


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
            'xlabel': None,  # x axis label
            'ylabels': None,  # y axis label
            'log': None,  # logscale: 'x','y','xy'
            'format': plot_format,
            'path': None,  # save path
            'linestyles': None,
            'labels': None,
            'title': None,
            'xpos_ylabel': None,
            'grid': False
            }
