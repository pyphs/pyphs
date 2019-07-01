
.. title: Mass
.. slug: mechanics_dual-Mass
.. date: 2019-04-28 12:31:26.765706
.. tags: mechanics_dual, mathjax
.. category: component
.. type: text

Mass moving in 1D space. In Laplace domain with :math:`s\in\mathbb C`:

.. math::

    f(s) = \frac{e(s)}{M\,s}.



.. TEASER_END


======
 Mass 
======


Mass moving in 1D space. In Laplace domain with :math:`s\in\mathbb C`:

.. math::

    f(s) = \frac{e(s)}{M\,s}.



Power variables
---------------

**flux**: Velocity :math:`v`   (m/s)

**effort**: Force :math:`f`   (N)

Arguments
---------

label : str
    Mass label.

nodes : ('N1', 'N2')
    Nodes associated with the component terminals with positive flux N1->N2.

parameters : keyword arguments
    Component parameter.

+-----+-----------------+------+---------+
| Key | Description     | Unit | Default |
+=====+=================+======+=========+
| M   | Mechanical mass | kg   | 0.01    |
+-----+-----------------+------+---------+


Usage
-----

``mass = Mass('mass', ('N1', 'N2'), M=0.01)``

Netlist line
------------

``mechanics_dual.mass mass ('N1', 'N2'): M=0.01;``

Example
-------

>>> # Import dictionary
>>> from pyphs.dictionary import mechanics_dual
>>> # Define component label
>>> label = 'mass'
>>> # Define component nodes
>>> nodes = ('N1', 'N2')
>>> # Define component parameters
>>> parameters = {'M': 0.01,  # Mechanical mass (kg)
...              }
>>> # Instanciate component
>>> component = mechanics_dual.Mass(label, nodes, **parameters)
>>> # Graph dimensions
>>> len(component.nodes)
2
>>> len(component.edges)
1




