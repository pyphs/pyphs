# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 14:31:08 2016

@author: Falaize
"""

from pyphs.cpp.numcore2cpp import numcore2cpp
from tools import indent
from preamble import str_preamble
import os


def simu2cpp(simu, objlabel=None):
    if objlabel is None:
        objlabel = 'core'.upper()
    path = simu.config['path'] + os.sep + 'cpp'
    if not os.path.exists(path):
        os.mkdir(path)
    numcore2cpp(simu.nums, objlabel=objlabel, path=path,
                eigen_path=simu.config['eigen_path'])
    filename = path + os.sep + 'main.cpp'
    _file = open(filename, 'w')
    _file.write(main(simu, objlabel))
    _file.close()


def main(simu, objlabel):
    string = ""
    string += str_preamble(objlabel)
    string += _str_includes()
    string += _str_namespaces()
    string += _str_timer()
    string += "\n\n\nint main() {"
    string += _str_body(simu, objlabel)
    string += "\n    return 0;\n}\n"
    return string


# -----------------------------------------------------------------------------


def _str_body(simu, objlabel):
    """
    return piece of cpp code.
    collects body pieces for main.cpp
    """
    string = ""
    string += _str_initvecs(simu)
    string += _str_open_files(simu)
    string += _str_instanciate(simu, objlabel)
    string += """\n\n    int barWidth = 20;
    int ETA, ETAm, ETAs;
    float progress = 0.0;
    timer t;"""
    string += _str_process(simu, objlabel)
    return string


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

#include "core.h"
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


def _str_initvecs(simu):
    string = "\nconst unsigned int nt = %i;\n" % simu.data.config['nt']
    names = ('x0', 'u', 'p')
    for name in names:
        dim = getattr(simu.nums, name[0])().shape[0]
        string += "\nvector<double> %sVector(%i);" % (name, dim)
    string += "\n"
    names = simu.config['files_to_save']
    for name in names:
        dim = getattr(simu.nums, name)().shape[0]
        string += "\nvector<double> %sVector(%i);" % (name, dim)
    return indent(string)


def _str_open_files(simu):
    """
    return piece of cpp code.
    open files 'x0.txt', 'u.txt' and 'p.txt'
    """
    string = "\n"
    names = ('x0', 'u', 'p')
    for name in names:
        string += """
    ifstream %sFile;
    %sFile.open("%s%sdata%s%s.txt");

    if (%sFile.fail()) {
        cerr << "Failed opening %s file" << endl;
        exit(1);
    }
""" % (name, name, simu.config['path'], os.sep, os.sep, name, name, name)
    return string


def _str_readx0():
    string = """\n
    for (unsigned int i=0; i<nx; i++) {
        x0File >> x0Vector[i];
    }"""
    return string


def _str_readdata(simu):
    string = ""
    dimu = simu.nums.u().shape[0]
    dimp = simu.nums.p().shape[0]
    if dimu + dimp > 0:
        string = ""
        if dimu > 0:
            string += """\n
        // Get input data
        for (unsigned int i=0; i<%i; i++) {
            uFile >> uVector[i];
        }""" % dimu
        if dimp > 0:
            string += """\n
        // Get parameters data
        for (unsigned int i=0; i<%i; i++) {
            pFile >> pVector[i];
        }""" % dimp
    return string


# -----------------------------------------------------------------------------


def _init_file(simu, name):
    """
    open files for saving data
    """
    string = """
    ofstream """ + name + """File;
    """ + name + """File.open(""" + '"' + simu.config['path'] + os.sep + \
        'data' + os.sep + name + """.txt");"""
    return string


# -----------------------------------------------------------------------------


def _init_files(phs):
    string = ""
    names = ('x', 'dx', 'dxH', 'w', 'z', 'y')
    for name in names:
        string += _init_file(phs, name)
    return string


# -----------------------------------------------------------------------------


def _str_instanciate(simu, objlabel):
    string = """\n
    // Get init data
    for (unsigned int i=0; i<%i; i++) {
        x0File >> x0Vector[i];
    }

    // Instance of PyPHS numerical core
    %s %s(x0Vector);""" % (simu.nums.x().shape[0],
                           objlabel.upper(), objlabel.lower())
    return string


# -----------------------------------------------------------------------------


def _str_process(simu, objlabel):
    dimu = getattr(simu.method.core.dims, 'y')()
    dimp = getattr(simu.method.core.dims, 'p')()
    string = """\n
    // Process
    t.start();\n"""
    string += _init_files(simu)
    string += """\n\n
    for (unsigned int n = 0; n < nt; n++) {\n""" + _str_readdata(simu) + """
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
    string += """\n
        // Process update
        """ + objlabel.lower() + """.update("""
    string += "uVector"
    string += ', '
    string += "pVector"
    string += ");\n\n        // Get quantities"
    string += indent(indent(_gets(simu, objlabel)))
    string += "\n    }"
    string += '\n    uFile.close();'
    string += '\n    pFile.close();'
    string += indent(_close(simu)) + """\n
    cout << endl;
    cout << "Data written at" << endl;
    cout << endl;
    cout << """ + '"' + simu.config['path'] + os.sep + '"' + """<< endl;
    cout << endl;
"""
    return string


def _gets(simu, objlabel):
    string = ''
    names = simu.config['files_to_save']
    for name in names:
        dim = getattr(simu.nums, name)().shape[0]
        string += ("\n\n%sVector = " % name) + \
            objlabel.lower() + (".%s_vector();" % name)
        string += """
for (unsigned int i = 0; i<%i; i++) {
    %sFile << %sVector[i] << " ";
}""" % (dim, name, name)
        string += "\n%sFile << endl;\n" % name
    return string


def _close(simu):
    string = ''
    names = simu.config['files_to_save']
    for name in names:
        dim = getattr(simu.nums, name)().shape[0]
        string += "\n%sFile.close();" % name
    return string


if __name__ == '__main__':
    simu2cpp(simu, objlabel)