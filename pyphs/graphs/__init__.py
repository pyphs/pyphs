
from .netlists import PHSNetlist
from .graph import PHSGraph, datum

__all__ = ['PHSNetlist', 'PHSGraph', 'datum']


def netlist2graph(netlist):
    if not isinstance(netlist, PHSNetlist):
        netlist = PHSNetlist(netlist)
    return PHSGraph(netlist=netlist)


def netlist2core(netlist):
    return netlist2graph(netlist).buildCore()
