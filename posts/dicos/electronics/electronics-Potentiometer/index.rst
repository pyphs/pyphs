
.. title: Potentiometer
.. slug: electronics-Potentiometer
.. date: 2019-04-28 12:31:26.753675
.. tags: electronics, mathjax
.. category: component
.. type: text

Potentiometer, i.e. two connected resistors with inverse varying resistance.

.. TEASER_END


===============
 Potentiometer 
===============


Potentiometer, i.e. two connected resistors with inverse varying resistance.

Power variables
---------------

**flux**: Electrical current :math:`i`   (A)

**effort**: Electrical Voltage :math:`v`   (V)

Arguments
---------

label : str
    Potentiometer label.

nodes : ('N1', 'N2', 'N3')
    Resitances are: :math:`R_{12}=1 + R\,A^E` and :math:`R_{23}=1 + R\,(1-A^E)`.

parameters : keyword arguments
    Parameters description and default value.

+-----+---------------------+--------+----------+
| Key | Description         | Unit   | Default  |
+=====+=====================+========+==========+
| R   | Total resistance    | Ohms   | 100000.0 |
+-----+---------------------+--------+----------+
| A   | Label for parameter | string | alpha    |
+-----+---------------------+--------+----------+
| E   | Exponent            | d.u.   | 1.0      |
+-----+---------------------+--------+----------+


Usage
-----

``pot = Potentiometer('pot', ('N1', 'N2', 'N3'), R=100000.0, A='alpha', E=1.0)``

Netlist line
------------

``electronics.potentiometer pot ('N1', 'N2', 'N3'): R=100000.0; A=alpha; E=1.0;``

Example
-------

>>> # Import dictionary
>>> from pyphs.dictionary import electronics
>>> # Define component label
>>> label = 'pot'
>>> # Define component nodes
>>> nodes = ('N1', 'N2', 'N3')
>>> # Define component parameters
>>> parameters = {'R': 100000.0,  # Total resistance (Ohms)
...               'A': 'alpha',   # Label for parameter (string)
...               'E': 1.0,       # Exponent (d.u.)
...              }
>>> # Instanciate component
>>> component = electronics.Potentiometer(label, nodes, **parameters)
>>> # Graph dimensions
>>> len(component.nodes)
3
>>> len(component.edges)
2




