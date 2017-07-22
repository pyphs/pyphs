# -*- coding: utf-8 -*-
"""
Created on Wed May 10 23:48:24 2017

@author: Falaize

Use data_generator.py to generate a valid data.txt;
Uncomment below to regenerate the netlist.

"""


from pyphs import Graph
import os
from pyphs.examples.pwl.data_generator import (netlist_name,
                                               generate_data,
                                               generate_netlist)

generate_data()
generate_netlist()
path = os.path.realpath(__file__)[:os.path.realpath(__file__).rfind(os.sep)]
netlist_path = os.path.join(path, netlist_name + '.net')
graph = Graph(netlist=netlist_path, label=netlist_name)
core = graph.to_core()

#if __name__ == '__main__':
#    import sympy as sp
#    sp.plot(graph.core.H, (graph.core.x[0], -10, 10))
#    sp.plot(graph.core.z[0], (graph.core.w[0], -10, 10))
