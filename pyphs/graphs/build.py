# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 00:58:26 2016

@author: Falaize
"""
import sympy


def buildCore(graph):
    vstack = sympy.Matrix.vstack
    hstack = sympy.Matrix.hstack
    nec = len(graph.analysis.ec_edges)
    nfc = len(graph.analysis.fc_edges)
    # incidence matrix for the effort-controlled edges
    gamma_ec = sympy.Matrix(graph.analysis.gamma_ec)
    # incidence matrix for the flux-controlled edges
    igamma_fc = sympy.Matrix(graph.analysis.igamma_fc)
    # solve linear relations to get the port-Hamiltonian structure
    gamma = igamma_fc * gamma_ec
    # build J matrix
    graph.analysis.J = vstack(hstack(sympy.zeros(nec), gamma.T),
                              hstack(-gamma, sympy.zeros(nfc)))
    _sort_edges(graph.analysis)
    _setCore(graph)


def _sort_edges(analysis):
    # according to storage, dissipation, ports and connectors
    # get indices of storage edges
    analysis.stor_edges = []
    analysis.diss_edges = []
    analysis.port_edges = []
    analysis.conn_edges = []
    for e in range(analysis.ne):
        if analysis.get_edge_data(e, 'type') is 'storage':
            analysis.stor_edges.append(e)
        elif analysis.get_edge_data(e, 'type') is 'dissipative':
            analysis.diss_edges.append(e)
        elif analysis.get_edge_data(e, 'type') is 'port':
            analysis.port_edges.append(e)
        else:
            assert analysis.get_edge_data(e, 'type') is 'connector'
            analysis.conn_edges.append(e)
    all_edges = analysis.stor_edges + analysis.diss_edges + \
        analysis.port_edges + analysis.conn_edges
    analysis.J = analysis.J[all_edges, all_edges]


def _select_relations(graph):
    """
    select the dissipative relation 'z' and connectors coefficients 'alpha' \
according to the control type of each indeterminate edge
    """
    # select dissipative relations
    for e in graph.analysis.diss_edges:
        ctrl = graph.analysis.get_edge_data(e, 'ctrl')
        # select for indeterminate edges only
        if ctrl == '?':
            # get edge label index in 'w'
            label = graph.analysis.get_edge_data(e, 'label')
            indw = graph.core.w.index(label)
            if e in graph.analysis.ec_edges:
                graph.core.z[indw] = \
                    graph.analysis.get_edge_data(e, 'z')['e_ctrl']
            else:
                assert e in graph.analysis.fc_edges
                graph.core.z[indw] = \
                    graph.analysis.get_edge_data(e, 'z')['f_ctrl']


def _setCore(graph):
    new_indices_x = []
    for e in graph.analysis.stor_edges:
        e_label = graph.analysis.get_edge_data(e, 'label')
        index_e_in_x = graph.core.x.index(e_label)
        new_indices_x.append(index_e_in_x)
    graph.core.x = [graph.core.x[el] for el in new_indices_x]

    new_indices_w = []
    for e in graph.analysis.diss_edges:
        e_label = graph.analysis.get_edge_data(e, 'label')
        index_e_in_w = graph.core.w.index(e_label)
        new_indices_w.append(index_e_in_w)
    graph.core.w = [graph.core.w[el] for el in new_indices_w]
    graph.core.z = [graph.core.z[el] for el in new_indices_w]

    new_indices_y = []
    for e in graph.analysis.port_edges:
        e_label = graph.analysis.get_edge_data(e, 'label')
        index_e_in_y = graph.core.y.index(e_label)
        new_indices_y.append(index_e_in_y)
    graph.core.y = [graph.core.y[el] for el in new_indices_y]
    graph.core.u = [graph.core.u[el] for el in new_indices_y]

    new_indices_connector = []
    for e in graph.analysis.conn_edges:
        e_label = graph.analysis.get_edge_data(e, 'label')
        index_e_in_connector = graph.core.cy.index(e_label)
        alpha = graph.analysis.get_edge_data(e, 'alpha')
        if alpha is not None:
            graph.core.connectors[index_e_in_connector]['alpha'] = alpha
        new_indices_connector.append(index_e_in_connector)
    graph.core.cy = [graph.core.cy[el] for el in new_indices_connector]
    graph.core.cu = [graph.core.cu[el] for el in new_indices_connector]

    _select_relations(graph)
    graph.core.M = graph.analysis.J
