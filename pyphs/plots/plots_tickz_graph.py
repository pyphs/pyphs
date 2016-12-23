# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 00:29:41 2016

@author: Falaize
"""

import networkx as nx


def string_script():
    return """
# -*- coding: utf-8 -*-

import networkx as nx

def graph():
    g = nx.MultiDiGraph()
    g.add_nodes_from(['A', 'B'])
    g.add_edge('A', 'B', key='edge1', value=1, label='misc1')
    g.add_edge('B', 'A', key='edge2', value=2, label='misc2')
    return g
    """



def write_tikz():
#    import os
#    fname = os.getcwd() + os.sep + 'mygraph'
#    g = graph()
#    tikz = nx2tikz.dumps_tikz(g)
#    print(tikz)
#    with open(fname, 'w') as f:
#        f.write(tikz)

    import os
    folder = os.getcwd() + os.sep
    label = "graph"
    with open(folder+label+".py", 'w') as f:
        f.write(string_script())
    import subprocess
    string = """
    cd """ + folder + """
    \nnx2tikz --input """+label+""".py --output out --format pdf"""
    p = subprocess.Popen(string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in iter(p.stdout.readline, ''): print(line),

def graph():
    g = nx.MultiDiGraph()
    g.add_nodes_from(['A', 'B'])
    g.add_edge('A', 'B', key='edge1', value=1, label='misc1')
    g.add_edge('B', 'A', key='edge2', value=2, label='misc2')
    return g

def graph2():
    g = nx.DiGraph()
    # nodes
    g.add_node(1, label='$a$', color='yellow', shape='ellipse')
    g.add_node(2, label='$b$', color='blue', fill='orange', shape='circle')
    g.add_node(3, label='$c$', shape='rectangle')
    g.add_node(4, label='$E=mc^2$')
    g.add_node(5, label=r'$\begin{bmatrix} x_1\\ x_2\\ x_3\end{bmatrix}$')
    # edges
    g.add_edge(1, 2, label='$\{p\}$')
    g.add_edge(1, 3, label='$\{a,b\}$', color='purple')
    g.add_edge(3, 4, label=r'$\begin{matrix} x=1\\ y=2\\ z=10 \end{matrix}$')
    g.add_edge(4, 5)
    g.add_edge(5, 4, color='red')
    g.add_edge(2, 2, color='blue')
    g.add_edge(4, 1)
    return g


if __name__ == '__main__':
    write_tikz()
