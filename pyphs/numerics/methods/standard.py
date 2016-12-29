#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 13:39:59 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

from pyphs.numerics.tools import PHSNumericalOperation as op
from pyphs.numerics.method import PHSNumericalMethod


class PHSNumericalMethodStandard(PHSNumericalMethod):

    def __init__(self, core, config=None):
        PHSNumericalMethod.__init__(self, core, config=config)

        ud_x = op('add',
                  ('x', 'dx'))
        self.setfunc('ud_x', ud_x)

        if self.nl > 0:

            #######################################
            # Dl
            Dl = op('inv',
                    ('iDl', ))
            self.setfunc('Dl', Dl)

            #######################################
            # Nlxl
            Nlxl = op('dot',
                      ('Dl', 'barNlxl'))
            self.setfunc('Nlxl', Nlxl)

            #######################################
            # Nlnl
            if self.nnl > 0:
                Nlnl = op('dot',
                          ('Dl', 'barNlnl'))
                self.setfunc('Nlnl', Nlnl)

            #######################################
            # Nly
            if self.ny > 0:
                Nly = op('dot',
                         ('Dl', 'barNly'))
                self.setfunc('Nly', Nly)

        if self.nnl > 0:

            #######################################
            # Nnlxl
            if self.nl > 0:
                temp = op('dot',
                          ('barNnll', 'barNlxl'))
                Nnlxl = op('add',
                           ('barNnlxl', temp))
                self.setfunc('Nnlxl', Nnlxl)

            #######################################
            # Nnlnl
            if self.nl > 0:
                temp = op('dot',
                          ('barNnll', 'barNlnl'))
            else:
                temp = 0.
            Nnlnl = op('add',
                       ('barNnlnl', temp))
            self.setfunc('Nnlnl', Nnlnl)

            #######################################
            # Nnly
            if self.ny > 0:
                if self.nl > 0:
                    temp = op('dot',
                              ('barNnll', 'barNly'))
                else:
                    temp = 0.
                Nnly = op('add', ('barNnly', temp))
                self.setfunc('Nnly', Nnly)

            #######################################
            # c
            if self.nl > 0:
                temp1 = op('dot',
                           ('Nnlxl', 'xl'))
            else:
                temp1 = 0.

            if self.ny > 0:
                temp2 = op('dot',
                           ('Nnly', 'u'))
            else:
                temp2 = 0.
            c = op('add',
                   (temp1, temp2))
            self.setfunc('c', c)

            #######################################
            # impfunc
            temp1 = op('dot',
                       ('Inl', 'vnl'))      # Inl*vnl
            temp2 = op('dot',
                       ('Nnlnl', 'fnl'))    # Nnlnl*fnl
            temp3 = op('dot',
                       (-1., temp2))        # - Nnlnl*fnl
            temp4 = op('add',
                       (temp1, temp3))      # Inl*vnl - Nnlnl*fnl
            temp5 = op('dot',
                       (-1., 'c'))          # - c
            impfunc = op('add',
                         (temp4, temp5))    # Inl*vnl - Nnlnl*fnl - c
            self.setfunc('impfunc', impfunc)

            #######################################
            # save_impfunc
            self.setfunc('save_impfunc', 'impfunc')

            #######################################
            # jac_impfunc
            temp1 = op('dot',
                       ('Nnlnl', 'jac_fnl'))
            temp2 = op('dot', (-1., temp1))
            jac_impfunc = op('add',
                             ('Inl', temp2))
            self.setfunc('jac_impfunc', jac_impfunc)

            #######################################
            # ijac_impfunc
            ijac_impfunc = op('inv',
                              ('jac_impfunc', ))
            self.setfunc('ijac_impfunc', ijac_impfunc)

            #######################################
            # res_impfunc
            res_impfunc = op('norm',
                             ('impfunc', ))
            self.setfunc('res_impfunc', res_impfunc)

            #######################################
            # step_impfunc
            temp1 = op('dot',
                       (-1., 'save_impfunc'))
            temp2 = op('add',
                       ('impfunc', temp1))
            step_impfunc = op('norm',
                              (temp2, ))
            self.setfunc('step_impfunc', step_impfunc)

            #######################################
            # ud_vnl
            temp1 = op('dot',
                       ('ijac_impfunc', 'impfunc'))
            temp2 = op('dot',
                       (-1., temp1))
            ud_vnl = op('add',
                        ('vnl', temp2))
            self.setfunc('ud_vnl', ud_vnl)

        if self.nl > 0:
            #######################################
            # ud_vl
            temp1 = op('dot',
                       ('Nlxl', 'xl')) # Nlxl*xl
            if self.nnl > 0:
                temp2 = op('dot',
                           ('Nlnl', 'fnl')) # Nlnl*fnl
            else:
                temp2 = 0.
            temp3 = op('add', (temp1, temp2)) # Nlxl*xl + Nlnl*fnl
            if self.ny > 0:
                temp4 = op('dot',
                           ('Nly', 'u')) # Nly*u
            else:
                temp4 = 0.
            ud_vl = op('add',
                       (temp3, temp4)) # lxl*xl + Nlnl*fnl + Nly*u
            self.setfunc('ud_vl', ud_vl)

        self.setupdate()

    def setupdate(self):

        list_ = []
        list_.append(('x', 'ud_x'))
        if self.nl > 0:
            list_.append('iDl')
            list_.append('Dl')
            list_.append('Nlxl')
            if self.nnl > 0:
                list_.append('Nlnl')
            if self.ny > 0:
                list_.append('Nly')
        if self.nnl > 0:
            list_.append('Nnlnl')
            if self.nl > 0:
                list_.append('Nnlxl')
            if self.ny > 0:
                list_.append('Nnly')
            list_.append('c')
            list_.append('Inl')
            list_.append('fnl')
            list_.append('impfunc')
            list_.append('res_impfunc')

        self.set_execaction(list_)

        if self.nnl > 0:
            list_ = []
            list_.append('save_impfunc')
            list_.append('jac_fnl')
            list_.append('jac_impfunc')
            list_.append('ijac_impfunc')
            list_.append(('vnl', 'ud_vnl'))
            list_.append('fnl')
            list_.append('impfunc')
            list_.append('res_impfunc')
            list_.append('step_impfunc')

            self.set_iteraction(list_,
                                'res_impfunc',
                                'step_impfunc')
        list_ = []
        if self.nl > 0:
            list_.append(('vl', 'ud_vl'))
        list_.append('dxH')
        list_.append('z')
        list_.append('y')

        self.set_execaction(list_)
