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


def expr2Cpp(phs, name):
    from sympy import Matrix
    from sympy.printing import ccode

    dim = getattr(phs.simu.exprs, name2dim(name))
    expr = getattr(phs.simu.exprs, name + '_expr')
    args = getattr(phs.simu.exprs, name + '_args')
    subs = getattr(phs.simu.exprs, name + '_subs')
        
    str_args = ""    
    for n in range(na):
        str_args += "vector<double>& " + arg_labels[n]
        if n<na-1:
            str_args += ", "    
    str_header =  label_func +"()"

    str_init = ""
    for n in range(na):
        list_args = [e for e in dict_args[arg_labels[n]] ]
        str_args = ""
        naa = list_args.__len__()
        if naa>0:
            for m in range(naa):
                test = set([list_args[m]]).issubset(expr_symbols) if expr.__len__()>0 else False
                if test:
                    if str_args.__len__() == 0:
                        str_args += '    const double '
                    else:
                        str_args += ', '
                    str_args += str(list_args[m]) + " = "+arg_labels[n]+"["+str(m)+"]"
            if str_args.__len__() > 0:
                str_init += str_args +";\n"
    str_init += '    double ' if nexpr>0 else ''
    for n in range(nexpr):
        end_line = ', ' if n<nexpr-1 else ';'
        str_init += 'dummy_float'+str(n)+' = '+str(0) + end_line        
    

    if type(Out_variables)==str:
        label_out = [Out_variables+'['+str(n)+']' for n in range(nexpr)]
    else :
        label_out = Out_variables

    str_out1 = ""
    str_out2 = ""
    
    if out=="c":
        for n in range(nexpr):
            str_out1 += "    dummy_float" + str(n)+" = "+ccode(expr[n]) +";\n"
            str_out2 += "    "+label_out[n]+" = dummy_float"+str(n)+";\n"
        str_c = "\n"+"void " + phs_label+"::" + str_header + " {\n"+ str_init + "\n" + str_out1 + str_out2 + "\n}\n"
        return str_c
    else: 
        str_h = "    "+"void " +str_header + ";\n"
        return str_h

def Matrix2Cpp(matrixExpr, dict_args, phs_label, label_func, Out_Matrix, out="c"):

    from sympy.printing import ccode
    from sympy import Matrix
    
    arg_labels = dict_args.keys()
    na = arg_labels.__len__()
        
    expr_symbols = Matrix(matrixExpr).free_symbols if matrixExpr.__len__()>0 else []    

    listMatrixExpr = list(matrixExpr)
    nexpr = listMatrixExpr.__len__()
    
    str_args = ""    
    for n in range(na):
        str_args += "vector<double>& " + arg_labels[n]
        if n<na-1:
            str_args += ", "    
    str_header =  label_func +"()"

    str_init = ""
    for n in range(na):
        list_args = [e for e in dict_args[arg_labels[n]] ]
        str_args = ""
        naa = list_args.__len__()
        if naa>0:
            for m in range(naa):
                test = set([list_args[m]]).issubset(expr_symbols) if matrixExpr.__len__()>0 else False
                if test:
                    if str_args.__len__() == 0:
                        str_args += '    const double '
                    else:
                        str_args += ', '
                    str_args += str(list_args[m]) + " = "+arg_labels[n]+"["+str(m)+"]"
            if str_args.__len__() > 0:
                str_init += str_args +";\n"
    
    
    if out=="c":
        
        if matrixExpr.__len__()>0:
            str_out = '    ' + Out_Matrix + ' << '
            for n in range(nexpr):
                str_out += ccode(matrixExpr[n])
                if n!=nexpr-1:
                    str_out += ' , '
    
            str_out += ' ;\n '
        else:
            str_out = '\n'
            
        str_c = "\n"+"void "+phs_label+"::"+str_header + " {\n"+ str_init + "\n" + str_out + "\n}\n"
        return str_c
    else: 
        str_h = "    "+"void " +str_header + ";\n"
        return str_h


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
""


def mat2cpp(phs, name):
    expr, args = phs.simu.exprs.get(name)
    str_shape = str(expr.shape[0]), str(expr.shape[0])
    h_def = "Matrix<double, "+ str_shape[0] + ", " + str_shape[1] + "> " + xl()
