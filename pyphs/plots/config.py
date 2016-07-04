# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 12:45:42 2016

@author: Falaize
"""

plot_format = 'pdf'


def plot_options():
    return {'loc': 1,
            'unitx': None,
            'unity': None,
            'linestyles': ('-b', '--r', '-.g', ':m'),
            'axedef': (0.15, 0.15, 0.75, 0.75),
            'fontsize': 20,
            'log': None,
            'legendfontsize': None,
            'linewidth': 3,
            'figsize': (7., 6.),
            'nbinsx': 5,
            'nbinsy': 5,
            'minor': True,
            'markersize': 6,
            'markeredgewidth': 0.5,
            'latex': False,
            'maxnplot': int(1e5),
            'ylims': 'extend',
            'format': plot_format,
            'limits': None,
            'labels': None,
            'maintitle': None,
            'filelabel': None,
            'nfft': 2**12,
            'colormap': 'BuPu',
            'xpos_ylabel': -0.08,
            'cmap': 'BuPu',  #  'inferno',  #'gnuplot2', # 'CMRmap',  # 'PuBu',
            'dpi': 100}


def plotopts(which='single'):
    pp = plot_options()
    if which == 'multi':
        pp.update({'linewidth': 2,
                   'axedef': (.15, .15, .85, .85, .1, .3),
                   'minor': False})
    return pp
latex_preamble = [' ', ]
