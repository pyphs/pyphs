# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 13:47:47 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import os
from pyphs.core.symbs_tools import simplify

standard_config = {'path': os.getcwd()}




###############################################################################

# MATRICES

###############################################################################

def _pieces_matrix(method, name, objlabel):
    from sympy.printing import ccode
    mat = getattr(method, name + '_expr')
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


###############################################################################

# UPDATE

###############################################################################

def _update(name, operation):
    string_h = ""
    string_cpp = ""

    string_h += '\n' + indent('void vnl_update();')
    string_cpp += """\n
void """ + cppobj_name(phs) + '::' + """vnl_update(){
    vnl << vnl - jac_Fnl.inverse()*Fnl;
}"""
    files['h'] += string_h
    files['cpp'] += string_cpp
    pass

###############################################################################

# PROCESS

###############################################################################

def _process(method):
    string_h = ""
    string_cpp = ""
    if method.core.dims.y() > 0:
        str_u_cpp = "vector<double> & u_vec"
        str_u_h = "vector<double> &"
    else:
        str_u_h = str_u_cpp = ""
    if (method.core.dims.y() > 0) and (phs.simu.exprs.np > 0):
        str_coma = ', '
    else:
        str_coma = ""
    if phs.simu.exprs.np > 0:
        str_p_cpp = "vector<double> & p_vec"
        str_p_h = "vector<double> &"
    else:
        str_p_cpp = str_p_h = ""
    string_h += '\n' + indent("void process(" + str_u_h +
                              str_coma + str_p_h + ");")
    string_cpp += """\n
void """ + cppobj_name(phs) + '::' + """process(""" + str_u_cpp + str_coma +\
        str_p_cpp + """){\n"""
    if phs.simu.exprs.ny > 0:
        string_cpp += '\n' + indent('set_u(u_vec);')
    if phs.simu.exprs.np > 0:
        string_cpp += '\n' + indent('set_p(p_vec);')
    parser = {'x': 'x',
              'iDl': 'iDl',
              'barNlxl': 'barNlxl',
              'barNlnl': 'barNlnl',
              'barNly': 'barNly',
              'barNnlnl': 'barNnlnl',
              'barNnll': 'barNnll',
              'barNnlxl': 'barNnlxl',
              'barNnly': 'barNnly',
              'Dl': 'iDl',
              'Nlxl': 'barNlxl',
              'Nlnl': 'barNlnl',
              'Nly': 'barNly',
              'Nnlnl': 'barNnlnl',
              'Nnll': 'barNnll',
              'Nnlxl': 'barNnlxl',
              'Nnly': 'barNnly',
              'c': 'vnl',
              'fnl': 'fnl',
              'jac_fnl': 'jac_fnl',
              'Fnl': 'fnl',
              'jac_Fnl': 'jac_fnl',
              'vnl': 'fnl',
              'vl': 'fl',
              'fl': 'fl',
              'fnl': 'fnl',
              'dx': 'dx',
              'dxH': 'dxH',
              'w': 'w',
              'z': 'z',
              'y': 'y'}
    names = ('x', 'iDl', 'barNlxl', 'barNlnl', 'barNly',
             'barNnlxl', 'barNnlnl', 'barNnly',
             'Dl', 'Nlxl', 'Nlnl', 'Nly',
             'Nnlxl', 'Nnlnl', 'Nnly',
             'c', 'Fnl')
    for name in names:
        shape = sympy.Matrix(getattr(phs.simu.exprs,
                                     parser[name] + '_expr')).shape
        if not any(dim == 0 for dim in shape):
            string_cpp += '\n' + indent(name + '_update();')

    if phs.simu.exprs.nnl > 0:
        string_cpp += """
    unsigned int n = 0;
    while (n<""" + str(phs.simu.config['maxit']) + \
            """ & Fnl.transpose()*Fnl > """ + str(phs.simu.config['numtol']) + \
        "){"
        names = ('jac_fnl', 'jac_Fnl', 'vnl', 'fnl', 'Fnl')
        for name in names:
            shape = sympy.Matrix(getattr(phs.simu.exprs,
                                         parser[name] + '_expr')).shape
            if not any(dim == 0 for dim in shape):
                string_cpp += '\n' + indent(indent(name + '_update();'))
        string_cpp += '\n' + indent(indent('n++;'))
        string_cpp += "\n    }"
    names = ('vl', 'fl',
             'dx', 'dxH', 'w', 'z', 'y')
    for name in names:
        shape = sympy.Matrix(getattr(phs.simu.exprs,
                                     parser[name] + '_expr')).shape
        if not any(dim == 0 for dim in shape):
            string_cpp += '\n' + indent(name + '_update();')
    string_cpp += "\n}"
    files['h'] += string_h
    files['cpp'] += string_cpp


###############################################################################

# SUBS

###############################################################################

# SUBS

###############################################################################

def add_arg():
    pass


def add_func():
    pass


def add_op():
    pass


def add_update():
    pass


class CppCode:

    def __init__(self, method, config=None):

        self.config = standard_config

        if config is None:
            config = {}
        self.config.update(config)

        self.method = method

def write(self, name, extension=None):
    if extension is None:
        filename = self._phs.paths['cpp'] + os.sep + name + ".cpp"
        string = getattr(self, name)
    else:
        filename = self._phs.paths['cpp'] + os.sep + name + "." + extension
        string = getattr(self, name)[extension]
    _file = open(filename, 'w')
    print(string)
    _file.write(string)
    _file.close()

def generate(self, target='main'):
    self.gen_phobj()
    self.gen_data()
    if target == 'main':
        self.gen_main()




def str_vecargs(phs):
    """
    arrays of pointers for x, xnl, dxH, y, etc...
    """
    string = "\n\n// Definition of vectors of pointers"
    for lnl in ['l', 'nl']:
        if getattr(phs.simu.exprs, 'n' + lnl) > 0:
            string += '\nMatrix<double, n' + lnl + ', 1> v' + lnl + ';'
            if getattr(phs.simu.exprs, 'nx' + lnl) > 0:
                string += '\ndouble * ptr_dx' + lnl + ' = & v' + lnl + '[0];'
            if getattr(phs.simu.exprs, 'nw' + lnl) > 0:
                string += '\ndouble * ptr_w' + lnl +\
                    ' = & v' + lnl + '[nx' + lnl + '];'
    string += '\n'
    parser_arg2dim = {'u': 'y', 'p':'p'}
    for name in ['u', 'p']:
        if getattr(phs.simu.exprs, 'n' + parser_arg2dim[name]) > 0:
            string += '\nMatrix<double, n' + parser_arg2dim[name] + \
                ', 1> ' + name + ';'
            string += '\ndouble * ptr_' + name + ' = & ' + name + '[0];'
    return string


def str_args(phs):
    """
    define the pointers associated with symbols in phs.simu.exprs.args
    """
    string = "\n\n// Arguments"
    names = ('xl', 'xnl', 'dxl', 'dxnl', 'wl', 'wnl', 'u', 'p')
    for name in names:
        expr = phs.simu.exprs.get(name)[0]
        if len(expr) > 0:
            string += "\ndouble "
            for i, symb in enumerate(expr):
                string += '*' + str(symb) +\
                    " = & ptr_" + name + '[' + str(i) + '], '
            string = string[:-2] + ';'
    return string


def str_args_full(phs):
    string = "\n\n// Definition of arguments and vectors of pointers"
    string += str_dims(phs)
    string += str_vecargs(phs)
    string += str_args(phs)
    return string


from tools import include_Eigen, name2dim, str_matblk, \
    str_dims, cppobj_name, indent, matrix_type
from preamble import str_preamble
import sympy
from pyphs.symbolics.tools import simplify


def phobj(phs):
    files = {'cpp': str_preamble(phs),
             'h': str_preamble(phs)}
    files['h'] += "\n#ifndef " + cppobj_name(phs) + "_H"
    files['h'] += "\n#define " + cppobj_name(phs) + "_H"
    _append_includes(files)
    _append_namespaces(files)
    files['h'] += "\n\nclass " + cppobj_name(phs) + " {"
    files['h'] += "\n\npublic:"
    _append_dims_accessors(phs, files)
    _append_blocks_accessors(phs, files)
    _append_blocks_mutators(phs, files)
    _append_process(phs, files)
    _append_constructor(phs, files)
    if phs.simu.exprs.nx > 0:
        _append_constructor_init(phs, files)
    _append_destructuor(phs, files)
    files['h'] += "\n\nprivate:"
    _append_dims(phs, files)
    _append_runtime_vectors(phs, files)
    _append_block(phs, files)
    _append_concat_updates(phs, files)
    _append_funcs(phs, files)
    _append_update_process(phs, files)
    _append_args(phs, files)
    _append_subs(phs, files)
    _append_matrices(phs, files)
    files['h'] += "\n};\n\n#endif /* " + cppobj_name(phs) + "_H */\n"
    return files


# -----------------------------------------------------------------------------


def _append_concat_updates(phs, files):
    title = "\n\n// Concatenation updates"
    files['h'] += indent(title)
    files['cpp'] += title
    for name in ('dx', 'w', 'z', 'dxH'):
        dim = getattr(phs.simu.exprs, name2dim(name))
        if dim > 0:
            files['h'] += "\n" + indent("void " + name + '_update();')
            mats = ""
            for lnl in ('l', 'nl'):
                dimlnl = getattr(phs.simu.exprs, name2dim(name+lnl))
                if dimlnl > 0:
                    mats += name + lnl + ','
            files['cpp'] += """\n
void """ + cppobj_name(phs) + "::" + name + """_update(){
    """ + name + """ << """ + mats[:-1] + """;
}"""

# -----------------------------------------------------------------------------


def _append_runtime_vectors(phs, files):
    title = "\n\n// Runtime vectors"
    files['h'] += indent(title)
    names = ('x', 'dx', 'dxH',
             'w', 'z',
             'u', 'y',
             'p',
             'vl', 'vnl',
             'fl', 'fnl')

    for name in names:
        dim = getattr(phs.simu.exprs, name2dim(name))
        if dim > 0:
            files['h'] += indent('\n' + matrix_type(dim, 1) + ' ' +
                                 name + ';')


# -----------------------------------------------------------------------------


def _pieces_block(phs, name):

    def _block_to_mat(block):
        parser = {'xl': ('xl', 'x', 'x'),
                  'xnl': ('xnl', 'x', 'x'),
                  'dxl': ('dxl', 'vl', 'vl'),
                  'dxnl': ('dxnl', 'vnl', 'vnl'),
                  'wl': ('wl', 'vl', 'vl'),
                  'wnl': ('wnl', 'vnl', 'vnl'),
                  'dxHl': ('dxl', 'vl', 'fl'),
                  'dxHnl': ('dxnl', 'vnl', 'fnl'),
                  'zl': ('wl', 'vl', 'fl'),
                  'znl': ('wnl', 'vnl', 'fnl')}
        return parser[block]

    declaration = ""
    initialization = ""
    dim = getattr(phs.simu.exprs, name2dim(name))
    if dim > 0:
        declaration = "\nMap<" + matrix_type(dim, 1) + "> " +\
            name + ";"
        labels_arg, labels_vec, labels_container = _block_to_mat(name)
        ind = getattr(phs.simu.exprs,
                      labels_vec+'_args').index(getattr(phs.simu.exprs,
                                                        labels_arg+'_args')[0])
        initialization = '\n' + name + "( & " + labels_container + ".block<" +\
            str(dim) + ', 1>(' + str(ind) + ', 0)(0)),'
    return declaration, initialization


def _pieces_blocks(phs):
    declarations = ""
    initializations = ""
    names = ('xl', 'xnl',
             'dxl', 'dxnl',
             'wl', 'wnl',
             'dxHl', 'dxHnl',
             'zl', 'znl')
    for name in names:
        declaration, initialization = _pieces_block(phs, name)
        declarations += declaration
        initializations += initialization
    return declarations, initializations[:-1]


# -----------------------------------------------------------------------------


def _append_block(phs, files):
    title = "\n\n// Arguments blocks"
    declarations, _ = _pieces_blocks(phs)
    files['h'] += indent(title)
    files['h'] += indent(declarations)


# -----------------------------------------------------------------------------



def _append_vecs_args(phs, files):
    files['h'] += "\n\n// System vectors"
    names = ('x', 'dx', 'dxH', 'w', 'z')
    for name in names:
        dim = getattr(phs.simu.exprs, name2dim(name))
        if dim > 0:
            files['h'] += "\n\n" + matrix_type(dim, 1) + " " +\
                name + ";"
            n = 0
            for lnl in ('l', 'nl'):
                namelnl = name + lnl
                dimlnl = getattr(phs.simu.exprs, name2dim(namelnl))
                if dimlnl > 0:
                    string_h, string_cpp = str_matblk(name, name + lnl,
                                                      (dimlnl, 1), (n, 0))
                    files['h'] += string_h
                    files['cpp'] += string_cpp
                n += dimlnl

    names = ('u', 'y', 'p')
    for name in names:
        dim = getattr(phs.simu.exprs, name2dim(name))
        if dim > 0:
            files['h'] += "\n\nMatrix" + matrix_type(dim, 1) + " " + \
                name + ";"


# -----------------------------------------------------------------------------


