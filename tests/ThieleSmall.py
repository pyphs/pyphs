# -*- coding: utf-8 -*-
"""
Created on Fri Oct 7 23:33:48 2016

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
    return "ThieleSmall"


def netlist_filename():
    import os
    return workingdirectory() + os.sep + label() + '.net'


def samplerate():
    """
    global sample rate
    """
    return 96e3


def write_netlist(R=1e3, L=5e-2, Bl=5, M=0.1, K=5e3, A=1):
    """
    Write netlist for Thiele/Small model of loudspeaker
    """
    from pyphs.graphs.netlists import Netlist

    netlist = Netlist()

    datum = netlist.datum

#    from utils.graphs import build_netlist

    # input voltage
    source = {'dictionary': 'electronics',
              'component': 'source',
              'label': 'IN',
              'nodes': ('A', datum),
              'arguments': {'type': "'voltage'"}}
    netlist.add_line(source)

    # resistor 1
    resistance = {'dictionary': 'electronics',
                  'component': 'resistor',
                  'label': 'R',
                  'nodes': ('A', 'B'),
                  'arguments': {'R': ('R', R)}}
    netlist.add_line(resistance)

    # inductor
    inductor = {'dictionary': 'electronics',
                'component': 'inductor',
                'label': 'L',
                'nodes': ('B', 'C'),
                'arguments': {'L': ('L', L)}}
    netlist.add_line(inductor)

    # gyrator
    gyrator = {'dictionary': 'connectors',
               'component': 'gyrator',
               'label': 'G',
               'nodes': ('C', datum, 'D', datum),
               'arguments': {'alpha': ('Bl', Bl)}}
    netlist.add_line(gyrator)

    # masse
    mass = {'dictionary': 'mechanics',
            'component': 'mass',
            'label': 'M',
            'nodes': ('D', 'E'),
            'arguments': {'M': ('M', M)}}
    netlist.add_line(mass)

    # raideur
    stifness = {'dictionary': 'mechanics',
                'component': 'stiffness',
                'label': 'K',
                'nodes': ('E', 'F'),
                'arguments': {'K': ('K', K)}}
    netlist.add_line(stifness)

    # amortissement
    damper = {'dictionary': 'mechanics',
                 'component': 'damper',
                 'label': 'A',
                 'nodes': ('F', datum),
                 'arguments': {'A': ('A', A)}}
    netlist.add_line(damper)

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


def input_sequence(amp=100., f0=100.):
    from pyphs.misc.signals.synthesis import signalgenerator
    fs = samplerate()
    nsin = int(2*fs/f0)
    SigIn = signalgenerator(which="sin", n=nsin, ramp_on=False,
                            A=amp, f0=f0, fs=fs)

    def genu():
        for el in SigIn():
            yield [el, ]

    return genu(), nsin


def simulation(phs, sequ, nt):
    opts = {'fs': samplerate(),
            'language': 'c++',
            'split': False}
    phs.simu.init(sequ=u, nt=nt, opts=opts)


if __name__ is '__main__':
    add_path()
    write_netlist()
    phs = init_phs()
    build_graph(phs)
#    u, nt = input_sequence()
#    simulation(phs, u, nt)
#    phs.cppbuild()
#    phs.cpp.gen_main()
#    phs.cpp.gen_phobj()
#    phs.cpp.gen_data()
#    phs.plot_powerBal()
#    phs.plot_variables([('x', 0), ('dtx', 1), ('dxHd', 1)])
