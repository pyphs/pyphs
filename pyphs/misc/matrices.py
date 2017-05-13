# -*- coding: utf-8 -*-
"""
Created on Mon May 23 22:46:56 2016

@author: Falaize
"""
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
    