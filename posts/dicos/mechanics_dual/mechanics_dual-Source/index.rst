
.. title: Mechanical Source (Source)
.. slug: mechanics_dual-Source
.. date: 2019-04-28 12:31:26.766070
.. tags: mechanics_dual, mathjax
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

**flux**: Velocity :math:`v`   (m/s)

**effort**: Force :math:`f`   (N)

Arguments
---------

label : str
    Source label.

nodes : ('N1', 'N2')
    Nodes associated with the component terminals with positive flux N1->N2.

parameters : keyword arguments
    Component parameter.

+------+--------------------------------------+--------+---------+
| Key  | Description                          | Unit   | Default |
+======+======================================+========+=========+
| type | Source type in {'velocity', 'force'} | string | force   |
+------+--------------------------------------+--------+---------+


Usage
-----

``sourc = Source('sourc', ('N1', 'N2'), type='force')``

Netlist line
------------

``mechanics_dual.source sourc ('N1', 'N2'): type=force;``

Example
-------

>>> # Import dictionary
>>> from pyphs.dictionary import mechanics_dual
>>> # Define component label
>>> label = 'sourc'
>>> # Define component nodes
>>> nodes = ('N1', 'N2')
>>> # Define component parameters
>>> parameters = {'type': 'force',  # Source type in {'velocity', 'force'} (string)
...              }
>>> # Instanciate component
>>> component = mechanics_dual.Source(label, nodes, **parameters)
>>> # Graph dimensions
>>> len(component.nodes)
2
>>> len(component.edges)
1




