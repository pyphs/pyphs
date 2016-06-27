# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 16:01:13 2016

@author: Falaize
"""


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
