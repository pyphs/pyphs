# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 00:58:26 2016

@author: Falaize
"""
import sympy
from pyphs.core.tools import types


def buildCore(graph):
    vstack = types.matrix_types[0].vstack
    hstack = types.matrix_types[0].hstack
    nec = len(graph.analysis.ec_edges)
    nfc = len(graph.analysis.fc_edges)
    # incidence matrix for the effort-controlled edges
    gamma_ec = types.matrix_types[0](graph.analysis.Gamma_ec)
    # incidence matrix for the flux-controlled edges
    igamma_fc = types.matrix_types[0](graph.analysis.iGamma_fc)
    # solve linear relations to get the port-Hamiltonian structure
    gamma = igamma_fc * gamma_ec
    # build J matrix
    graph.analysis.J = vstack(hstack(types.matrix_types[0](sympy.zeros(nec)),
                                     gamma.T),
                              hstack(-gamma,
                                     types.matrix_types[0](sympy.zeros(nfc))))
    all_edges = graph.analysis.stor_edges + graph.analysis.diss_edges + \
        graph.analysis.port_edges + graph.analysis.conn_edges
    graph.analysis.J = graph.analysis.J[all_edges, all_edges]

    # Add core to graph
    _setCore(graph)


def _select_relations(graph):
    """
    select the dissipative relation 'z' and connectors coefficients 'alpha' \
according to the control type of each indeterminate edge
    """
    # select dissipative relations
    for e in graph.analysis.diss_edges:

        # get edge label index in 'w'
        label = graph.analysis.get_edge_data(e, 'label')
        # get index in w
        indw = graph.core.w.index(label)

        if e in graph.analysis.ec_edges:
            # select effocrt-controlled constitutive law
            graph.core.z[indw] = \
                graph.analysis.get_edge_data(e, 'z')['e_ctrl']
        elif e in graph.analysis.fc_edges:
            # select flux-controlled constitutive law
            graph.core.z[indw] = \
                graph.analysis.get_edge_data(e, 'z')['f_ctrl']
        else:
            message = "Control of edge {0} is not known."
            raise ValueError(message)


def _setCore(graph):

    # sort storages
    new_indices_x = []
    for e in graph.analysis.stor_edges:
        e_label = graph.analysis.get_edge_data(e, 'label')
        index_e_in_x = graph.core.x.index(e_label)
        new_indices_x.append(index_e_in_x)
    graph.core.x = [graph.core.x[el] for el in new_indices_x]

    # sort dissipatives
    new_indices_w = []
    for e in graph.analysis.diss_edges:
        e_label = graph.analysis.get_edge_data(e, 'label')
        index_e_in_w = graph.core.w.index(e_label)
        new_indices_w.append(index_e_in_w)
    graph.core.w = [graph.core.w[el] for el in new_indices_w]
    graph.core.z = [graph.core.z[el] for el in new_indices_w]

    # sort sources
    new_indices_y = []
    for e in graph.analysis.port_edges:
        e_label = graph.analysis.get_edge_data(e, 'label')
        index_e_in_y = graph.core.y.index(e_label)
        new_indices_y.append(index_e_in_y)
    graph.core.y = [graph.core.y[el] for el in new_indices_y]
    graph.core.u = [graph.core.u[el] for el in new_indices_y]

    # sort connectors
    new_indices_connector = []
    for e in graph.analysis.conn_edges:
        e_label = graph.analysis.get_edge_data(e, 'label')
        new_indices_connector.append(graph.core.cy.index(e_label))
        index_e_in_connector = [e_label in c['y']
                                for c in graph.core.connectors].index(True)
        alpha = graph.analysis.get_edge_data(e, 'alpha')
        if alpha is not None:
            graph.core.connectors[index_e_in_connector]['alpha'] = alpha
    graph.core.cy = [graph.core.cy[el] for el in new_indices_connector]
    graph.core.cu = [graph.core.cu[el] for el in new_indices_connector]

    # select constitutive law (ec or fc) for dissipative components
    _select_relations(graph)

    # set structure matrix
    graph.core.M = graph.analysis.J
