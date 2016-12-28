#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 13:39:59 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

from pyphs.numerics.tools import PHSNumericalOperation
from pyphs.numerics.method import PHSNumericalMethod


class PHSNumericalMethodStandard(PHSNumericalMethod):

    def __init__(self, core):
        PHSNumericalMethod.__init__(self, core)

        operation = 'add'
        args = (self.x_symb, self.dx_symb)
        ud_x = PHSNumericalOperation(operation, args)
        self.setfunc('ud_x', ud_x)

        operation = 'inv'
        args = (self.iDl_symb, )
        Dl = PHSNumericalOperation(operation, args)
        self.setfunc('Dl', Dl)

        operation = 'dot'
        args = (self.Dl_symb, self.barNlxl_symb)
        Nlxl = PHSNumericalOperation(operation, args)
        self.setfunc('Nlxl', Nlxl)

        operation = 'dot'
        args = (self.Dl_symb, self.barNlnl_symb)
        Nlnl = PHSNumericalOperation(operation, args)
        self.setfunc('Nlnl', Nlnl)

        operation = 'dot'
        args = (self.Dl_symb, self.barNly_symb)
        Nly = PHSNumericalOperation(operation, args)
        self.setfunc('Nly', Nly)

        operation = 'dot'
        args = (self.barNnll_symb, self.barNlxl_symb)
        temp = PHSNumericalOperation(operation, args)
        operation = 'add'
        args = (self.barNnlxl_symb, temp)
        Nnlxl = PHSNumericalOperation(operation, args)
        self.setfunc('Nnlxl', Nnlxl)

        operation = 'dot'
        args = (self.barNnll_symb, self.barNlnl_symb)
        temp = PHSNumericalOperation(operation, args)
        operation = 'add'
        args = (self.barNnlnl_symb, temp)
        Nnlnl = PHSNumericalOperation(operation, args)
        self.setfunc('Nnlnl', Nnlnl)

        operation = 'dot'
        args = (self.barNnll_symb, self.barNly_symb)
        temp = PHSNumericalOperation(operation, args)
        operation = 'add'
        args = (self.barNnly_symb, temp)
        Nnly = PHSNumericalOperation(operation, args)
        self.setfunc('Nnly', Nnly)

        operation = 'dot'
        args = (self.Nnlxl_symb, self.xl_symb)
        temp1 = PHSNumericalOperation(operation, args)
        operation = 'dot'
        args = (self.Nnly_symb, self.u_symb)
        temp2 = PHSNumericalOperation(operation, args)
        operation = 'add'
        args = (temp1, temp2)
        c = PHSNumericalOperation(operation, args)
        self.setfunc('c', c)

        operation = 'dot'
        args = (self.Inl_symb, self.vnl_symb)
        temp1 = PHSNumericalOperation(operation, args)
        operation = 'dot'
        args = (self.Nnlnl_symb, self.fnl_symb)
        temp2 = PHSNumericalOperation(operation, args)
        operation = 'dot'
        args = (-1., temp2)
        temp3 = PHSNumericalOperation(operation, args)
        operation = 'add'
        args = (temp1, temp3)
        temp4 = PHSNumericalOperation(operation, args)
        operation = 'dot'
        args = (-1., self.c_symb)
        temp5 = PHSNumericalOperation(operation, args)
        operation = 'add'
        args = (temp4, temp5)
        impfunc = PHSNumericalOperation(operation, args)
        self.setfunc('impfunc', impfunc)

        self.setfunc('save_impfunc', self.impfunc_symb)

        operation = 'dot'
        args = (self.Nnlnl_symb, self.jac_fnl_symb)
        temp1 = PHSNumericalOperation(operation, args)
        operation = 'dot'
        args = (-1., temp1)
        temp2 = PHSNumericalOperation(operation, args)
        operation = 'add'
        args = (self.Inl_symb, temp2)
        jac_impfunc = PHSNumericalOperation(operation, args)
        self.setfunc('jac_impfunc', jac_impfunc)

        operation = 'inv'
        args = (self.jac_impfunc_symb, )
        ijac_impfunc = PHSNumericalOperation(operation, args)
        self.setfunc('ijac_impfunc', ijac_impfunc)

        operation = 'norm'
        args = (self.impfunc_symb, )
        res_impfunc = PHSNumericalOperation(operation, args)
        self.setfunc('res_impfunc', res_impfunc)

        operation = 'dot'
        args = (-1., self.save_impfunc_symb)
        temp1 = PHSNumericalOperation(operation, args)
        operation = 'add'
        args = (self.impfunc_symb, temp1)
        temp2 = PHSNumericalOperation(operation, args)
        operation = 'norm'
        args = (temp2, )
        step_impfunc = PHSNumericalOperation(operation, args)
        self.setfunc('step_impfunc', step_impfunc)

        operation = 'dot'
        args = (self.ijac_impfunc_symb, self.impfunc_symb)
        temp1 = PHSNumericalOperation(operation, args)
        operation = 'dot'
        args = (-1., temp1)
        temp2 = PHSNumericalOperation(operation, args)
        operation = 'add'
        args = (self.vnl_symb, temp2)
        ud_vnl = PHSNumericalOperation(operation, args)
        self.setfunc('ud_vnl', ud_vnl)

        operation = 'dot'
        args = (self.Nlxl_symb, self.xl_symb)
        temp1 = PHSNumericalOperation(operation, args)
        operation = 'dot'
        args = (self.Nlnl_symb, self.fnl_symb)
        temp2 = PHSNumericalOperation(operation, args)
        operation = 'add'
        args = (temp1, temp2)
        temp3 = PHSNumericalOperation(operation, args)
        operation = 'dot'
        args = (self.Nly_symb, self.u_symb)
        temp4 = PHSNumericalOperation(operation, args)
        operation = 'add'
        temp3 = (temp3, temp4)
        ud_vl = PHSNumericalOperation(operation, args)
        self.setfunc('ud_vl', ud_vl)

        operation = 'dot'
        args = (self.Nyl_symb, self.vl_symb)
        temp1 = PHSNumericalOperation(operation, args)
        operation = 'dot'
        args = (self.Nynl_symb, self.fnl_symb)
        temp2 = PHSNumericalOperation(operation, args)
        operation = 'add'
        args = (temp1, temp2)
        temp3 = PHSNumericalOperation(operation, args)
        operation = 'dot'
        args = (self.Nyy_symb, self.u_symb)
        temp4 = PHSNumericalOperation(operation, args)
        operation = 'add'
        temp3 = (temp3, temp4)
        ud_y = PHSNumericalOperation(operation, args)
        self.setfunc('ud_y', ud_y)

        self.setupdate()

    def setupdate(self):
        iterstruc = len(set(self.M_args).intersection(set(self.vnl_args)))
        list_ = []
        list_ += [('x', 'ud_x'), ]
        if bool(iterstruc):
            self.setupdate_exec(list_)
            list_ = []
        list_ += [('Dl', 'Dl')]
        list_ += [('Nlxl', 'Nlxl')]
        list_ += [('Nlnl', 'Nlnl')]
        list_ += [('Nly', 'Nly')]
        list_ += [('Nnlxl', 'Nnlxl')]
        list_ += [('Nnlnl', 'Nnlnl')]
        list_ += [('Nnly', 'Nnly')]
        list_ += [('Nyl', 'Nyl')]
        list_ += [('Nynl', 'Nynl')]
        list_ += [('Nyy', 'Nyy')]
        list_ += [('c', 'c')]
        list_ += [('impfunc', 'impfunc')]
        if not bool(iterstruc):
            self.setupdate_exec(list_)
            list_ = []
        list_ += [('jac_impfunc', 'jac_impfunc')]
        list_ += [('vnl', 'ud_vnl'), ]
        list_ += [('impfunc', 'impfunc')]
        list_ += [('res_impfunc', 'res_impfunc')]
        list_ += [('step_impfunc', 'step_impfunc')]
        self.setupdate_iter(list_,
                            self.res_impfunc_symb,
                            self.step_impfunc_symb)
        list_ = []
        list_ += [('y', 'ud_y')]
        self.setupdate_exec(list_)
