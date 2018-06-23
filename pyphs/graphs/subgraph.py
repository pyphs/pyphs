#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 12:37:43 2018

@author: afalaize
"""

from .graph import Graph
import sympy


def nonrealizable_merge_storages(x, H):
    from pyphs import Core
    from pyphs.core.maths import gradient
    y = Core.symbols('y:{0}'.format(len(x)))
    X = Core.symbols('X')
    Y = Core.symbols('Y')
    grad = gradient(H, x)
    igrad = list(map(lambda arg: sympy.solve(arg[0]-arg[2], arg[1])[0],
                 zip(grad, x, y)))
    Q = sum([e.subs(yi, Y) for e, yi in zip(igrad, y)])
    iQ = sympy.solve(Q-X, Y)[0]

    return


class SubGraph(Graph):

    def __init__(self, label, root):
        Graph.__init__(self, label=label)
        self.root = root
        self.core = self.root.core

    def sort_edges(self):
        self.fc_storages = list()
        self.ec_storages = list()
        self.fc_dissipatives = list()
        self.ec_dissipatives = list()
        for edge in self.edges(data=True):
            if edge[-1]['type'] == 'storage' and edge[-1]['ctrl'] == 'f':
                self.fc_storages.append(edge)
            elif edge[-1]['type'] == 'storage' and edge[-1]['ctrl'] == 'e':
                self.ec_storages.append(edge)
            elif edge[-1]['type'] == 'dissipative' and edge[-1]['ctrl'] == 'f':
                self.fc_dissipatives.append(edge)
            elif edge[-1]['type'] == 'dissipative' and edge[-1]['ctrl'] == 'e':
                self.ec_dissipatives.append(edge)

class SubGraphParallel(SubGraph):
    def __init__(self, label):
        SubGraph.__init__(self, label=label)

    def detect_realizability_issue(self):
        self.sort_edges()





