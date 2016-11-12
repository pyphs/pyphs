# -*- coding: utf-8 -*-
"""
Created on Sat May 21 10:50:30 2016

@author: Falaize
"""


def label():
    """
    System's netlist and folder label
    """
    return "RLC"


def netlist_filename(phs=None):
    import os
    if phs is None:
        return os.getcwd() + os.sep + label() + '.net'
    else:
        return phs.path + os.sep + label() + '.net'


def samplerate():
    """
    global sample rate
    """
    return 96e3


def write_netlist(phs, R1=1e3, L=5e-2, C=2e-6):
    """
    Write netlist for RLC circuit
    """

    datum = phs.graph.netlist.datum

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
                  'label': 'R1',
                  'nodes': ('A', 'B'),
                  'arguments': {'R': ('R1', R1)}}
    phs.graph.netlist.add_line(resistance)

    # inductor
    inductor = {'dictionary': 'electronics',
                'component': 'inductor',
                'label': 'L',
                'nodes': ('B', 'C'),
                'arguments': {'L': ('L', L)}}
    phs.graph.netlist.add_line(inductor)

    # capacitor
    capacitor = {'dictionary': 'electronics',
                 'component': 'capacitor',
                 'label': 'C',
                 'nodes': ('C', datum),
                 'arguments': {'C': ('C', C)}}
    phs.graph.netlist.add_line(capacitor)

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


def simulation(phs):
    opts = {'fs': samplerate(),
            'language': 'python',
            'split': False}
    u, nt = input_sequence()
    phs.simu.init(sequ=u, nt=nt, opts=opts)
    phs.simu.process()


def gen_cpp(phs):
    phs.cppbuild()
    phs.cpp.gen_main()
    phs.cpp.gen_phobj()
    phs.cpp.gen_data()


def run_test():
    phs = init_phs()
    write_netlist(phs)
    build_graph(phs)
    simulation(phs)
    gen_cpp(phs)
#    phs.plot_powerbal()
#    phs.plot_data([('x', 0), ('dx', 1), ('dxH', 1)])
    import shutil
    shutil.rmtree(phs.path, ignore_errors=True)
    return True

if __name__ is '__main__':
    succeed = run_test()
