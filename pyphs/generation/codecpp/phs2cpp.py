# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 13:47:47 2016

@author: Falaize
"""


class CppCode:

    def __init__(self, phs):
        self._phs = phs

    def _gen(self, name, extension=None):
        import os
        if extension is None:
            filename = self._phs.paths['cpp'] + os.sep + name + ".cpp"
            string = getattr(self, name)
        else:
            filename = self._phs.paths['cpp'] + os.sep + name + "." + extension
            string = getattr(self, name)[extension]
        _file = open(filename, 'w')
        print string
        _file.write(string)
        _file.close()

    def generate(self, target='main'):
        self.gen_phobj()
        self.gen_data()
        if target == 'main':
            self.gen_main()

# -----------------------------------------------------------------------------

    def _set_main(self):
        from main import main
        self.main = main(self._phs)

    def gen_main(self):
        if not hasattr(self, 'main'):
            self._set_main()
        self._gen('main')

# -----------------------------------------------------------------------------

    def _set_phobj(self):
        from phobj import phobj
        self.phobj = phobj(self._phs)

    def gen_phobj(self):
        if not hasattr(self._phs.simu, 'exprs'):
            self._phs.simu.init_expressions()
        if not hasattr(self, 'phobj'):
            self._set_phobj()
        self._gen('phobj', extension='cpp')
        self._gen('phobj', extension='h')

# -----------------------------------------------------------------------------

    def _set_data(self):
        from subs import data
        self.data = data(self._phs)

    def gen_data(self):
        if not hasattr(self, 'data'):
            self._set_data()
        self._gen('data', extension='cpp')
        self._gen('data', extension='h')

# -----------------------------------------------------------------------------


    def gen_subs(self):
        self._gen('subs')

    def _set_vecs_args(self):
        string = "\n\n// System vectors"
        parser_arg2dim = {'x': 'x',
                          'dx': 'x',
                          'dxH': 'x',
                          'w': 'w',
                          'z': 'w',
                          'p': 'p',
                          'u': 'y',
                          'y': 'y'}
        names = ('x', 'dx', 'dxH', 'w', 'z')
        for name in names:
            dimlab = 'n' + parser_arg2dim[name]
            dim = getattr(self._phs.simu.exprs, dimlab)
            if dim > 0:
                string += "\nMatrix<double, " + dimlab + ", 1> " +\
                    name + ";"
                n = 0
                for lnl in ('l', 'nl'):
                    dimlablnl = 'n' + parser_arg2dim[name] + lnl
                    dimlnl = getattr(self._phs.simu.exprs, dimlablnl)
                    if dimlnl > 0:
                        string += str_matblk(name, name + lnl,
                                             (dimlablnl, 1), (n, 0))
                    n += dimlnl

        names = ('u', 'y', 'p')
        for name in names:
            dimlab = 'n' + parser_arg2dim[name]
            dim = getattr(self._phs.simu.exprs, dimlab)
            if dim > 0:
                string += "\nMatrix<double, " + dimlab + ", 1> " +\
                    name + ";"
        self.phobj['h'] += string


def str_matblk(mat_name, blck_name, blck_dims, blck_pos):
    string = "\ndouble * ptr_" + blck_name + " = "
    str_dims = "<" + str(blck_dims[0]) + ', ' + str(blck_dims[1]) + ">"
    str_pos = "(" + str(blck_pos[0]) + ', ' + str(blck_pos[1]) + ")"
    string += " & " + mat_name + ".block" + str_dims + str_pos + "(0);"
    string += "\nMap<Matrix<double, " + str_dims[1:-1] + ">> "
    string += blck_name + '(ptr_' + blck_name + ', ' + str_dims[1:-1] + ');'
    return string


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
    