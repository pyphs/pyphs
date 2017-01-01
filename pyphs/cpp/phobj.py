# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 13:55:00 2016

@author: Falaize
"""

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


def _append_includes(files):
    files['cpp'] += '\n#include "phobj.h"'
    include_vector = """\n
#include "iostream"
#include "vector"
#include "math.h"

# include "data.h"\n
"""
    files['h'] += include_vector + include_Eigen()


# -----------------------------------------------------------------------------


def _append_namespaces(files):
    files['h'] += '\n'
    files['h'] += '\nusing namespace std;'
    files['h'] += '\nusing namespace Eigen;'


# -----------------------------------------------------------------------------


def _append_dims(phs, files):
    files['h'] += indent(str_dims(phs))


# -----------------------------------------------------------------------------


def _append_dims_accessors(phs, files):
    title = "\n\n// Acessors to system dimensions"
    files['h'] += indent(title)
    files['cpp'] += title
    dims = str_dims(phs).split('\n')
    while dims[0].find('const') < 0:
        dims.pop(0)
    for dim in dims:
        name = dim.split(' = ')[0].split(' ')[-1]
        files['cpp'] += """\nconst unsigned int """ + cppobj_name(phs) +\
            "::get_" + name + """() const { return """ + name + "; }"""
        files['h'] += indent("\nconst unsigned int get_" + name + "() const;")


# -----------------------------------------------------------------------------


def _append_blocks_accessors(phs, files):
    title = "\n\n// Acessors to system variables"
    files['h'] += indent(title)
    files['cpp'] += title
    names = ('x', 'dx', 'dxH', 'w', 'z', 'y')
    for name in names:
        dim = getattr(phs.simu.exprs, name2dim(name))
        if dim > 0:
            files['h'] += indent('\nvector<double> get_' +
                                 name + '() const;')
            files['cpp'] += """
\nvector<double> """ + cppobj_name(phs) + '::get_' + name + """() const {
    vector<double> v = vector<double>(""" + str(dim) + """);
    for (int i=0; i<""" + str(dim) + """; i++) {
        v[i] = """ + name + """[i];
    }
    return v;
}"""


def _append_blocks_mutators(phs, files):
    title = "\n\n// Mutators for system variables"
    files['h'] += indent(title)
    files['cpp'] += title
    names = ('x', 'u', 'p')
    for name in names:
        dim = getattr(phs.simu.exprs, name2dim(name))
        if dim > 0:
            files['h'] += indent('\nvoid set_' + name + '(vector<double> &);')
            files['cpp'] += """\n
void """ + cppobj_name(phs) + '::set_' + name + """(vector<double> & v) {
    for (int i=0; i<""" + str(dim) + """; i++) {
        """ + name + """[i] = v[i];
    }
}"""


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

def _str_init_matrices(phs):
    _, _, _, str_init_datas, str_init_cpps = _pieces_matrices(phs)
    string = "\n\n// Matrices constants"
    string += str_init_datas
    string += "\n\n// Matrices init"
    string += str_init_cpps
    return indent(string)


def _append_constructor(phs, files):
    if phs.simu.exprs.nnl > 0:
        init = """for(int i=0; i<""" + str(phs.simu.exprs.nnl) + """; i++){
        vnl[i] = 0;
    }"""
    else:
        init = ""
    string = """\n
// Default Constructor:
""" + cppobj_name(phs) + """();"""
    files['h'] += indent(string)
    _, init_blocks = _pieces_blocks(phs)
    string = """\n
// Default Constructor:
""" + cppobj_name(phs) + """::""" + cppobj_name(phs) + """() : """ + \
            init_blocks + """\n{

    """ + init + _str_init_matrices(phs) + """
};"""
    files['cpp'] += string

# -----------------------------------------------------------------------------


def _append_constructor_init(phs, files):
    if phs.simu.exprs.nnl > 0:
        init = """for(int i=0; i<""" + str(phs.simu.exprs.nnl) + """; i++){
        vnl[i] = 0;
    }"""
    else:
        init = ""
    string = """\n
// Constructor with state initalization:
""" + cppobj_name(phs) + \
            """(vector<double> &);"""
    files['h'] += indent(string)
    _, init_blocks = _pieces_blocks(phs)
    string = """\n
// Constructor with state initalization:
""" + cppobj_name(phs) + """::""" + cppobj_name(phs) + \
            """(vector<double> & x0) : """ + init_blocks + """\n{

    if (x.size() == x0.size()) {
        set_x(x0);
    }
    else {
        cerr << "Size of x0 does not match size of x" << endl;
        exit(1);
    }

    """ + init + _str_init_matrices(phs) + """
};"""
    files['cpp'] += string


# -----------------------------------------------------------------------------


def _append_destructuor(phs, files):
        string = """\n
// Default Destructor:
~""" + cppobj_name(phs) + """();"""
        files['h'] += indent(string)

        string = """\n
// Default Destructor:
""" + cppobj_name(phs) + """::~""" + cppobj_name(phs) + """() {};"""
        files['cpp'] += string

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


def _append_args(phs, files):
    title = "\n\n// Functions arguments"
    files['h'] += indent(title)
    names = ('x', 'vl', 'vnl', 'u', 'p')
    for name in names:
        args = getattr(phs.simu.exprs, name + '_args')
        for i, arg in enumerate(args):
            files['h'] += indent('\ndouble * ' + str(arg) + ' = & ' +
                                 str(name) + '(' + str(i) + ', 0);')


def _append_subs(phs, files):
    title = "\n\n// Functions parameters"
    files['h'] += indent(title)
    files['h'] += '\n' + indent('const unsigned int subs_ref = 0;') + '\n'
    for i, sub in enumerate(phs.simu.exprs.subs):
        files['h'] += indent('\nconst double * ' + str(sub) +
                             ' = & subs[subs_ref][' + str(i) + '];')

# -----------------------------------------------------------------------------


def _append_funcs(phs, files):
    from sympy.printing import ccode
    title = "\n\n// Functions updates"
    files['h'] += indent(title)
    files['cpp'] += title
    names = ('fl', 'fnl')
    for name in names:
        dim = getattr(phs.simu.exprs, name2dim(name))
        if dim > 0:
            expr = getattr(phs.simu.exprs, name+'_expr')
            if isinstance(expr, list):
                expr = sympy.Matrix(expr)
            expr = simplify(expr)

            files['h'] += "\n" + indent("void " + name + '_update();')
            files['cpp'] += "\nvoid " + cppobj_name(phs) + '::' + \
                name + '_update(){'

            if isinstance(expr, sympy.Expr):
                code = ccode(expr)
                files['cpp'] += "\n" + name + ' = ' + code + ';'
            elif isinstance(expr, sympy.Matrix):
                for m in range(expr.shape[0]):
                    for n in range(expr.shape[1]):
                        code = ccode(expr[m, n],
                                     dereference=phs.simu.exprs.args +
                                     phs.simu.exprs.subs)
                        files['cpp'] += "\n" + name + \
                            '(' + str(m) + ', ' + str(n) + ') = ' + code + ';'
            files['cpp'] += '\n};'

# -----------------------------------------------------------------------------


def _pieces_matrix(phs, name):
    from sympy.printing import ccode
    mat = getattr(phs.simu.exprs, name + '_expr')
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
        str_update_cpp += '\n' + 'void ' + cppobj_name(phs) + '::' +\
            name + '_update(){'
        for n in range(mat.shape[1]):
            for m in range(mat.shape[0]):
                expr = mat[m, n]
                symbs = expr.free_symbols
                if any(symb in phs.simu.exprs.args for symb in symbs):
                    str_init_data += "0, "
                    str_update_cpp += '\n' + name + str((m, n)) + ' = '
                    str_update_cpp += ccode(expr,
                                            dereference=phs.simu.exprs.args +
                                            phs.simu.exprs.subs)
                    str_update_cpp += ';'
                else:
                    str_init_data += ccode(expr,
                                           dereference=phs.simu.exprs.args +
                                           phs.simu.exprs.subs) + ', '
        str_update_cpp += '\n};'
        str_init_data = str_init_data[:-2] + '};'
    return str_definition, str_update_cpp, str_update_h, str_init_data,\
        str_init_cpp


def _pieces_matrices(phs):
    names = ('iDl', 'barNlxl', 'barNlnl', 'barNly',
             'barNnlnl', 'barNnll', 'barNnlxl', 'barNnly',
             'jac_fnl', 'Inl', 'Nyl', 'Nynl', 'Nyy')
    str_definitions, str_update_cpps, str_update_hs, str_init_datas,\
        str_init_cpps = "", "", "", "", ""
    for name in names:
        str_definition, str_update_cpp, str_update_h, str_init_data,\
            str_init_cpp = _pieces_matrix(phs, name)
        str_definitions += str_definition
        str_update_cpps += str_update_cpp
        str_update_hs += str_update_h
        str_init_datas += str_init_data
        str_init_cpps += str_init_cpp
    return str_definitions, str_update_cpps, str_update_hs, str_init_datas,\
        str_init_cpps


def _append_matrices(phs, files):
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

# -----------------------------------------------------------------------------


def _append_update_x(phs, files):
    string_h = ""
    string_cpp = ""
    if phs.simu.exprs.nx > 0:
        string_h += '\n' + indent('void x_update();')
        string_cpp += """\n
void """ + cppobj_name(phs) + '::' + """x_update(){
    x << x + dx;
}"""
    files['h'] += string_h
    files['cpp'] += string_cpp


def _append_update_Dl(phs, files):
    string_h = ""
    string_cpp = ""
    if phs.simu.exprs.nl > 0:
        string_h += '\n' + indent('void Dl_update();')
        string_cpp += """\n
void """ + cppobj_name(phs) + '::' + """Dl_update(){
    Dl << iDl.inverse();
}"""
    files['h'] += string_h
    files['cpp'] += string_cpp


def _append_update_Nlxl(phs, files):
    string_h = ""
    string_cpp = ""
    if phs.simu.exprs.nxl > 0:
        string_h += '\n' + indent('void Nlxl_update();')
        string_cpp += """\n
void """ + cppobj_name(phs) + '::' + """Nlxl_update(){
    Nlxl << Dl*barNlxl;
}"""
    files['h'] += string_h
    files['cpp'] += string_cpp


def _append_update_Nlnl(phs, files):
    string_h = ""
    string_cpp = ""
    if (phs.simu.exprs.nl > 0) and (phs.simu.exprs.nnl > 0):
        string_h += '\n' + indent('void Nlnl_update();')
        string_cpp += """\n
void """ + cppobj_name(phs) + '::' + """Nlnl_update(){
    Nlnl << Dl*barNlnl;
}"""
    files['h'] += string_h
    files['cpp'] += string_cpp


def _append_update_Nly(phs, files):
    string_h = ""
    string_cpp = ""
    if (phs.simu.exprs.nl > 0) and (phs.simu.exprs.ny > 0):
        string_h += '\n' + indent('void Nly_update();')
        string_cpp += """\n
void """ + cppobj_name(phs) + '::' + """Nly_update(){
    Nly << Dl*barNly;
}"""
    files['h'] += string_h
    files['cpp'] += string_cpp


def _append_update_Nnlxl(phs, files):
    string_h = ""
    string_cpp = ""
    if (phs.simu.exprs.nnl > 0) and (phs.simu.exprs.nxl > 0):
        vlin = " + barNnll*Nlxl"
        string_h += '\n' + indent('void Nnlxl_update();')
        string_cpp += """\n
void """ + cppobj_name(phs) + '::' + """Nnlxl_update(){
    Nnlxl << barNnlxl""" + vlin + """;
}"""
    files['h'] += string_h
    files['cpp'] += string_cpp


def _append_update_Nnlnl(phs, files):
    string_h = ""
    string_cpp = ""
    if phs.simu.exprs.nnl > 0:
        if phs.simu.exprs.nl > 0:
            vlin = " + barNnll*Nlnl"
        else:
            vlin = ""
        string_h += '\n' + indent('void Nnlnl_update();')
        string_cpp += """\n
void """ + cppobj_name(phs) + '::' + """Nnlnl_update(){
    Nnlnl << barNnlnl""" + vlin + """;
}"""
    files['h'] += string_h
    files['cpp'] += string_cpp


def _append_update_Nnly(phs, files):
    string_h = ""
    string_cpp = ""
    if phs.simu.exprs.nnl > 0:
        if phs.simu.exprs.nl > 0:
            vlin = " + barNnll*Nly"
        else:
            vlin = ""
        string_h += '\n' + indent('void Nnly_update();')
        string_cpp += """\n
void """ + cppobj_name(phs) + '::' + """Nnly_update(){
    Nnly << barNnly""" + vlin + """;
}"""
    files['h'] += string_h
    files['cpp'] += string_cpp


def _append_update_c(phs, files):
    string_h = ""
    string_cpp = ""
    if phs.simu.exprs.nnl > 0:
        if phs.simu.exprs.nxl > 0:
            vlin = "Nnlxl*x"
        else:
            vlin = ""
        if phs.simu.exprs.ny > 0:
            vu = ""
            if (phs.simu.exprs.nxl > 0) and (phs.simu.exprs.nl > 0):
                vu += ' + '
            vu += "Nnly*u"
        else:
            vu = ""
        string_h += '\n' + indent('void c_update();')
        string_cpp += """\n
void """ + cppobj_name(phs) + '::' + """c_update(){
    c << """ + vlin + vu + """;
}"""
    files['h'] += string_h
    files['cpp'] += string_cpp


def _append_update_Fnl(phs, files):
    string_h = ""
    string_cpp = ""
    if phs.simu.exprs.nnl > 0:
        string_h += '\n' + indent('void Fnl_update();')
        string_cpp += """\n
void """ + cppobj_name(phs) + '::' + """Fnl_update(){
    Fnl << Inl * vnl - Nnlnl*fnl - c;
}"""
    files['h'] += string_h
    files['cpp'] += string_cpp


def _append_update_jac_Fnl(phs, files):
    string_h = ""
    string_cpp = ""
    if phs.simu.exprs.nnl > 0:
        string_h += '\n' + indent('void jac_Fnl_update();')
        string_cpp += """\n
void """ + cppobj_name(phs) + '::' + """jac_Fnl_update(){
    jac_Fnl << Inl - Nnlnl*jac_fnl;
}"""
    files['h'] += string_h
    files['cpp'] += string_cpp


def _append_update_vnl(phs, files):
    string_h = ""
    string_cpp = ""
    if phs.simu.exprs.nnl > 0:
        string_h += '\n' + indent('void vnl_update();')
        string_cpp += """\n
void """ + cppobj_name(phs) + '::' + """vnl_update(){
    vnl << vnl - jac_Fnl.inverse()*Fnl;
}"""
    files['h'] += string_h
    files['cpp'] += string_cpp


def _append_update_vl(phs, files):
    string_h = ""
    string_cpp = ""
    if phs.simu.exprs.nl > 0:
        vxl = ""
        if phs.simu.exprs.nxl > 0:
            vxl += 'Nlxl*xl'
            if (phs.simu.exprs.nxnl > 0) or (phs.simu.exprs.ny > 0):
                vxl += ' + '
        vfnl = ""
        if phs.simu.exprs.nnl > 0:
            vfnl += 'Nlnl*fnl'
            if phs.simu.exprs.ny > 0:
                vfnl += ' + '
        vy = ""
        if phs.simu.exprs.ny > 0:
            vy += 'Nly*u'
            string_h += '\n' + indent('void vl_update();')
            string_cpp += """\n
void """ + cppobj_name(phs) + '::' + """vl_update(){
    vl << """ + vxl + vfnl + vy + """;
}"""
    files['h'] += string_h
    files['cpp'] += string_cpp


def _append_update_y(phs, files):
    string_h = ""
    string_cpp = ""
    if phs.simu.exprs.ny > 0:
        vxl = ""
        if phs.simu.exprs.nxl > 0:
            vxl += 'Nyl*fl'
            if (phs.simu.exprs.nxnl > 0) or (phs.simu.exprs.ny > 0):
                vxl += ' + '
        vfnl = ""
        if phs.simu.exprs.nnl > 0:
            vfnl += 'Nynl*fnl'
            if phs.simu.exprs.ny > 0:
                vfnl += ' + '
        vy = ""
        if phs.simu.exprs.ny > 0:
            vy += 'Nyy*u'
            string_h += '\n' + indent('void y_update();')
            string_cpp += """\n
void """ + cppobj_name(phs) + '::' + """y_update(){
    y << """ + vxl + vfnl + vy + """;
}"""
    files['h'] += string_h
    files['cpp'] += string_cpp


def _append_process(phs, files):
    string_h = ""
    string_cpp = ""
    if phs.simu.exprs.ny > 0:
        str_u_cpp = "vector<double> & u_vec"
        str_u_h = "vector<double> &"
    else:
        str_u_h = str_u_cpp = ""
    if (phs.simu.exprs.ny > 0) and (phs.simu.exprs.np > 0):
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


def _append_update_process(phs, files):
    _append_update_x(phs, files)
    _append_update_Dl(phs, files)
    _append_update_Nlxl(phs, files)
    _append_update_Nlnl(phs, files)
    _append_update_Nly(phs, files)
    _append_update_Nnlxl(phs, files)
    _append_update_Nnlnl(phs, files)
    _append_update_Nnly(phs, files)
    _append_update_c(phs, files)
    _append_update_Fnl(phs, files)
    _append_update_jac_Fnl(phs, files)
    _append_update_vnl(phs, files)
    _append_update_vl(phs, files)
    _append_update_y(phs, files)
