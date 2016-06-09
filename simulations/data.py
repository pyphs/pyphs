# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 10:22:56 2016

@author: Falaize
"""

class Data:
    """
    container for simulation data
    """
    def __init__(self, simulation, phs):

        def path(self):
            return phs.paths['data']
        self.path = path

        def options(self):
            return simulation.config['load_options']
        self.options = options

    def data_generator(self, var, ind=None, postprocess=None):
        from misc.io import data_generator
        import os
        filename = self.path() + os.sep + var.lower() + '.txt'
        generator = data_generator(filename, ind=ind, postprocess=postprocess,
                                   **self.options())
        return generator
        