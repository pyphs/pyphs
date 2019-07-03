# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 15:53:51 2016

@author: Falaize

This is the old Data class that uses ASCII format
for saving values (not efficient...)

"""
# from __future__ import absolute_import, division, print_function
# import numpy
#
# try:
#     import itertools.imap as map
# except ImportError:
#     pass
#
# import os
#
# numpy_float_resolution = numpy.finfo(float).resolution
# float_resolution = int(numpy.abs(numpy.log10(numpy_float_resolution)))
#
#
# def list2str(l):
#     return ('{:} '*len(l)).format(*l)[:-1] + '\n'
#
#
# def open_files(path, files_to_open):
#     files = {}
#     for var in files_to_open:
#         _file = open(path + os.sep + var + '.txt', 'w')
#         files.update({var: _file})
#     return files
#
#
# def close_files(files):
#     for key in files:
#             _file = files[key]
#             _file.close()
#
#
# def with_files(path, files_to_open, process, files=None):
#     """
# open the files in files_to_open into folder path and execute process(files)
#     """
#     if files is None:
#         files = {}
#     name = files_to_open.pop()
#     with open(os.path.join(path, name + '.txt'), 'w') as files[name]:
#         if len(files_to_open) == 0:
#             process(files)
#             return files
#         else:
#             with_files(path, files_to_open, process, files=files)
#
#
# def dump_files(nums, files):
#     for key in files:
#         _file = files[key]
#         obj = getattr(nums, key)()
#         if not isinstance(obj, list):
#             obj = list(obj.flatten())
#         _file.write(list2str(obj))
#
#
# def write_data(path, seq, var):
#     if not os.path.exists(path):
#         os.makedirs(path)
#     _file = open(path + os.sep + var + '.txt', 'w')
#     for el in seq:
#         _file.write(list2str(el))
#     _file.close()
#     return
#
#
# def data_generator(path, ind=None, decim=None,
#                    postprocess=None, imin=None, imax=None):
#     """
#     Generator that read file from path. Each line is returned as a list of
#     floats, if index i is such that imin <= i < imax, with decimation factor
#     decim. A function can be passed as postprocess, to be applied on each
#     output.
#     """
#
#     if imin is None:
#         imin = 0
#     if imax is None:
#         imax = float('Inf')
#     if decim is None:
#         decim = 1
#
#     if ind is not None and not isinstance(ind, int):
#         text = 'Index should be an integer. Got {0}'
#         text = text.format(type(ind))
#         raise ValueError(text)
#
#     i = 0
#
#     with open(path, "r") as f:
#         for line in f:
#             if imin <= i < imax and not bool((i-imin) % decim):
#                 # export full line
#                 if ind is None:
#                     out = [float(x) for x in line.split()]
#                     if postprocess is None:
#                         y = out
#                     else:
#                         y = list(map(postprocess, out))
#                     yield y
#                 # export selected index in line
#                 else:
#                     out = float(line.split()[ind])
#                     yield out if postprocess is None else postprocess(out)
#             i += 1

#class ASCIIData(BaseData):
#
#    # -------------------------------------------------------------------------
#    def init_data(self, sequ=None, seqp=None, nt=None):
#
#        sequ, seqp, nt = BaseData.__init_data__(self, sequ, seqp, nt)
#        # write input sequence
#        self.write_data(self.config['path']+os.sep+'data', sequ, 'u')
#
#        # write parameters sequence
#        self.write_data(self.config['path']+os.sep+'data', seqp, 'p')
#
#        self._build_generators()
#
#    init_data.__doc__ = BaseData.__init_data__.__doc__
#
#    # -------------------------------------------------------------------------
#
#    def write_data(self, path, seq, var):
#        if not os.path.exists(path):
#            os.makedirs(path)
#        with open(path + os.sep + var + '.txt', 'w') as _file:
#            for el in seq:
#                _file.write(list2str(el))
#
#    # -------------------------------------------------------------------------
#
#    def build_generator(self, name):
#        "Build data_generator from data name."
#        filename = os.path.join(self.config['path'], name + '.txt')
#        default = self.config['load']
#
#        def data_generator(**kwargs):
#            """
#            Generator that read file from path. Each line is returned as a list
#            of floats, if index i is such that imin<=i<imax, with decimation
#            factor decim. A function can be passed as postprocess, to be
#            applied on each output.
#            """
#            imin = kwargs.get('imin', default['imin'])
#            imax = kwargs.get('imax', default['imax'])
#            decim = kwargs.get('decim', default['decim'])
#            ind = kwargs.get('ind', None)
#            postprocess = kwargs.get('postprocess', None)
#
#            if ind is not None and not isinstance(ind, int):
#                raise ValueError('Index should be an integer,not {0}'.format(type(ind)))
#
#            with open(filename, "r") as f:
#                for i, line in enumerate(f):
#                    if (i < imin) or (imax <= i) or ((i - imin) % decim > 0):
#                        continue
#                    if ind is None:
#                        # export full line
#                        out = [float(x) for x in line.split()]
#                        if postprocess is not None:
#                            out = [postprocess(el) for el in out]
#                        yield out
#                    else:
#                        # export selected index in line
#                        out = float(line.split()[ind])
#                        yield out if postprocess is None else postprocess(out)
#
#        data_generator.__doc__ = self.__doc_template__.format(name, filename)
#        return data_generator
#
#
