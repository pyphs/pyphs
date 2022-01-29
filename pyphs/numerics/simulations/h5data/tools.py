#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 20:54:23 2019

@author: Fabrice Silva

"""

from __future__ import absolute_import, division, print_function
import numpy as np
from pyphs.config import VERBOSE
import itertools

from_iterable = itertools.chain.from_iterable


# Naive method: Python-side scan of the iterable
# def set_dataset_from_iterable_naive(dataset, iterable, chunksize=1024):
#     """
#     Dump data from iterable in an h5py dataset naively, expecting elements of
#     iterable are numpy arrays.
#     """
#     offset, npt = 0, chunksize
#     while npt:
#         buffer = [el for ind, el in zip(range(chunksize), iterable)]
#         npt = len(buffer)
#         dataset[offset:offset+npt] = buffer
#         offset += npt

# Numpy method
def set_dataset_from_iterable(
    dataset, iterable, rslice=None, cslice=None, chunksize=1024
):
    """
    Dump data from 2D array passed as row-major iterable in an h5py dataset
    using flattened numpy array as buffer.

    Parameters
    ----------

    dataset : h5py dataset
        Dataset where to store values from iterable.

    iterable : self-typed
        Iterable whose each element is a 1D array with appropriate shape
        w.r.t cslice. The number of elements is prescribed by rslice.

    rslice : slice or None (optional)
        Slice in the rows of the dataset. If None, the length of the iterable
        must equal the number of rows in the dataset. Default is None.

    cslice : slice or None (optional)
        Slice in the columns of the dataset. If None, the length of each
        elements in the iterable must equal the number of colums in the dataset.
        Default is None.

    chunksize : int (optional)
        The size (i.e. number of rows) in the buffer stored at once in the dataset.
        Default is 1024.

    """

    if cslice is None:
        cslice = slice(None)
        ncols = dataset.shape[1]
    elif cslice.stop is None:
        ncols = dataset.shape[1]
    else:
        ncols = len(range(cslice.stop)[cslice])

    if rslice is None:
        nrows = dataset.shape[0]
    elif rslice.stop is None:
        nrows = dataset.shape[1]
    else:
        nrows = len(range(rslice.stop)[rslice])

    chunksize = min((chunksize, nrows))
    offset = 0

    flattened_iterable = from_iterable(iterable)

    while True:
        if chunksize <= nrows - offset:
            buffer_rslice = slice(offset, offset + chunksize)
            if rslice is not None:
                buffer_rslice = range(rslice.stop)[rslice][buffer_rslice]
            count = chunksize * ncols
            buffer = np.fromiter(flattened_iterable, dataset.dtype, count)
            dataset[buffer_rslice, cslice] = buffer.reshape(chunksize, ncols)
            offset += chunksize
        elif offset == nrows:
            break
        else:
            buffer_rslice = slice(offset, None)
            if rslice is not None:
                buffer_rslice = range(rslice.stop)[rslice][buffer_rslice]
            count = (nrows - offset) * ncols
            buffer = np.fromiter(flattened_iterable, dataset.dtype)
            dataset[buffer_rslice, cslice] = buffer.reshape(-1, ncols)
            break
