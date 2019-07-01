
.. title: Stiffness
.. slug: mechanics_dual-Stiffness
.. date: 2019-04-28 12:31:26.767062
.. tags: mechanics_dual, mathjax
.. category: component
.. type: text

Linear stiffness between two points in a 1D space. In Laplace domain with :math:`s\in\mathbb C`:

.. math::

    e(s) = \frac{K\,f(s)}{s}.



.. TEASER_END


===========
 Stiffness 
===========


Linear stiffness between two points in a 1D space. In Laplace domain with :math:`s\in\mathbb C`:

.. math::

    e(s) = \frac{K\,f(s)}{s}.



Power variables
---------------

**flux**: Velocity :math:`v`   (m/s)

**effort**: Force :math:`f`   (N)

Arguments
---------

label : str
    Stiffness label.

nodes : ('N1', 'N2')
    Nodes associated with the component terminals with positive flux N1->N2.

parameters : keyword arguments
    Component parameter.

+-----+----------------------+------+---------+
| Key | Description          | Unit | Default |
+=====+======================+======+=========+
| K   | Mechanical stiffness | N/m  | 1000.0  |
+-----+----------------------+------+---------+


Usage
-----

``stiff = Stiffness('stiff', ('N1', 'N2'), K=1000.0)``

Netlist line
------------

``mechanics_dual.stiffness stiff ('N1', 'N2'): K=1000.0;``

Example
-------

>>> # Import dictionary
>>> from pyphs.dictionary import mechanics_dual
>>> # Define component label
>>> label = 'stiff'
>>> # Define component nodes
>>> nodes = ('N1', 'N2')
>>> # Define component parameters
>>> parameters = {'K': 1000.0,  # Mechanical stiffness (N/m)
...              }
>>> # Instanciate component
>>> component = mechanics_dual.Stiffness(label, nodes, **parameters)
>>> # Graph dimensions
>>> len(component.nodes)
2
>>> len(component.edges)
1




