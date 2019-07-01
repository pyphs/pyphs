
.. title: Linear Damper (Damper)
.. slug: mechanics_dual-Damper
.. date: 2019-04-28 12:31:26.764881
.. tags: mechanics_dual, mathjax
.. category: component
.. type: text

Linear mechanical damping (i.e. opposing force proportional to the velocity). In Laplace domain with :math:`s\in\mathbb C`:

.. math::

    e(s) = A \, f(s).



.. TEASER_END


========================
 Linear Damper (Damper) 
========================


Linear mechanical damping (i.e. opposing force proportional to the velocity). In Laplace domain with :math:`s\in\mathbb C`:

.. math::

    e(s) = A \, f(s).



Power variables
---------------

**flux**: Velocity :math:`v`   (m/s)

**effort**: Force :math:`f`   (N)

Arguments
---------

label : str
    Damper label.

nodes : ('N1', 'N2')
    Nodes associated with the component terminals with positive flux N1->N2.

parameters : keyword arguments
    Component parameter

+-----+---------------------+-------+---------+
| Key | Description         | Unit  | Default |
+=====+=====================+=======+=========+
| A   | Damping coefficient | N.s/m | 1.0     |
+-----+---------------------+-------+---------+


Usage
-----

``damp = Damper('damp', ('N1', 'N2'), A=1.0)``

Netlist line
------------

``mechanics_dual.damper damp ('N1', 'N2'): A=1.0;``

Example
-------

>>> # Import dictionary
>>> from pyphs.dictionary import mechanics_dual
>>> # Define component label
>>> label = 'damp'
>>> # Define component nodes
>>> nodes = ('N1', 'N2')
>>> # Define component parameters
>>> parameters = {'A': 1.0,  # Damping coefficient (N.s/m)
...              }
>>> # Instanciate component
>>> component = mechanics_dual.Damper(label, nodes, **parameters)
>>> # Graph dimensions
>>> len(component.nodes)
2
>>> len(component.edges)
1




