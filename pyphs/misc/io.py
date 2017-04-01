# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 15:53:51 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

import numpy

try:
    import itertools.izip as zip
except ImportError:
    pass

try:
    import itertools.imap as map
except ImportError:
    pass

import os

numpy_float_resolution = numpy.finfo(float).resolution
float_resolution = int(numpy.abs(numpy.log10(numpy_float_resolution)))

def list2str(l):
    return ('{:} '*len(l)).format(*l)[:-1]  + '\n'


def open_files(path, files_to_open):
    files = {}
    for var in files_to_open:
        _file = open(path + os.sep + var + '.txt', 'w')
        files.update({var: _file})
    return files


def close_files(files):
    for key in files:
            _file = files[key]
            _file.close()


def dump_files(nums, files):
    for key in files:
        _file = files[key]
        obj = getattr(nums, key)()
        if not isinstance(obj, list):
            obj = list(obj.flatten())
        _file.write(list2str(obj))


def write_data(path, seq, var):
    if not os.path.exists(path):
        os.makedirs(path)
    _file = open(path + os.sep + var + '.txt', 'w')
    for el in seq:
        _file.write(list2str(el))
    _file.close()
    return


def data_generator(filename, ind=None, decim=1,
                   postprocess=None, imin=0, imax=None):
    if imax is None:
        imax = float('Inf')
    f = open(filename, "r")
    i = 0
    for line in f:
        if imin <= i < imax and not bool(i % decim):
            if ind is None:
                out = [float(x) for x in line.split()]
                if postprocess is None:
                    y = out
                else:
                    y = list(map(postprocess, out))
                yield y
            else:
                assert isinstance(ind, int), 'Index should be an \
    integer. Got {0!s}'.format(type(ind))
                out = float(line.split()[ind])
                yield out if postprocess is None else postprocess(out)
        i += 1


def load_data(phs, var, ind=None, decim=1,
              postprocess=None, imin=0, imax=None):
    filename = phs.folders['data']+os.sep+var+'.txt'
    data = data_generator(filename, ind=ind, decim=decim,
                          postprocess=postprocess, imin=imin, imax=imax)
    return [el for el in data]


def load_io(numerics):
    load_options = numerics.config['load_options']
    numerics.seq_u = load_data(numerics.phs, 'u', **load_options)
    numerics.seq_y = load_data(numerics.phs, 'y', **load_options)
    return len(numerics.seq_u)


def load_storage(numerics):
    load_options = numerics.config['load_options']
    numerics.seq_x = load_data(numerics.phs, 'x', **load_options)
    numerics.seq_dtx = load_data(numerics.phs, 'dx',
                                 postprocess=lambda dx: dx*numerics.fs,
                                 **load_options)
    numerics.seq_dxHd = load_data(numerics.phs, 'dxHd', **load_options)
    return len(numerics.seq_dxHd)


def load_dissipation(numerics):
    load_options = numerics.config['load_options']
    numerics.seq_w = load_data(numerics.phs, 'w', **load_options)
    numerics.seq_z = load_data(numerics.phs, 'z', **load_options)
    return len(numerics.seq_w)


def load_all(numerics):
    list_powers = list()
#    if numerics.phs.nx() > 0:
    nt = load_storage(numerics)
    list_powers.append(zip(numerics.seq_dtx, numerics.seq_dxHd))
    nt = load_dissipation(numerics)
    list_powers.append(zip(numerics.seq_w, numerics.seq_z))
    nt = load_io(numerics)
    list_powers.append(zip(numerics.seq_u, numerics.seq_y))
    imin = numerics.config['load_options']['imin']
    decim = numerics.config['load_options']['decim']
    t0 = imin*numerics.fs
    fsdecim = float(numerics.fs)/float(decim)
    numerics.seq_t = [t0 + el*fsdecim**-1 for el in range(nt)]
    numerics.nt = nt

    from utils.parallelize import parallel_map
    numerics.seq_dtE, numerics.seq_pd, numerics.seq_ps = \
        parallel_map(scalar_product, list_powers)


def scalar_product(tup):
    """
    Used to parallelize the computation of power balance elements
    Yields [sum([e1*e2 for (e1, e2) in zip(l1, l2)]) for (l1, l2) in tup]
    """
    return [sum([e1*e2 for (e1, e2) in zip(l1, l2)]) for (l1, l2) in tup]
