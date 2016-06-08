# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 02:08:01 2016

@author: Falaize
"""

def phs2mainfile(phs):
    if phs.presolve:
        from .phs2cpp_templates.template_main import main_presolve
        return main_presolve(phs)
    else:
        from .phs2cpp_templates.template_main import main_full
        return main_full(phs)

def phs2cppfile(phs):
    if phs.presolve:
        from .phs2cpp_templates.template_cpp import cfile_presolve
        return cfile_presolve(phs)
    else:
        from .phs2cpp_templates.template_cpp import cfile_full
        return cfile_full(phs)

def phs2headerfile(phs):
    if phs.presolve:
        from .phs2cpp_templates.template_header import hfile_presolve
        return hfile_presolve(phs)
    else:
        from .phs2cpp_templates.template_header import hfile_full
        return hfile_full(phs)


def Expr2Cpp(expr, dict_args, phs_label, label_func, Out_variables, out="c"):

    from sympy import Matrix
    from sympy.printing import ccode

    arg_labels = dict_args.keys()
    na = arg_labels.__len__()
    
    expr_symbols = Matrix(expr).free_symbols if expr.__len__()>0 else []    
    nexpr = expr.__len__()
    
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
#        widgets = ['\nWrite '+ label_func, pb.Percentage(), ' ', pb.ETA()]
#        pbar = pb.ProgressBar(widgets=widgets, maxval=nexpr).start()
        for n in range(nexpr):
            str_out1 += "    dummy_float"+str(n)+" = "+ccode(expr[n]) +";\n"
            str_out2 += "    "+label_out[n]+" = dummy_float"+str(n)+";\n"
#           pbar.update(n+1)
        str_c = "\n"+"void "+phs_label+"::"+str_header + " {\n"+ str_init + "\n" + str_out1+str_out2 + "\n}\n"
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

