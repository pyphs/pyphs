# -*- coding: utf-8 -*-
"""
Created on Nov 22 2016

@author: Falaize
"""


def label():
    """
    System's netlist and folder label
    """
    return "DLC"


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


def init_phs():
    # import pHobj
    from pyphs import PortHamiltonianObject
    import os
    phs = PortHamiltonianObject(label=label(),
                                path=os.getcwd() + os.sep + label())
    return phs


def build_graph(phs):
    phs.build_from_netlist('./dlc.net')


def input_sequence(amp=5., f0=100.):
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
            'split': True}
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
