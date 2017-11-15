#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 11:50:23 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

from pyphs.core.tools import free_symbols
from sympy.printing import ccode
import sympy as sp
from pyphs.core.tools import simplify
import time

def faust_expr(name, args, expr, subs):
    previous_expr = sp.sympify(0.)
    start = time.time()
    while previous_expr != expr and time.time()-start<10:
        previous_expr = expr
        expr = simplify(previous_expr)
    code = '\n' + name + " = \(" + ('{}, '*len(args)).format(*map(str, args))[:-2] + ').('
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
        code += faust_expr(name+str(i), argsnames, e, subs)
    code += '\n' + name + " = "
    if len(expr) > 0:
        code += joinListArgsNames
        code += " <: " + ''.join([name+str(i)+', ' for i in range(len(expr))])[:-2]
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

from pyphs.misc.tools import geteval

def multirecursive(method, process, nin, nout, inits):
    string = process
    for i in range(nin):
        if i < method.dims.x():
            initname = 'dx'
            initstart = 0
        elif i < method.dims.x()+method.dims.w():
            initname = 'w'
            initstart += method.dims.x()
        elif i < initstart+method.dims.w()+method.dims.x():
            initname = 'x'
            initstart += method.dims.w()
        elif i < initstart+method.dims.x()+method.dims.u():
            initname = 'u'
            initstart += method.dims.x()
        else:
            initname = 'o'
            initstart += method.dims.u()

        p1 = listToPassAllExcept([None, ]*(nin-i), 0)+',' if nin-i>0 else ''
        p2 = listToAllPass([None, ]*(nout-nin))
        prefix = 'prefix({0}, _)'.format(inits[initname][i-initstart])
        string = '(' + string + ') ~ {2} <: {0}{1}'.format(p1, p2, prefix)
    return string

def write_faust_fx(method, path=None, inputs=None, outputs=None, inits=None,
                   nIt=3):
    if inputs is None:
        inputs = list(map(str, method.u))
    if outputs is None:
        outputs = list(map(str, method.y))
    indin = []
    for i, u in enumerate(inputs):
        if isinstance(u, float):
            iin.append(i)
    iout = []
    for y in outputs:
        iout.append(method.y.index(method.symbols(y)))

    print('FAUST init...')
    if inits is None:
        inits = {}
    for name in ('x', 'dx', 'w', 'u', 'o', 'p'):
        if not name in inits.keys():
            inits[name] = [0, ]*len(geteval(method, name))
    if path is None:
        path = method.label + '.dsp'
    argsnames = ['dx', 'w', 'x', 'o', 'u']

    print('FAUST parameters...')
    code = '// Faust code associated with the PyPHS Method {0}'.format(method.label)
    code += '\n'
    code += '\nimport("stdfaust.lib");'
    code += '\n'
    nin = len(method.x)*2 + len(method.w) + len(method.observers)
    nout = nin + len(method.y)
    code += '\nprocess = {0}Recursion;'.format(method.label)
    code += '\n'
    code += '\n// Sample Rate'
    code += '\n{0} = ma.SR;'.format(str(method.fs))
    code += '\n'
    code += '\n// Constant Parameters'
    for k in method.subs.keys():
        code += '\n{0} = {1};'.format(str(k), method.subs[k])
    code += '\n'
    code += '\n// Constant Inputs'
    for i, k in enumerate(method.u):
        if i not in iin:
            code += '\n{0} = {1};'.format(str(k), inputs[i])
    code += '\n'
    code += '\n// Sliders Parameters'
    for p in method.p:
        code += '\n{0} = hslider("{0}", 0.5, 0., 1., 0.01);'.format(str(p))
    code += '\n'
    print('FAUST signals...')
    code += '\n// Pass'
    def code_pass(name):
        a = geteval(method, name)
        if len(a) > 0:
            return '\n{0} = {1};'.format(name, listToAllPass(a))
        else:
            return '\n{0} = 0. : !;'.format(name)
    for name in 'xwupov':
        cr = False
        for suffix in ('', 'l', 'nl'):
            try:
                c = code_pass(name+suffix)
                if not c == '':
                    code += c
                    cr = True
            except:
                pass
        if cr:
            code += '\n'
    code += '\n// Terminate'
    def code_terminate(name):
        a = geteval(method, name)
        if len(a) > 0:
            return '\n{0}T = {1};'.format(name, listToAllTerminate(a))
        else:
            return '\n{0}T = 0. : !;'.format(name)
    for name in 'xwupov':
        cr = False
        for suffix in ('', 'l', 'nl'):
            try:
                c = code_terminate(name+suffix)
                if not c == '':
                    code += c
                    cr = True
            except:
                pass
        if cr:
            code += '\n'
    print('FAUST arguments...')
    code += '\n// Arguments'
    code += '\nargs = x, w, x, o, u;\n'
    code += '\nargsT = xT, wT, xT, oT, uT;\n'
    code += '\n'
    code += '\n// Constants'
    code += '\nc = x, o, u;\n'
    code += '\ncT = xT, oT, uT;\n'
    code += '\n'
    code += '\n// Shortcuts'
    code += '\nv2vl = v :(vl, vnlT);\n'
    code += '\nv2vnl = v :(vlT, vnl);\n'
    code += '\nvlvnl2v = (vl, vnl) <: ((xl, wlT, vnlT), (vlT, xnl, wnlT), (xlT, wl, vnlT), (vlT, xnlT, wnl));\n'
    code += '\n'
    code += '\n// Update X and return args'
    code += '\nUpdateX = args <: (x, w, cT), ((x, wT, x, oT, uT) :> x), (xT, wT, xT, o, uT);'
    code += '\n'
    code += '\n// Define UpdateVl(dx, w, x, u, p, o)'
    code += faust_vector('UpdateVl', method.ud_vl, argsnames, method.subs, method)
    code += '\n'
    code += '\n// Define UpdateVnl(v, c)'
    code += faust_vector('UpdateVnl', method.ud_vnl, argsnames, method.subs, method)
    code += '\n'
    code += '\n// Define y'
    code += faust_vector('y', [method.output()[i] for i in iout],
                         argsnames, method.subs, method)
    code += '\n'
    code += '\n// UpdateLinear'
    code += '\nUpdateLinear = args <: (UpdateVl, (vlT, vnl, c)) : (vlvnl2v, c) : args;'
    code += '\n'
    code += '\n// UpdateNonLinear'
    code += '\nUpdateNonLinear = args <: ((vl, vnlT, cT), UpdateVnl, (vT, c)) : (vlvnl2v, c) : args;'
    udNL = 'UpdateNonLinear:'*nIt if len(method.vnl()) > 0 else ''
    udL = 'UpdateLinear' if len(method.vl()) > 0 else ''
    udXY = '<: (UpdateX, y)' if len(method.x) > 0 else '<: y'
    code += '\n'
    code += '\n// Main'
    code += '\n{0}Main = {1} {2} {3} ;'.format(method.label, udNL, udL, udXY)
    code += '\n'
    code += '\n// Recursion'
    code += '\n{0}Recursion = '.format(method.label)
    nin = len(method.x)*2 + len(method.w) + len(method.observers)
    nout = nin + len(method.y)
    code += multirecursive(method, method.label+'Main', nin, nout, inits) + ';'

    cin = '('
    for i in range(len(method.u)):
        if i in iin:
            index = iin.index(i)
            cin += '('
            for j in range(2):
                if j == index:
                    cin += '_, '
                else:
                    cin += '!, '
            cin = cin[:-2] + '), '
        else:
            cin += '((!, !) : ' + str(method.u[i]) + '), '

    cin = cin[:-2] + ')'
    code += '\n{0}InputToOutput = (_,_):{1}:{0}Recursion;'.format(method.label, cin, cout)

    with open(path, 'w') as f:
        for i, l in enumerate(code.splitlines()):
            if i > 0:
                f.write('\n')
            f.write(l)
#%%
#    simu = netlist.to_simulation(config=config)
#
#    dur = 0.01
#    u = signalgenerator(which='sin', f0=800., tsig=dur, fs=simu.config['fs'])
#
#    def sequ():
#        for el in u():
#            yield (el, )
#
#    simu.init(u=sequ(), nt=int(dur*simu.config['fs']))
#
#    # Run the simulation
#    simu.process()
#
#    simu.data.plot([('x', 0)])
#
#    # Plots
#    simu.data.plot_powerbal(mode='single')
#    simu.data.plot(['u', 'x', 'y'])
#
#    # clean: delete folders 'data' and 'figures'
#    shutil.rmtree(os.path.join(here, 'data'))
#    shutil.rmtree(os.path.join(here, 'figures'))
#
#    # clean: delete folder 'rlc'
#    if config['lang'] == 'c++':
#        shutil.rmtree(os.path.join(here, 'rlc'))
