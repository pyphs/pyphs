# -*- coding: utf-8 -*-
"""
Created on Mon May 23 22:46:56 2016

@author: Falaize
"""
import sympy as sp
import numpy as np


def isequal(M1, M2):
    """
    Test M1==M2 with M1 and M2 of type sympy.Matrix or numpy.matrix
    """
    return not (M1-M2).any()


def get_ind_nonzeros_col(Mat, col):
    col2line = np.transpose(Mat[:, col])
    line2list = col2line.tolist()[0]
    nonzeros = np.nonzero(line2list)[0]
    return list(nonzeros)


def get_ind_nonzeros_row(Mat, row):
    row = Mat[row, :]
    row2list = row.tolist()[0]
    nonzeros = np.nonzero(row2list)[0]
    return list(nonzeros)


def move_col(mat, indi, indf):
    mat = sp.Matrix(mat)
    if indi < indf:
        deb = sp.Matrix.hstack(mat[:, :indi], mat[:, indi+1:indf+1])
        end = mat[:, indf+1:]
        eli = mat[:, indi]
        mat = sp.Matrix.hstack(deb, eli, end)
    elif indi > indf:
        deb = mat[:, :indf]
        end = sp.Matrix.hstack(mat[:, indf:indi], mat[:, indi+1:])
        eli = mat[:, indi]
        mat = sp.Matrix.hstack(deb, eli, end)
    return mat


def move_row(mat, indi, indf):
    mat = sp.Matrix(mat)
    if indi < indf:
        deb = sp.Matrix.vstack(mat[:indi, :], mat[indi+1:indf+1, :])
        end = mat[indf+1:, :]
        eli = mat[indi, :]
        mat = sp.Matrix.vstack(deb, eli, end)
    elif indi > indf:
        deb = mat[:indf, :]
        end = sp.Matrix.vstack(mat[indf:indi, :], mat[indi+1:, :])
        eli = mat[indi, :]
        mat = sp.Matrix.vstack(deb, eli, end)
    return mat

if __name__ is '__main__':
    M = np.matrix(np.eye(4))
    print(M)
    print(get_ind_nonzeros_col(M, 2))
    print(get_ind_nonzeros_row(M, 2))

    lis = range(10)
    mat = np.eye(4, dtype=int)
    print(np.matrix(move_row(mat, 1, 2)))
