# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 10:50:48 2015

@author: Falaize
"""



def add_path():
    """
    add pypHs path to sys path
    """
    import sys
    # path to pyphs
    pypHs_path = "/Users/Falaize/Documents/DEV/python/pypHs/"
    # add path
    sys.path.append(pypHs_path)


def label():
    """
    System's netlist and folder label
    """
    return "ThieleSmall"


def samplerate():
    """
    global sample rate
    """
    return 96e3


def write_netlist(R=1e3, L=5e-2, C=2e-6, Bl=5, M=0.1, K=5e3, A=1):
    """
    Write netlist for Thiele/Small model of loudspeaker
    """
    from utils.graphs import build_netlist, datum
    s_netlist = ""
    # input voltage
    comp_dic = 'connectors'
    comp_comp = 'port'
    comp_label = 'I'
    comp_nodes = ['A', datum]
    comp_parameters = ['e']
    s_netlist += build_netlist(comp_dic,
                               comp_comp,
                               comp_label,
                               comp_nodes,
                               comp_parameters)
    # resistor
    comp_dic = 'electronics'
    comp_comp = 'resistor'
    comp_label = 'R'
    comp_nodes = ['A', 'B']
    comp_parameters = [('R', R)]
    s_netlist += build_netlist(comp_dic,
                               comp_comp,
                               comp_label,
                               comp_nodes,
                               comp_parameters)
    # inductor
    comp_dic = 'electronics'
    comp_comp = 'inductor'
    comp_label = 'L'
    comp_nodes = ['B', 'C']
    comp_parameters = [('L', L)]
    s_netlist += build_netlist(comp_dic,
                               comp_comp,
                               comp_label,
                               comp_nodes,
                               comp_parameters)
    # gyrator
    comp_dic = 'connectors'
    comp_comp = 'gyrator'
    comp_label = 'Bl'
    comp_nodes = ['C', datum, 'D', datum]
    comp_parameters = [('Bl', Bl)]
    s_netlist += build_netlist(comp_dic,
                               comp_comp,
                               comp_label,
                               comp_nodes,
                               comp_parameters)
    # mass
    comp_dic = 'mechanics'
    comp_comp = 'mass'
    comp_label = 'M'
    comp_nodes = ['D', 'E']
    comp_parameters = [('M', M)]
    s_netlist += build_netlist(comp_dic,
                               comp_comp,
                               comp_label,
                               comp_nodes,
                               comp_parameters)
    # stiffness
    comp_dic = 'mechanics'
    comp_comp = 'stiffness'
    comp_label = 'KK'
    comp_nodes = ['E', 'F']
    comp_parameters = [('K', K)]
    s_netlist += build_netlist(comp_dic,
                               comp_comp,
                               comp_label,
                               comp_nodes,
                               comp_parameters)
    # damper
    comp_dic = 'mechanics'
    comp_comp = 'damper'
    comp_label = 'A'
    comp_nodes = ['F', datum]
    comp_parameters = [('A', A)]
    s_netlist += build_netlist(comp_dic,
                               comp_comp,
                               comp_label,
                               comp_nodes,
                               comp_parameters)
    netlist_file = open(label()+".net", 'w')
    netlist_file.write(s_netlist[:-1])  # remove the last cariage return
    netlist_file.close()


def init_phs():
    # import pHobj
    from pypHs import pHobj
    # phs = pHobj(label=label, path='label', netlist=label)
    phs = pHobj(label=label(), path='label')
    return phs


def build_graph(phs):
    from utils.graphs import netlist2graph
    from utils.structure import copy
    copy(netlist2graph(phs, label()), phs)


def analysis(phs):
    from utils.graphs import realizability_analysis, build_J
    realizability_analysis(phs)
    build_J(phs)


def input_sequence(amp=100., f0=100.):
    from utils.signal import SignalGenerator
    fs = samplerate()
    nsin = int(0.05*fs)
    SigIn = SignalGenerator(which="sin", n=nsin, ramp_on=False,
                            A=amp, f0=f0, fs=fs)

    def gen_u():
        for el in SigIn:
            yield [el, ]

    return gen_u(), nsin


def simulation(phs, seq_u, nt):
    fs = samplerate()
    phs.simulation(fs, seq_u=seq_u, nt=nt)


if __name__ is '__main__':
    add_path()
    write_netlist()
    phs = init_phs()
    build_graph(phs)
    analysis(phs)
    phs.build()
    seq_u, nt = input_sequence()
    phs.build_numerics(fs=samplerate())
    num = phs.numerics
    simulation(phs, seq_u, nt)
    phs.plot_powerBal()
#    phs.plot_variables([('x', 0), ('dtx', 1), ('dxHd', 1)])
