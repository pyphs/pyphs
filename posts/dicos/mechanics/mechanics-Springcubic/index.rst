
.. title: Cubic spring (Springcubic)
.. slug: mechanics-Springcubic
.. date: 2019-04-28 12:31:26.760461
.. tags: mechanics, mathjax
.. category: component
.. type: text

Cubic spring with state :math:`q\in \mathbb R` and parameters described below. The energy is

.. math::

    H(q) = \frac{F_1\,q^2}{2\,q_{ref}} + \frac{F_3\,q^4}{4q_{ref}^3}.

The resulting force is:

.. math::

    f(q)= \frac{d \, H(q)}{d q} = F_1 \,\frac{q}{q_{ref}} + F_3 \, \frac{q^3}{q_{ref}^3}.

so that :math:`f(q_{ref}) = F1+F3`.

.. TEASER_END


============================
 Cubic spring (Springcubic) 
============================


Cubic spring with state :math:`q\in \mathbb R` and parameters described below. The energy is

.. math::

    H(q) = \frac{F_1\,q^2}{2\,q_{ref}} + \frac{F_3\,q^4}{4q_{ref}^3}.

The resulting force is:

.. math::

    f(q)= \frac{d \, H(q)}{d q} = F_1 \,\frac{q}{q_{ref}} + F_3 \, \frac{q^3}{q_{ref}^3}.

so that :math:`f(q_{ref}) = F1+F3`.

Power variables
---------------

**flux**: Force :math:`f`   (N)

**effort**: Velocity :math:`v`   (m/s)

Arguments
---------

label : str
    Springcubic label.

nodes : ('P1', 'P2')
    Mechanical points associated with component endpoints (positive flux P1->P2).

parameters : keyword arguments
    Component parameters

+------+----------------------------------------+------+---------+
| Key  | Description                            | Unit | Default |
+======+========================================+======+=========+
| F1   | Linear contribution to restoring force | N    | 10.0    |
+------+----------------------------------------+------+---------+
| F3   | Cubic contribution to restoring force  | N    | 10.0    |
+------+----------------------------------------+------+---------+
| xref | Reference elongation                   | N    | 0.01    |
+------+----------------------------------------+------+---------+


Usage
-----

``spring = Springcubic('spring', ('P1', 'P2'), F1=10.0, F3=10.0, xref=0.01)``

Netlist line
------------

``mechanics.springcubic spring ('P1', 'P2'): F1=10.0; F3=10.0; xref=0.01;``

Example
-------

>>> # Import dictionary
>>> from pyphs.dictionary import mechanics
>>> # Define component label
>>> label = 'spring'
>>> # Define component nodes
>>> nodes = ('P1', 'P2')
>>> # Define component parameters
>>> parameters = {'F1': 10.0,    # Linear contribution to restoring force (N)
...               'F3': 10.0,    # Cubic contribution to restoring force (N)
...               'xref': 0.01,  # Reference elongation (N)
...              }
>>> # Instanciate component
>>> component = mechanics.Springcubic(label, nodes, **parameters)
>>> # Graph dimensions
>>> len(component.nodes)
2
>>> len(component.edges)
1




