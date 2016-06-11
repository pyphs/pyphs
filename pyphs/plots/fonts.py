# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 19:40:55 2016

@author: Falaize
"""


def font_lists():
    lis = list()
    lis.append(('serif',
                ['Times', 'Bitstream Vera Serif', 'New Century Schoolbook',
                 'Century Schoolbook L', 'Utopia', 'ITC Bookman', 'Bookman',
                 'Nimbus Roman No9 L', 'Times New Roman', 'Palatino',
                 'Charter', 'Computer Modern', 'serif']))
    lis.append(('sans-serif',
                ['Bitstream Vera Sans', 'Lucida Grande', 'Verdana', 'Geneva',
                 'Lucid', 'Arial', 'Helvetica', 'Avant Garde', 'sans-serif']))
    lis.append(('cursive',
                ['Apple Chancery', 'Textile', 'Zapf Chancery', 'Sand',
                 'Script MT', 'Felipa', 'cursive']))
    lis.append(('fantasy',
                ['Comic Sans MS', 'Chicago', 'Charcoal', 'Impact', 'Western',
                 'Humor Sans', 'fantasy']))
    lis.append(('monospace',
                ['Bitstream Vera Sans Mono', 'Andale Mono', 'Nimbus Mono L',
                 'Courier New', 'Courier', 'Fixed', 'Terminal', 'monospace']))
    return lis


def globalfonts():
    font_properties = {'family': 'serif',
                       'weight': 'normal',
                       'variant': 'small-caps'}
    for fonts in font_lists():
        font_properties[fonts[0]] = fonts[1]
    return font_properties


def test_fonts():
    import numpy as np
    t = list(1+np.linspace(0, 1, 2000))
    s1 = [2*np.sin(2*np.pi*3*elt) for elt in t]
    s2 = [np.sin(2*np.pi*4*elt) for elt in t]
    Nplot = 2
    datax = t
    datay = [(s1, s2), ]*Nplot
    lab = [None, ]*Nplot
    lab[0] = (0.5, r'5Hz')
    lab[1] = (0.25, r'7Hz')

    labels = list()
    labels.append((r'5Hz', r'7Hz'))
    labels.append(lab)
    labels = list()
    labels.append((r'5Hz', r'7Hz'))
    labels.append(lab)
    plot_properties = {'unitx': r'Impedance $\frac{v_\mathtt{I}}' +
                                r'{i_\mathtt{I}}$ ($\Omega$=V/A)',
                       'unity': (r'$\sum_{i=1}^n\beta_i$',
                                 r'Integral $\int_0^{x_i} f(\alpha)' +
                                 r'\mathtt{d}$ (V)'),
                       'labels': labels,
                       'limits': 'extend',
                       'fontsize': 20,
                       'legendfontsize': None,
                       'linewidth': 2,
                       'figsize': (8., 8.),
                       'loc': 1,
                       'log': ('y', 'x'),
                       'linestyles': ('-b', '--r', ':g', '-.m'),
                       'axedef': (.15, .15, .85, .85, .1, .3),
                       'nbinsx': 4,
                       'nbinsy': 4,
                       'minor': True}

    for (family, fonts) in font_lists():
        for font in fonts:
            global Globalfont

            def Globalfont():

                return {'family': family,
                        family: [font],
                        'weight': 'normal',
                        'variant': 'small-caps'}
            import os
            plot_properties['maintitle'] = family + ': ' + font + \
                r'; $\sum_{i=1}^n\int_0^{x_i} f(\alpha) \mathtt{d}\beta$'
            plot_properties['filelabel'] = 'fonts'+os.sep+family+'_'+font
            multiplot(datax, datay, **plot_properties)


if __name__ == '__main__':
    import numpy as np
    f0 = 100
    t = list(1/2.+np.linspace(0, 1, 2000))
    s1 = [2*np.sin(2*np.pi*3*elt) for elt in t]
    s2 = [np.sin(2*np.pi*4*elt) for elt in t]
    Nplot = 2
    datax = t
    datay = [(s1, s2), ]*Nplot
    lab = [None, ]*Nplot
    lab[0] = (0.5, r'5Hz')
    lab[1] = (0.25, r'7Hz')

    labels = list()
    labels.append((r'5Hz', r'7Hz'))
    labels.append(lab)
    plot_properties = {'unitx': '',
                       'unity': (r'yo $yo$', r'yo $2\,yo=3$'),
                       'labels': labels,
                       'limits': 'extend',
                       'fontsize': 20,
                       'legendfontsize': None,
                       'linewidth': 2,
                       'figsize': (8., 8.),
                       'filelabel': None,
                       'maintitle': None,
                       'loc': 1,
                       'log': ('y', 'x'),
                       'linestyles': ('-b', '--r', ':g', '-.m'),
                       'axedef': (.15, .15, .85, .85, .1, .3),
                       'nbinsx': 20,
                       'nbinsy': 4,
                       'minor': True}
    from multiplots import multiplot
    multiplot(datax, datay, **plot_properties)
    datay = [s1, s2]
    labels = [r'5Hz', r'7Hz']
    labels[0] = (0.45, r'5Hz')
    labels[-1] = (0.25, r'7Hz')
    datax = t
    plot_properties = {
                       'labels': None,
                       'unitx': None,
                       'unity': None,
                       'ylims': 'extend',
                       'fontsize': 30,
                       'legendfontsize': None,
                       'linewidth': 2,
                       'figsize': (6., 6.),
                       'axedef': [.15, .15, .75, .75],
                       'filelabel': None,
                       'maintitle': None,
                       'loc': 1,
                       'log': '',
                       'linestyles': ['-b', '--r', ':g', '-.m'],
                       'nbinsx': 4,
                       'nbinsy': 4,
                       'minor': False}
    # singleplot(datax, datay, **plot_properties)
    # test_fonts()
