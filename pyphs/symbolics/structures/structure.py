# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 14:29:46 2016

@author: Falaize
"""
import sympy
from pyphs.misc.tools import geteval
class Structure:
    """
    Class that serves as a container for structure of PortHamiltonianObject
    * M = J - R: Structure matrix
    * Mxx: get bloc (x, x) of M
    * set_Mxx(): set bloc (x, x) of M
    """
    def __init__(self, phs):
        self._names = list()
        self.M = sympy.zeros(0)
        setattr(self,
                '_build_get_mat',
                lambda mat, name: _build_get_mat(phs, self, mat, name))
        setattr(self,
                '_build_set_mat',
                lambda mat, name: _build_set_mat(phs, self, mat, name))

    def __add__(phs1, phs2):
        """
        return concatenation of structures for phs 1 and 2 with \
M = block_diag(M1, M2).
        """
        struc = phs1.struc
        for vari in phs1.dims._names:
            for varj in phs1.dims._names:
                Mij1 = getattr(phs1.struc, 'M'+vari+varj)()
                Mij2 = getattr(phs2.struc, 'M'+vari+varj)()
                Mij1 = sympy.diag(Mij1, Mij2)
                getattr(struc, 'set_M'+vari+varj)(Mij1)
        return struc

    def _build_getset(self, phs, dims_names=None):
        """
        define atttributes set and get for all structure matrices
        """
        for part in ['M', 'R', 'J']:
            if dims_names is None:
                dims_names = phs.dims._names
            for vari in dims_names:
                for varj in dims_names:
                    self._set_block(part, part+vari+varj, (vari, varj))

    def _set_block(self, part, name, dims_names):
        "effectively adds get and set attributes"
        self._names += (name, )
        setattr(self,
                name, self._build_get_mat(dims_names, part))
        setattr(self,
                'set_'+name, self._build_set_mat(dims_names, part))


    def J(self):
        """
        return conservative part of structure matrix M = J - R
        """
        return (self.M - self.M.T)/2.

    def R(self):
        """
        return resistive part of structure matrix M = J - R
        """
        return -(self.M + self.M.T)/2.


def _build_get_mat(phs, struct, dims_names, name):
    """
    mat is ('matrix, ('m', 'n')) with matrix the matrix argument to define \
and 'x' and 'y' the variables that corresponds to block of struct.name
    """
    namei, namej = dims_names

    def get_mat():
        """
        return bloc (""" + namei + ', ' + namej + """) of structure matrix M.
        """
        debi, endi = getattr(phs.inds, namei)()
        debj, endj = getattr(phs.inds, namej)()
        return geteval(struct, name)[debi:endi, debj:endj]
    return get_mat


def _build_set_mat(phs, struct, dims_names, name):
    """
    mat is ('matr', ('m', 'n')) with matr the matrix argument to define \
and 'x' and 'y' the variables that corresponds to block of struct.name
    """
    vari, varj = dims_names

    def set_mat(val):
        """
        set bloc (""" + vari + ', ' + varj + """) of structure matrix """ + \
            name + """ to val
        """
        if struct.M.shape[0] != phs.dims.tot():
            struct.M = sympy.zeros(phs.dims.tot())
        if name == 'J':
            J = val
            R = struct.R()
            M = J - R
        if name == 'R':
            J = struct.J()
            R = val
            M = J - R
        if name == 'M':
            M = val
        debi, endi = getattr(phs.inds, vari)()
        debj, endj = getattr(phs.inds, varj)()
        struct.M[debi:endi, debj:endj] = M
    return set_mat

###############################################################################
