# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 00:58:26 2016

@author: Falaize
"""
import sympy


def buildCore(Graph):
    vstack = sympy.Matrix.vstack
    hstack = sympy.Matrix.hstack
    nec = len(Graph.Analysis.ec_edges)
    nfc = len(Graph.Analysis.fc_edges)
    # incidence matrix for the effort-controlled edges
    gamma_ec = sympy.Matrix(Graph.Analysis.gamma_ec)
    # incidence matrix for the flux-controlled edges
    igamma_fc = sympy.Matrix(Graph.Analysis.igamma_fc)
    # solve linear relations to get the port-Hamiltonian structure
    gamma = igamma_fc * gamma_ec
    # build J matrix
    Graph.Analysis.J = vstack(hstack(sympy.zeros(nec), gamma.T),
                              hstack(-gamma, sympy.zeros(nfc)))
    _sort_edges(Graph.Analysis)
    _setCore(Graph)


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


def _select_relations(Graph):
    """
    select the dissipative relation 'z' and connectors coefficients 'alpha' \
according to the control type of each indeterminate edge
    """
    # select dissipative relations
    for e in Graph.Analysis.diss_edges:
        ctrl = Graph.Analysis.get_edge_data(e, 'ctrl')
        # select for indeterminate edges only
        if ctrl == '?':
            # get edge label index in 'w'
            label = Graph.Analysis.get_edge_data(e, 'label')
            indw = Graph.core.w.index(label)
            if e in Graph.Analysis.ec_edges:
                Graph.core.z[indw] = \
                    Graph.Analysis.get_edge_data(e, 'z')['e_ctrl']
            else:
                assert e in Graph.Analysis.fc_edges
                Graph.core.z[indw] = \
                    Graph.Analysis.get_edge_data(e, 'z')['f_ctrl']


def _setCore(Graph):
    new_indices_x = []
    for e in Graph.Analysis.stor_edges:
        e_label = Graph.Analysis.get_edge_data(e, 'label')
        index_e_in_x = Graph.core.x.index(e_label)
        new_indices_x.append(index_e_in_x)
    Graph.core.x = [Graph.core.x[el] for el in new_indices_x]

    new_indices_w = []
    for e in Graph.Analysis.diss_edges:
        e_label = Graph.Analysis.get_edge_data(e, 'label')
        index_e_in_w = Graph.core.w.index(e_label)
        new_indices_w.append(index_e_in_w)
    Graph.core.w = [Graph.core.w[el] for el in new_indices_w]
    Graph.core.z = [Graph.core.z[el] for el in new_indices_w]

    new_indices_y = []
    for e in Graph.Analysis.port_edges:
        e_label = Graph.Analysis.get_edge_data(e, 'label')
        index_e_in_y = Graph.core.y.index(e_label)
        new_indices_y.append(index_e_in_y)
    Graph.core.y = [Graph.core.y[el] for el in new_indices_y]
    Graph.core.u = [Graph.core.u[el] for el in new_indices_y]

    new_indices_connector = []
    for e in Graph.Analysis.conn_edges:
        e_label = Graph.Analysis.get_edge_data(e, 'label')
        index_e_in_connector = Graph.core.cy.index(e_label)
        alpha = Graph.Analysis.get_edge_data(e, 'alpha')
        if alpha is not None:
            Graph.core.connectors[index_e_in_connector]['alpha'] = alpha
        new_indices_connector.append(index_e_in_connector)
    Graph.core.cy = [Graph.core.cy[el] for el in new_indices_connector]
    Graph.core.cu = [Graph.core.cu[el] for el in new_indices_connector]
    _select_relations(Graph)
    Graph.core.M = Graph.Analysis.J
