#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 15 20:19:21 2017

@author: Falaize
"""

from ..tools import types, simplify
from sympy import Matrix


def inverse(Mat, dosimplify=False):
    """
    same method for every matrix inversions
    """
    if Mat.shape == (0, 0):
        return Mat
    else:
        iMat = Mat.inv()
        if dosimplify:
            iMat = simplify(iMat)
        return iMat


def matvecprod(mat, vec):
    """
    Safe dot product of a matrix whith shape (m, n) and a vector (list)
    """

    types.matrix_test(mat)
    m, n = mat.shape

    types.vector_test(vec)
    l = len(vec)
    vec = types.matrix_types[0](vec)

    if not l == n:
        text = 'Matrix shape ({}) and vector shape ({}) do not coincide.'
        raise IndexError(text.format((m, n), l))

    if l == 0:
        res = [0,]*m
    else:
        res = list(mat * Matrix(vec))
#        if m == 1:
#            res = [res, ]
    return res
