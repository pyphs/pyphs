
.. title: Electrical source (Source)
.. slug: electronics-Source
.. date: 2019-04-28 12:31:26.754585
.. tags: electronics, mathjax
.. category: component
.. type: text

Controlled voltage or current source.

.. TEASER_END


============================
 Electrical source (Source) 
============================


Controlled voltage or current source.

Power variables
---------------

**flux**: Electrical current :math:`i`   (A)

**effort**: Electrical Voltage :math:`v`   (V)

Arguments
---------

label : str
    Source label.

nodes : ('N1', 'N2')
    source terminals with positive current N1->N2.

parameters : keyword arguments
    Parameters description and default value.

+------+---------------------------------------+--------+---------+
| Key  | Description                           | Unit   | Default |
+======+=======================================+========+=========+
| type | Source type in {'voltage', 'current'} | string | voltage |
+------+---------------------------------------+--------+---------+


Usage
-----

``sourc = Source('sourc', ('N1', 'N2'), type='voltage')``

Netlist line
------------

``electronics.source sourc ('N1', 'N2'): type=voltage;``

Example
-------

>>> # Import dictionary
>>> from pyphs.dictionary import electronics
>>> # Define component label
>>> label = 'sourc'
>>> # Define component nodes
>>> nodes = ('N1', 'N2')
>>> # Define component parameters
>>> parameters = {'type': 'voltage',  # Source type in {'voltage', 'current'} (string)
...              }
>>> # Instanciate component
>>> component = electronics.Source(label, nodes, **parameters)
>>> # Graph dimensions
>>> len(component.nodes)
2
>>> len(component.edges)
1




