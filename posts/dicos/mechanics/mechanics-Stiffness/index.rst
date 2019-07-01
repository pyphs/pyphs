
.. title: Stiffness
.. slug: mechanics-Stiffness
.. date: 2019-04-28 12:31:26.761412
.. tags: mechanics, mathjax
.. category: component
.. type: text

Linear stiffness between two points in a 1D space. In Laplace domain with :math:`s\in\mathbb C`:

.. math::

    f(s) = \frac{K\,e(s)}{s}.



.. TEASER_END


===========
 Stiffness 
===========


Linear stiffness between two points in a 1D space. In Laplace domain with :math:`s\in\mathbb C`:

.. math::

    f(s) = \frac{K\,e(s)}{s}.



Power variables
---------------

**flux**: Force :math:`f`   (N)

**effort**: Velocity :math:`v`   (m/s)

Arguments
---------

label : str
    Stiffness label.

nodes : ('P1', 'P2')
    Mechanical points associated with the stiffness endpoints with positive flux P1->P2.

parameters : keyword arguments
    Component parameter.

+-----+----------------------+------+---------+
| Key | Description          | Unit | Default |
+=====+======================+======+=========+
| K   | Mechanical stiffness | N/m  | 1000.0  |
+-----+----------------------+------+---------+


Usage
-----

``stiff = Stiffness('stiff', ('P1', 'P2'), K=1000.0)``

Netlist line
------------

``mechanics.stiffness stiff ('P1', 'P2'): K=1000.0;``

Example
-------

>>> # Import dictionary
>>> from pyphs.dictionary import mechanics
>>> # Define component label
>>> label = 'stiff'
>>> # Define component nodes
>>> nodes = ('P1', 'P2')
>>> # Define component parameters
>>> parameters = {'K': 1000.0,  # Mechanical stiffness (N/m)
...              }
>>> # Instanciate component
>>> component = mechanics.Stiffness(label, nodes, **parameters)
>>> # Graph dimensions
>>> len(component.nodes)
2
>>> len(component.edges)
1




