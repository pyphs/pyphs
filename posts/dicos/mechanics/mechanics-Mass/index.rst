
.. title: Mass
.. slug: mechanics-Mass
.. date: 2019-04-28 12:31:26.759785
.. tags: mechanics, mathjax
.. category: component
.. type: text

Mass moving in 1D space. In Laplace domain with :math:`s\in\mathbb C`:

.. math::

    e(s) = \frac{f(s)}{M\,s}.



.. TEASER_END


======
 Mass 
======


Mass moving in 1D space. In Laplace domain with :math:`s\in\mathbb C`:

.. math::

    e(s) = \frac{f(s)}{M\,s}.



Power variables
---------------

**flux**: Force :math:`f`   (N)

**effort**: Velocity :math:`v`   (m/s)

Arguments
---------

label : str
    Mass label.

nodes : ('P',)
    Mechanical point associated with the mass. The velocity is measured from a reference point with edge datum->P.

parameters : keyword arguments
    Component parameter.

+-----+-----------------+------+---------+
| Key | Description     | Unit | Default |
+=====+=================+======+=========+
| M   | Mechanical mass | kg   | 0.01    |
+-----+-----------------+------+---------+


Usage
-----

``mass = Mass('mass', ('P',), M=0.01)``

Netlist line
------------

``mechanics.mass mass ('P',): M=0.01;``

Example
-------

>>> # Import dictionary
>>> from pyphs.dictionary import mechanics
>>> # Define component label
>>> label = 'mass'
>>> # Define component nodes
>>> nodes = ('P',)
>>> # Define component parameters
>>> parameters = {'M': 0.01,  # Mechanical mass (kg)
...              }
>>> # Instanciate component
>>> component = mechanics.Mass(label, nodes, **parameters)
>>> # Graph dimensions
>>> len(component.nodes)
2
>>> len(component.edges)
1




