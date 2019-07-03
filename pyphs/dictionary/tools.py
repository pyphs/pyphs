# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 18:57:18 2016

@author: Falaize
"""
from __future__ import absolute_import, division, print_function

from ..core.core import Core
from ..core.tools import types

symbols = Core.symbols


def parametersTable(parameters):
    """
    Return table of parameters as a restructured-text table.
    """
    from pyphs.misc.rst import rstTable
    header = ['Key', 'Description', 'Unit', 'Default']
    return rstTable(header, parameters)


def parametersDicFull(parameters):
    """
    Build a dictionary from list of parameters.
    """
    dic = {}
    for p in parameters:
        dic[p[0]] = {'description': p[1],
                     'unit': p[2],
                     'default': p[3]}
    return dic


def parametersDefault(pars):
    """
    Build a dictionary of defaults values from list of parameters.
    """
    dic = {}
    for p in pars:
        dic[p[0]] = p[3]
    return dic


doc_template = """
$title

$desc

Power variables
---------------

**flux**: $flux

**effort**: $effort

Arguments
---------

label : str
    $component label.

nodes : $nodes
    $nodesdesc

parameters : keyword arguments
    $parametersdesc

$parameterstable

Usage
-----

``$label = $component('$label', $nodes, $usepars)``

Netlist line
------------

``$dico.$linecomponent $label $nodes: $linepars``

Example
-------

>>> # Import dictionary
>>> from pyphs.dictionary import $dico
>>> # Define component label
>>> label = '$label'
>>> # Define component nodes
>>> nodes = $nodes
>>> # Define component parameters
>>> parameters = {$expars
...              }
>>> # Instanciate component
>>> component = $dico.$component(label, nodes, **parameters)
>>> # Graph dimensions
>>> len(component.nodes)
$nnodes
>>> len(component.edges)
$nedges

$references

"""

def componentDoc(metadata):
    """
    Build the documentation for a component of pyphs.dictionary.
    """

    from pyphs.misc.rst import title, indent

    metadata.setdefault('parametersdesc',
                        'Parameters description and default value.')

    pars = parametersDefault(metadata['parameters'])

    refs = metadata['refs']

    def refline(i, ref):
        return '\n.. [{}] {}\n'.format(i, ref)

    if len(refs) > 1:
        references = title('References', 3)
        for i in refs:
            references += refline(i, refs[i])
    elif len(refs) > 0:
        references = title('Reference', 3)
        references += refline(1, refs[1])
    else:
        references = ''

    temp = [(k, d, u, "'" + v + "'" if isinstance(v, str) else str(v)) for (k, d, u, v) in metadata['parameters']]
    blanks = [len(str(v) + str(k)) for (k, d, u, v) in temp]
    bmax = max(blanks) + 2
    for i, b in enumerate(blanks):
        blanks[i] = bmax - b
    expars = ('\n... ' + 14*' ').join(["'{0}': {1},{4}# {2} ({3})".format(k, v, d, u, b*' ') for ((k, d, u, v), b) in zip(temp, blanks)])
    realtitle = metadata['title'] if metadata['component'] == metadata['title'] else '{} ({})'.format(metadata['title'], metadata['component'])
    subs = {'title': title(realtitle, 0),
            'label': metadata['label'],
            'dico': metadata['dico'],
            'component': metadata['component'],
            'desc': metadata['desc'],
            'nodes': metadata['nodes'],
            'flux': '{1} :math:`{0}`   ({2})'.format(*metadata['flux']),
            'effort': '{1} :math:`{0}`   ({2})'.format(*metadata['effort']),
            'nodesdesc': metadata['nodesdesc'],
            'parameterstable': parametersTable(metadata['parameters']),
            'parametersdesc': metadata['parametersdesc'],
            'expars': expars,
            'usepars': ', '.join(['{}={}'.format(k, "'" + v + "'" if isinstance(v, str) else str(v)) for (k, v) in zip(pars.keys(), pars.values())]),
            'linepars': '; '.join(['{}={}'.format(k, v) for (k, v) in zip(pars.keys(), pars.values())]) + ';',
            'references': references
            }
    for k in ['nnodes', 'nedges']:
        subs[k] = metadata[k]

    subs['linecomponent'] = subs['component'].lower()

    import string
    template = string.Template(doc_template)
    return template.substitute(subs)


class Argument:

    def __init__(self, name, obj):
        self.symb, self.sub, self.par = form(name, obj)


def form(name, obj):
    """
    Pyphs formating of argument format 'obj' to a symbol

    Parameters
    ----------
    argname : str
    argobj : {str, float, (str, float)}

    Outputs
    -------
    symb : Core.symbol
    subs : Core.subs
    """
    if isinstance(obj, tuple):
        if not isinstance(obj[0], str):
            raise TypeError('For tupple parameter, \
first element should be a str, got {0}'.format(type(obj[0])))
        try:
            if not isinstance(obj[1], types.scalar_types):
                raise TypeError('For tupple parameter, \
second element should be numeric, got \
{0}'.format(type(obj[1])))
        except AssertionError:
            types.scalar_test(obj[1])
        string = obj[0]
        symb = Core.symbols(string)
        sub = {symb: obj[1]}
        par = None
    elif isinstance(obj, (float, int)):
        string = name
        symb = Core.symbols(string)
        sub = {symb: obj}
        par = None
    elif isinstance(obj, str):
        string = obj
        symb = Core.symbols(string)
        sub = {}
        par = symb
    else:
        types.scalar_test(obj)
        string = name
        symb = Core.symbols(string)
        sub = {symb: obj}
        par = None

    return symb, sub, par


def mappars(graph, **kwargs):
    """
    map dictionary of 'par':('label', value) to dictionary of substitutions \
for parameters in component expression 'dicpars' and for parameters in phs \
'subs'.
    """
    dicpars = {}
    subs = {}
    for key in kwargs.keys():
        symb, sub, par = form(graph.label + '_' + str(key), kwargs[key])
        dicpars.update({Core.symbols(key): symb})
        subs.update(sub)
        if par is not None:
            graph.core.add_parameters(par)
    return dicpars, subs


def nicevarlabel(var, label):
    """
    return a formated string eg. xcapa if 'var' is 'x' and label is 'capa'.
    """
    return var + label


dicdocTemplate = """
.. title: $title
.. slug: $slug
.. date: $date
.. tags: $dico, mathjax
.. category: component
.. type: text

$desc

.. TEASER_END

$doc
"""

dicindexTemplate = """
.. title: Index - $dico
.. slug: $dico-index
.. date: $date
.. tags: $dico, mathjax
.. category: index
.. type: text

Index of sub-dictionary **$dico**.

.. TEASER_END

$content
"""


def generateDicDoc(folder):
    from pyphs import dictionary
    import string
    import os
    import datetime
    import shutil

    for d in dictionary.__all__:
        if not d == 'path_to_dictionary':
            comps = dict()
            titles = dict()
            dic = getattr(dictionary, d)
            if os.path.exists(os.path.join(folder, d)):
                shutil.rmtree(os.path.join(folder, d))
            os.mkdir(os.path.join(folder, d))
            dcomps = dic.__all__
            dcomps.sort()
            for c in dcomps:
                comp = getattr(dic, c)
                realtitle = comp.metadata['title'] if comp.metadata['component'] == comp.metadata['title'] else '{} ({})'.format(comp.metadata['title'], comp.metadata['component'])
                comps[c] = '{}-{}'.format(d, c)
                titles[c] = realtitle
                temp = string.Template(dicdocTemplate)
                subs = {'title': realtitle,
                        'dico': d,
                        'desc': comp.metadata['desc'],
                        'component': c,
                        'slug': comps[c],
                        'date': datetime.datetime.now(),
                        'doc': comp.__doc__}
                with open(os.path.join(folder, comp.metadata['dico'], comp.metadata['component']+'.rst'), 'w') as f:
                    for l in temp.substitute(subs).splitlines():
                        f.write('{}\n'.format(l))

            content = '\n'.join(['- `{0} </posts/dicos/{1}/{2}>`_'.format(titles[c], d, comps[c]) for c in comps])
            subs = {'content': content,
                    'dico': d,
                    'date': datetime.datetime.now(),
                    }

            with open(os.path.join(folder, comp.metadata['dico'], 'index.rst'), 'w') as f:
                temp = string.Template(dicindexTemplate)
                for l in temp.substitute(subs).splitlines():
                    f.write(l + '\n')
