# -*- coding: utf-8 -*-
"""
Created on Sat May 21 10:50:30 2016

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


def workingdirectory():
    return '/Users/Falaize/Documents/DEV/python/pypHs/test'


def label():
    """
    System's netlist and folder label
    """
    return "RLC"


def netlist_filename():
    import os
    return workingdirectory() + os.sep + label() + '.net'


def samplerate():
    """
    global sample rate
    """
    return 96e3


def write_netlist(R=1e3, L=5e-2, C=2e-6):
    """
    Write netlist for RLC circuit
    """
    from graphs.netlists import Netlist

    netlist = Netlist()

    datum = netlist.datum

    # input voltage
    source = {'dictionary': 'electronics',
              'component': 'source',
              'label': 'IN',
              'nodes': ('A', datum),
              'arguments': {'type': "'voltage'"}}
    netlist.add_line(source)

    # resistor 2
    resistance = {'dictionary': 'electronics',
                  'component': 'resistor',
                  'label': 'R1',
                  'nodes': ('A', 'B'),
                  'arguments': {'R': ('R1', R)}}
    netlist.add_line(resistance)

    # resistor 2
    resistance = {'dictionary': 'electronics',
                  'component': 'resistor',
                  'label': 'R2',
                  'nodes': ('B', 'C'),
                  'arguments': {'R': ('R2', R)}}
    netlist.add_line(resistance)

    # inductor
    inductor = {'dictionary': 'electronics',
                'component': 'inductor',
                'label': 'L',
                'nodes': ('B', 'C'),
                'arguments': {'L': ('L', L)}}
    netlist.add_line(inductor)

    # capacitor
    capacitor = {'dictionary': 'electronics',
                 'component': 'capacitor',
                 'label': 'C',
                 'nodes': ('C', datum),
                 'arguments': {'C': ('C', C)}}
    netlist.add_line(capacitor)

    netlist.write(filename=netlist_filename())


def init_phs():
    # import pHobj
    from pypHs import PortHamiltonianObject
    import os
    phs = PortHamiltonianObject(label=label(),
                                path=workingdirectory() + os.sep + label())
    return phs


def build_graph(phs):
    phs.build_from_netlist(netlist_filename())


def input_sequence(amp=100., f0=100.):
    from misc.signals.synthesis import signalgenerator
    fs = samplerate()
    nsin = int(2.*fs/f0)
    SigIn = signalgenerator(which="sin", n=nsin, ramp_on=False,
                            A=amp, f0=f0, fs=fs)

    def genu():
        for el in SigIn:
            yield [el, ]

    return genu(), nsin


def simulation(phs, sequ, nt):
    fs = samplerate()
    phs.build_simulation(fs, sequ=sequ, nt=nt)


def test():
    add_path()
    write_netlist()
    phs = init_phs()
    build_graph(phs)
    phs.build()
    seq_u, nt = input_sequence()
    phs.build_numerics(fs=samplerate())
    num = phs.numerics
    simulation(phs, seq_u, nt)
    phs.plot_powerBal()
#    phs.plot_variables([('x', 0), ('dtx', 1), ('dxHd', 1)])
    
if __name__ is '__main__':
    add_path()
    write_netlist()
    phs = init_phs()
    build_graph(phs)
    sequ, nt = input_sequence()
    phs.build_exprs()
    phs.build_nums()
    simulation(phs, sequ, nt)
#    phs.plot_powerBal()
