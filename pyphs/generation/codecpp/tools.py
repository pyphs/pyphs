# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 16:01:13 2016

@author: Falaize
"""


def matrix_type(dim1, dim2):
    return "Matrix<double, " + str(dim1) + ', ' + str(dim2) + '>'
#    return "Matrix<double, " + str(dim1) + ', ' + str(dim2) + ', RowMajor>'


def indent(string):
    return "\n".join(['    ' + el for el in string.split('\n')])


def cppobj_name(phs):
    return phs.label.upper()


def name2dim(name):
    """
    return dim label associated with variable 'name' (eg. 'nx' if name='dxH').
    """
    parser = {'x': 'nx',
              'dx': 'nx',
              'dxH': 'nx',
              'xl': 'nxl',
              'dxl': 'nxl',
              'dxHl': 'nxl',
              'xnl': 'nxnl',
              'dxnl': 'nxnl',
              'dxHnl': 'nxnl',
              'x0': 'nx',
              'w': 'nw',
              'z': 'nw',
              'wl': 'nwl',
              'zl': 'nwl',
              'wnl': 'nwnl',
              'znl': 'nwnl',
              'u': 'ny',
              'y': 'ny',
              'p': 'np',
              'subs': 'nsubs',
              'vl': 'nl',
              'vnl': 'nnl',
              'fl': 'nl',
              'fnl': 'nnl'}
    return parser[name]


def include_Eigen():
    from config import eigen_path
    return '#include <' + eigen_path + '/Eigen/Dense>'


def str_matblk(mat_name, blck_name, blck_dims, blck_pos):
    string_h = "\ndouble * ptr_" + blck_name + " = "
    str_dims = "<" + str(blck_dims[0]) + ', ' + str(blck_dims[1]) + ">"
    str_pos = "(" + str(blck_pos[0]) + ', ' + str(blck_pos[1]) + ")"
    string_h += " & " + mat_name + ".block" + str_dims + str_pos + "(0);"
    string_cpp = "\nMap<Matrix<double, " + str_dims[1:-1] + ">> "
    string_cpp += blck_name + '(ptr_' + blck_name + ', ' + \
        str_dims[1:-1] + ');'
    return string_h, string_cpp


def str_dims(phs):
    string = "\n\n// System dimensions"
    names = ('x', 'xl', 'xnl', 'w', 'wl', 'wnl', 'y', 'p', 'subs')
    for name in names:
        dim = getattr(phs.simu.exprs, name2dim(name))
        if dim > 0:
            string += "\nconst unsigned int " + name2dim(name) + " = " + \
                str(dim) + ";"
    return string


def cppsubs(phs):
    """
    build the dictionary of parameters substitution and return the piece of \
cpp code for the pointers in subs and values in subsvals

    Parameters
    -----------

    phs : PortHamiltonianObject

    Outputs
    ---------

    str_subs : string

        cpp code, piece of header (.h) that defines the pointers for \
all parameters.

    str_subs : string

        cpp code, piece of header (.h) that defines the values for \
all parameters (table of pointers).
    """
    return str_subs(phs), str_subsvals(phs)


def str_subs(phs):
    """
    return the cpp piece of header that defines the as a string
    """
    string = ""
    for i, symb in enumerate(phs.simu.exprs.subs):
        string += "\nconst double * " + str(symb) + "= & subs[" + str(i) + "];"
    return string


def str_subsvals(phs):
    """
    return the cpp piece of header that defines the as a string
    """
    string = ""
    for i, symb in enumerate(phs.simu.exprs.subs):
        string += "\nconst double * " + str(symb) + "= & subs[" + str(i) + "];"
    return string


def str_get_int(cpp, name):
    strget = "const unsigned int " + cpp.class_ref + "get_" + name \
        + "() const {\n    return " + name + ";\n}\n"
    return strget


def str_get_vec(cpp, name, dim):
    strget = ""
    strget += "\nvector<double> "
    strget += cpp.class_ref
    strget += "get_" + name + "() const { \n"
    strget += "    vector<double> v = vector<double>(get_" + dim + "());\n"
    strget += "    for (int i=0; i<get_" + dim + "(); i++) {\n"
    strget += "        v[i] = " + name + "[i];\n"
    strget += "    }\n"
    strget += "    return v;\n"
    strget += "    }"
    return strget
