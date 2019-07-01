
.. title: Linear Damper (Damper)
.. slug: mechanics-Damper
.. date: 2019-04-28 12:31:26.758936
.. tags: mechanics, mathjax
.. category: component
.. type: text

Linear mechanical damping (i.e. opposing force proportional to the velocity). In Laplace domain with :math:`s\in\mathbb C`:

.. math::

    f(s) = A \, e(s).



.. TEASER_END


========================
 Linear Damper (Damper) 
========================


Linear mechanical damping (i.e. opposing force proportional to the velocity). In Laplace domain with :math:`s\in\mathbb C`:

.. math::

    f(s) = A \, e(s).



Power variables
---------------

**flux**: Force :math:`f`   (N)

**effort**: Velocity :math:`v`   (m/s)

Arguments
---------

label : str
    Damper label.

nodes : ('P1', 'P2')
    Mechanical points associated with the damper endpoints with positive flux N1->N2.

parameters : keyword arguments
    Component parameter

+-----+---------------------+-------+---------+
| Key | Description         | Unit  | Default |
+=====+=====================+=======+=========+
| A   | Damping coefficient | N.s/m | 1.0     |
+-----+---------------------+-------+---------+


Usage
-----

``damp = Damper('damp', ('P1', 'P2'), A=1.0)``

Netlist line
------------

``mechanics.damper damp ('P1', 'P2'): A=1.0;``

Example
-------

>>> # Import dictionary
>>> from pyphs.dictionary import mechanics
>>> # Define component label
>>> label = 'damp'
>>> # Define component nodes
>>> nodes = ('P1', 'P2')
>>> # Define component parameters
>>> parameters = {'A': 1.0,  # Damping coefficient (N.s/m)
...              }
>>> # Instanciate component
>>> component = mechanics.Damper(label, nodes, **parameters)
>>> # Graph dimensions
>>> len(component.nodes)
2
>>> len(component.edges)
1




