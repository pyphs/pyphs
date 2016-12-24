# -*- coding: utf-8 -*-
"""
Created on Sat May 21 10:50:30 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function
import pyphs
import os


def label():
    """
    System's netlist and folder label
    """
    return "rlc"


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


def netlist(R1=1e3, L=5e-2, C=2e-6):
    """
    Write netlist for RLC circuit
    """
    netlist = pyphs.PHSNetlist(path() + os.sep + label() + '.net', clear=True)

    datum = netlist.datum

    # input voltage
    source = {'dictionary': 'electronics',
              'component': 'source',
              'label': 'IN',
              'nodes': (datum, 'A'),
              'arguments': {'type': 'voltage'}}
    netlist.add_line(source)

    # resistor 1
    resistance = {'dictionary': 'electronics',
                  'component': 'resistor',
                  'label': 'R1',
                  'nodes': ('A', 'B'),
                  'arguments': {'R': ('R1', R1)}}
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
    return netlist


def init_phs():
    # import pHobj
    phs = pyphs.PHSObject(netlist(), label=label(), path=path())
    return phs


def input_sequence(amp=100., f0=100.):
    from pyphs import signalgenerator
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
            'split': True,
            'progressbar': True}
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
    succeed = run_test()
