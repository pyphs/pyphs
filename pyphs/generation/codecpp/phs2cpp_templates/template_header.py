# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 02:19:47 2016

@author: Falaize
"""


NbItNR=100
NumTolNr=1e-12
from ..phs2cpp import Expr2Cpp, Matrix2Cpp

def hfile_presolve(phs):

    header_label = ('phobj').upper()+"_H"
    str_test = "#ifndef " + header_label + "\n#define " + header_label +"\n\n"
    
    str_includes =  '#include "iostream"\n#include "vector"\n#include "math.h"\n\n'+\
                    "using namespace std;\n\n"

    str_class = "class " + phs.label.upper() + " {\n"

    str_publics_variables = "public:\n\n"
    str_constructor = "\n    "+"// Default Constructor:\n"+"    "+phs.label.upper()+"();\n"    
    str_initx_constructor = "\n    "+"// Constructor Initializing x:\n"+"    "+phs.label.upper()+"(vector<double>&);\n"    
    str_destructor = "\n    "+"// Default Destructor:\n"+"    "+ "~"+phs.label.upper()+"();\n"    

    str_accesors = "\n    // Accesors to private variables\n"
    str_accesors += "    vector<double> get_y() const;\n"
    str_accesors += "    vector<double> get_u() const;\n"
    str_accesors += "    vector<double> get_x() const;\n"
    str_accesors += "    vector<double> get_dx() const;\n"
    str_accesors += "    vector<double> get_dxH() const;\n"
    str_accesors += "    vector<double> get_w() const;\n"
    str_accesors += "    vector<double> get_z() const;\n"
    str_accesors += "    const unsigned int get_nx() const;\n"
    str_accesors += "    const unsigned int get_nxl() const;\n"
    str_accesors += "    const unsigned int get_nxnl() const;\n"
    str_accesors += "    const unsigned int get_nw() const;\n"
    str_accesors += "    const unsigned int get_nwl() const;\n"
    str_accesors += "    const unsigned int get_nwnl() const;\n"
    str_accesors += "    const unsigned int get_ny() const;\n"
    str_accesors += "    const unsigned int get_np() const;\n"

    str_modificators = "\n    // Mutators of private variables\n"
    str_modificators += "    void set_u(vector<double>);\n"
    str_modificators += "    void set_x(vector<double>);\n"
    
    str_phs_functions = "\n    // Port-Hamiltonian runtime functions\n"
    
    dict_args = {"x":phs.symbs.x, "dx": phs.dx, "w": phs.symbs.w, "u": phs.symbs.u, "p": phs.symbs.p}
    phs_label = phs.label.upper()

    expr = list(phs.Fl)
    label_variable = ["dxl["+str(n)+"]" for n in range(phs.dims.xl)]+ ["wl["+str(n)+"]" for n in range(phs.dims.wl)]
    label_func = "Fl"
    str_phs_functions += Expr2Cpp(expr,dict_args,phs_label, label_func, label_variable, "h")

    if phs.dims.xnl() + phs.dims.wnl() > 0:
        from sympy import Matrix
        expr = list(Matrix(phs.dxnl()+phs.wnl())+Matrix(phs.Fnl))
        label_variable = ["dxnl["+str(n)+"]" for n in range(phs.dims.xnl())]+ ["wnl["+str(n)+"]" for n in range(phs.dims.wnl())]
        label_func = "Fnl"
        str_phs_functions += Expr2Cpp(expr,dict_args,phs_label, label_func, label_variable, "h")
    
        expr = [phs.Fnl_residual]
        label_variable = "residual_NR"
        label_func = "FresidualNR"
        str_phs_functions += Expr2Cpp(expr,dict_args,phs_label, label_func, label_variable, "h").replace('residual_NR[0] ', 'residual_NR ')

    expr = phs.exprs.dxHd
    label_variable = "dxH"
    label_func = "FdxH"
    str_phs_functions += Expr2Cpp(expr,dict_args,phs_label, label_func, label_variable, "h")

    expr = phs.exprs.z
    label_variable = "z"
    label_func = "Fz"
    str_phs_functions += Expr2Cpp(expr,dict_args,phs_label, label_func, label_variable, "h")
            
    expr = phs.exprs.yd
    label_variable = "y"
    label_func = "Fy"
    str_phs_functions += Expr2Cpp(expr,dict_args,phs_label, label_func, label_variable, "h")
    
    str_phs_functions += "    void process(vector<double>&, vector<double>&);\n"
    
    str_privates_variables = "\nprivate:\n\n"

    str_privates_variables += "    // Dimensions of the port-Hamiltonian system\n"
    str_privates_variables += "    "+"const unsigned int nx=" + str(phs.dims.x()) + ";\n"
    str_privates_variables += "    "+"const unsigned int nxl=" + str(phs.dims.xl) + ";\n"
    str_privates_variables += "    "+"const unsigned int nxnl=" + str(phs.dims.xnl()) + ";\n"
    str_privates_variables += "    "+"const unsigned int nw=" + str(phs.dims.w()) + ";\n"
    str_privates_variables += "    "+"const unsigned int nwl=" + str(phs.dims.wl) + ";\n"
    str_privates_variables += "    "+"const unsigned int nwnl=" + str(phs.dims.wnl()) + ";\n"
    str_privates_variables += "    "+"const unsigned int ny=" + str(phs.dims.y) + ";\n"
    str_privates_variables += "    "+"const unsigned int np=" + str(phs.dims.p()) + ";\n\n"
    
    str_privates_variables += "    // Port-Hamiltonian system's vectors\n"
    str_privates_variables += "    vector<double> x = vector<double>(" + str(phs.dims.x()) + ");\n"
    str_privates_variables += "    vector<double> dx = vector<double>(" + str(phs.dims.x()) + ");\n"
    str_privates_variables += "    vector<double> dxH = vector<double>(" + str(phs.dims.x()) + ");\n"
    str_privates_variables += "    vector<double> w = vector<double>(" + str(phs.dims.w()) + ");\n"
    str_privates_variables += "    vector<double> z = vector<double>(" + str(phs.dims.w()) + ");\n"
    str_privates_variables += "    vector<double> u = vector<double>(" + str(phs.dims.y) + ");\n"
    str_privates_variables += "    vector<double> y = vector<double>(" + str(phs.dims.y) + ");\n"
    str_privates_variables += "    vector<double> p = vector<double>(" + str(phs.dims.p()) + ");\n\n"
    
    str_privates_variables += "    // Pointers to the linear part of each vector\n"
    str_privates_variables += "    double * xl = "+"& x[0];\n"
    str_privates_variables += "    double * dxl = "+"& dx[0];\n"
    str_privates_variables += "    double * dxHl = "+"& dxH[0];\n"
    str_privates_variables += "    double * wl = "+"& w[0];\n"
    str_privates_variables += "    double * zl = "+"& z[0];\n\n"

    str_privates_variables += "    // Pointers to the nonlinear part of each vector\n"
    str_privates_variables += "    double * xnl = "+"& x[" + str(phs.dims.xl)+ "];\n"
    str_privates_variables += "    double * dxnl = "+"& dx[" + str(phs.dims.xl)+ "];\n"
    str_privates_variables += "    double * dxHnl = "+"& dxH[" + str(phs.dims.xl)+ "];\n"
    str_privates_variables += "    double * wnl = "+"& w[" + str(phs.dims.wl)+ "];\n"
    str_privates_variables += "    double * znl = "+"& z[" + str(phs.dims.wl)+ "];\n\n"

    str_privates_variables += "    // Variables for NR iterations\n"
    str_privates_variables += "    double NbItNR = " + str(NbItNR) + ";\n"
    str_privates_variables += "    double residual_NR = 0;\n"
    str_privates_variables += "    double it = 0;\n"
    str_privates_variables += "    double eps = "+ str(NumTolNr) + ";\n"

    str_outro = "};\n#endif /* " + header_label + " */"
    str_out = str_test + str_includes + str_class + str_publics_variables  +\
            str_constructor +str_initx_constructor+str_destructor+ str_accesors +\
            str_modificators +str_phs_functions+ str_privates_variables + str_outro
    h_file = open(phs.paths['cpp']+"/"+"phobj.h", 'w')
    h_file.write(str_out)
    h_file.close()
    return str_out

def hfile_full(phs):  

    from pyphs.configs.cpp import eigen_path
    
    header_label = phs.label.upper()+"_H"
    str_test = "#ifndef " + header_label + "\n#define " + header_label +"\n\n"
    
    str_includes =  '#include "iostream"\n#include "vector"\n#include "math.h"\n\n'+\
                    "#include <" + eigen_path + "/Eigen/Dense>\n\nusing namespace Eigen;\nusing namespace std;\n\n"

    str_class = "class " + phs.label.upper() + " {\n"

    str_publics_variables = "public:\n\n"
    str_constructor = "\n    "+"// Default Constructor:\n"+"    "+phs.label.upper()+"();\n"    
    str_initx_constructor = "\n    "+"// Constructor Initializing x:\n"+"    "+phs.label.upper()+"(vector<double>&);\n"    
    str_destructor = "\n    "+"// Default Destructor:\n"+"    "+ "~"+phs.label.upper()+"();\n"    

    str_accesors = "\n    // Accesors to private variables\n"
    str_accesors += "    vector<double> get_y() const;\n"
    str_accesors += "    vector<double> get_u() const;\n"
    str_accesors += "    vector<double> get_x() const;\n"
    str_accesors += "    vector<double> get_dx() const;\n"
    str_accesors += "    vector<double> get_dxH() const;\n"
    str_accesors += "    vector<double> get_w() const;\n"
    str_accesors += "    vector<double> get_z() const;\n"
    str_accesors += "    const unsigned int get_nx() const;\n"
    str_accesors += "    const unsigned int get_nxl() const;\n"
    str_accesors += "    const unsigned int get_nxnl() const;\n"
    str_accesors += "    const unsigned int get_nw() const;\n"
    str_accesors += "    const unsigned int get_nwl() const;\n"
    str_accesors += "    const unsigned int get_nwnl() const;\n"
    str_accesors += "    const unsigned int get_ny() const;\n"
    str_accesors += "    const unsigned int get_np() const;\n"

    str_modificators = "\n    // Mutators of private variables\n"
    str_modificators += "    void set_u(vector<double>);\n"
    str_modificators += "    void set_x(vector<double>);\n"
    
    str_phs_functions = "\n    // Port-Hamiltonian runtime functions\n"
    
    dict_args = {"x":phs.symbs.x, "dx": phs.symbs.dx(), "w": phs.symbs.w, "u": phs.symbs.u, "p": phs.symbs.p}
    phs_label = phs.label.upper()

    expr = list(phs.exprs.eval_varsl)
    label_variable = ["dxl["+str(n)+"]" for n in range(phs.dims.xl)] + \
["wl["+str(n)+"]" for n in range(phs.dims.wl)]
    label_func = "UpDate_l"
    str_phs_functions += Expr2Cpp(expr,dict_args,phs_label, label_func, label_variable, "h")

    expr = phs.exprs.dxHd
    label_variable = "dxH"
    label_func = "UpDate_dxH"
    str_phs_functions += Expr2Cpp(expr,dict_args,phs_label, label_func, label_variable, "h")

    expr = phs.exprs.z
    label_variable = "z"
    label_func = "UpDate_z"
    str_phs_functions += Expr2Cpp(expr,dict_args,phs_label, label_func, label_variable, "h")
            
    expr = phs.exprs.yd
    label_variable = "y"
    label_func = "UpDate_y"
    str_phs_functions += Expr2Cpp(expr,dict_args,phs_label, label_func, label_variable, "h")


    from pyphs.misc.tools import geteval    
    names = ('xl', 'xnl', 'wl', 'wnl', 'y')
    for namei in names:
        for namej in names:
            matrix_name = 'Jxlxl'
            matrix_expr = geteval(phs.struc, matrix_name)
    funcLabel = 'UpDate_' + matrix_name
    str_phs_functions += Matrix2Cpp(matrix_expr, dict_args, phs_label,
                                    funcLabel, matrix_name, "h")

    matrixExpr = phs.exprs.R
    matrixLabel = 'R'
    funcLabel = 'UpDate_R'
    str_phs_functions += Matrix2Cpp(matrixExpr, dict_args, phs_label,
                                    funcLabel, matrixLabel, "h")

    matrixExpr = phs.exprs.Q
    matrixLabel = 'Q'
    funcLabel = 'UpDate_Q'
    str_phs_functions += Matrix2Cpp(matrixExpr, dict_args, phs_label,
                                    funcLabel, matrixLabel, "h")

    str_phs_functions += "    void UpDate_Matrices();\n"
    str_phs_functions += "    void process(vector<double>&, vector<double>&);\n"
    str_phs_functions += "    Matrix<double,"+str(phs.dims.xl)+","+str(1)+"> xl();\n"
    str_phs_functions += "    Matrix<double,"+str(phs.dims.xl)+","+str(1)+"> dxl();\n"
    str_phs_functions += "    Matrix<double,"+str(phs.dims.xl)+","+str(1)+"> dxHl();\n"
    str_phs_functions += "    Matrix<double,"+str(phs.dims.wl)+","+str(1)+"> wl();\n"
    str_phs_functions += "    Matrix<double,"+str(phs.dims.wl)+","+str(1)+"> zl();\n"
    str_phs_functions += "    Matrix<double,"+str(phs.dims.xnl()+ phs.dims.wnl())+","+str(phs.dims.xnl() + phs.dims.wnl())+"> iJacobianImplicitFunc();\n"

    if phs.dims.xnl() + phs.dims.wnl():
        str_phs_functions += "    void UpDate_residualNR();\n"
        str_phs_functions += "    void UpDate_nl();\n"
        str_phs_functions += "    void UpDate_Fnl();\n"
        str_phs_functions += "    void UpDate_ImpFunc();\n"
        str_phs_functions += "    void UpDate_JacobianFnl();\n"
        if phs.dims.xnl()>0:
            str_phs_functions += "    Matrix<double,"+str(phs.dims.xnl())+","+str(1)+"> xnl();\n"
            str_phs_functions += "    Matrix<double,"+str(phs.dims.xnl())+","+str(1)+"> dxnl();\n"
            str_phs_functions += "    Matrix<double,"+str(phs.dims.xnl())+","+str(1)+"> dxHnl();\n"
        if phs.dims.wnl()>0:
            str_phs_functions += "    Matrix<double,"+str(phs.dims.wnl())+","+str(1)+"> wnl();\n"
            str_phs_functions += "    Matrix<double,"+str(phs.dims.wnl())+","+str(1)+"> znl();\n"

    str_privates_variables = "\nprivate:\n\n"

    str_privates_variables += "    // Dimensions of the port-Hamiltonian system\n"
    str_privates_variables += "    "+"const unsigned int nx=" + str(phs.dims.x()) + ";\n"
    str_privates_variables += "    "+"const unsigned int nxl=" + str(phs.dims.xl) + ";\n"
    str_privates_variables += "    "+"const unsigned int nxnl=" + str(phs.dims.xnl()) + ";\n"
    str_privates_variables += "    "+"const unsigned int nw=" + str(phs.dims.w()) + ";\n"
    str_privates_variables += "    "+"const unsigned int nwl=" + str(phs.dims.wl) + ";\n"
    str_privates_variables += "    "+"const unsigned int nwnl=" + str(phs.dims.wnl()) + ";\n"
    str_privates_variables += "    "+"const unsigned int ny=" + str(phs.dims.y) + ";\n"
    str_privates_variables += "    "+"const unsigned int np=" + str(phs.dims.p()) + ";\n\n"
    
    str_privates_variables += "    // Port-Hamiltonian system's vectors\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.x())+",1> x ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.x())+",1> dx ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.x())+",1> dxH ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.w())+",1> w ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.w())+",1> z ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.y)+",1> u ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.y)+",1> y ;\n"
    str_privates_variables += "    vector<double> p = vector<double>(" + str(phs.dims.p()) + ");\n\n"
    
    str_privates_variables += "    // Runtime matrices \n"

    str_privates_variables += "    Matrix<double,"+str(phs.dims.xl)+","+str(phs.dims.xl)+"> Jxlxl ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.xl)+","+str(phs.dims.xnl())+"> Jxlxnl ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.xnl())+","+str(phs.dims.xnl())+"> Jxnlxnl ;\n"

    str_privates_variables += "    Matrix<double,"+str(phs.dims.wl)+","+str(phs.dims.wl)+"> Jwlwl ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.wl)+","+str(phs.dims.wnl())+"> Jwlwnl ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.wnl())+","+str(phs.dims.wnl())+"> Jwnlwnl ;\n"

    str_privates_variables += "    Matrix<double,"+str(phs.dims.xl)+","+str(phs.dims.wl)+"> Jxlwl ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.xl)+","+str(phs.dims.wnl())+"> Jxlwnl ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.xnl())+","+str(phs.dims.wl)+"> Jxnlwl ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.xnl())+","+str(phs.dims.wnl())+"> Jxnlwnl ;\n"

    str_privates_variables += "    Matrix<double,"+str(phs.dims.xl)+","+str(phs.dims.y)+"> Jxly ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.xnl())+","+str(phs.dims.y)+"> Jxnly ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.wl)+","+str(phs.dims.y)+"> Jwly ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.wnl())+","+str(phs.dims.y)+"> Jwnly ;\n"

    str_privates_variables += "    Matrix<double,"+str(phs.dims.wl)+","+str(phs.dims.wl)+"> iDw ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.wl)+","+str(phs.dims.wl)+"> Dw ;\n"

    str_privates_variables += "    Matrix<double,"+str(phs.dims.wl)+","+str(phs.dims.xl)+"> A1 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.wl)+","+str(phs.dims.xnl())+"> B1 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.wl)+","+str(phs.dims.wnl())+"> C1 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.wl)+","+str(phs.dims.y)+"> D1 ;\n"

    str_privates_variables += "    Matrix<double,"+str(phs.dims.xl)+","+str(phs.dims.xl)+"> tildeA2 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.xl)+","+str(phs.dims.xnl())+"> tildeB2 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.xl)+","+str(phs.dims.wnl())+"> tildeC2 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.xl)+","+str(phs.dims.y)+"> tildeD2 ;\n"

    str_privates_variables += "    Matrix<double,"+str(phs.dims.xl)+","+str(phs.dims.xl)+"> iDx ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.xl)+","+str(phs.dims.xl)+"> Dx ;\n"

    str_privates_variables += "    Matrix<double,"+str(phs.dims.xl)+","+str(phs.dims.xl)+"> A2 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.xl)+","+str(phs.dims.xnl())+"> B2 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.xl)+","+str(phs.dims.wnl())+"> C2 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.xl)+","+str(phs.dims.y)+"> D2 ;\n"

    str_privates_variables += "    Matrix<double,"+str(phs.dims.xl)+","+str(phs.dims.xl)+"> A3 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.xl)+","+str(phs.dims.xnl())+"> B3 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.xl)+","+str(phs.dims.wnl())+"> C3 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.xl)+","+str(phs.dims.y)+"> D3 ;\n"

    str_privates_variables += "    Matrix<double,"+str(phs.dims.xnl())+","+str(phs.dims.xl)+"> tildeA4 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.xnl())+","+str(phs.dims.xnl())+"> tildeB4 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.xnl())+","+str(phs.dims.wnl())+"> tildeC4 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.xnl())+","+str(phs.dims.y)+"> tildeD4 ;\n"

    str_privates_variables += "    Matrix<double,"+str(phs.dims.xnl())+","+str(phs.dims.xl)+"> A4 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.xnl())+","+str(phs.dims.xnl())+"> B4 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.xnl())+","+str(phs.dims.wnl())+"> C4 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.xnl())+","+str(phs.dims.y)+"> D4 ;\n"

    str_privates_variables += "    Matrix<double,"+str(phs.dims.wnl())+","+str(phs.dims.xl)+"> tildeA5 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.wnl())+","+str(phs.dims.xnl())+"> tildeB5 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.wnl())+","+str(phs.dims.wnl())+"> tildeC5 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.wnl())+","+str(phs.dims.y)+"> tildeD5 ;\n"

    str_privates_variables += "    Matrix<double,"+str(phs.dims.wnl())+","+str(phs.dims.xl)+"> A5 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.wnl())+","+str(phs.dims.xnl())+"> B5 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.wnl())+","+str(phs.dims.wnl())+"> C5 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.wnl())+","+str(phs.dims.y)+"> D5 ;\n"

    str_privates_variables += "    Matrix<double,"+str(phs.dims.wl)+","+str(phs.dims.xl)+"> A6 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.wl)+","+str(phs.dims.xnl())+"> B6 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.wl)+","+str(phs.dims.wnl())+"> C6 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.wl)+","+str(phs.dims.y)+"> D6 ;\n"

    str_privates_variables += "    Matrix<double,"+str(phs.dims.xl+phs.dims.wl)+","+str(phs.dims.xl)+"> A7 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.xl+phs.dims.wl)+","+str(phs.dims.xnl())+"> B7 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.xl+phs.dims.wl)+","+str(phs.dims.wnl())+"> C7 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.xl+phs.dims.wl)+","+str(phs.dims.y)+"> D7 ;\n"

    str_privates_variables += "    Matrix<double,"+str(phs.dims.xnl())+","+str(phs.dims.xnl()+phs.dims.wnl())+"> Bxnl ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.wnl())+","+str(phs.dims.xnl()+phs.dims.wnl())+"> Bwnl ;\n"

    str_privates_variables += "    Matrix<double,"+str(phs.dims.xl)+","+str(phs.dims.xl)+"> Q ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.dims.wl)+","+str(+phs.dims.wl)+"> R ;\n"

    str_privates_variables += "\n    // Pointers to the sample rate\n"
    str_fs = ("\n        const int fs = " + str(phs.simulation.config['fs']) + ";\n") if isinstance(phs.simulation.config['fs'], (int, float)) else "    double & fs = p[0];\n"
    str_privates_variables += str_fs
    
    str_privates_variables += "\n    // Pointers to the linear part of each vector\n"
    str_privates_variables += "    double * pointer_xl = "+"& x[0];\n"
    str_privates_variables += "    double * pointer_dxl = "+"& dx[0];\n"
    str_privates_variables += "    double * pointer_dxHl = "+"& dxH[0];\n"
    if phs.dims.wl>0:
        str_privates_variables += "    double * pointer_wl = "+"& w[0];\n"
        str_privates_variables += "    double * pointer_zl = "+"& z[0];\n\n"


    str_privates_variables += "    Matrix<double,"+str(phs.dims.xl+phs.dims.wl)+","+str(1)+"> Fl ;\n"

    if phs.dims.xnl() + phs.dims.wnl() > 0:
        str_privates_variables += "    // Pointers to the nonlinear part of each vector\n"
        if phs.dims.xnl()>0:
            str_privates_variables += "    double * pointer_xnl = "+"& x[" + str(phs.dims.xl)+ "];\n"
            str_privates_variables += "    double * pointer_dxnl = "+"& dx[" + str(phs.dims.xl)+ "];\n"
            str_privates_variables += "    double * pointer_dxHnl = "+"& dxH[" + str(phs.dims.xl)+ "];\n"
        if phs.dims.wnl()>0:
            str_privates_variables += "    double * pointer_wnl = "+"& w[" + str(phs.dims.wl)+ "];\n"
            str_privates_variables += "    double * pointer_znl = "+"& z[" + str(phs.dims.wl)+ "];\n\n"

        str_privates_variables += "    // Variables for NR iterations\n"
        str_privates_variables += "    double NbItNR = " + str(NbItNR) + ";\n"
        str_privates_variables += "    double residual_NR = 0;\n"
        str_privates_variables += "    double it = 0;\n"
        str_privates_variables += "    double eps = "+ str(NumTolNr) + ";\n"

        str_privates_variables += "    Matrix<double,"+str(phs.dims.xnl()+phs.dims.wnl())+","+str(1)+"> Fnl ;\n"
        str_privates_variables += "    Matrix<double,"+str(phs.dims.xnl()+phs.dims.wnl())+","+str(1)+"> ImpFunc ;\n"
        str_privates_variables += "    Matrix<double,"+str(phs.dims.xnl()+phs.dims.wnl())+","+str(phs.dims.xnl()+phs.dims.wnl())+"> JacobianFnl ;\n"
        str_privates_variables += "    Matrix<double,"+str(phs.dims.xnl()+phs.dims.wnl())+","+str(phs.dims.xnl()+phs.dims.wnl())+"> JacobianImplicitFunc ;\n"

    str_outro = "};\n#endif /* " + header_label + " */"
    str_out = str_test + str_includes + str_class + str_publics_variables  +\
            str_constructor +str_initx_constructor+str_destructor+ str_accesors +\
            str_modificators +str_phs_functions+ str_privates_variables + str_outro
    h_file = open(phs.paths['cpp']+"/"+"phobj.h", 'w')
    h_file.write(str_out)
    h_file.close()
    return str_out

