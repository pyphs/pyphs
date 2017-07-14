# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 14:31:08 2016

@author: Falaize
"""

from .tools import indent, main_path, SEP, make_executable
from .preamble import str_preamble
from .cmake import cmake_write
import os


def simu2cpp(simu):
    objlabel = simu.nums.label
    path = simu.cpp_path
    src_path = simu.src_path

    # Generate simu.cpp
    filename = os.path.join(src_path, 'simu.cpp')
    _file = open(filename, 'w+')
    _file.write(main(simu, objlabel.upper()))
    _file.close()

    # Generate CMakeLists.txt
    simu.cmakelists_path = cmake_write(objlabel, path)

    # Define bash script
    simu.run_script_path = os.path.join(path, 'run.sh')
    simu.run_script = bash_script_template(path, objlabel.lower(),
                                           simu.config['cmake'])

    # Generate bash script
    f = open(simu.run_script_path, 'w+')
    f.write(simu.run_script)
    f.close()
    make_executable(simu.run_script_path)
    make_executable(simu.cmakelists_path)


def bash_script_template(path, label, cmakepath):
    return """#!/bin/sh

# chg dir to app dir
cd {0}

# CMake Build
{3} . -Bbuild

# Binary Build
{3} --build build -- -j3

# Binary Exec
.{1}bin{1}{2}

        """.format(path,
                   os.path.sep,
                   label, cmakepath)


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
    string = "\nconst unsigned int nt = {0};\n".format(simu.data.config['nt'])
    names = ('u', 'p')
    for name in names:
        dim = getattr(simu.nums, name[0])().shape[0]
        string += "\nvector<double> {0}Vector({1});".format(name, dim)
    string += "\n"
    names = simu.config['files']
    for name in names:
        val = getattr(simu.nums, name)()
        if len(val.shape) == 0:
            dim = 1
        else:
            dim = val.shape[0]
        string += "\nvector<double> {0}Vector({1});".format(name, dim)
    return indent(string)


def _str_open_files(simu):
    """
    return piece of cpp code.
    open files 'u.txt' and 'p.txt'
    """
    string = "\n"
    names = ('u', 'p')
    for name in names:
        string += r"""
    ifstream {0}File;
    {0}File.open("{1}{2}data{2}{0}.txt");

    if ({0}File.fail()) """.format(name, main_path(simu), SEP)
        string += "{" + """
        cerr << "Failed opening {0} file" << endl;
        exit(1);""".format(name) + "}"
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
        for (unsigned int i=0; i<{0}; i++) """.format(dimu)
            string += """{
            uFile >> uVector[i];
        }"""
        if dimp > 0:
            string += """\n
        // Get parameters data
        for (unsigned int i=0; i<{0}; i++)""".format(dimp) + """ {
            pFile >> pVector[i];
        }"""
    return string


# -----------------------------------------------------------------------------


def _init_file(simu, name):
    """
    open files for saving data
    """
    string = """
    ofstream {0}File;
    {0}File.open("{1}{2}data{2}{0}.txt");""".format(name, main_path(simu), SEP)
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
    string = ""
    string += """\n
    // Instance of Py numerical core
    {0} {1};""".format(objlabel.upper(), objlabel.lower())
    return string


# -----------------------------------------------------------------------------


def _str_process(simu, objlabel):
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
            std::cout << "] " << int(progress * 100.0) << "% done, ETA: " \
<< ETAm << "m" << ETAs << "s\\r" << endl ;
            std::cout.flush();
        }"""
    string += """\n
        // Update Input
        """ + objlabel.lower() + """.set_u(uVector);

        // Update Parameters
        """ + objlabel.lower() + """.set_p(pVector);

        // Process update
        """ + objlabel.lower() + """.update();\n\n        // Get quantities"""
    string += indent(indent(_gets(simu, objlabel)))
    string += "\n    }"
    string += '\n    uFile.close();'
    string += '\n    pFile.close();'
    string += indent(_close(simu))
    string += """
    cout << endl;
    cout << "Data written at" << endl;
    cout << endl;
    cout << "{0}{1}data{1}"<< endl;
    cout << endl;
""".format(main_path(simu), SEP)
    return string


def _gets(simu, objlabel):
    string = ''
    names = simu.config['files']
    for name in names:
        val = getattr(simu.nums, name)()
        if len(val.shape) == 0:
            dim = 1
        else:
            dim = val.shape[0]
        string += ("\n\n{0}Vector = ".format(name)) + \
            objlabel.lower() + (".{0}_vector();".format(name))
        string += """
for (unsigned int i = 0; i<{0}; i++)""".format(dim) + "{" + """
    {0}File << {0}Vector[i] << " ";""".format(name) + "\n}"
        string += "\n{0}File << endl;\n".format(name)
    return string


def _close(simu):
    string = ''
    names = simu.config['files']
    for name in names:
        string += "\n{0}File.close();".format(name)
    return string
