
.. title: Mechanical Source (Source)
.. slug: thermics-Source
.. date: 2019-04-28 12:31:26.763072
.. tags: thermics, mathjax
.. category: component
.. type: text

Thermal source, i.e. imposed temperature delta (type='temp') or entropy variation (type='ev') between points.

.. TEASER_END


============================
 Mechanical Source (Source) 
============================


Thermal source, i.e. imposed temperature delta (type='temp') or entropy variation (type='ev') between points.

Power variables
---------------

**flux**: Force :math:`f`   (N)

**effort**: Velocity :math:`v`   (m/s)

Arguments
---------

label : str
    Source label.

nodes : ('T',)
    Thermal point associated with the source with positive flux #->temp. The node label must be the same as the component label.

parameters : keyword arguments
    Component parameter.

+------+----------------------------------------------+--------+-------------+
| Key  | Description                                  | Unit   | Default     |
+======+==============================================+========+=============+
| type | Source type in {'entropyvar', 'temperature'} | string | temperature |
+------+----------------------------------------------+--------+-------------+


Usage
-----

``T = Source('T', ('T',), type='temperature')``

Netlist line
------------

``thermics.source T ('T',): type=temperature;``

Example
-------

>>> # Import dictionary
>>> from pyphs.dictionary import thermics
>>> # Define component label
>>> label = 'T'
>>> # Define component nodes
>>> nodes = ('T',)
>>> # Define component parameters
>>> parameters = {'type': 'temperature',  # Source type in {'entropyvar', 'temperature'} (string)
...              }
>>> # Instanciate component
>>> component = thermics.Source(label, nodes, **parameters)
>>> # Graph dimensions
>>> len(component.nodes)
2
>>> len(component.edges)
1




