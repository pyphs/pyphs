# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 14:31:08 2016

@author: Falaize
"""

from .tools import indent, main_path, SEP, make_executable, linesplit, comment
from .cmake import cmake_write
import os
from pyphs.config import CONFIG_CPP
import string
from pyphs.misc.tools import get_time, geteval
import pyphs

def simu2cpp(simu):
    objlabel = simu.label
    path = simu.cpp_path
    src_path = simu.src_path

    filename = os.path.join(src_path, 'simu.cpp')

    from pyphs import path_to_templates

    # read license template
    with open(os.path.join(path_to_templates,
                           'license.template'), 'r') as f:
        _license = string.Template(f.read())

    # substitutions for templates
    subs = dict()
    subs['license'] = comment(_license.substitute({
        'time': get_time(),
        'url_pyphs': pyphs.__url__}))
    subs['vectors'] = _str_vectors(simu)
    subs['nt'] = simu.data.nt
    subs['dim'] = simu.data.dim
    subs['h5path'] = simu.data.h5path
    subs['dname'] = simu.data.dname
    subs['labelUp'] = objlabel.upper()
    subs['labelLow'] = objlabel.lower()
    subs['updateInputs'] = _str_updateInputs(simu, objlabel)
    subs['updateResults'] = _str_updateResults(simu, objlabel)
    subs['pbar'] = int(simu.config['pbar'])

    with open(os.path.join(path_to_templates, 'cpp',
                           'simu_main.template'), 'r') as f:
        _main = string.Template(f.read())

    # Generate simu.cpp
    with open(filename, 'w+') as _file:
        _file.write(_main.substitute(subs))

    # Generate CMakeLists.txt
    simu.cmakelists_path = cmake_write(objlabel, path)

    # Define bash script
    simu.run_script_path = os.path.join(path, 'run.sh')
    with open(os.path.join(path_to_templates, 'cpp',
                           'simu_bash.template'), 'r') as f:
        _bash = string.Template(f.read())

    # Generate bash script
    subs['license'] = comment(
        _license.substitute({
            'time': get_time(),
            'url_pyphs': pyphs.__url__
        }),
        '#')
    subs['folder'] = path
    subs['cmakepath'] = simu.config['cmake']
    subs['sep'] = os.path.sep

    bash_script = _bash.substitute(subs)
    with open(simu.run_script_path, 'w+') as _file:
        _file.write(_bash.substitute(subs))

    simu.run_script = bash_script

    make_executable(simu.run_script_path)
    make_executable(simu.cmakelists_path)


# -----------------------------------------------------------------------------


def _str_vectors(simu):
    vectors = str()
    for name in simu.data.names:
        dim = len(geteval(simu.method, name))
        if dim > 0:
            temp = name, dim, CONFIG_CPP['float']
            vectors += "\n    {2} {0}[{1}];".format(*temp)
    return indent(vectors)


def _str_updateInputs(simu, objlabel):
    updateInputs = str()
    for name in ['u', 'p']:
        dim = len(geteval(simu.method, name))
        if dim > 0:
            temp = objlabel.lower(), name, CONFIG_CPP['float'], dim
            updateInputs += "\n{0}.set_{1}((Matrix<double, {3}, 1> &)mystruct.{1});".format(*temp)
    return indent(indent(updateInputs))


def _str_updateResults(simu, objlabel):
    updateResults = str()
    for name in simu.data.names[2:]:
        dim = len(geteval(simu.method, name))
        if dim > 0:
            temp = {'dim':dim,
                    'obj': objlabel.lower(),
                    'name': name
                    }
            updateResults += """
for (unsigned int ind=0; ind<{dim}; ind++)""".format(**temp) + "{" + """
    mystruct.{name}[ind] = {obj}.{name}_vector()[ind];
""".format(**temp) + "}"
    return indent(indent(updateResults))
