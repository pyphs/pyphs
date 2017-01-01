#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 19:42:27 2016

@author: Falaize
"""
from pyphs.cpp.tools import indent, include_Eigen, matrix_type
import sympy
from pyphs.core.symbs_tools import simplify




def _pieces_matrix(method, name, objlabel):
    from sympy.printing import ccode
    mat = sympy.Matrix(getattr(method, name + '_expr'))
    str_definition = ""
    str_update_h, str_update_cpp = "", ""
    str_init_data, str_init_cpp = "", ""
    if not any(dim == 0 for dim in mat.shape):
        mtype = matrix_type(mat.shape[0], mat.shape[1])
        str_definition += '\n' + mtype + ' ' + name + ';'
        str_init_cpp += '\n' + name + " = Map<" + mtype +\
            "> (" + name + '_data);'
        str_init_data += '\ndouble ' + name + '_data[] = {'
        str_update_h += '\n' + 'void ' + name + '_update();'
        str_update_cpp += '\n' + 'void ' + objlabel + '::' +\
            name + '_update(){'
        for n in range(mat.shape[1]):
            for m in range(mat.shape[0]):
                expr = mat[m, n]
                symbs = expr.free_symbols
                if any(symb in method.args for symb in symbs):
                    str_init_data += "0, "
                    str_update_cpp += '\n' + name + str((m, n)) + ' = '
                    str_update_cpp += ccode(expr,
                                            dereference=method.args +
                                            [k for k in method.core.subs])
                    str_update_cpp += ';'
                else:
                    str_init_data += ccode(expr,
                                           dereference=method.args +
                                           [k for k in method.core.subs]) + \
                                           ', '
        str_update_cpp += '\n};'
        str_init_data = str_init_data[:-2] + '};'
    return str_definition, str_update_cpp, str_update_h, str_init_data,\
        str_init_cpp


def _pieces_matrices(method, objlabel):
    defs, udcpps, udhs, datas, inits = [str(), ]*5
    for name in method.funcs_names:
        de, udcpp, udh, data, init = _pieces_matrix(method,
                                                     name, objlabel)
        defs += de
        udcpps += udcpp
        udhs += udh
        datas += data
        inits += init
    return defs, udcpps, udhs, datas, inits


def _append_matrices(method, name, objlabel, files):
    str_definitions, str_update_cpps, str_update_hs, _, _ = \
        _pieces_matrices(phs)
    title = "\n\n// Matrices definitions"
    files['h'] += indent(title)
    files['h'] += indent(str_definitions)
    parser = {'Dl': 'iDl',
              'Nlxl': 'barNlxl',
              'Nlnl': 'barNlnl',
              'Nly': 'barNly',
              'Nnlnl': 'barNnlnl',
              'Nnll': 'barNnll',
              'Nnlxl': 'barNnlxl',
              'Nnly': 'barNnly',
              'c': 'fnl',
              'Fnl': 'fnl',
              'jac_Fnl': 'jac_fnl',}
    names = ('Dl',
             'Nlxl', 'Nlnl', 'Nly',
             'Nnlxl', 'Nnlnl', 'Nnly',
             'c', 'Fnl', 'jac_Fnl')
    for name in names:
        shape = sympy.Matrix(getattr(phs.simu.exprs,
                                     parser[name] + '_expr')).shape
        if not any(dim == 0 for dim in shape):
            files['h'] += '\n' + indent(matrix_type(shape[0], shape[1]) +
                                        ' ' + name + ';')

    title = "\n\n// Matrices updates"
    files['h'] += indent(title)
    files['h'] += indent(str_update_hs)
    files['cpp'] += title
    files['cpp'] += str_update_cpps


def _str_init_matrices(method):
    _, _, _, str_init_datas, str_init_cpps = _pieces_matrices(method)
    string = "\n\n// Matrices constants"
    string += str_init_datas
    string += "\n\n// Matrices init"
    string += str_init_cpps
    return indent(string)



def _append_includes(files):
    files['cpp'] += '\n#include "core.h"'
    include_vector = """\n
#include "iostream"
#include "vector"
#include "math.h"

# include "data.h"\n
"""
    files['h'] += include_vector + include_Eigen()


def _append_namespaces(files):
    files['h'] += '\n'
    files['h'] += '\nusing namespace std;'
    files['h'] += '\nusing namespace Eigen;'


def _append_args(method, files):
    title = "\n\n// Arguments"
    files['h'] += indent(title)
    files['h'] += indent('\n%s args;\n' % matrix_type(len(method.args), 1))
    for i, arg in enumerate(method.args):
        files['h'] += indent(
            '\ndouble * %s = & args(%i, 0);' % (str(arg), i))

def _append_args_accessors_vector(method, files, objlabel):
    title = "\n\n// Acessors to Arguments, return vector<double>."
    files['h'] += indent(title)
    files['cpp'] += title
    for name in method.args_names:
        arg = getattr(method, name+'_expr')
        dim = len(arg)
        files['h'] += indent('\nvector<double> ' +
                             name + '() const;')
        files['cpp'] += """
\nvector<double> """ + objlabel + '::' + name + """() const {
    vector<double> v = vector<double>(""" + str(dim) + """);"""
        for i, symb in enumerate(arg):
            files['cpp'] += """
    v[""" + str(i) + "] = *" + str(symb) + ";"
        files['cpp'] += """
    return v;
}"""


def _append_args_accessors_matrix(method, files, objlabel):
    title = "\n\n// Acessors to Arguments, return Matrix<double, n, m>."
    files['h'] += indent(title)
    files['cpp'] += title
    for name in method.args_names:
        arg = getattr(method, name+'_expr')
        dim = len(arg)
        files['h'] += indent('\nMatrix<double, ' + str(dim) + ', 1> ' +
                             name + '() const;')
        files['cpp'] += """
\nMatrix<double, """ + str(dim) + """, 1> """ + objlabel + '::' + name + """() const {
    Matrix<double, """ + str(dim) + """, 1> m;"""
        for i, symb in enumerate(arg):
            files['cpp'] += """
    m(""" + str(i) + ", 0) = *" + str(symb) + ";"
        files['cpp'] += """
    return m;
}"""


def _append_args_mutators_matrix(method, files, objlabel):
    title = "\n\n// Mutators for Arguments, type = Matrix<double, n, m>"
    files['h'] += indent(title)
    files['cpp'] += title
    for name in method.args_names:
        arg = getattr(method, name+'_expr')
        dim = len(arg)
        files['h'] += indent('\nvoid set_' + name + '(Matrix<double, ' + str(dim) + ', 1> &);')
        files['cpp'] += """\n
void """ + objlabel + '::set_' + name + """(Matrix<double, """ + str(dim) + ", 1> & m) {"
        for i, symb in enumerate(arg):
            files['cpp'] += """
    *"""+ str(symb) + " = m(" + str(i) + ", 0);"
        files['cpp'] += """
}"""


def _append_args_mutators_vectors(method, files, objlabel):
    title = "\n\n// Mutators for Arguments, type = vector<double>"
    files['h'] += indent(title)
    files['cpp'] += title
    for name in method.args_names:
        arg = getattr(method, name+'_expr')
        files['h'] += indent('\nvoid set_' + name + '(vector<double> &);')
        files['cpp'] += """\n
void """ + objlabel + '::set_' + name + """(vector<double> & v) {"""
        for i, symb in enumerate(arg):
            files['cpp'] += """
    *"""+ str(symb) + " = v[" + str(i) + "];"
        files['cpp'] += """
}"""

###########################################################################
def dereference(method):
    return method.core.args() + [k for k in method.core.subs]


def _append_funcs_updates(method, files, objlabel):
    from sympy.printing import ccode
    title = "\n\n// Functions updates"
    files['h'] += indent(title)
    files['cpp'] += title
    for name in method.funcs_names:
        expr = getattr(method, name+'_expr')
        if isinstance(expr, list):
            expr = sympy.Matrix(expr)
        expr = simplify(expr)

        files['h'] += "\n" + indent("void " + name + '_update();')
        files['cpp'] += "\nvoid " + objlabel + '::' + \
            name + '_update(){'

        if isinstance(expr, sympy.Expr):
            code = ccode(expr)
            files['cpp'] += "\n" + name + ' = ' + code + ';'
        elif isinstance(expr, sympy.Matrix):
            for m in range(expr.shape[0]):
                for n in range(expr.shape[1]):
                    code = ccode(expr[m, n],
                                 dereference=dereference(method))
                    files['cpp'] += "\n" + name + \
                        '(' + str(m) + ', ' + str(n) + ') = ' + code + ';'
        files['cpp'] += '\n};'


###########################################################################


def _str_matblk(mat_name, blck_name, blck_dims, blck_pos):
    string = "\ndouble * ptr_" + blck_name + " = "
    str_dims = "<" + str(blck_dims[0]) + ', ' + str(blck_dims[1]) + ">"
    str_pos = "(" + str(blck_pos[0]) + ', ' + str(blck_pos[1]) + ")"
    string += " & " + mat_name + ".block" + str_dims + str_pos + "(0);"
    string += "\nMap<Matrix<double, " + str_dims[1:-1] + ">> "
    string += blck_name + '(ptr_' + blck_name + ', ' + str_dims[1:-1] + ');'
    return string


def _append_matblk(method, files):
    string = "\n\n// System vectors"
    names = ('x', 'dx', 'dxH', 'w', 'z')
    for name in names:
        string += "\nMatrix<double, " + str(1212) + ", 1> " +\
            name + ";"
        string += _str_matblk(name, name + 'lnl', (1213, 1), (1214, 0))
    names = ('u', 'y', 'p')
    for name in names:
        string += "\nMatrix<double, " + str(1215) + ", 1> " +\
                name + ";"
    files['h'] += string


def _append_matblk_accessors_vector(method, files, objlabel):
    title = "\n\n// Acessors to system variables"
    files['h'] += indent(title)
    files['cpp'] += title
    names = ('x', 'dx', 'dxH', 'w', 'z', 'y')
    for name in names:
        files['h'] += indent('\nvector<double> get_' +
                             name + '() const;')
        files['cpp'] += """
\nvector<double> """ + objlabel + '::get_' + name + """() const {
vector<double> v = vector<double>(""" + str('#dim#') + """);
for (int i=0; i<""" + str('#dim#') + """; i++) {
    v[i] = """ + name + """[i];
}
return v;
}"""


###########################################################################


if __name__ == '__main__':
    files = {'h':'', 'cpp':''}
    objlabel = 'test'.upper()
#    _append_includes(files)
#    _append_namespaces(files)
    _append_subs(method, files)
    _append_args(method, files)
#    _append_args_accessors_matrix(method, files, objlabel)
#    _append_funcs(method, files, objlabel)
#    _append_vecs_args(method, files)
#    _append_blocks_accessors(method, files, objlabel)
#    _append_args_mutators_matrix(method, files, objlabel)
#    _append_args_mutators_vectors(method, files, objlabel)
    print(files['h'])

