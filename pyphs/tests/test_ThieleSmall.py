# -*- coding: utf-8 -*-
"""
Created on Fri Oct 7 23:33:48 2016

@author: Falaize
"""


from unittest import TestCase


class TestTS(TestCase):
    def test_ts(self):
        self.assertTrue(run_test())


def netlist_filename(phs=None):
    import os
    if phs is None:
        return os.getcwd() + os.sep + label() + '.net'
    else:
        return phs.path + os.sep + label() + '.net'


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


def write_netlist(phs, R=1e3, L=5e-2, Bl=5, M=0.1, K=5e3, A=1):
    """
    Write netlist for Thiele/Small model of loudspeaker
    """

    datum = phs.graph.netlist.datum

#    from utils.graphs import build_netlist

    # input voltage
    source = {'dictionary': 'electronics',
              'component': 'source',
              'label': 'IN',
              'nodes': ('A', datum),
              'arguments': {'type': "'voltage'"}}
    phs.graph.netlist.add_line(source)

    # resistor 1
    resistance = {'dictionary': 'electronics',
                  'component': 'resistor',
                  'label': 'R',
                  'nodes': ('A', 'B'),
                  'arguments': {'R': ('R', R)}}
    phs.graph.netlist.add_line(resistance)

    # inductor
    inductor = {'dictionary': 'electronics',
                'component': 'inductor',
                'label': 'L',
                'nodes': ('B', 'C'),
                'arguments': {'L': ('L', L)}}
    phs.graph.netlist.add_line(inductor)

    # gyrator
    gyrator = {'dictionary': 'connectors',
               'component': 'gyrator',
               'label': 'G',
               'nodes': ('C', datum, 'D', datum),
               'arguments': {'alpha': ('Bl', Bl)}}
    phs.graph.netlist.add_line(gyrator)

    # masse
    mass = {'dictionary': 'mechanics',
            'component': 'mass',
            'label': 'M',
            'nodes': ('D', 'E'),
            'arguments': {'M': ('M', M)}}
    phs.graph.netlist.add_line(mass)

    # raideur
    stifness = {'dictionary': 'mechanics',
                'component': 'stiffness',
                'label': 'K',
                'nodes': ('E', 'F'),
                'arguments': {'K': ('K', K)}}
    phs.graph.netlist.add_line(stifness)

    # amortissement
    damper = {'dictionary': 'mechanics',
                 'component': 'damper',
                 'label': 'A',
                 'nodes': ('F', datum),
                 'arguments': {'A': ('A', A)}}
    phs.graph.netlist.add_line(damper)

    phs.graph.netlist.write(filename=netlist_filename(phs))


def init_phs():
    # import pHobj
    from pyphs import PortHamiltonianObject
    import os
    phs = PortHamiltonianObject(label=label(),
                                path=os.getcwd() + os.sep + label())
    return phs


def build_graph(phs):
    phs.build_from_netlist(netlist_filename(phs))


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
            'language': 'python',
            'split': False}
    u, nt = input_sequence()
    phs.simu.init(sequ=u, nt=nt, opts=opts)
    phs.simu.process()


def run_test():
    phs = init_phs()
    write_netlist(phs)
    build_graph(phs)
    u, nt = input_sequence()
    simulation(phs, u, nt)
    phs.cppbuild()
    phs.cpp.gen_main()
    phs.cpp.gen_phobj()
    phs.cpp.gen_data()
    phs.plot_powerbal()
    phs.plot_powerbal(mode='multi')
    phs.plot_data([('x', 0), ('dx', 1), ('dxH', 1)])
    import shutil
    shutil.rmtree(phs.path, ignore_errors=True)
    return True

if __name__ is '__main__':
    succeed = run_test()
