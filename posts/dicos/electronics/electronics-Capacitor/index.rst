
.. title: Capacitor
.. slug: electronics-Capacitor
.. date: 2019-04-28 12:31:26.752250
.. tags: electronics, mathjax
.. category: component
.. type: text

Linear capacitor.

.. TEASER_END


===========
 Capacitor 
===========


Linear capacitor.

Power variables
---------------

**flux**: Electrical current :math:`i`   (A)

**effort**: Electrical Voltage :math:`v`   (V)

Arguments
---------

label : str
    Capacitor label.

nodes : ('N1', 'N2')
    Capacitor terminals with positive current N1->N2.

parameters : keyword arguments
    Parameters description and default value.

+-----+-------------+------+---------+
| Key | Description | Unit | Default |
+=====+=============+======+=========+
| C   | Capacitance | F    | 1e-9    |
+-----+-------------+------+---------+


Usage
-----

``capa = Capacitor('capa', ('N1', 'N2'), C='1e-9')``

Netlist line
------------

``electronics.capacitor capa ('N1', 'N2'): C=1e-9;``

Example
-------

>>> # Import dictionary
>>> from pyphs.dictionary import electronics
>>> # Define component label
>>> label = 'capa'
>>> # Define component nodes
>>> nodes = ('N1', 'N2')
>>> # Define component parameters
>>> parameters = {'C': '1e-9',  # Capacitance (F)
...              }
>>> # Instanciate component
>>> component = electronics.Capacitor(label, nodes, **parameters)
>>> # Graph dimensions
>>> len(component.nodes)
2
>>> len(component.edges)
1




