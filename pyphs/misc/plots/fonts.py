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
