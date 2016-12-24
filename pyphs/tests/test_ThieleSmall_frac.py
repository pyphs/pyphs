# -*- coding: utf-8 -*-
"""
Created on Fri Oct 7 23:33:48 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function
import os
import pyphs


def label():
    """
    System's netlist and folder label
    """
    return "ThieleSmall"


def path():
    """
    System's netlist and folder path
    """
    p = os.getcwd() + os.sep + label()
    if not os.path.exists(p):
        os.makedirs(p)
    return p


def samplerate():
    """
    global sample rate
    """
    return 96e3


def netlist(R=1e3, L=5e-2, Bl=50, M=0.1, K=5e3, A=1):
    """
    Write netlist for RLC circuit
    """
    netlist = pyphs.PHSNetlist(path() + os.sep + label() + '.net', clear=True)

    datum = netlist.datum

    # input voltage
    source = {'dictionary': 'electronics',
              'component': 'source',
              'label': 'IN',
              'nodes': ('A', datum),
              'arguments': {'type': "voltage"}}
    netlist.add_line(source)

    # resistor 1
    resistance = {'dictionary': 'electronics',
                  'component': 'resistor',
                  'label': 'R',
                  'nodes': ('A', 'B'),
                  'arguments': {'R': ('R', R)}}
    netlist.add_line(resistance)

    # fractional inductor
    fracintec = {'dictionary': 'fraccalc',
                 'component': 'int_e',
                 'label': 'L',
                 'nodes': ('B', datum),
                 'arguments': {'p': L, 'beta': 0.5}}
    netlist.add_line(fracintec)

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

    # ressort cubic
    stifness = {'dictionary': 'mechanics',
                'component': 'springcubic',
                'label': 'K',
                'nodes': ('E', 'F'),
                'arguments': {'K0': ('K0', K),
                              'K2': ('K2', 1e20)}
                }
    netlist.add_line(stifness)

    # amortissement
    damper = {'dictionary': 'mechanics',
              'component': 'damper',
              'label': 'A',
              'nodes': ('F', datum),
              'arguments': {'A': ('A', A)}}
    netlist.add_line(damper)

    return netlist


def init_phs():
    # import pHobj
    phs = pyphs.PHSObject(netlist(), label=label(), path=path())
    return phs


def input_sequence(amp=10000., f0=100.):
    from pyphs import signalgenerator
    fs = samplerate()
    nsin = int(1.*fs/f0)
    SigIn = signalgenerator(which="sin", n=nsin, ramp_on=False,
                            A=amp, f0=f0, fs=fs)

    def genu():
        for el in SigIn():
            yield [el, ]

    return genu(), nsin


def simulation(phs):
    opts = {'fs': samplerate(),
            'language': 'python',
            'split': True,
            'progressbar': True,
            'presolve': False}
    u, nt = input_sequence()
    phs.Simu.config.update(opts)
    phs.Simu.init(sequ=u, nt=nt)
    phs.Simu.process()


def run_test(clean=True):
    phs = init_phs()
    simulation(phs)
    if clean:
        import shutil
        shutil.rmtree(phs.path, ignore_errors=True)
    return True


if __name__ is '__main__':
    phs = init_phs()
    simulation(phs)
    phs.Simu.Data.plot_powerbal()
    phs.Simu.Data.plot_powerbal(mode='multi')
#    succeed = run_test(clean=True)
