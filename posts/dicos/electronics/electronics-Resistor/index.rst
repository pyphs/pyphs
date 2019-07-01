
.. title: Resistor
.. slug: electronics-Resistor
.. date: 2019-04-28 12:31:26.754189
.. tags: electronics, mathjax
.. category: component
.. type: text

Linear resistor.

.. TEASER_END


==========
 Resistor 
==========


Linear resistor.

Power variables
---------------

**flux**: Electrical current :math:`i`   (A)

**effort**: Electrical Voltage :math:`v`   (V)

Arguments
---------

label : str
    Resistor label.

nodes : ('N1', 'N2')
    Resistor terminals with positive current N1->N2.

parameters : keyword arguments
    Parameters description and default value.

+-----+-------------+------+---------+
| Key | Description | Unit | Default |
+=====+=============+======+=========+
| R   | Resistance  | Ohms | 1000.0  |
+-----+-------------+------+---------+


Usage
-----

``resi = Resistor('resi', ('N1', 'N2'), R=1000.0)``

Netlist line
------------

``electronics.resistor resi ('N1', 'N2'): R=1000.0;``

Example
-------

>>> # Import dictionary
>>> from pyphs.dictionary import electronics
>>> # Define component label
>>> label = 'resi'
>>> # Define component nodes
>>> nodes = ('N1', 'N2')
>>> # Define component parameters
>>> parameters = {'R': 1000.0,  # Resistance (Ohms)
...              }
>>> # Instanciate component
>>> component = electronics.Resistor(label, nodes, **parameters)
>>> # Graph dimensions
>>> len(component.nodes)
2
>>> len(component.edges)
1




