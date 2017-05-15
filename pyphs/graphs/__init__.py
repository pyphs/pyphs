
from .netlists import PHSNetlist
from .graph import PHSGraph, datum

__all__ = ['PHSNetlist', 'PHSGraph', 'datum']


def netlist2core(netlist):
    if not isinstance(netlist, PHSNetlist):
        netlist = PHSNetlist(netlist)
    graph = PHSGraph(netlist=netlist)
    return graph.buildCore()
