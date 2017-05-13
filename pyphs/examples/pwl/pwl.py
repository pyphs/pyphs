# -*- coding: utf-8 -*-
"""
Created on Wed May 10 23:48:24 2017

@author: Falaize

Use data_generator.py to generate a valid data.txt;
Uncomment below to regenerate the netlist.

"""


from pyphs import PHSGraph
import os
import sympy as sp

label = 'PWL'
netlist_path = os.path.join(os.getcwd(), 'pwl.net')
graph = PHSGraph(netlist=netlist_path, label=label)
core = graph.buildCore()
    
if __name__ == '__main__':
    sp.plot(graph.core.H, (graph.core.x[0], -10, 10))
    sp.plot(graph.core.z[0], (graph.core.w[0], -10, 10))
