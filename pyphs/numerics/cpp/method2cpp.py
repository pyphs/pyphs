# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 13:47:47 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

from .preamble import str_preamble
from .arguments import append_args
from .functions import append_funcs, append_funcs_constructors
from .operations import append_ops
from .tools import indent, SEP, formatPath
from pyphs.config import VERBOSE, CONFIG_NUMERIC, CONFIG_CPP
from pyphs.misc.tools import geteval
from pyphs.core.tools import substitute, free_symbols
from .tools import linesplit
import numpy
import sympy
import os
import copy

standard_config = {'path': os.getcwd()}


def init_eval(method, name):

    if (name not in method.inits_evals.keys() or
            method.inits_evals[name] is None):

        if VERBOSE >= 2:
            print('    Init value for {}'.format(name))

        if name in method.ops_names:
            obj = copy.copy(getattr(method, name+'_op'))
            sobj = eval_op(method, obj)
        elif name == 'y':
            obj = copy.copy(geteval(method, 'output'))
            sobj = substitute(obj, method.subscpp)
            sobj = numpy.asarray(sobj, dtype=float)
        else:
            obj = copy.copy(geteval(method, name))
            sobj = substitute(obj, method.subscpp)
            while not len(free_symbols(sobj)) == 0:
                sobjpre = copy.copy(sobj)
                sobj = substitute(sobj, method.subscpp)
                if sobj == sobjpre:
                    freesymbs = free_symbols(sobj)
                    text = 'Missing substitution symbols: {}'.format(freesymbs)
                    raise AttributeError(text)
            if not isinstance(sobj, (float, list)):
                sobj = numpy.asarray(sobj.tolist(), dtype=float)
            else:
                sobj = numpy.asarray(sobj, dtype=float)
        method.inits_evals[name] = sobj


def eval_op(method, op):

    def evaluate(args):
        return op.call[0](*args)

    args = []
    for arg in op.args:
        if isinstance(arg, method.Operation):
            args.append(eval_op(method, arg))
        elif isinstance(arg, str):
            init_eval(method, arg)
            args.append(method.inits_evals[arg])
        else:
            if not isinstance(arg, (float, int)):
                raise TypeError
            args.append(arg)

    return evaluate(args)


def method2cpp(method, objlabel=None, path=None,
               inits=None, config=None, subs=None):
    """
    Writes all files that define the c++ class associated with a given
    pyphs.Method.

    Parameters
    ----------

    method : pyphs.Method
        The object that will be converted to c++.


    objlabel : string (default is None)
        Name of the c++ class.


    path : string (default is None)
        Path to the folder where the source files will be generated.


    inits : dictionary (default is None)
        Dictionary of initialization values `{name: array}` with `name` in
        ('x', 'dx', 'w', 'u', 'p', 'o') and `array` an vector of floats with
        appropriate shape.

    config : dictionary (default is None)
        Dictionary of configuration options (see pyphs.config.CONFIG_NUMERIC).

    subs : dictionary or list (default is None)
        Dictionary or list of dictionaries of substitution parameters.
    """

    if VERBOSE >= 1:
        print('Prepare method {} for C++ generation...'.format(method.label))

    if inits is None:
        inits = {}

    if config is None:
        config = {}

    method.configcpp = CONFIG_NUMERIC.copy()
    method.configcpp.update(config)

    args_names = ['x', 'dx', 'w', 'u', 'p', 'o']
    for name in args_names:
        if name not in inits.keys() or inits[name] is None:
            inits[name] = list(sympy.zeros(len(geteval(method, name)), 1))

    method.inits = inits
    method.inits_evals = {}

    method.subscpp = method.subs.copy()

    method.subscpp[method.fs] = method.configcpp['fs']
    for name in args_names:
        for i, a in enumerate(geteval(method, name)):
            method.subscpp[a] = method.inits[name][i]

    for name in method.update_actions_deps():
        init_eval(method, name)

    if VERBOSE >= 1:
        print('Generate core C++ object {}...'.format(method.label))

    if objlabel is None:
        objlabel = 'phscore'.upper()
    else:
        objlabel = objlabel.upper()

    if path is None:
        path = os.getcwd() + os.sep + objlabel

    if not os.path.exists(path):
        os.makedirs(path)

    files = {}
    exts = ['cpp', 'h']

    for name in exts:
        files.update({name: {'public': '',
                             'private': '',
                             'init': '',
                             'data': '',
                             'starting': str_preamble(objlabel),
                             'closing': ''}})
    files['h']['starting'] += '\n'
    files['h']['starting'] += "\n#ifndef {0}_H".format(objlabel)
    files['h']['starting'] += "\n#define {0}_H".format(objlabel)
    h, cpp = _str_includes()
    files['h']['starting'] += h
    files['cpp']['starting'] += cpp
    files['h']['starting'] += _str_namespaces()
    files['h']['starting'] += "\n\nclass {0} ".format(objlabel) + "{"
    files['h']['closing'] += "\n}"+";\n\n#endif /* {0}_H */\n".format(objlabel)
    files['h']['private'] += '\nprivate:'
    files['h']['public'] += '\npublic:'
    if VERBOSE >= 2:
        print('    Build parameters...')
    append_parameters(method, files, objlabel)
    if VERBOSE >= 2:
        print('    Build update...')
    append_update(method, files, objlabel)
    if VERBOSE >= 2:
        print('    Build arguments...')
    append_args(method, files, objlabel)
    if VERBOSE >= 2:
        print('    Build functions...')
    append_funcs(method, files, objlabel)
    if VERBOSE >= 2:
        print('    Build operations...')
    append_ops(method, files, objlabel)
    if VERBOSE >= 2:
        print('    Build initialisation...')
    append_init(objlabel, files)
    if VERBOSE >= 2:
        print('    Build constructors...')
    append_constructor(method, objlabel, files)
#    append_constructor_init_vector(objlabel, files)
#    append_constructor_init_matrix(nums.method, objlabel, files)
    if VERBOSE >= 2:
        print('    Build destructor...')
    append_destructuor(objlabel, files)
    for e in exts:
        filename = path + os.sep + 'core.{0}'.format(e)
        if VERBOSE >= 1:
            print('    Write {}...'.format(filename))

        string = files[e]['starting']
        string += linesplit + '\n// PUBLIC'
        string += indent(files[e]['public'])
        string += '\n' + linesplit + '\n// PRIVATE'
        string += indent(files[e]['private'])
        string += files[e]['closing']

        _file = open(filename, 'w')
        _file.write(string)
        _file.close()

    if subs is None:
        subs = method.subs

    parameters_files = parameters(subs, objlabel)
    for e in exts:
        filename = path + os.sep + 'parameters.{0}'.format(e)
        if VERBOSE >= 1:
            print('    Write {}'.format(filename))
        string = parameters_files[e]
        _file = open(filename, 'w')
        _file.write(string)
        _file.close()


###############################################################################
# parameters

def append_parameters(method, files, objlabel):
    files['h']['private'] += linesplit + "\n// Sample Rate"
    files['h']['private'] += \
        '\n{0} sampleRate = {1};'.format(CONFIG_CPP['float'], method.subscpp[method.fs])
    files['h']['private'] += '\nconst {0} * F_S = & sampleRate;'.format(CONFIG_CPP['float'])
    files['h']['public'] += linesplit + "\n// Sample Rate"
    files['h']['public'] += '\nvoid set_sampleRate(float &);'
    files['h']['public'] += '\nvoid set_sampleRate(double &);'
    files['cpp']['public'] += linesplit + "\n// Sample Rate"
    files['cpp']['public'] += \
        "\nvoid {0}::set_sampleRate(float & value)".format(objlabel) +\
        " {\n" + indent('sampleRate = value;\ninit();') + '\n}'
    files['cpp']['public'] += \
        "\nvoid {0}::set_sampleRate(double & value)".format(objlabel) +\
        " {\n" + indent('sampleRate = value;\ninit();') + '\n}'
    files['h']['private'] += linesplit + "\n// Parameters"
    files['h']['private'] += '\nconst unsigned int indexParameters = 0;  // See file "parameters.cpp".'
    for i, sub in enumerate(method.subs):
        if not sub == method.fs:
            files['h']['private'] += \
                '\nconst {2} * {0} = & subs[indexParameters][{1}];'.format(str(sub), i, CONFIG_CPP['float'])


def parameters(subs, objlabel):
    """
    Generates the C++ files associated with the parameters
    """
    files = {'h': str_preamble(objlabel),
             'cpp': str_preamble(objlabel)}
    files['h'] += """
#ifndef PARAMETERS_H
#define PARAMETERS_H"""
    _append_include(files)
    _append_subs(subs, files)
    files['h'] += """\n
#endif /* defined(PARAMETERS_H) */
"""
    return files


def _append_include(files):
    """
    Used in .parameters()
    """
    files['cpp'] += """
# include "parameters.h"\
"""


def _append_subs(subs, files):
    """
    Used in .parameters()
    """
    if isinstance(subs, (tuple, list)):
        nsubs = len(subs)
    else:
        nsubs = 1
        subs = [subs, ]
    npars = len(subs[0])
    if npars > 0:
        files['h'] += """\n
extern const {2} subs[{0}][{1}];""".format(nsubs, npars, CONFIG_CPP['float'])
        files['cpp'] += """\n
// Correspondance is
"""
        for i, k in enumerate(subs[0].keys()):
            if not str(k) == 'F_S':
                files['cpp'] += '// subs[key][{}] = {}\n'.format(i, k)
        files['cpp'] += """\n
const {0} subs[{1}][{2}]""".format(CONFIG_CPP['float'], nsubs, npars) + """ = { """
        for i, s in enumerate(subs):
            files['cpp'] += indent(linesplit + '\n// key {}'.format(i))
            files['cpp'] += """
    {"""
            for k in s.keys():
                files['cpp'] += str(float(s[k])) + ', '
            files['cpp'] = files['cpp'][:-2] + """},
};"""


###############################################################################
# Constructors

def append_init(objlabel, files):
    title = linesplit + "\n// Initialization\n"
    files['h']['private'] += "{0}void {1}();".format(title, 'init')
    files['cpp']['private'] += title
    string = 'void {0}::{1}()'.format(objlabel, 'init') + '{'
    string += indent(files['cpp']['init'])
    string += '\n};'
    files['cpp']['private'] += string


def append_initParameters(objlabel, files):
    title = linesplit + "\n// Initialization\n"
    files['h']['private'] += "{0}void {1}(int &);".format(title, 'initParameters')
    files['cpp']['private'] += title
    string = 'void {0}::{1}(int & i)'.format(objlabel,
                                                           'init') + '{'
    string += indent('\nindexParameters = i;')
    string += indent('\ninit();')
    string += '\n};'
    files['cpp']['private'] += string


# ----------------------------------------------------------------------- #

def append_constructor(method, objlabel, files):
    title = linesplit + "\n// Default Constructor\n"
    files['h']['public'] += "{0}{1}();".format(title, objlabel)
    files['cpp']['public'] += title
    string = '{0}::{0}()'.format(objlabel)
    string += '{'
    string += indent(files['cpp']['data'])
    files['cpp']['public'] += string
    append_funcs_constructors(method, files, objlabel)
    string = indent(linesplit + "\n// Initialization")
    string += indent('\ninit();')
    string += '\n};'
    files['cpp']['public'] += string


#def append_constructor_init_matrix(method, objlabel, files):
#    title = "\n\n// Constructor with matrix state initalization\n\n"
#    mtype = matrix_type(method.dims.x(), 1)
#    files['h']['public'] += "{0}{1}({2} &);".format(title, objlabel, mtype)
#    files['cpp']['public'] += title
#    string = '{0}::{0}({1} & x0)'.format(objlabel, mtype) + '{\n'
#    string += "set_x(x0);"
#    string += '\n' + indent('init();') + '\n};'
#    files['cpp']['public'] += string
#
#
#def append_constructor_init_vector(objlabel, files):
#    title = "\n\n// Constructor with vector state initalization\n\n"
#    files['h']['public'] += "{0}{1}(vector<double> &);".format(title, objlabel)
#    files['cpp']['public'] += title
#    string = '{0}::{0}(vector<double> & x0)'.format(objlabel) + '{\n'
#    string += """
#    if (x().size() == x0.size()) {
#        set_x(x0);
#    }
#    else {
#        cerr << "Size of x0 does not match size of x" << endl;
#        exit(1);
#    }"""
#    string += '\n' + indent('init();') + '\n};'
#    files['cpp']['public'] += string


def append_destructuor(objlabel, files):
    title = linesplit + "\n// Default Destructor\n"
    files['h']['public'] += "{0}~{1}();".format(title, objlabel)
    files['cpp']['public'] += title
    string = '{0}::~{0}()'.format(objlabel) + '{\n};'
    files['cpp']['public'] += string


###############################################################################
def _str_includes():
    string_c = '\n#include "core.h"'
    string_h = """\n
#include <iostream>
#include <vector>
#include <cmath>
#include <Eigen/Dense>
#include "parameters.h"\n
"""
    return string_h, string_c


def _str_namespaces():
    string = '\n'
    string += '\nusing namespace std;'
    string += '\nusing namespace Eigen;'
    return string

###############################################################################


def execs(actions):
    string = ''
    for action in actions:
        if isinstance(action, str):
            string += '\n{0}_update();'.format(action)
        else:
            string += '\n{0}_update();'.format(action[1])
            string += '\nset_{0}(_{1});'.format(*action)
    return string


def iterate(method, actions, res_label, step_label):
    string = ''
    string += "\nunsigned int iter_{0} = 0;".format(res_label)
    string += "\n_{0} = 1;".format(step_label)
    it = "(iter_{0}<{1})".format(res_label, method.configcpp['maxit'])
    res = "({0}()>{1})".format(res_label, method.configcpp['eps'])
    step = "({0}()>{1})".format(step_label, method.configcpp['eps'])
    string += \
        "\nwhile ({0} & {1} & {2})".format(it, res, step) + '{'
    string += \
        indent(execs(actions) + 'iter_{0} += 1;'.format(res_label)) + '\n}'
    return string


def append_update(method, files, objlabel):
    string_h = ""
    string_cpp = ""
    string_h += "\nvoid update();"
    string_cpp += """
void """ + objlabel + '::' + """update(){"""
    for action in method.update_actions:
        if action[0] == 'exec':
            string_cpp += indent(execs(action[1]))
        elif action[0] == 'iter':
            string_cpp += indent(iterate(method, *action[1]))
    string_cpp += "\n}"
    files['h']['public'] += linesplit + "\n// Core update"
    files['h']['public'] += string_h
    files['cpp']['public'] += linesplit + "\n// Core update"
    files['cpp']['public'] += string_cpp
