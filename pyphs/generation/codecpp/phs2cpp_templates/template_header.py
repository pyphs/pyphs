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
    
    dict_args = {"x":phs.x, "dx": phs.dx, "w": phs.w, "u": phs.u, "p": phs.params}
    phs_label = phs.label.upper()

    expr = list(phs.Fl)
    label_variable = ["dxl["+str(n)+"]" for n in range(phs.nxl())]+ ["wl["+str(n)+"]" for n in range(phs.nwl())]
    label_func = "Fl"
    str_phs_functions += Expr2Cpp(expr,dict_args,phs_label, label_func, label_variable, "h")

    if phs.isNL:
        from sympy import Matrix
        expr = list(Matrix(phs.dxnl()+phs.wnl())+Matrix(phs.Fnl))
        label_variable = ["dxnl["+str(n)+"]" for n in range(phs.nxnl())]+ ["wnl["+str(n)+"]" for n in range(phs.nwnl())]
        label_func = "Fnl"
        str_phs_functions += Expr2Cpp(expr,dict_args,phs_label, label_func, label_variable, "h")
    
        expr = [phs.Fnl_residual]
        label_variable = "residual_NR"
        label_func = "FresidualNR"
        str_phs_functions += Expr2Cpp(expr,dict_args,phs_label, label_func, label_variable, "h").replace('residual_NR[0] ', 'residual_NR ')

    expr = phs.dxH
    label_variable = "dxH"
    label_func = "FdxH"
    str_phs_functions += Expr2Cpp(expr,dict_args,phs_label, label_func, label_variable, "h")

    expr = phs.z
    label_variable = "z"
    label_func = "Fz"
    str_phs_functions += Expr2Cpp(expr,dict_args,phs_label, label_func, label_variable, "h")
            
    expr = phs.Fy
    label_variable = "y"
    label_func = "Fy"
    str_phs_functions += Expr2Cpp(expr,dict_args,phs_label, label_func, label_variable, "h")
    
    str_phs_functions += "    void process(vector<double>&, vector<double>&);\n"
    
    str_privates_variables = "\nprivate:\n\n"

    str_privates_variables += "    // Dimensions of the port-Hamiltonian system\n"
    str_privates_variables += "    "+"const unsigned int nx=" + str(phs.nx()) + ";\n"
    str_privates_variables += "    "+"const unsigned int nxl=" + str(phs.nxl()) + ";\n"
    str_privates_variables += "    "+"const unsigned int nxnl=" + str(phs.nxnl()) + ";\n"
    str_privates_variables += "    "+"const unsigned int nw=" + str(phs.nw()) + ";\n"
    str_privates_variables += "    "+"const unsigned int nwl=" + str(phs.nwl()) + ";\n"
    str_privates_variables += "    "+"const unsigned int nwnl=" + str(phs.nwnl()) + ";\n"
    str_privates_variables += "    "+"const unsigned int ny=" + str(phs.ny()) + ";\n"
    str_privates_variables += "    "+"const unsigned int np=" + str(phs.params.__len__()) + ";\n\n"
    
    str_privates_variables += "    // Port-Hamiltonian system's vectors\n"
    str_privates_variables += "    vector<double> x = vector<double>(" + str(phs.nx()) + ");\n"
    str_privates_variables += "    vector<double> dx = vector<double>(" + str(phs.nx()) + ");\n"
    str_privates_variables += "    vector<double> dxH = vector<double>(" + str(phs.nx()) + ");\n"
    str_privates_variables += "    vector<double> w = vector<double>(" + str(phs.nw()) + ");\n"
    str_privates_variables += "    vector<double> z = vector<double>(" + str(phs.nw()) + ");\n"
    str_privates_variables += "    vector<double> u = vector<double>(" + str(phs.ny()) + ");\n"
    str_privates_variables += "    vector<double> y = vector<double>(" + str(phs.ny()) + ");\n"
    str_privates_variables += "    vector<double> p = vector<double>(" + str(phs.params.__len__()) + ");\n\n"
    
    str_privates_variables += "    // Pointers to the linear part of each vector\n"
    str_privates_variables += "    double * xl = "+"& x[0];\n"
    str_privates_variables += "    double * dxl = "+"& dx[0];\n"
    str_privates_variables += "    double * dxHl = "+"& dxH[0];\n"
    str_privates_variables += "    double * wl = "+"& w[0];\n"
    str_privates_variables += "    double * zl = "+"& z[0];\n\n"

    str_privates_variables += "    // Pointers to the nonlinear part of each vector\n"
    str_privates_variables += "    double * xnl = "+"& x[" + str(phs.nxl())+ "];\n"
    str_privates_variables += "    double * dxnl = "+"& dx[" + str(phs.nxl())+ "];\n"
    str_privates_variables += "    double * dxHnl = "+"& dxH[" + str(phs.nxl())+ "];\n"
    str_privates_variables += "    double * wnl = "+"& w[" + str(phs.nwl())+ "];\n"
    str_privates_variables += "    double * znl = "+"& z[" + str(phs.nwl())+ "];\n\n"

    str_privates_variables += "    // Variables for NR iterations\n"
    str_privates_variables += "    double NbItNR = " + str(NbItNR) + ";\n"
    str_privates_variables += "    double residual_NR = 0;\n"
    str_privates_variables += "    double it = 0;\n"
    str_privates_variables += "    double eps = "+ str(NumTolNr) + ";\n"

    str_outro = "};\n#endif /* " + header_label + " */"
    str_out = str_test + str_includes + str_class + str_publics_variables  +\
            str_constructor +str_initx_constructor+str_destructor+ str_accesors +\
            str_modificators +str_phs_functions+ str_privates_variables + str_outro
    h_file = open(phs.folders['cpp']+"/"+"phobj.h", 'w')
    h_file.write(str_out)
    h_file.close()
    return str_out

def hfile_full(phs):  

    from pyphs_config import eigen_path    
    
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
    
    dict_args = {"x":phs.x, "dx": phs.dx, "w": phs.w, "u": phs.u, "p": phs.params}
    phs_label = phs.label.upper()

    expr = list(phs.Fl)
    label_variable = ["dxl["+str(n)+"]" for n in range(phs.nxl())]+ ["wl["+str(n)+"]" for n in range(phs.nwl())]
    label_func = "UpDate_l"
    str_phs_functions += Expr2Cpp(expr,dict_args,phs_label, label_func, label_variable, "h")

    expr = phs.dxH
    label_variable = "dxH"
    label_func = "UpDate_dxH"
    str_phs_functions += Expr2Cpp(expr,dict_args,phs_label, label_func, label_variable, "h")

    expr = phs.z
    label_variable = "z"
    label_func = "UpDate_z"
    str_phs_functions += Expr2Cpp(expr,dict_args,phs_label, label_func, label_variable, "h")
            
    expr = phs.Fy
    label_variable = "y"
    label_func = "UpDate_y"
    str_phs_functions += Expr2Cpp(expr,dict_args,phs_label, label_func, label_variable, "h")

    matrixExpr = phs.J1        
    matrixLabel = 'J1'
    funcLabel = 'UpDate_J1'
    str_phs_functions += Matrix2Cpp(matrixExpr, dict_args, phs_label, funcLabel, matrixLabel, "h")

    matrixExpr = phs.J2        
    matrixLabel = 'J2'
    funcLabel = 'UpDate_J2'
    str_phs_functions += Matrix2Cpp(matrixExpr, dict_args, phs_label, funcLabel, matrixLabel, "h")

    matrixExpr = phs.J3        
    matrixLabel = 'J3'
    funcLabel = 'UpDate_J3'
    str_phs_functions += Matrix2Cpp(matrixExpr, dict_args, phs_label, funcLabel, matrixLabel, "h")

    matrixExpr = phs.J4        
    matrixLabel = 'J4'
    funcLabel = 'UpDate_J4'
    str_phs_functions += Matrix2Cpp(matrixExpr, dict_args, phs_label, funcLabel, matrixLabel, "h")

    matrixExpr = phs.K1        
    matrixLabel = 'K1'
    funcLabel = 'UpDate_K1'
    str_phs_functions += Matrix2Cpp(matrixExpr, dict_args, phs_label, funcLabel, matrixLabel, "h")

    matrixExpr = phs.K2        
    matrixLabel = 'K2'
    funcLabel = 'UpDate_K2'
    str_phs_functions += Matrix2Cpp(matrixExpr, dict_args, phs_label, funcLabel, matrixLabel, "h")

    matrixExpr = phs.K3        
    matrixLabel = 'K3'
    funcLabel = 'UpDate_K3'
    str_phs_functions += Matrix2Cpp(matrixExpr, dict_args, phs_label, funcLabel, matrixLabel, "h")

    matrixExpr = phs.K4        
    matrixLabel = 'K4'
    funcLabel = 'UpDate_K4'
    str_phs_functions += Matrix2Cpp(matrixExpr, dict_args, phs_label, funcLabel, matrixLabel, "h")

    matrixExpr = phs.G1        
    matrixLabel = 'G1'
    funcLabel = 'UpDate_G1'
    str_phs_functions += Matrix2Cpp(matrixExpr, dict_args, phs_label, funcLabel, matrixLabel, "h")

    matrixExpr = phs.G2        
    matrixLabel = 'G2'
    funcLabel = 'UpDate_G2'
    str_phs_functions += Matrix2Cpp(matrixExpr, dict_args, phs_label, funcLabel, matrixLabel, "h")

    matrixExpr = phs.G3     
    matrixLabel = 'G3'
    funcLabel = 'UpDate_G3'
    str_phs_functions += Matrix2Cpp(matrixExpr, dict_args, phs_label, funcLabel, matrixLabel, "h")

    matrixExpr = phs.G4        
    matrixLabel = 'G4'
    funcLabel = 'UpDate_G4'
    str_phs_functions += Matrix2Cpp(matrixExpr, dict_args, phs_label, funcLabel, matrixLabel, "h")

    matrixExpr = phs.M1        
    matrixLabel = 'M1'
    funcLabel = 'UpDate_M1'
    str_phs_functions += Matrix2Cpp(matrixExpr, dict_args, phs_label, funcLabel, matrixLabel, "h")

    matrixExpr = phs.M2        
    matrixLabel = 'M2'
    funcLabel = 'UpDate_M2'
    str_phs_functions += Matrix2Cpp(matrixExpr, dict_args, phs_label, funcLabel, matrixLabel, "h")

    matrixExpr = phs.R()        
    matrixLabel = 'R'
    funcLabel = 'UpDate_R'
    str_phs_functions += Matrix2Cpp(matrixExpr, dict_args, phs_label, funcLabel, matrixLabel, "h")

    matrixExpr = phs.Q()        
    matrixLabel = 'Q'
    funcLabel = 'UpDate_Q'
    str_phs_functions += Matrix2Cpp(matrixExpr, dict_args, phs_label, funcLabel, matrixLabel, "h")
    
    str_phs_functions += "    void UpDate_Matrices();\n"

    str_phs_functions += "    void process(vector<double>&, vector<double>&);\n"
    
    str_phs_functions += "    Matrix<double,"+str(phs.nxl())+","+str(1)+"> xl();\n"
    str_phs_functions += "    Matrix<double,"+str(phs.nxl())+","+str(1)+"> dxl();\n"
    str_phs_functions += "    Matrix<double,"+str(phs.nxl())+","+str(1)+"> dxHl();\n"
    str_phs_functions += "    Matrix<double,"+str(phs.nwl())+","+str(1)+"> wl();\n"
    str_phs_functions += "    Matrix<double,"+str(phs.nwl())+","+str(1)+"> zl();\n"
    str_phs_functions += "    Matrix<double,"+str(phs.nxnl()+ phs.nwnl())+","+str(phs.nxnl()+ phs.nwnl())+"> iJacobianImplicitFunc();\n"

    if phs.isNL:
        str_phs_functions += "    void UpDate_residualNR();\n"
        str_phs_functions += "    void UpDate_nl();\n"
        str_phs_functions += "    void UpDate_Fnl();\n"
        str_phs_functions += "    void UpDate_ImpFunc();\n"
        str_phs_functions += "    void UpDate_JacobianFnl();\n"
        if phs.nxnl()>0:
            str_phs_functions += "    Matrix<double,"+str(phs.nxnl())+","+str(1)+"> xnl();\n"
            str_phs_functions += "    Matrix<double,"+str(phs.nxnl())+","+str(1)+"> dxnl();\n"
            str_phs_functions += "    Matrix<double,"+str(phs.nxnl())+","+str(1)+"> dxHnl();\n"
        if phs.nwnl()>0:
            str_phs_functions += "    Matrix<double,"+str(phs.nwnl())+","+str(1)+"> wnl();\n"
            str_phs_functions += "    Matrix<double,"+str(phs.nwnl())+","+str(1)+"> znl();\n"

    str_privates_variables = "\nprivate:\n\n"

    str_privates_variables += "    // Dimensions of the port-Hamiltonian system\n"
    str_privates_variables += "    "+"const unsigned int nx=" + str(phs.nx()) + ";\n"
    str_privates_variables += "    "+"const unsigned int nxl=" + str(phs.nxl()) + ";\n"
    str_privates_variables += "    "+"const unsigned int nxnl=" + str(phs.nxnl()) + ";\n"
    str_privates_variables += "    "+"const unsigned int nw=" + str(phs.nw()) + ";\n"
    str_privates_variables += "    "+"const unsigned int nwl=" + str(phs.nwl()) + ";\n"
    str_privates_variables += "    "+"const unsigned int nwnl=" + str(phs.nwnl()) + ";\n"
    str_privates_variables += "    "+"const unsigned int ny=" + str(phs.ny()) + ";\n"
    str_privates_variables += "    "+"const unsigned int np=" + str(phs.params.__len__()) + ";\n\n"
    
    str_privates_variables += "    // Port-Hamiltonian system's vectors\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nx())+",1> x ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nx())+",1> dx ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nx())+",1> dxH ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nw())+",1> w ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nw())+",1> z ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.ny())+",1> u ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.ny())+",1> y ;\n"
    str_privates_variables += "    vector<double> p = vector<double>(" + str(phs.params.__len__()) + ");\n\n"
    
    str_privates_variables += "    // Runtime matrices \n"

    str_privates_variables += "    Matrix<double,"+str(phs.nxl())+","+str(phs.nxl())+"> J1 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nxl())+","+str(phs.nxnl())+"> M1 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nxnl())+","+str(phs.nxnl())+"> J2 ;\n"

    str_privates_variables += "    Matrix<double,"+str(phs.nwl())+","+str(phs.nwl())+"> J3 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nwl())+","+str(phs.nwnl())+"> M2 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nwnl())+","+str(phs.nwnl())+"> J4 ;\n"

    str_privates_variables += "    Matrix<double,"+str(phs.nxl())+","+str(phs.nwl())+"> K1 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nxl())+","+str(phs.nwnl())+"> K2 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nxnl())+","+str(phs.nwl())+"> K3 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nxnl())+","+str(phs.nwnl())+"> K4 ;\n"

    str_privates_variables += "    Matrix<double,"+str(phs.nxl())+","+str(phs.ny())+"> G1 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nxnl())+","+str(phs.ny())+"> G2 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nwl())+","+str(phs.ny())+"> G3 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nwnl())+","+str(phs.ny())+"> G4 ;\n"

    str_privates_variables += "    Matrix<double,"+str(phs.nwl())+","+str(phs.nwl())+"> iDw ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nwl())+","+str(phs.nwl())+"> Dw ;\n"

    str_privates_variables += "    Matrix<double,"+str(phs.nwl())+","+str(phs.nxl())+"> A1 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nwl())+","+str(phs.nxnl())+"> B1 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nwl())+","+str(phs.nwnl())+"> C1 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nwl())+","+str(phs.ny())+"> D1 ;\n"

    str_privates_variables += "    Matrix<double,"+str(phs.nxl())+","+str(phs.nxl())+"> tildeA2 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nxl())+","+str(phs.nxnl())+"> tildeB2 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nxl())+","+str(phs.nwnl())+"> tildeC2 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nxl())+","+str(phs.ny())+"> tildeD2 ;\n"

    str_privates_variables += "    Matrix<double,"+str(phs.nxl())+","+str(phs.nxl())+"> iDx ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nxl())+","+str(phs.nxl())+"> Dx ;\n"

    str_privates_variables += "    Matrix<double,"+str(phs.nxl())+","+str(phs.nxl())+"> A2 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nxl())+","+str(phs.nxnl())+"> B2 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nxl())+","+str(phs.nwnl())+"> C2 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nxl())+","+str(phs.ny())+"> D2 ;\n"

    str_privates_variables += "    Matrix<double,"+str(phs.nxl())+","+str(phs.nxl())+"> A3 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nxl())+","+str(phs.nxnl())+"> B3 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nxl())+","+str(phs.nwnl())+"> C3 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nxl())+","+str(phs.ny())+"> D3 ;\n"

    str_privates_variables += "    Matrix<double,"+str(phs.nxnl())+","+str(phs.nxl())+"> tildeA4 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nxnl())+","+str(phs.nxnl())+"> tildeB4 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nxnl())+","+str(phs.nwnl())+"> tildeC4 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nxnl())+","+str(phs.ny())+"> tildeD4 ;\n"

    str_privates_variables += "    Matrix<double,"+str(phs.nxnl())+","+str(phs.nxl())+"> A4 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nxnl())+","+str(phs.nxnl())+"> B4 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nxnl())+","+str(phs.nwnl())+"> C4 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nxnl())+","+str(phs.ny())+"> D4 ;\n"

    str_privates_variables += "    Matrix<double,"+str(phs.nwnl())+","+str(phs.nxl())+"> tildeA5 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nwnl())+","+str(phs.nxnl())+"> tildeB5 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nwnl())+","+str(phs.nwnl())+"> tildeC5 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nwnl())+","+str(phs.ny())+"> tildeD5 ;\n"

    str_privates_variables += "    Matrix<double,"+str(phs.nwnl())+","+str(phs.nxl())+"> A5 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nwnl())+","+str(phs.nxnl())+"> B5 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nwnl())+","+str(phs.nwnl())+"> C5 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nwnl())+","+str(phs.ny())+"> D5 ;\n"

    str_privates_variables += "    Matrix<double,"+str(phs.nwl())+","+str(phs.nxl())+"> A6 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nwl())+","+str(phs.nxnl())+"> B6 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nwl())+","+str(phs.nwnl())+"> C6 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nwl())+","+str(phs.ny())+"> D6 ;\n"

    str_privates_variables += "    Matrix<double,"+str(phs.nxl()+phs.nwl())+","+str(phs.nxl())+"> A7 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nxl()+phs.nwl())+","+str(phs.nxnl())+"> B7 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nxl()+phs.nwl())+","+str(phs.nwnl())+"> C7 ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nxl()+phs.nwl())+","+str(phs.ny())+"> D7 ;\n"

    str_privates_variables += "    Matrix<double,"+str(phs.nxnl())+","+str(phs.nxnl()+phs.nwnl())+"> Bxnl ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nwnl())+","+str(phs.nxnl()+phs.nwnl())+"> Bwnl ;\n"

    str_privates_variables += "    Matrix<double,"+str(phs.nxl())+","+str(phs.nxl())+"> Q ;\n"
    str_privates_variables += "    Matrix<double,"+str(phs.nwl())+","+str(+phs.nwl())+"> R ;\n"

    str_privates_variables += "\n    // Pointers to the sample rate\n"
    str_fs = ("\n        const int fs = " + str(phs.fs) + ";\n") if isinstance(phs.fs, (int, float)) else "    double & fs = p[0];\n"
    str_privates_variables += str_fs
    
    str_privates_variables += "\n    // Pointers to the linear part of each vector\n"
    str_privates_variables += "    double * pointer_xl = "+"& x[0];\n"
    str_privates_variables += "    double * pointer_dxl = "+"& dx[0];\n"
    str_privates_variables += "    double * pointer_dxHl = "+"& dxH[0];\n"
    if phs.nwl()>0:
        str_privates_variables += "    double * pointer_wl = "+"& w[0];\n"
        str_privates_variables += "    double * pointer_zl = "+"& z[0];\n\n"


    str_privates_variables += "    Matrix<double,"+str(phs.nxl()+phs.nwl())+","+str(1)+"> Fl ;\n"

    if phs.isNL:
        str_privates_variables += "    // Pointers to the nonlinear part of each vector\n"
        if phs.nxnl()>0:
            str_privates_variables += "    double * pointer_xnl = "+"& x[" + str(phs.nxl())+ "];\n"
            str_privates_variables += "    double * pointer_dxnl = "+"& dx[" + str(phs.nxl())+ "];\n"
            str_privates_variables += "    double * pointer_dxHnl = "+"& dxH[" + str(phs.nxl())+ "];\n"
        if phs.nwnl()>0:
            str_privates_variables += "    double * pointer_wnl = "+"& w[" + str(phs.nwl())+ "];\n"
            str_privates_variables += "    double * pointer_znl = "+"& z[" + str(phs.nwl())+ "];\n\n"

        str_privates_variables += "    // Variables for NR iterations\n"
        str_privates_variables += "    double NbItNR = " + str(NbItNR) + ";\n"
        str_privates_variables += "    double residual_NR = 0;\n"
        str_privates_variables += "    double it = 0;\n"
        str_privates_variables += "    double eps = "+ str(NumTolNr) + ";\n"

        str_privates_variables += "    Matrix<double,"+str(phs.nxnl()+phs.nwnl())+","+str(1)+"> Fnl ;\n"
        str_privates_variables += "    Matrix<double,"+str(phs.nxnl()+phs.nwnl())+","+str(1)+"> ImpFunc ;\n"
        str_privates_variables += "    Matrix<double,"+str(phs.nxnl()+phs.nwnl())+","+str(phs.nxnl()+phs.nwnl())+"> JacobianFnl ;\n"
        str_privates_variables += "    Matrix<double,"+str(phs.nxnl()+phs.nwnl())+","+str(phs.nxnl()+phs.nwnl())+"> JacobianImplicitFunc ;\n"

    str_outro = "};\n#endif /* " + header_label + " */"
    str_out = str_test + str_includes + str_class + str_publics_variables  +\
            str_constructor +str_initx_constructor+str_destructor+ str_accesors +\
            str_modificators +str_phs_functions+ str_privates_variables + str_outro
    h_file = open(phs.folders['cpp']+"/"+"phobj.h", 'w')
    h_file.write(str_out)
    h_file.close()
    return str_out

