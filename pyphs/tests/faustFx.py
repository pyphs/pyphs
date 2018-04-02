#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
from pyphs import Netlist

here = os.path.realpath(__file__)[:os.path.realpath(__file__).rfind(os.sep)]

def test_faust_fx_generation():
    path = os.path.join(here, 'lowpass.net')     # Absolute path

    netlist = Netlist(path)              # Init Netlist with path to '.net' file
    #print(netlist.netlist())             # print netlist content

    graph = netlist.to_graph()           # Build Graph object from netlist

    core = graph.to_core()     # perform graph analysis and produce `Core`object
    #core.pprint()              # show structure

    core.M, core.J(), core.R()

    core.reduce_z()            # reduce linear dissipation functions in matrix R
    #core.pprint()              # show structure
    core.M, core.J(), core.R()

    pfc, C, R1 = core.symbols(['pfc', 'CCapa', 'R1'])  # define some symbols

    fref = 20
    cutoff = fref*10**(3*pfc)           # pfc in [0, 1] => cutoff in [2e1, 2e4]
    rc = 1/(2*3.14157*cutoff*C)         # resistance = 1/(2*pi*cutoff*C)

    # 1 remplacer
    core.subs[R1] = rc                  # substitute symbol R1 by expression rc

    # 2 appliquer
    core.substitute(selfexprs=True)     # substitute symbols by expressions
    core.R()

    # 3 déclarer
    core.add_parameters(pfc)            # add pfc to the list of control parameters

    # path to generated .dsp file
    label = 'lowpass'
    dsppath = os.path.join(here, label+'.dsp')

    # Select inputs: list of constant values and input labels
    # Here, we select input as 'uI' and set 'uO' to constant 0
    inputs = (0., 'uI')

    # Select outputs: list of outputs labels
    outputs = ('yO', )

    from pyphs import core2faustfx
    core2faustfx(core, path=dsppath, inputs=inputs, outputs=outputs)

    os.remove(dsppath)

    return True
