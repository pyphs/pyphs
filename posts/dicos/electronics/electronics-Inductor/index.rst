
.. title: Inductor
.. slug: electronics-Inductor
.. date: 2019-04-28 12:31:26.753183
.. tags: electronics, mathjax
.. category: component
.. type: text

Linear inductor.

.. TEASER_END


==========
 Inductor 
==========


Linear inductor.

Power variables
---------------

**flux**: Electrical current :math:`i`   (A)

**effort**: Electrical Voltage :math:`v`   (V)

Arguments
---------

label : str
    Inductor label.

nodes : ('N1', 'N2')
    Inductor terminals with positive current N1->N2.

parameters : keyword arguments
    Parameters description and default value.

+-----+-------------+------+---------+
| Key | Description | Unit | Default |
+=====+=============+======+=========+
| L   | Inductance  | H    | 1e-3    |
+-----+-------------+------+---------+


Usage
-----

``induc = Inductor('induc', ('N1', 'N2'), L='1e-3')``

Netlist line
------------

``electronics.inductor induc ('N1', 'N2'): L=1e-3;``

Example
-------

>>> # Import dictionary
>>> from pyphs.dictionary import electronics
>>> # Define component label
>>> label = 'induc'
>>> # Define component nodes
>>> nodes = ('N1', 'N2')
>>> # Define component parameters
>>> parameters = {'L': '1e-3',  # Inductance (H)
...              }
>>> # Instanciate component
>>> component = electronics.Inductor(label, nodes, **parameters)
>>> # Graph dimensions
>>> len(component.nodes)
2
>>> len(component.edges)
1




