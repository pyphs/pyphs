# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 14:29:46 2016

@author: Falaize
"""
import sympy
from dimensions import names_dims

class Structure:
    """
    Class that serves as a container for structure of PortHamiltonianObject
    * dimensions: see pyphs.structure.dimensions for details
    * J: Structure matrix
    * Jxx: get bloc (x, x) of J
    * setJxx(): set bloc (x, x) of J
    """
    def __init__(self, phs):
        self._names = tuple()
        self.J = sympy.zeros(0)
        setattr(self,
                '_build_get_mat',
                lambda mat: _build_get_mat(phs, self, mat))
        setattr(self,
                '_build_set_mat',
                lambda mat: _build_set_mat(phs, self, mat))
        # define set and get for all structure matrices
        matrices = set()
        for vari in names_dims:
            for varj in phs.dims._names:
                matrices = matrices.union({('J'+vari+varj, (vari, varj))})
        for mat in matrices:
            self._set_block(mat[0], mat[1])

    def _set_block(self, name, dims_names):
        self._names += (name, )
        setattr(self, name, self._build_get_mat(dims_names))
        setattr(self, 'set_'+name, self._build_set_mat(dims_names))

    def __add__(struc1, struc2):
        """
        concatenate structures 1 and 2 J = block_diag(J1, J2)
        """
        struc = struc1
        for vari in names_dims:
            for varj in names_dims:
                Jij1 = getattr(struc1, 'J'+vari+varj)()
                Jij2 = getattr(struc2, 'J'+vari+varj)()
                Jij1 = sympy.diag(Jij1, Jij2)
                getattr(struc, 'set_J'+vari+varj)(Jij1)
        return struc


def _build_get_mat(phs, struct, dims_names):
    """
    mat is ('M', ('m', 'n')) with M the matrix argument to define and 'x' and \
'y' the variables that corresponds to block of struct.J
    """
    namei, namej = dims_names

    def get_mat():
        """
        return bloc (""" + namei + ', ' + namej + """) of structure matrix J.
        """
        debi, endi = getattr(phs.inds, namei)()
        debj, endj = getattr(phs.inds, namej)()
        return struct.J[debi:endi, debj:endj]
    return get_mat


def _build_set_mat(phs, struct, dims_names):
    """
    mat is ('M', ('m', 'n')) with M the matrix argument to define and 'x' and \
'y' the variables that corresponds to block of struct.J
    """
    vari, varj = dims_names

    def set_mat(val):
        """
        set bloc (""" + vari + ', ' + varj + """) of structure matrix J to val
        """
        if struct.J.shape[0] != phs.dims.tot():
            struct.J = sympy.zeros(phs.dims.tot())
        debi, endi = getattr(phs.inds, vari)()
        debj, endj = getattr(phs.inds, varj)()
        struct.J[debi:endi, debj:endj] = val
    return set_mat

###############################################################################
