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
    return '/Users/Falaize/Documents/DEV/python/pypHs/tests'


def label():
    """
    System's netlist and folder label
    """
    return "DLC"


def netlist_filename():
    import os
    return workingdirectory() + os.sep + label() + '.net'


def samplerate():
    """
    global sample rate
    """
    return 48e3


def write_netlist(C=2e-10, Is=1e-9, v0=25e-3):
    """
    Write netlist for RLC circuit
    """
    from pyphs.graphs.netlists import Netlist

    netlist = Netlist()

    datum = netlist.datum

    # input voltage
    source = {'dictionary': 'electronics',
              'component': 'source',
              'label': 'IN',
              'nodes': ('A', datum),
              'arguments': {'type': "'voltage'"}}
    netlist.add_line(source)

    # diode
    diode = {'dictionary': 'electronics',
             'component': 'diodepn',
             'label': 'D',
             'nodes': ('A', 'B'),
             'arguments': {'Is': ('Is', Is),
                           'v0': ('v0', v0)}}
    netlist.add_line(diode)

    # capacitor
    capacitor = {'dictionary': 'electronics',
                 'component': 'capacitor',
                 'label': 'C',
                 'nodes': ('B', datum),
                 'arguments': {'C': ('C', C)}}
    netlist.add_line(capacitor)

    netlist.write(filename=netlist_filename())


def init_phs():
    # import pHobj
    from pyphs import PortHamiltonianObject
    import os
    phs = PortHamiltonianObject(label=label(),
                                path=workingdirectory() + os.sep + label())
    return phs


def build_graph(phs):
    phs.build_from_netlist(netlist_filename())


def input_sequence(amp=50., f0=100.):
    from pyphs.misc.signals.synthesis import signalgenerator
    fs = samplerate()
    nsin = int(10*fs/f0)
    SigIn = signalgenerator(which="sin", n=nsin, ramp_on=False,
                            A=amp, f0=f0, fs=fs)

    def genu():
        for el in SigIn:
            yield [el, ]

    return genu(), nsin


def simulation(phs, sequ, nt):
    config = {'fs': samplerate()}
    phs.build_simulation(config=config, sequ=sequ, nt=nt)
    phs.run_simulation()


if __name__ is '__main__':
    add_path()
    write_netlist()
    phs = init_phs()
    build_graph(phs)
    sequ, nt = input_sequence()
    phs.build_exprs()
    phs.build_nums()
    phs.export_latex()
    simulation(phs, sequ, nt)
    phs.plot_powerBal()
    phs.plot_variables([('u', 0), ('x', 0), ('w', 0)])
