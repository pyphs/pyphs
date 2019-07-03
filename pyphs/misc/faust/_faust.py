#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 11:50:23 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

from sympy.printing import ccode
import sympy as sp
from pyphs.core.tools import simplify
from pyphs.misc.tools import geteval
from pyphs.config import VERBOSE
import time
from ._method_invmat import MethodInvMat
import os
import string

here = os.path.realpath(__file__)[:os.path.realpath(__file__).rfind(os.sep)]


def faust_expr(name, args, expr, subs):
    previous_expr = sp.sympify(0.)
    start = time.time()
    while previous_expr != expr and time.time()-start < 10:
        previous_expr = expr
        expr = simplify(previous_expr)
    code = '\n' + \
        name + " = \(" + \
        ('{}, '*len(args)).format(*map(str, args))[:-2] + ').('
    code += ccode(expr)
    code += ');'
    return code.replace('(-', '(0-')


def faust_vector(name, expr, argsnames, subs, method):
    joinListArgsNames = ', '.join(map(lambda s: s[-1], argsnames))
    methodargs = []
    for namea in argsnames:
        methodargs.extend(geteval(method, namea))
    argsnames = list(map(str, methodargs))
    code = str()
    for i, e in enumerate(expr):
        if VERBOSE >= 2:
            print('    Generate Faust expression {}[{}]'.format(name, i))
        code += faust_expr(name+str(i), argsnames, e, subs)
    code += '\n'*2 + name + " = "
    if len(expr) > 0:
        code += joinListArgsNames
        code += " <: " + ''.join([name+str(i)+', '
                                  for i in range(len(expr))])[:-2]
    else:
        code += '0. : ! '
    code += ';'
    return code


def listToAllPass(l):
    return ('_, '*len(l))[:-2]


def listToAllTerminate(l):
    return ('!, '*len(l))[:-2]


def listToTerminateAllExcept(l, i):
    string = ''
    for n, el in enumerate(l):
        string += '_, ' if n == i else '!, '
    return string[:-2]


def listToPassAllExcept(l, i):
    string = ''
    for n, el in enumerate(l):
        string += '!, ' if n == i else '_, '
    return string[:-2]


def multirecursive(method, process, nin, nout, inits):

    # init string with "process" content
    string = process

    # get dims
    nx = method.dims.x()
    nw = method.dims.w()
    nu = method.dims.y()

    # for each input to recursion process
    for i in range(nin):
        # select name and index depending on the type of recursion input
        if i < nx:
            # State increment
            initname = 'dx'
            initstart = 0
        elif i < nx + nw:
            # Dissipative variable
            initname = 'w'
            initstart = nx
        elif i < nx + nw + nx:
            # State
            initname = 'x'
            initstart = nx + nw
        elif i < nx + nw + nx + nu:
            # Input
            initname = 'u'
            initstart = nx + nw + nx
        else:
            # Observer
            initname = 'o'
            initstart += nx + nw + nx + nu

        # parameters for recursion
        p1 = listToPassAllExcept([None, ]*(nin-i), 0)+',' if nin-i > 0 else ''
        p2 = listToAllPass([None, ]*(nout-nin))

        # faust init (prefix)
        prefix = 'prefix({0}, _)'.format(inits[initname][i-initstart])

        # recursion
        string = '(' + string + ') ~ {2} <: {0}{1}'.format(p1, p2, prefix)
    return string


def write_faust_fx(method, path=None, inputs=None, outputs=None, inits=None,
                   nIt=10):
    """
    write a Faust process (.dsp)

    parameters
    ----------

    method : MethodInvMat

    path : str
        path to generated .dsp

    inputs : list of str
        list of inputs symbols

    outputs : list of str
        list of output symbols

    inits : dict
        Dictionary of initialisation values

    nIt : int
        Number of NL solver iterations
    """

    if VERBOSE >= 1:
        print('Generate Faust code')

    with open(os.path.join(here, 'faustfx.template'), 'r') as f:
        template = string.Template(f.read())

    if inputs is None:
        inputs = list(map(str, method.u))

    # list of input indices
    iin = []
    for i, u in enumerate(inputs):
        if not isinstance(u, float):
            iin.append(method.u.index(method.symbols(str(u))))

    if outputs is None:
        outputs = list(map(str, method.y))

    # list of output indices
    iout = []
    for y in outputs:
        iout.append(method.y.index(method.symbols(str(y))))

    # initializations
    if inits is None:
        inits = {}
    for name in ('x', 'dx', 'w', 'u', 'o', 'p'):
        if name not in inits.keys():
            inits[name] = [0., ]*len(geteval(method, name))

    # set path
    if path is None:
        path = method.label + '.dsp'
    argsnames = ['dx', 'w', 'x', 'o', 'u']

    # inputs processes
    cinputs = '('
    for i, ui in enumerate(method.u):
        if i in iin:
            cinputs += '_, '
        else:
            cinputs += str(ui) + ', '
    cinputs = cinputs[:-2] + ')'

    # constant values for parameters
    constPars = ''
    for k in method.subs.keys():
        constPars += '\n{0} = {1};'.format(str(k), method.subs[k])
    if constPars == '':
        constPars = '// None'

    # constant values for inputs
    constInputs = ''
    for i, ui in enumerate(method.u):
        if i not in iin:
            constInputs += '\n{0} = {1};'.format(str(ui), inputs[i])
    if constInputs == '':
        constInputs = '// None'

    # sliders for controlled parameters
    sliders = ''
    for p in method.p:
        sliders += '\n{0} = hslider("{0}", 0.5, 0., 1., 0.001);'.format(str(p))
    if sliders == '':
        sliders = '// None'

    # all-pass processes
    def code_pass(name):
        a = geteval(method, name)
        if len(a) > 0:
            return '\n{0} = {1};'.format(name, listToAllPass(a))
        else:
            return '\n{0} = 0. : !;'.format(name)

    cpass = ''
    for name in 'xwupov':
        cr = False
        for suffix in ('', 'l', 'nl'):
            try:
                c = code_pass(name+suffix)
                if not c == '':
                    cpass += c
                    cr = True
            except:
                pass
        if cr:
            cpass += '\n'

    # all-cut processes
    def code_terminate(name):
        a = geteval(method, name)
        if len(a) > 0:
            return '\n{0}T = {1};'.format(name, listToAllTerminate(a))
        else:
            return '\n{0}T = 0. : !;'.format(name)
    cstop = ''
    for name in 'xwupov':
        cr = False
        for suffix in ('', 'l', 'nl'):
            try:
                c = code_terminate(name+suffix)
                if not c == '':
                    cstop += c
                    cr = True
            except:
                pass
        if cr:
            cstop += '\n'

    # update vl = (dxl, wl)
    udvl = faust_vector('udvl', method.ud_vl, argsnames, method.subs, method)
    udL = 'iterationL' if len(method.vl()) > 0 else 'args'

    # update vnl = (dxnl, wnl)
    udvnl = faust_vector('udvnl',
                         method.ud_vnl,
                         argsnames,
                         method.subs,
                         method)
    udNL = ('iterationNL : '*nIt)[:-1] if len(method.vnl()) > 0 else ''

    # update x and y
    udXY = '<: (udx, y)' if len(method.x) > 0 else '<: y'
    y = faust_vector('y', [method.output()[i] for i in iout],
                     argsnames, method.subs, method)

    # Faust recursion
    nin = len(method.x)*2 + len(method.w) + len(method.observers)
    nout = nin + len(outputs)
    recursion = multirecursive(method, 'iteration', nin, nout, inits)

    # Faust comments
    infoIn = ''
    for i in range(len(method.u)):
        if i in iin:
            infoIn += str(method.u[i]) + ', '

    infoOut = ''
    for i in range(len(method.y)):
        if i in iout:
            infoOut += str(method.y[i]) + ', '

    infoPars = ''
    for p in method.p:
        infoPars += str(p) + ', '

    # Substitutions
    subs = {'inputs': cinputs,
            'label': method.label,
            'fs': str(method.fs),
            'constPars': constPars,
            'constInputs': constInputs,
            'sliders': sliders,
            'pass': cpass,
            'stop': cstop,
            'udvl': udvl,
            'udvnl': udvnl,
            'y': y,
            'udNL': udNL,
            'udL': udL,
            'udXY': udXY,
            'recursion': recursion,
            'in': infoIn[:-2] + '.',
            'out': infoOut[:-2] + '.',
            'pars': infoPars[:-2] + '.'}

    cfaust = template.substitute(subs)

    # Write FAUST .dsp file
    with open(path, 'w') as f:
        for i, l in enumerate(cfaust.splitlines()):
            if i > 0:
                f.write('\n')
            f.write(l)


def core2faustfx(core, config=None, path=None, inputs=None,
                 outputs=None, inits=None, nIt=10):
    """
    write a Faust process (.dsp)

    parameters
    ----------

    core : Core

    config : dict or None
        A dictionary of numerical parameters. If None, the standard
        pyphs.config.simulations is used (the default is None).
        keys and default values are

          'fs': 48e3,           # Sample rate (Hz)
          'grad': 'discret',    # In {'discret', 'theta', 'trapez'}
          'theta': 0.,          # Theta-scheme for the structure
          'split': True,        # split implicit from explicit part
          'maxit': 10,          # Max number of iterations for NL solvers

    path : str
        path to generated .dsp

    inputs : list of str
        list of inputs symbols

    outputs : list of str
        list of output symbols

    inits : dict
        Dictionary of initialisation values

    nIt : int
        Number of NL solver iterations
    """

    method = MethodInvMat(core, config)
    write_faust_fx(method, path=path, inputs=inputs, outputs=outputs,
                   inits=inits, nIt=nIt)
