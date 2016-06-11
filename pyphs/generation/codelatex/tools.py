# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 19:19:36 2016

@author: Falaize
"""


def nice_label(var, ind):
    if var in ('dxHd', 'dxH'):
        return r'$\overline{\nabla}\mathtt{H}_'+str(ind)+r'$'
    elif var == 'dtx':
        return r'$\mathrm D_t \,{x}_'+str(ind)+'$'
    else:
        return r'$'+var+'_'+str(ind)+r'$'
