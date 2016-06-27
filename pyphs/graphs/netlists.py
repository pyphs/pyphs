# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 08:50:42 2016

@author: Falaize
"""


def sep():
    return ','


class Netlist:
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
    def __init__(self, filename=None):
        """
        init with filename to read data from 'filename.net'
        """
        import config
        self.filename = filename
        self.datum = config.datum
        self.dictionaries = tuple()
        self.components = tuple()
        self.labels = tuple()
        self.nodes = tuple()
        self.arguments = tuple()

    def __getitem__(self, n):
        item = {'dictionary': self.dictionaries[n],
                'component': self.components[n],
                'label': self.labels[n],
                'nodes': self.nodes[n],
                'arguments': self.arguments[n]}
        return item

    def __add__(net1, net2):
        net = net1
        for n2 in range(net2.nlines()):
            net.add_line(net2[n2])
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

    def read(self, filename):
        """
        read and store data from netlist 'filename.net'
        """
        read_netlist(filename, self)

    def write(self, filename):
        """
        write the content of the netlist to file 'filename'
        """
        netlist = ""
        for n in range(self.nlines()):
            netlist += self.line(n)
        file_ = open(filename, 'w')
        file_.write(netlist[:-1])  # remove the last cariage return
        file_.close()

    def line(self, n):
        """
        print the netlist line 'n' whith appropriate format
        """
        return _print_netlist_line(self[n])


def _print_netlist_line(dic):
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
    component = '{}.{} {} {}:'.format(dic['dictionary'], dic['component'],
                                      dic['label'], dic['nodes'])
    pars = ""
    for par in dic['arguments'].keys():
        pars += ' {}={};'.format(par, str(dic['arguments'][par]))
    line = component + pars + '\n'
    return line


def read_netlist(filename, netlist):
    import ast
    file_ = open(filename, "r")
    netlist.__init__()
    with file_ as openfileobject:
        for line in openfileobject:
            # get 'infos' (dic, comp and nodes) and parameters
            infos, _, parameters = line.partition(':')
            # get ‘dic.comp' and 'label nodes'
            diccomp, _, labelnodes = infos.partition(' ')
            dic, _, comp = diccomp.partition('.')
            label, _, nodes = labelnodes.partition(' ')
            netlist.dictionaries = list(netlist.dictionaries)+[dic, ]
            netlist.components = list(netlist.components)+[comp, ]
            netlist.labels = list(netlist.labels)+[label, ]
            netlist.nodes = list(netlist.nodes)+[ast.literal_eval(nodes), ]
            nb_pars = parameters.count('=')
            pars = {}
            for n in range(nb_pars):
                par, _, parameters = parameters.partition(';')
                par = par.replace(' ', '')
                key, _, value = par.partition('=')
                pars.update({key: ast.literal_eval(value)})
            netlist.arguments = list(netlist.arguments)+[pars, ]
    file_.close()
