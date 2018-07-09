#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fry May 25 15:23:49 2018
by @author: Najnudel

Modified on Thr Jul 25 23:12:34 2018
by @author: afalaize

"""
#import warnings
#from pyphs.dictionary import pwl
#from pyphs.dictionary.pwl.tools import data_generator
#import numpy as np
#import os
#
#
#def PWL(X, Y, Xin):
#    n = len(X)
#    if n < 2:
#        raise ValueError('X must contain at least 2 elements')
#    if len(Y) != n:
#        raise ValueError('Y and X must have same length')
#    if not all(Y[i] < Y[i+1] and X[i] < X[i+1] for i in range(n-1)):
#        raise ValueError('PWL must be increasing')
#    if not 0 in X or Y[np.where(X==0)] != 0:
#        raise ValueError('PWL of zero must be zero')
#    else:
#        Yout = []
#        for x in Xin:
#            Xtemp = np.append(X,x)
#            Xtemp.sort()
#            i, = np.where(Xtemp==x)
#            if len(i) > 1:
#                y = Y[i[0]]
#            else :
#                if i == 0:
#                    y = (Y[1]-Y[0])/(Xtemp[2]-Xtemp[1])*(x-Xtemp[1]) + Y[0]
#                elif i == n:
#                    y = (Y[n-1]-Y[n-2])/(Xtemp[n-1]-Xtemp[n-2])*(x-Xtemp[n-2]) + Y[n-2]
#                else:
#                    y =  (Y[i]-Y[i-1])/(Xtemp[i+1]-Xtemp[i-1])*(x-Xtemp[i-1]) + Y[i-1]
#            Yout = np.append(Yout,y)
#        Yout.sort()
#        return Yout
#
#
#def PWL_inv(X, Y):
#    n = len(X)
#    if n < 2:
#        raise ValueError('X must contain at least 2 elements')
#    if len(Y) != n:
#        raise ValueError('Y and X must have same length')
#    if not all(Y[i] < Y[i+1] and X[i] < X[i+1] for i in range(n-1)):
#        raise ValueError('PWL must be increasing')
#    if not 0 in X or Y[np.where(X==0)] != 0:
#        raise ValueError('PWL of zero must be zero')
#    else:
#        return Y, X
#
#
#def PWL_comp(X, Y1, Y2, Z):
#    Zout = PWL(Y2, Z, Y1)
#    return X, Zout
#
#
#def PWL_sum(XX, YY, tol=2):
#    eps = np.finfo(float).eps
#    n = len(XX)
#    Xout = []
#    Yout = []
#    for i in range(n):
#        Ytemp = list(YY[i])
#        for k in range(n):
#            if k != i:
#                Ytemp += PWL(XX[k], YY[k], XX[i])
#        Yout = np.append(Yout, [y for y in Ytemp if not any(y/(el+eps) - 1 <= tol*eps for el in Yout)])
#        Yout.sort()
#        Xout = np.append(Xout, [x for x in XX[i] if not any(x/(el+eps) - 1 <= tol*eps for el in Xout)])
#        Xout.sort()
#    return Xout, Yout
#
#
#def PWL_integ(X, Y):
#    p = X[1]-X[0]  #step is supposedly constant
#    Yout = []
#    z, = np.where(X==0)
#    z = z[0]
#    for i in range(len(X)):
#        if z < i:
#            integ = p*(Y[z+1:i].sum() + Y[i]/2)  #trapezoidal rule
#        else:
#            integ = -p*(Y[i+1:z].sum() + Y[i]/2)
#        Yout = np.append(Yout, integ)
#    return X, Yout
#
#
#def PWL_Heq(XX, YY, tol=2):
#    n = len(XX)
#    XXo = []
#    YYo = []
#    Xq, Yq = PWL_sum(YY, XX, tol)
#    for i in range(n):
#        Xint, Yint = PWL_integ(XX[i], YY[i])
#        Xint, Yint = PWL_comp(YY[i], XX[i], Xint, Yint)
#        XXo.append(Xint)
#        YYo.append(Yint)
#    X, Y = PWL_sum(XXo, YYo, tol)
#    Xout, Yout = PWL_comp(Yq, Xq, X, Y)
#    return Xout, Yout
#
#
#def get_key(dic, value):
#    for k, v in dic.items():
#            if v == value:
#                return k
#
#
#def isStorage(edge):
#    _, _, dic = edge
#    return (dic['type'] == 'storage')
#
#
#def initialize_Heq():
#    XX, YY = [], []
#    label = 'Heq_'
#    keys = []
#    nodeslist = []
#    return XX, YY, label, keys, nodeslist
#
#
#def replace_Heq_par(graph, keys, nodes, path, label):
#    """
#        Replace all parallel storages within a parallel graph with
#        equivalent storage
#
#        Parameters
#        ---------
#
#        graph : Graph
#            Graph object to be modified
#
#        keys : list
#            list of edges keys to be removed
#
#        nodes : tuple
#            tuple of edges nodes to be removed
#
#        path : str
#            path to file containing pwl values of equivalent storage
#
#        label : str
#            label of the equivalent storage
#        """
#    for key in keys:
#        graph.remove_edge(*nodes, key)
#    dic = {'file':path, 'integ':False, 'ctrl':'f'}
#    Heq = pwl.Storage(label, nodes, **dic)
#    graph += Heq
#    warnings.warn('Replacing parallel storage with equivalent storage ' + label)
#
#
#def replace_Heq_ser(graph, keys, nodeslist, path, label, firstnode, lastnode):
#    """
#        Replace all serial storages within a serial graph with
#        equivalent storage
#
#        Parameters
#        ---------
#
#        graph : Graph
#            Graph object to be modified
#
#        keys : list
#            list of edges keys to be removed
#
#        nodeslist : list
#            list of edges nodes to be removed
#
#        path : str
#            path to file containing pwl values of equivalent storage
#
#        label : str
#            label of the equivalent storage
#
#        firstnode : str
#            first node of the equivalent storage
#
#        lastnode : str
#            last node of the equivalent storage
#        """
#    for key, nodes in zip(keys, nodeslist):
#        graph.remove_edge(*nodes, key)
#    dic = {'file':path, 'integ':False, 'ctrl':'e'}
#    Heq = pwl.Storage(label, (firstnode, lastnode), **dic)
#    graph += Heq
#    warnings.warn('Replacing serial storages with equivalent storage ' + label)
#
#
#def graph_analysis_serial(graph):
#    """
#        Walk through a serial graph and perform replace_Heq_ser wherever possible
#    """
#    edges = graph.edgeslist
#    XX, YY, label, keys, nodeslist = initialize_Heq()
#    nodesbin = []
#    for edge in edges:
#        node1, node2, dic = edge
#        nodes = node1, node2
#        data = graph.get_edge_data(*nodes)
#        key = get_key(data, dic)
#        if isStorage(edge) and dic['ctrl'] == 'e':
#            keys.append(key)
#            nodeslist.append(nodes)
#            path = dic['file']
#            vals = np.vstack(map(np.array, data_generator(path)))
#            x_vals = vals[0, :]
#            h_vals = vals[1, :]
#            XX.append(x_vals)
#            YY.append(h_vals)
#            label += str(dic['label'])
#            if len(keys) == 1:
#                firstnode = node1
#            else:
#                nodesbin.append(node1)
#            lastnode = node2
#            if edges.index(edge) == len(edges)-1 and len(keys) > 1:
#                Xeq, Yeq = PWL_Heq(XX, YY)
#                path = os.path.join(os.getcwd(), label + '_data.pwl')
#                np.savetxt(path, np.vstack((Xeq, Yeq)))
#                replace_Heq_ser(graph, keys, nodeslist, path, label, firstnode, lastnode)
#                XX, YY, label, keys, nodeslist = initialize_Heq()
#        elif len(keys) > 1:
#                Xeq, Yeq = PWL_Heq(XX, YY)
#                path = os.path.join(os.getcwd(), label + '_data.pwl')
#                np.savetxt(path, np.vstack((Xeq, Yeq)))
#                replace_Heq_ser(graph, keys, nodeslist, path, label, firstnode, lastnode)
#                XX, YY, label, keys, nodeslist = initialize_Heq()
#        else:
#            XX, YY, label, keys, nodeslist = initialize_Heq()
#    graph.remove_nodes_from(nodesbin)
#
#
#def graph_analysis_parallel(graph):
#    """
#        Walk through a parallel graph and perform replace_Heq_par wherever possible
#    """
#    edges = graph.edgeslist
#    XX, YY = [], []
#    label = 'Heq_'
#    keys = []
#    nodes = edges[0][0], edges[0][1]
#    for edge in edges:
#        _, _, dic = edge
#        data = graph.get_edge_data(*nodes)
#        key = get_key(data, dic)
#        if isStorage(edge) and dic['ctrl'] == 'f':
#            keys.append(key)
#            path = dic['file']
#            vals = np.vstack(map(np.array, data_generator(path)))
#            x_vals = vals[0, :]
#            h_vals = vals[1, :]
#            XX.append(x_vals)
#            YY.append(h_vals)
#            label += str(dic['label'])
#    if len(keys) > 1:
#        Xeq, Yeq = PWL_Heq(XX, YY)
#        path = os.path.join(os.getcwd(), label + '_data.pwl')
#        np.savetxt(path, np.vstack((Xeq, Yeq)))
#        replace_Heq_par(graph, keys, nodes, path, label)
#
#
#def graph_eq(splitgraph):
#    """
#        Walk through a split graph (call Graph.sp_split method first) and perform
#        replace_Heq_par and replace_Heq_ser wherever possible
#    """
#    edges = splitgraph.edgeslist
#    for edge in edges:
#        if edge[2]['type'] == 'graph':
#            subgraph = edge[2]['graph']
#            graph_eq(subgraph)
#    if edges[0][1] == edges[1][1]:
#        graph_analysis_parallel(splitgraph)
#    else:
#        graph_analysis_serial(splitgraph)