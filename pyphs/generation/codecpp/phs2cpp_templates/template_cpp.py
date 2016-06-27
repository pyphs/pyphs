# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 02:17:30 2016

@author: Falaize
"""

def str_get_int(phs, name):
    string = "const unsigned int " + \
        class_ref(phs) + "get_"+name+"() const {"+\
        "\n    return "+name+";\n}\n"
    return string


def str_get_vec(phs, name, dim_name):
    return \
        """vector<double> """+class_ref(phs)+"""get_"""+name+"""() const {
vector<double> v = vector<double>("""+dim+""");
 for (int i=0; i<get_"""+dim+"""(); i++) {
    v[i] = """+name+"""[i];
 }
return v;
}
"""


def str_accesors_presolve(phs):
    str_accesors = "\n// Accesors to private variables\n\n"
    str_accesors += str_get_int('nx')
    str_accesors += str_get_int('nxl')
    str_accesors += str_get_int('nxnl')
    str_accesors += str_get_int('nw')
    str_accesors += str_get_int('nwl')
    str_accesors += str_get_int('nwnl')
    str_accesors += str_get_int('ny')
    str_accesors += str_get_int('np')
    str_accesors += str_get_vec('u', 'ny')
    str_accesors += str_get_vec('y', 'ny')
    str_accesors += str_get_vec('x', 'nx')
    str_accesors += str_get_vec('dx', 'nx')
    str_accesors += str_get_vec('dxH', 'nx')
    str_accesors += str_get_vec('w', 'nw')
    str_accesors += str_get_vec('z', 'ny')
    return str_accesors

def str_modificators_presolve(phs):
    def str_set(var):
        return "void "+class_ref(phs)+"set_"+var+"(vector<double> v) {\n    "+var+" = v; \n}\n"
    str_modificators = "\n// Mutators of private variables\n"
    str_modificators += str_set('u')
    str_modificators += str_set('x')
    return str_modificators

def str_functions_presolve(phs):

    dict_args = {"x":phs.symbs.x, "dx": phs.dx, "w": phs.symbs.w, "u": phs.symbs.u, "p": phs.symbs.p}
    phs_label = phs.label.upper()

    from ..phs2cpp import Expr2Cpp
    exprcpp = lambda e, lf, lv: Expr2Cpp(e, dict_args, phs_label, lf, lv, "c")

    str_phs_functions = "\n// Port-Hamiltonian runtime functions\n"

    expr = list(phs.Fl)
    str_dxl = ["dx["+str(n)+"]" for n in range(phs.dims.xl)]
    str_mat_wl = ["w["+str(n)+"]" for n in range(phs.dims.wl)]
    label_variable = str_dxl + str_mat_wl
    label_func = "Fl"
    str_phs_functions += exprcpp(expr, label_func, label_variable)

    if phs.isNL:
        from sympy import Matrix
        expr = list(Matrix(phs.dxnl()+phs.symbs.wnl())+Matrix(phs.Fnl))
        str_dxl = ["dx["+str(phs.dims.xl+n)+"]" for n in range(phs.dims.xnl())]
        str_mat_wl = ["wnl["+str(phs.dims.wl+n)+"]" for n in range(phs.dims.wnl())]
        label_variable = str_dxl + str_mat_wl
        label_func = "Fnl"
        str_phs_functions += exprcpp(expr, label_func, label_variable)

        expr = [phs.Fnl_residual]
        label_variable = "residual_NR"
        label_func = "FresidualNR"
        str_phs_functions += exprcpp(expr, label_func, label_variable).replace('residual_NR[0] ', 'residual_NR ')

    expr = phs.exprs.dxHd
    label_variable = "dxH"
    label_func = "FdxH"
    str_phs_functions += exprcpp(expr, label_func, label_variable)

    expr = phs.exprs.z
    label_variable = "z"
    label_func = "Fz"
    str_phs_functions += exprcpp(expr, label_func, label_variable)

    expr = phs.Fy
    label_variable = "y"
    label_func = "Fy"
    str_phs_functions += exprcpp(expr, label_func, label_variable)
    return str_phs_functions

def str_process_presolve(phs):

    phs_label = phs.label.upper()
    if phs.isNL:
        str_newton_solver = \
    """
            // Newton-Raphson iteration
            it = 0;
            residual_NR = 1;
            while ((it<NbItNR) & (residual_NR>eps)) {
                Fnl();
                FresidualNR();
                it++;
            }
    """
    else:
        str_newton_solver = ""

    str_process = "void "+phs_label+"::process(vector<double>& In, vector<double>& parameters) {\n "+\
    """

        u = In;
        p = parameters;
    """ + str_newton_solver + \
    """
        Fl();
        FdxH();
        Fz();
        Fy();
        for (unsigned int i=0; i<get_nx(); i++ ) {
            x[i] += dx[i];
        }
    """ +"}\n"
    return str_process


def cfile_presolve(phs):

    str_includes = '#include "'+phs.paths['cpp']+"/" + ('phobj').upper() + '.h"\n\n'

    str_constructor = "\n// Default Constructor:\n"+class_ref(phs)+phs.label.upper()+"() {\n}\n"

    str_initx_constructor = "\n// Constructor Initializing x:\n"+class_ref(phs)+\
                        phs.label.upper()+"(vector<double>& x0) {\n"  +\
                        '    if (x.size() == x0.size()) {\n        x = x0;\n    }\n    else {\n        cerr << "Size of x0 does not match size of x" << endl;\n        exit(1);\n    }\n}\n'

    str_destructor = "\n// Default Destructor:\n"+class_ref(phs)+ "~"+phs.label.upper()+"() {\n\n}\n"

    str_c = ""
    str_c += str_includes
    str_c += str_constructor
    str_c += str_process_presolve(phs)
    str_c += str_initx_constructor+str_destructor
    str_c += str_accesors_presolve(phs)
    str_c += str_modificators_presolve(phs)
    str_c += str_functions_presolve(phs)

    c_file = open(phs.paths['cpp']+"/"+"phobj.cpp", 'w')
    c_file.write(str_c)
    c_file.close()

    return str_c


###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################


