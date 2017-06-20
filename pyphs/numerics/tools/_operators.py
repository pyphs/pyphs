#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 20:14:54 2017

@author: Falaize
"""
import numpy


# =========================================================================== #

def norm(x):
    """
Returns the discrete L2 norm of list of floats x considered as a vector:

.. math:: \parallel \mathbf{x} \parallel = \sqrt{\mathbf{x}^\intercal \cdot \mathbf{x}}

Parameter
---------
x : list of floats

Return
------
n : float
    L2 norm of x considered as a vector.
    """
    x = numpy.array(x)
    return numpy.sqrt(numpy.einsum('i,i', x, x))
