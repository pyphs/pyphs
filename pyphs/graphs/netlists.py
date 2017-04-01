# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 08:50:42 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import os
import ast
from pyphs.config import datum


def sep():
    return ','


class PHSNetlist:
    """
    Data structure for netlist elements. Each line of the netlist describes a\
 component, with data structured a follows
    > dic.comp label N1, N2, ..., Nn: par1=(lab, val) par2=val par3=lab
    where
    * component 'comp' is a module of dictionary 'dictionary.dic',
    * label is the component label (avoid creativity in chosen characters),
    * the N's are the nodes labels, which can be strings or numbers,
    * the par's are parameters identifiers defined in the component
    * lab is a new string label for the parameter,
    * val is a numerical value for the parameter.

    If no numerical value is provided, the parameter will be defined as a \
free-parameter that can be continuously controlled during the simulations. \
Else if no label is provided for the new component, the new label for the \
i-th parameter is defined as 'label_pari'.
    """
    def __init__(self, filename, clear=False):
        """
        init with filename to read data from 'filename.net'
        """
        self.filename = filename
        if not os.path.isfile(self.filename) or clear:
            file_ = open(self.filename, 'w')
            file_.close()
        self.datum = datum
        self.dictionaries = tuple()
        self.components = tuple()
        self.labels = tuple()
        self.nodes = tuple()
        self.arguments = tuple()
        self.read()

    def __getitem__(self, n):
        item = {'dictionary': self.dictionaries[n],
                'component': self.components[n],
                'label': self.labels[n],
                'nodes': self.nodes[n],
                'arguments': self.arguments[n]}
        return item

    def __add__(net1, net2):
        net = net1
        for l in net2:
            net.add_line(l)
        return net

    def nlines(self):
        """
        return the number of lines in the netlist (i.e. the number of \
components).
        """
        return len(self.components)

    def add_line(self, dic):
        self.dictionaries = list(self.dictionaries)+[dic['dictionary'], ]
        self.components = list(self.components)+[dic['component'], ]
        self.labels = list(self.labels)+[dic['label'], ]
        self.nodes = list(self.nodes)+[dic['nodes'], ]
        self.arguments = list(self.arguments)+[dic['arguments'], ]

    def read(self):
        """
        read and store data from netlist 'filename.net'
        """
        file_ = open(self.filename, "r")
        with file_ as openfileobject:
            for line in openfileobject:
                # get 'infos' (dic, comp and nodes) and parameters
                infos, _, parameters = line.partition(':')
                # get ‘dic.comp' and 'label nodes'
                diccomp, _, labelnodes = infos.partition(' ')
                dic, _, comp = diccomp.partition('.')
                label, _, nodes = labelnodes.partition(' ')
                self.dictionaries = list(self.dictionaries)+[dic, ]
                self.components = list(self.components)+[comp, ]
                self.labels = list(self.labels)+[label, ]
                self.nodes = list(self.nodes)+[ast.literal_eval(nodes), ]
                nb_pars = parameters.count('=')
                pars = {}
                for n in range(nb_pars):
                    par, _, parameters = parameters.partition(';')
                    par = par.replace(' ', '')
                    key, _, value = par.partition('=')
                    try:
                        value = ast.literal_eval(value)
                    except ValueError:
                        pass
                    pars.update({key: value})
                self.arguments = list(self.arguments)+[pars, ]
        file_.close()

    def netlist(self):
        """
        Return the netlist as a formated string
        """
        netlist = ""
        for n in range(self.nlines()):
            netlist += self.line(n)
        return netlist[:-1]

    def write(self, filename=None):
        """
        write the content of the netlist to file 'filename'
        """
        if filename is None:
            filename = self.filename
        file_ = open(filename, 'w')
        file_.write(self.netlist())  # remove the last cariage return
        file_.close()

    def line(self, n):
        """
        print the netlist line 'n' whith appropriate format
        """
        return print_netlist_line(self[n])

    def setline(self, n, line):
        """
        set the netlist line 'n' whith provided dictionary
        """
        value = line['dictionary']
        try:
            value = ast.literal_eval(value)
        except ValueError:
            pass
        self.dictionaries[n] = value

        value = line['component']
        try:
            value = ast.literal_eval(value)
        except ValueError:
            pass
        self.components[n] = value

        value = line['label']
        try:
            value = ast.literal_eval(value)
        except (ValueError, SyntaxError):
            pass
        self.labels[n] = value

        value = line['nodes']
        self.nodes[n] = value

        value = line['arguments']
        self.arguments[n] = value


def print_netlist_line(dic):
    """
    Return the line of the pyphs netlist associated to
    > dic.comp label nodes parameters

    Parameters
    ----------

    item : dict

        Dictionary that encodes the component with keys:

            * 'dictionary': str

                module in 'pyphs/dicitonary/'

            * 'component':

                component in 'dictionary'

            * 'label':

                component label

            * 'nodes':

                tuple of nodes identifiers

            * 'arguments': dict

                Dictionary of parameters. Keys are parameters labels in \
dic.comp, and values are float (parameter value), str (new parameter label) \
or tuple (str, float).

    Output
    -------

    line : str

        Formated string that corresponds to a single line in the netlist \
        (includes end cariage return).
    """
    
    component = '{0}.{1} {2} {3}:'.format(dic['dictionary'], 
                                          dic['component'],
                                          dic['label'], 
                                          dic['nodes'])
    pars = ""
    if dic['arguments'] is not None:
        for par in dic['arguments'].keys():
            pars += ' {}={};'.format(par, str(dic['arguments'][par]))
    line = component + pars + '\n'
    return line
