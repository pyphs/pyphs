
from .netlists import Netlist
from .graph import Graph, datum

__all__ = ['Netlist', 'Graph', 'datum']


def netlist2graph(netlist):
    if not isinstance(netlist, Netlist):
        netlist = Netlist(netlist)
    return Graph(netlist=netlist)


def netlist2core(netlist):
    return netlist2graph(netlist).buildCore()
