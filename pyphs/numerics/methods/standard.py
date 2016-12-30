#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 13:39:59 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

from pyphs.numerics.method import PHSNumericalMethod


class PHSNumericalMethodStandard(PHSNumericalMethod):

    def __init__(self, core, config=None):
        PHSNumericalMethod.__init__(self, core, config=config)

        ud_x = self.operation('add', ('x', 'dx'))
        self.setoperation('ud_x', ud_x)

        if self.core.dims.l() > 0:
            self.init_linear()

        if self.core.dims.nl() > 0:
            self.init_nonlinear()

        self.setupdate()

    def init_linear(self):

        # Dl
        Dl = self.operation('inv', ('iDl', ))
        self.setoperation('Dl', Dl)

        # Nlxl
        Nlxl = self.operation('dot', ('Dl', 'barNlxl'))
        self.setoperation('Nlxl', Nlxl)

        # Nlnl
        if self.core.dims.nl() > 0:
            Nlnl = self.operation('dot', ('Dl', 'barNlnl'))
            self.setoperation('Nlnl', Nlnl)

        # Nly
        if self.core.dims.y() > 0:
            Nly = self.operation('dot', ('Dl', 'barNly'))
            self.setoperation('Nly', Nly)

        # ud_vl
        # Nlxl*xl
        Nlxl_dot_xl = self.operation('dot', ('Nlxl', 'xl'))
        # Nlnl*fnl
        if self.core.dims.nl() > 0:
            Nlnl_dot_fnl = self.operation('dot', ('Nlnl', 'fnl'))
        else:
            Nlnl_dot_fnl = 0.
        # Nlxl*xl + Nlnl*fnl
        Nlxl_dot_xl_plus_Nlnl_dot_fnl = self.operation('add',
                                                       (Nlxl_dot_xl,
                                                        Nlnl_dot_fnl))
        # Nly*u
        if self.core.dims.y() > 0:
            Nly_dot_u = self.operation('dot', ('Nly', 'u'))
        else:
            Nly_dot_u = 0.
        # Nlxl*xl + Nlnl*fnl + Nly*u
        ud_vl = self.operation('add', (Nlxl_dot_xl_plus_Nlnl_dot_fnl,
                                       Nly_dot_u))
        self.setoperation('ud_vl', ud_vl)

    def init_nonlinear(self):

        # Nnlxl
        if self.core.dims.l() > 0:
            temp = self.operation('dot', ('barNnll', 'Nlxl'))
            Nnlxl = self.operation('add', ('barNnlxl', temp))
            self.setoperation('Nnlxl', Nnlxl)

        # Nnlnl
        if self.core.dims.l() > 0:
            temp = self.operation('dot', ('barNnll', 'Nlnl'))
        else:
            temp = 0.
        Nnlnl = self.operation('add', ('barNnlnl', temp))
        self.setoperation('Nnlnl', Nnlnl)

        # Nnly
        if self.core.dims.y() > 0:
            if self.core.dims.l() > 0:
                temp = self.operation('dot', ('barNnll', 'Nly'))
            else:
                temp = 0.
            Nnly = self.operation('add', ('barNnly', temp))
            self.setoperation('Nnly', Nnly)

        # c
        if self.core.dims.l() > 0:
            temp1 = self.operation('dot', ('Nnlxl', 'xl'))
        else:
            temp1 = 0.

        if self.core.dims.y() > 0:
            temp2 = self.operation('dot', ('Nnly', 'u'))
        else:
            temp2 = 0.
        c = self.operation('add', (temp1, temp2))
        self.setoperation('c', c)

        # impfunc
        temp1 = self.operation('dot', ('Inl', 'vnl'))      # Inl*vnl
        temp2 = self.operation('dot', ('Nnlnl', 'fnl'))    # Nnlnl*fnl
        temp3 = self.operation('dot', (-1., temp2))        # - Nnlnl*fnl
        temp4 = self.operation('add', (temp1, temp3))      # Inl*vnl-Nnlnl*fnl
        temp5 = self.operation('dot', (-1., 'c'))          # - c
        impfunc = self.operation('add', (temp4, temp5))  # Inl*vnl-Nnlnl*fnl-c
        self.setoperation('impfunc', impfunc)

        #######################################
        # save_impfunc
        save_impfunc = self.operation('return', ('impfunc', ))
        self.setoperation('save_impfunc', save_impfunc)

        #######################################
        # jac_impfunc
        temp1 = self.operation('dot', ('Nnlnl', 'jac_fnl'))
        temp2 = self.operation('dot', (-1., temp1))
        jac_impfunc = self.operation('add', ('Inl', temp2))
        self.setoperation('jac_impfunc', jac_impfunc)

        #######################################
        # ijac_impfunc
        ijac_impfunc = self.operation('inv', ('jac_impfunc', ))
        self.setoperation('ijac_impfunc', ijac_impfunc)

        #######################################
        # res_impfunc
        res_impfunc = self.operation('norm', ('impfunc', ))
        self.setoperation('res_impfunc', res_impfunc)

        #######################################
        # step_impfunc
        temp1 = self.operation('dot', (-1., 'save_impfunc'))
        temp2 = self.operation('add', ('impfunc', temp1))
        step_impfunc = self.operation('norm', (temp2, ))
        self.setoperation('step_impfunc', step_impfunc)

        #######################################
        # ud_vnl
        temp1 = self.operation('dot', ('ijac_impfunc', 'impfunc'))
        temp2 = self.operation('dot', (-1., temp1))
        ud_vnl = self.operation('add', ('vnl', temp2))
        self.setoperation('ud_vnl', ud_vnl)

    def setupdate(self):

        list_ = []
        list_.append(('x', 'ud_x'))
        self.set_execaction(list_)

        if self.core.dims.l() > 0:
            list_ = []
            list_.append('iDl')
            list_.append('Dl')
            list_.append('Nlxl')
            if self.core.dims.nl() > 0:
                list_.append('Nlnl')
            if self.core.dims.y() > 0:
                list_.append('Nly')
            self.set_execaction(list_)

        if self.core.dims.nl() > 0:
            list_ = []
            list_.append('Nnlnl')
            if self.core.dims.l() > 0:
                list_.append('Nnlxl')
            if self.core.dims.y() > 0:
                list_.append('Nnly')
            list_.append('c')
            list_.append('Inl')
            list_.append('fnl')
            list_.append('impfunc')
            list_.append('res_impfunc')
            self.set_execaction(list_)

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
        if self.core.dims.l() > 0:
            list_ = []
            list_.append(('vl', 'ud_vl'))
            self.set_execaction(list_)

        list_.append('dxH')
        list_.append('z')
        list_.append('y')
        self.set_execaction(list_)
