# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 14:29:46 2016

@author: Falaize
"""
import sympy


class Structure:
    """
    Class that serves as a container for structure of PortHamiltonianObject
    * nx: dimension of x with x in ('x', 'w', 'y', 'cy')
    * J: Structure matrix
    * Jxx: get bloc xx of J
    * setJxx(): set bloc xx of J
    """
    def __init__(self, pho):
        self.J = sympy.zeros(0)
        _init_dims(self, pho)
        _init_structure(self)

    def __add__(struc1, struc2):
        struc = struc1
        for vari in struc._labels_dims:
            for varj in struc._labels_dims:
                Jij1 = getattr(struc1, 'J'+vari+varj)()
                Jij2 = getattr(struc2, 'J'+vari+varj)()
                Jij1 = sympy.diag(Jij1, Jij2)
                getattr(struc, 'setJ'+vari+varj)(Jij1)
        return struc
##############################################################################


def _init_dims(struct, pho):
    """
    define accessors to len of var 'pho.symbs.nvar'
    """
    names_dims = ('x', 'w', 'y', 'cy')
    setattr(struct, '_labels_dims', names_dims)
    all_labels = ()
    for var in names_dims:
        all_labels += (var, )
        nvar = _dims_by_var(pho, var)
        setattr(pho, 'n' + var, nvar)
        setattr(struct, 'n' + var, getattr(pho, 'n' + var))
        indsvar = _inds_in_all(pho, all_labels)
        setattr(struct, 'ind' + var, indsvar)

    def nall():
        dim = 0
        for var in names_dims:
            dim += getattr(pho, 'n' + var)()
        return dim
    setattr(pho, 'nall', nall)
    setattr(struct, 'nall', getattr(pho, 'nall'))
    np = _dims_by_var(pho, 'p')
    setattr(pho, 'n' + 'p', np)


def _dims_by_var(pho, var):
    """
    return length of 'pho.symbs.var'
    """
    def nvar():
        return len(getattr(pho.symbs, var))
    return nvar


def _inds_in_all(pho, all_vars):
    """
    return position of the last variable in vars = ('var1', 'var2', 'var2')
    """
    def indsvar():
        deb = 0
        for var in all_vars[:-1]:
            deb += getattr(pho, 'n' + var)()
        end = deb + getattr(pho, 'n' + all_vars[-1])()
        return (deb, end)
    return indsvar

##############################################################################


def _init_structure(struct):
    """
    define set and get for all structure matrices
    """
    matrices = set()
    for vari in struct._labels_dims:
        for varj in struct._labels_dims:
            matrices = matrices.union({('J'+vari+varj, (vari, varj))})
    for mat in matrices:
        setattr(struct, mat[0], _build_get_mat(struct, mat))
        setattr(struct, 'set'+mat[0], _build_set_mat(struct, mat))


def _build_get_mat(struct, mat):
    """
    mat is ('M', ('m', 'n')) with M the matrix argument to define and 'x' and \
'y' the variables that corresponds to block of struct.J
    """
    def get_mat():
        vari, varj = mat[1]
        debi, endi = getattr(struct, 'ind'+vari)()
        debj, endj = getattr(struct, 'ind'+varj)()
        return struct.J[debi:endi, debj:endj]
    return get_mat


def _build_set_mat(struct, mat):
    """
    mat is ('M', ('m', 'n')) with M the matrix argument to define and 'x' and \
'y' the variables that corresponds to block of struct.J
    """
    def set_mat(val):
        if struct.J.shape[0] != struct.nall():
            struct.J = sympy.zeros(struct.nall())
        vari, varj = mat[1]
        debi, endi = getattr(struct, 'ind'+vari)()
        debj, endj = getattr(struct, 'ind'+varj)()
        struct.J[debi:endi, debj:endj] = val
    return set_mat

###############################################################################
