# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 12:45:42 2016

@author: Falaize
"""

plot_format = 'pdf'

plot_options = {'loc': 1,
                'linestyles': ('-b', '--r', '-.g', ':m'),
                'markeredgewidth': 1,
                'axedef': (0.15, 0.15, 0.75, 0.75),
                'legendfontsize': None,
                'linewidth': 2,
                'figsize': (7., 6.),
                'nbinsx': 5,
                'nbinsy': 5,
                'minor': True,
                'markersize': 6,
                'markeredgewidth': 0.5,
                'latex': False
                }


def plotopts(which='single'):
    if which == 'single':
        return plot_options
    if which == 'multi':
        return plot_options.update({'linewidth': 2,
                                    'figsize': (7., 6.),
                                    'axedef': (.15, .15, .85, .85, .1, .3),
                                    'nbinsx': 6,
                                    'nbinsy': 5,
                                    'minor': False})

latex_preamble = [' ', ]
