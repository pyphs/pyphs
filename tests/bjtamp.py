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
    return '/Users/Falaize/Documents/DEV/python/pyphs/tests'


def label():
    """
    System's netlist and folder label
    """
    return "BJTAMP"


def netlist_filename():
    import os
    return workingdirectory() + os.sep + label() + '.net'


def samplerate():
    """
    global sample rate
    """
    return 96e3


def write_netlist(Cin=10e-6, Cout=10e-6, Is=2.39e-14, Vt=26e-3,
                  betaR=7.946, betaF=294.3, mu=1.006, Rb=1, Rc=0.85, Re=0.4683, Rbc=270e3,
                  Rcd=1e3):
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

    # capacitor Cin
    capacitorCin = {'dictionary': 'electronics',
                    'component': 'capacitor',
                    'label': 'Cin',
                    'nodes': ('A', 'B'),
                    'arguments': {'C': ('Cin', Cin)}}
    netlist.add_line(capacitorCin)

    # resistor BC
    resistance = {'dictionary': 'electronics',
                  'component': 'resistor',
                  'label': 'Rbc',
                  'nodes': ('B', 'C'),
                  'arguments': {'R': ('Rcd', Rbc)}}
    netlist.add_line(resistance)

    # bjt
    bjt = {'dictionary': 'electronics',
           'component': 'bjt',
           'label': 'BJT',
           'nodes': ('B', 'C', datum),
           'arguments': {'Is': ('Is', Is),
                         'Vt': ('Vt', Vt),
                         'betaR': ('betaR', betaR),
                         'betaF': ('betaF', betaF),
                         'mu': ('mu', mu),
                         'Rb': ('Rb', Rb),
                         'Rc': ('Rc', Rc),
                         'Re': ('Re', Re)}}
    netlist.add_line(bjt)

    # resistor CD
    resistance = {'dictionary': 'electronics',
                  'component': 'resistor',
                  'label': 'Rcd',
                  'nodes': ('C', 'D'),
                  'arguments': {'R': ('Rcd', Rcd)}}
    netlist.add_line(resistance)

    # VCC voltage
    source = {'dictionary': 'electronics',
              'component': 'source',
              'label': 'VCC',
              'nodes': ('D', datum),
              'arguments': {'type': "'voltage'"}}
    netlist.add_line(source)

    # capacitor Cout
    capacitorCout = {'dictionary': 'electronics',
                     'component': 'capacitor',
                     'label': 'Cout',
                     'nodes': ('C', 'F'),
                     'arguments': {'C': ('Cout', Cout)}}
    netlist.add_line(capacitorCout)

    # output (0A current as input)
    source = {'dictionary': 'electronics',
              'component': 'source',
              'label': 'OUT',
              'nodes': ('F', datum),
              'arguments': {'type': "'current'"}}
    netlist.add_line(source)

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


def input_sequence(amp=0.2, f0=1e3, ndeb=int(0.3*samplerate())):
    from pyphs.misc.signals.synthesis import signalgenerator
    fs = samplerate()
    nsin = int(10.*fs/f0)
    sig = signalgenerator(which="sin", n=nsin, ramp_on=False,
                          A=amp, f0=f0, fs=fs, ndeb=ndeb, attack_ratio=1)

    nt = ndeb+nsin
    vcc = signalgenerator(which="step", n=nt, ramp_on=False, A=9.,
                          attack_ratio=0)

    def genu():
        for s, v in zip(sig, vcc):
            yield [s, v, 0.]

    return genu(), nt


def simulation(phs, sequ, nt):
    config = {'fs': samplerate(),
              'split': True,
              'maxit': 100}
    phs.build_simulation(config=config, sequ=sequ, nt=nt)
    phs.run_simulation()


if __name__ is '__main__':
    add_path()
    phs = init_phs()
    write_netlist()
    build_graph(phs)
    from pyphs.symbolics.structures.tools import move_port
    move_port(phs, phs.symbs.u.index(phs.symbols('uIN')), 0)
    move_port(phs, phs.symbs.u.index(phs.symbols('uOUT')), 2)
    ndeb = int(0.3*samplerate())
    sequ, nt = input_sequence(ndeb=ndeb)
    phs.export_latex()
    simulation(phs, sequ, nt)
    phs.plot_powerbal(imin=ndeb)
    phs.plot_data([('u', 0), ('yd', 2)], imin=ndeb)
