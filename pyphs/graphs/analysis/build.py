# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 00:58:26 2016

@author: Falaize
"""
import sympy


def build_phs(analysis, phs):
    vstack = sympy.Matrix.vstack
    hstack = sympy.Matrix.hstack
    nec = len(analysis.ec_edges)
    nfc = len(analysis.fc_edges)
    # incidence matrix for the effort-controlled edges
    gamma_ec = sympy.Matrix(analysis.gamma[1:, :len(analysis.ec_edges)])
    # incidence matrix for the flux-controlled edges
    gamma_fc = sympy.Matrix(analysis.gamma[1:, len(analysis.ec_edges):])
    # solve linear relations to get the port-Hamiltonian structure
    gamma = gamma_fc.inv() * gamma_ec
    # build J matrix
    analysis.J = vstack(hstack(sympy.zeros(nec), gamma.T),
                        hstack(-gamma, sympy.zeros(nfc)))
    _sort_edges(analysis)
    _set_phs(analysis, phs)


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


def _select_relations(analysis, phs):
    """
    select the dissipative relation 'z' and connectors coefficients 'alpha' \
according to the control type of each indeterminate edge
    """
    # select dissipative relations
    for e in analysis.diss_edges:
        ctrl = analysis.get_edge_data(e, 'ctrl')
        # select for indeterminate edges only
        if ctrl == '?':
            # get edge label index in 'w'
            label = analysis.get_edge_data(e, 'label')
            indw = phs.symbs.w.index(label)
            if e in analysis.ec_edges:
                phs.exprs.z[indw] = analysis.get_edge_data(e, 'z')['e_ctrl']
            else:
                assert e in analysis.fc_edges
                phs.exprs.z[indw] = analysis.get_edge_data(e, 'z')['f_ctrl']


def _set_phs(analysis, phs):
    new_indices_x = []
    for e in analysis.stor_edges:
        e_label = analysis.get_edge_data(e, 'label')
        index_e_in_x = phs.symbs.x.index(e_label)
        new_indices_x.append(index_e_in_x)
    phs.symbs.x = [phs.symbs.x[el] for el in new_indices_x]

    new_indices_w = []
    for e in analysis.diss_edges:
        e_label = analysis.get_edge_data(e, 'label')
        index_e_in_w = phs.symbs.w.index(e_label)
        new_indices_w.append(index_e_in_w)
    phs.symbs.w = [phs.symbs.w[el] for el in new_indices_w]
    phs.exprs.z = [phs.exprs.z[el] for el in new_indices_w]

    new_indices_y = []
    for e in analysis.port_edges:
        e_label = analysis.get_edge_data(e, 'label')
        index_e_in_y = phs.symbs.y.index(e_label)
        new_indices_y.append(index_e_in_y)
    phs.symbs.y = [phs.symbs.y[el] for el in new_indices_y]
    phs.symbs.u = [phs.symbs.u[el] for el in new_indices_y]

    new_indices_connector = []
    for e in analysis.conn_edges:
        e_label = analysis.get_edge_data(e, 'label')
        index_e_in_connector = phs.symbs.cy.index(e_label)
        new_indices_connector.append(index_e_in_connector)
    phs.symbs.cy = [phs.symbs.cy[el] for el in new_indices_connector]
    phs.symbs.cu = [phs.symbs.cu[el] for el in new_indices_connector]

    _select_relations(analysis, phs)

    phs.struc.M = analysis.J
