# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 13:47:47 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

from .preamble import str_preamble
from .arguments import append_args
from .functions import append_funcs
from .operations import append_ops
from .tools import indent, matrix_type, SEP, formatPath
from pyphs.config import EIGEN_PATH as config_eigen_path
from pyphs.config import VERBOSE
import os

standard_config = {'path': os.getcwd()}


def numcore2cpp(nums, objlabel=None, path=None, eigen_path=None):
    if VERBOSE >= 1:
        print('Generate core C++ object...')
    if objlabel is None:
        objlabel = 'phscore'.upper()
    else:
        objlabel = objlabel.upper()
    if path is None:
        path = os.getcwd() + os.sep + objlabel
    if not os.path.exists(path):
        os.makedirs(path)
    if eigen_path is None:
        eigen_path = config_eigen_path
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
    h, cpp = _str_includes(formatPath(eigen_path))
    files['h']['starting'] += h
    files['cpp']['starting'] += cpp
    files['h']['starting'] += _str_namespaces()
    files['h']['starting'] += "\n\nclass {0} ".format(objlabel) + "{"
    files['h']['closing'] += "\n}"+";\n\n#endif /* {0}_H */\n".format(objlabel)
    files['h']['private'] += '\nprivate:'
    files['h']['public'] += '\npublic:'
    if VERBOSE >= 2:
        print('    Build parameters...')
    append_parameters(nums.method, files, objlabel)
    if VERBOSE >= 2:
        print('    Build update...')
    append_update(nums.method, files, objlabel)
    if VERBOSE >= 2:
        print('    Build arguments...')
    append_args(nums, files, objlabel)
    if VERBOSE >= 2:
        print('    Build functions...')
    append_funcs(nums, files, objlabel)
    if VERBOSE >= 2:
        print('    Build operations...')
    append_ops(nums, files, objlabel)
    if VERBOSE >= 2:
        print('    Build initialisation...')
    append_init(objlabel, files)
    if VERBOSE >= 2:
        print('    Build constructors...')
    append_constructor(objlabel, files)
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
        string += '\n\n// PUBLIC'
        string += indent(files[e]['public'])
        string += '\n\n\n// PRIVATE'
        string += indent(files[e]['private'])
        string += files[e]['closing']

        _file = open(filename, 'w')
        _file.write(string)
        _file.close()

    parameters_files = parameters(nums.method.subs, objlabel)
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
    files['h']['private'] += "\n\n// Parameters\n"
    files['h']['private'] += '\nconst unsigned int indexParameters = 0;' + '\n'
    for i, sub in enumerate(method.subs):
        if str(sub) == 'F_S':
            files['h']['private'] += "\n\n// Sample Rate"
            files['h']['private'] += \
                '\n\ndouble sampleRate = {};'.format(method.subs[sub])
            files['h']['private'] += \
                '\nconst double * F_S = & sampleRate;'
            files['h']['public'] += "\n\n// Sample Rate\n"
            files['h']['public'] += \
                '\nvoid set_sampleRate(double &);'
            files['cpp']['public'] += "\n\n// Sample Rate\n"
            files['cpp']['public'] += \
                "\nvoid {0}::set_sampleRate(double & value)".format(objlabel) +\
                " {\n" + indent('sampleRate = value;') + '\n}'                
        else:
            files['h']['private'] += \
                '\nconst double * {0} = & subs[indexParameters][{1}];'.format(str(sub), i)
            

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
    dim = len(subs)
    if dim > 0:
        files['h'] += """\n
extern const double subs[1][""" + str(dim) + """];"""
        files['cpp'] += """\n
// Correspondance is
"""
        for i, k in enumerate(subs):
            if not str(k) == 'F_S':
                files['cpp'] += '// subs[i][{}] = {}\n'.format(i, k)
                
        files['cpp'] += """\n
const double subs[1][""" + str(dim) + """] = {
    {"""
        for k in subs:
            if not str(k) == 'F_S':
                files['cpp'] += str(float(subs[k])) + ', '
        files['cpp'] = files['cpp'][:-2] + """},
};"""


###############################################################################
# Constructors

def append_init(objlabel, files):
    title = "\n\n// Initialization\n\n"
    files['h']['private'] += "{0}void {1}();".format(title, 'init')
    files['cpp']['private'] += title
    string = 'void {0}::{1}()'.format(objlabel, 'init') + '{'
    string += indent(files['cpp']['data'])
    string += indent(files['cpp']['init'])
    string += '\n};'
    files['cpp']['private'] += string


def append_initParameters(objlabel, files):
    title = "\n\n// Initialization\n\n"
    files['h']['private'] += "{0}void {1}(int &);".format(title, 'initParameters')
    files['cpp']['private'] += title
    string = 'void {0}::{1}(int & i)'.format(objlabel, 
                                                           'init') + '{'
    string += indent('\nindexParameters = i;')
    string += indent('\ninit();')
    string += '\n};'
    files['cpp']['private'] += string


# ----------------------------------------------------------------------- #

def append_constructor(objlabel, files):
    title = "\n\n// Default Constructor\n\n"
    files['h']['public'] += "{0}{1}();".format(title, objlabel)
    files['cpp']['public'] += title
    string = '{0}::{0}()'.format(objlabel)
    string += '{\n' + indent('init();') + '\n};'
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
    title = "\n\n// Default Destructor\n\n"
    files['h']['public'] += "{0}~{1}();".format(title, objlabel)
    files['cpp']['public'] += title
    string = '{0}::~{0}()'.format(objlabel) + '{\n};'
    files['cpp']['public'] += string


###############################################################################
def include_Eigen(eigen_path):
    return r'#include <{0}{1}Eigen{1}Dense>'.format(eigen_path, SEP)


def _str_includes(eigen_path):
    string_c = '\n#include "core.h"'
    string_h = """\n
#include "iostream"
#include "vector"
#include "math.h"

# include "parameters.h"\n
"""
    string_h += include_Eigen(eigen_path)
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
    it = "(iter_{0}<{1})".format(res_label, method.config['maxit'])
    res = "({0}()>{1})".format(res_label, method.config['eps'])
    step = "({0}()>{1})".format(step_label, method.config['eps'])
    string += \
        "\nwhile ({0} & {1} & {2})".format(it, res, step) + '{'
    string += \
        indent(execs(actions) + 'iter_{0} += 1;'.format(res_label)) + '\n}'
    return string


def append_update(method, files, objlabel):
    string_h = ""
    string_cpp = ""
    string_h += "\nvoid update();"
    string_cpp += """\n
void """ + objlabel + '::' + """update(){\n"""
    for action in method.update_actions:
        if action[0] == 'exec':
            string_cpp += '\n' + indent(execs(action[1]))
        elif action[0] == 'iter':
            string_cpp += '\n' + indent(iterate(method, *action[1]))
    string_cpp += "\n}"
    files['h']['public'] += "\n\n// Core update\n"
    files['h']['public'] += string_h
    files['cpp']['public'] += "\n\n// Core update\n"
    files['cpp']['public'] += string_cpp
