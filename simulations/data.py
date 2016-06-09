# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 10:22:56 2016

@author: Falaize
"""
from misc.io import data_generator
import os


class Data:
    """
    container for simulation data
    """
    def __init__(self, simulation, phs):

        setattr(self, 'path', phs.paths['data'])
        setattr(self, 'options', simulation.config['load_options'])
        setattr(self, 'fs', simulation.config['fs'])
        setattr(self, 'nt', simulation.nt)

        def dummy_func(name):
            def get_seq(ind=None, postprocess=None):
                return self.data_generator(name, ind=ind,
                                           postprocess=postprocess)
            return get_seq

        for name in list(phs.nums.args_names) + ['yd', 'dxHd', 'z', 'dtx']:
            setattr(self, name, dummy_func(name))

    def t(self):
        imin = self.options['imin']
        imax = self.options['imax']
        if imax is None:
            imax = float('Inf')
        decim = self.options['decim']

        def generator():
            for n in range(self.nt):
                yield n/self.fs
        i = 0
        for el in generator():
            if i >= imin and i < imax:
                if not bool(i % decim):
                    yield el
            i += 1

    def dtE(self):
        """
        Energy variation
        """
        def dxtodtx(dx):
            return dx*self.fs
        for dtx, dxh in zip(self.dx(postprocess=dxtodtx), self.dxHd()):
            yield scalar_product(dtx, dxh)

    def pd(self):
        """
        Dissipated power
        """
        for w, z in zip(self.w(), self.z()):
            yield scalar_product(w, z)

    def ps(self):
        """
        Source power
        """
        for u, yd in zip(self.u(), self.yd(postprocess=lambda el: -el)):
            yield scalar_product(u, yd)

    def data_generator(self, name, ind=None, postprocess=None):
        filename = self.path + os.sep + name.lower() + '.txt'
        generator = data_generator(filename, ind=ind, postprocess=postprocess,
                                   **self.options)
        return generator


def scalar_product(list1, list2):
    return sum(el1*el2 for (el1, el2) in zip(list1, list2))
