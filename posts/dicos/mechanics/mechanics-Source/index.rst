
.. title: Mechanical Source (Source)
.. slug: mechanics-Source
.. date: 2019-04-28 12:31:26.760104
.. tags: mechanics, mathjax
.. category: component
.. type: text

Source of force or velocity imposed between two points.

.. TEASER_END


============================
 Mechanical Source (Source) 
============================


Source of force or velocity imposed between two points.

Power variables
---------------

**flux**: Force :math:`f`   (N)

**effort**: Velocity :math:`v`   (m/s)

Arguments
---------

label : str
    Source label.

nodes : ('P1', 'P2')
    Mechanical points associated with the source with positive flux P1->P2

parameters : keyword arguments
    Component parameter.

+------+--------------------------------------+--------+---------+
| Key  | Description                          | Unit   | Default |
+======+======================================+========+=========+
| type | Source type in {'velocity', 'force'} | string | force   |
+------+--------------------------------------+--------+---------+


Usage
-----

``sourc = Source('sourc', ('P1', 'P2'), type='force')``

Netlist line
------------

``mechanics.source sourc ('P1', 'P2'): type=force;``

Example
-------

>>> # Import dictionary
>>> from pyphs.dictionary import mechanics
>>> # Define component label
>>> label = 'sourc'
>>> # Define component nodes
>>> nodes = ('P1', 'P2')
>>> # Define component parameters
>>> parameters = {'type': 'force',  # Source type in {'velocity', 'force'} (string)
...              }
>>> # Instanciate component
>>> component = mechanics.Source(label, nodes, **parameters)
>>> # Graph dimensions
>>> len(component.nodes)
2
>>> len(component.edges)
1




