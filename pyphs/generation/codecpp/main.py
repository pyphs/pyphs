# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 14:31:08 2016

@author: Falaize
"""

from tools import name2dim, indent
from preamble import str_preamble
import os


def main(phs):
    string = ""
    string += str_preamble(phs)
    string += _str_includes()
    string += _str_namespaces()
    string += _str_timer()
    string += "\n\n\nint main() {"
    string += _str_body(phs)
    string += "\n    return 0;\n}\n"
    return string


# -----------------------------------------------------------------------------


def _str_body(phs):
    """
    return piece of cpp code.
    collects body pieces for main.cpp
    """
    string = ""
    string += _str_dims(phs)
    string += _str_initvecs(phs)
    string += _str_open_files(phs)
    string += _str_instanciate(phs)
    string += """\n\n    int barWidth = 20;
    int ETA, ETAm, ETAs;
    float progress = 0.0;
    timer t;"""
    string += _str_process(phs)
    return string


# -----------------------------------------------------------------------------


def object_label():
    return 'PHS'


# -----------------------------------------------------------------------------


def _str_includes():
    """
    return piece of cpp code.
    includes for main.cpp
    """
    string = """\n
#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <cstdio>
#include <time.h>
#include <math.h>

#include "phobj.h"
"""
    return string


# -----------------------------------------------------------------------------


def _str_namespaces():
    """
    return piece of cpp code.
    namespaces for main.cpp
    """
    return """
using namespace std;"""


# -----------------------------------------------------------------------------


def _str_timer():
    """
    return piece of cpp code.
    timer for process in main.cpp
    """
    string = """\n
class timer {
private:
    unsigned long begTime;
public:
    void start() {
        begTime = clock();
    }
    unsigned long elapsedTime() {
        return ((unsigned long) clock() - begTime) / \
CLOCKS_PER_SEC;
    }
    bool isTimeout(unsigned long seconds) {
        return seconds >= elapsedTime();
    }
};"""
    return string


# -----------------------------------------------------------------------------

def _str_dims(phs):
    from tools import str_dims
    string = str_dims(phs) + "\n\nconst unsigned int nt = " + \
        str(phs.simu.config['nt']) + ";"
    return indent(string)


# -----------------------------------------------------------------------------


def _str_initvecs(phs):
    string = "\n"
    names = ('x0', 'u', 'p', 'x', 'dx', 'dxH', 'w', 'z', 'y')
    for name in names:
        string += str_initvec(phs, name)
    return string


# -----------------------------------------------------------------------------


def _str_open_files(phs):
    """
    return piece of cpp code.
    open files 'x0.txt', 'u.txt' and 'p.txt'
    """
    string = "\n"
    names = ('x0', 'u', 'p')
    for name in names:
        if getattr(phs.simu.exprs, name2dim(name)) > 0:
            string += str_open_file(phs, name)
    return string


# -----------------------------------------------------------------------------


def _str_readx0():
    string = """\n
    for (unsigned int i=0; i < """ + name2dim('x0') + """; i++) {
        x0File >> x0Vector[i];
    }"""
    return string


# -----------------------------------------------------------------------------


def _str_readdata(phs):
    string = ""
    dimu = getattr(phs.simu.exprs, name2dim('u'))
    dimp = getattr(phs.simu.exprs, name2dim('p'))
    if dimu + dimp > 0:
        string = ""
        if dimu > 0:
            string += """\n
        // Get input data
        for (unsigned int i=0; i<""" + name2dim('u') + """; i++) {
            uFile >> uVector[i];
        }"""
        if dimp > 0:
            string += """\n
        // Get parameters data
        for (unsigned int i=0; i<""" + name2dim('p') + """; i++) {
            pFile >> pVector[i];
        }"""
    return string


# -----------------------------------------------------------------------------


def _init_file(phs, name):
    """
    open files for saving data
    """
    string = """
    ofstream """ + name + """File;
    """ + name + """File.open(""" + '"' + phs.paths['data'] + os.sep + \
        name + """.txt");"""
    return string


# -----------------------------------------------------------------------------


def _init_files(phs):
    string = ""
    names = ('x', 'dx', 'dxH', 'w', 'z', 'y')
    for name in names:
        string += _init_file(phs, name)
    return string


# -----------------------------------------------------------------------------


def _str_instanciate(phs):
    string = """\n
    // Instance of port-Hamiltonian system
    """ + phs.label.upper() + ' ' + object_label()
    string += "(x0Vector);" if phs.simu.exprs.nx > 0 else ';'
    return string


# -----------------------------------------------------------------------------


def _str_process(phs):
    dimu = getattr(phs.simu.exprs, name2dim('u'))
    dimp = getattr(phs.simu.exprs, name2dim('p'))
    string = """\n
    // Process
    t.start();\n"""
    string += _init_files(phs)
    string += """\n\n
    for (unsigned int n = 0; n < nt; n++) {\n""" + _str_readdata(phs) + """
        std::cout << "[";
        int pos = barWidth * progress;
        for (int i = 0; i < barWidth; ++i) {
            if (i < pos) std::cout << "=";
            else if (i == pos) std::cout << ">";
            else std::cout << " ";
        }
        progress = float(n)/float(nt);
        if(1){
            ETA = (float(nt)/float(n+1)-1.)*(t.elapsedTime());
            ETAm = int(floor(ETA))/60;
            ETAs = floor(ETA%60);
            std::cout << "] " << int(progress * 100.0) << " % done, ETA: " \
<< ETAm << "m" << ETAs << "s\\r" << endl ;
            std::cout.flush();
        }"""
    string += """
        // Process update
        """ + object_label() + """.process("""
    if dimu > 0:
        string += "uVector"
        if dimp > 0:
            string += ', '
    if dimp > 0:
        string += "pVector"
    string += """);
        // Get quantities""" + _get_x(phs) + '\n' + _get_w(phs) + '\n' \
        + _get_y(phs) + """
    }"""
    string += '\n    uFile.close();\n    yFile.close();' if dimu > 0 else ''
    string += '\n    pFile.close();' if dimp > 0 else ''
    string += """
    xFile.close();
    dxFile.close();
    dxHFile.close();""" if phs.simu.exprs.nx > 0 else ''
    string += """
    wFile.close();
    zFile.close();""" if phs.simu.exprs.nw > 0 else ''
    string += """
    cout << endl;
    cout << "Data written at" << endl;
    cout << endl;
    cout << """ + '"' + phs.paths['data'] + os.sep + '"' + """<< endl;
    cout << endl;
"""
    return string


def _get_x(phs):
    string = ''
    if phs.simu.exprs.nx > 0:
        string += "\nxVector = " + object_label() + ".get_x();"
        string += "\ndxVector = " + object_label() + ".get_dx();"
        string += "\ndxHVector = " + object_label() + ".get_dxH();"
        string += """
        for (unsigned int i = 0; i < """ + name2dim('x') + """; i++) {
            xFile << xVector[i] << " ";
            dxFile << dxVector[i] << " ";
            dxHFile << dxHVector[i] << " ";
        }"""
    string += """
        xFile << endl;
        dxFile << endl;
        dxHFile << endl;"""
    return string


def _get_w(phs):
    string = ''
    if phs.simu.exprs.nw > 0:
        string += "\nwVector = " + object_label() + ".get_w();"
        string += "\nzVector = " + object_label() + ".get_z();"
        string += """
        for (unsigned int i = 0; i < """ + name2dim('w') + """; i++) {
            wFile << wVector[i] << " ";
            zFile << zVector[i] << " ";
        }"""
    string += """
        wFile << endl;
        zFile << endl;"""
    return string


def _get_y(phs):
    string = ''
    if phs.simu.exprs.nw > 0:
        string += "\nyVector = " + object_label() + ".get_y();"
        string += """
        for (unsigned int i = 0; i < """ + name2dim('y') + """; i++) {
            yFile << yVector[i] << " ";
        }"""
    string += """
        yFile << endl;"""
    return string
# -----------------------------------------------------------------------------


def str_open_file(phs, name):
    """
    return piece of cpp code.
    try to open file 'name.txt' with read access.
    """
    string = """
    ifstream """ + name + """File;
    """ + name + """File.open(""" + '"' + phs.paths['data'] + os.sep + \
        name + """.txt");

    if (""" + name + """File.fail()) {
        cerr << "Failed opening """ + name + """ file" << endl;
        exit(1);
    }
"""
    return string


# -----------------------------------------------------------------------------


def str_initvec(phs, name):
    """
    return piece of cpp code.
    define runtime vectors.
    """
    string = ""
    if getattr(phs.simu.exprs, name2dim(name)) > 0:
        string += """
    vector<double> """ + name + """Vector(""" + name2dim(name) + """);"""
    return string
