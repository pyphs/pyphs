# -*- coding: utf-8 -*-
"""
Created on Sat May 21 16:29:43 2016

@author: Falaize
"""


from utils.dic import linear_storage_fc, linear_storage_ec, linear_diss_ic, \
    linear_diss_fc, linear_diss_ec, nonlinear_dissipative

import sympy as sp
from utils.dic import nice_var_label

class Stiffness(linear_storage_fc):
    """
    Linear stiffness
    """
    def __init__(self, label, nodes_labels, value):
        linear_storage_fc.__init__(self, label, nodes_labels,
                                   value, inv_par=False)


class Mass(linear_storage_ec):
    """
    Linear inductor
    """
    def __init__(self, label, nodes_labels, value):
        linear_storage_ec.__init__(self, label, nodes_labels, value)


class Damper(linear_diss_ic):
    """ Linear resistor (indeterminate control)
    """
    def __init__(self, label, nodes_labels, value):
        linear_diss_ic.__init__(self, label, nodes_labels, value)


class Damper_fc(linear_diss_fc):
    """ Linear flux-controlled resistor
    """
    def __init__(self, label, nodes_labels, value):
        linear_diss_fc.__init__(self, label, nodes_labels, value)


class Damper_ec(linear_diss_ec):
    """ Linear effort-controlled resistor
    """
    def __init__(self, label, nodes_labels, value):
        linear_diss_ec.__init__(self, label, nodes_labels, value)


#
#from pypHs import pHobj
#import sympy as sp
#import numpy as np
#from sympy.physics import units
#
#class stiffness(pHobj):
#    """ Linear Capacitor
#    usgae: capacitor label ['n1','n2'] [value]
#
#    """
#    def __init__(self, label, nodes_labels, value):
#        pHobj.__init__(self,label)
#        if type(value[0])==tuple:
#            string = value[0][0]
#            K = sp.symbols(string)
#            subs = {string:value[0][1]}            
#            pars = [K]
#        else:
#            K = value[0]
#            subs = {}            
#            pars = []
#        self.subs.update(subs)
#        self.params += pars
#
#        self.AddLinearStorageComponents(["x"+label],[K], [units.m])
#        edge_data_dic = {'ref':"x"+label, 'type':'storage', 'realizability':'flux_controlled', 'linear':True, 'link_ref':"x"+label}
#        self.Graph.add_edges_from([(nodes_labels[0], nodes_labels[1], edge_data_dic)])
#        
#class mass(pHobj):
#    """ Linear Inductor
#    """
#    def __init__(self,label,nodes_labels,value):
#        pHobj.__init__(self,label)
#        if type(value[0])==tuple:
#            string = value[0][0]
#            m = sp.symbols(string)
#            subs = {string:value[0][1]}            
#            pars = [m]
#        else:
#            m = value[0]
#            subs = {}            
#            pars = []
#        self.subs.update(subs)
#        self.params += pars
#
#        self.AddLinearStorageComponents(["x"+label],[1./m], [units.kg*units.m/units.s])
#        edge_data_dic = {'ref':"x"+label, 'type':'storage', 'realizability':'effort_controlled', 'linear':True, 'link_ref':"x"+label}
#        self.Graph.add_edges_from([(nodes_labels[0], nodes_labels[1], edge_data_dic)])
#
#class damper(pHobj):
#    """ Linear Resistor
#    """
#    def __init__(self,label,nodes_labels,value):
#        pHobj.__init__(self,label)
#        if type(value[0])==tuple:
#            string = value[0][0]
#            a = sp.symbols(string)
#            subs = {string:value[0][1]}            
#            pars = [a]
#        else:
#            a = value[0]
#            subs = {}            
#            pars = []
#        self.subs.update(subs)
#        self.params += pars
#
#        self.AddLinearDissipativeComponents(["w"+label],[a], [units.m/units.s])
#        edge_data_dic = {'ref':"w"+label, 'type':'dissipative', 'realizability':'?', 'linear':True, 'link_ref':"w"+label}
#        self.Graph.add_edges_from([(nodes_labels[0], nodes_labels[1], edge_data_dic)])
