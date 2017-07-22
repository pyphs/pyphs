# -*- coding: utf-8 -*-
"""
Created on Sat May 21 16:29:43 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function
from ..edges import StorageLinear
from pyphs.graphs import datum


class Mass(StorageLinear):
    """
    Mass moving in 1D space

    Parameters
    -----------

    label : str
        Mass component label.

    nodes: (str, )
        Edge is `datum -> nodes[0]`.

    kwargs: dic with following `keys: values`:

        * `M` : Mass `value` or symbol `Mlabel` or tuple `(Mlabel, value)`.
    """
    def __init__(self, label, nodes, **kwargs):
        par_name = 'M'
        par_val = kwargs[par_name]
        kwargs = {'name': par_name,
                  'value': par_val,
                  'inv_coeff': True,
                  'ctrl': 'f'}
        StorageLinear.__init__(self, label, (datum, nodes[0]), **kwargs)

    @staticmethod
    def metadata():
        return {'nodes': ('M'),
                'arguments': {'M': ('M', 1e-2)}}
