
.. title: Felt material (Felt)
.. slug: mechanics_dual-Felt
.. date: 2019-04-28 12:31:26.765295
.. tags: mechanics_dual, mathjax
.. category: component
.. type: text

Nonlinear felt material used in piano-hammer. The model is that found in [1]_ eq. (11). It includes a nonlinear restoring force and a nonlinear damper as follows:

.. math::

    e_{total}\left(c, \dot c\right) = e_{elastic}(c) + e_{damper}\left(c, \dot c\right),

with

.. math::

    e_{elastic}(c)  = F \,c ^B,

and

.. math::

    e_{damper}\left(c, \dot c\right) = \frac{A \, L}{B} c^{B-1} \,\dot c,

where :math:`c = \frac{\max (q, 0)}{L}` is the crush of the hammer with contraction :math:`q\in\mathbb R`.

.. TEASER_END


======================
 Felt material (Felt) 
======================


Nonlinear felt material used in piano-hammer. The model is that found in [1]_ eq. (11). It includes a nonlinear restoring force and a nonlinear damper as follows:

.. math::

    e_{total}\left(c, \dot c\right) = e_{elastic}(c) + e_{damper}\left(c, \dot c\right),

with

.. math::

    e_{elastic}(c)  = F \,c ^B,

and

.. math::

    e_{damper}\left(c, \dot c\right) = \frac{A \, L}{B} c^{B-1} \,\dot c,

where :math:`c = \frac{\max (q, 0)}{L}` is the crush of the hammer with contraction :math:`q\in\mathbb R`.

Power variables
---------------

**flux**: Velocity :math:`v`   (m/s)

**effort**: Force :math:`f`   (N)

Arguments
---------

label : str
    Felt label.

nodes : ('N1', 'N2')
    Nodes associated with the component terminals with positive flux N1->N2.

parameters : keyword arguments
    Component parameters.

+-----+------------------------------+-------+---------+
| Key | Description                  | Unit  | Default |
+=====+==============================+=======+=========+
| L   | Height at rest               | m     | 0.01    |
+-----+------------------------------+-------+---------+
| F   | Elastic characteristic force | N     | 10.0    |
+-----+------------------------------+-------+---------+
| A   | Damping coefficient          | N.s/m | 100.0   |
+-----+------------------------------+-------+---------+
| B   | Hysteresis coefficient       | d.u.  | 2.5     |
+-----+------------------------------+-------+---------+


Usage
-----

``felt = Felt('felt', ('N1', 'N2'), L=0.01, F=10.0, A=100.0, B=2.5)``

Netlist line
------------

``mechanics_dual.felt felt ('N1', 'N2'): L=0.01; F=10.0; A=100.0; B=2.5;``

Example
-------

>>> # Import dictionary
>>> from pyphs.dictionary import mechanics_dual
>>> # Define component label
>>> label = 'felt'
>>> # Define component nodes
>>> nodes = ('N1', 'N2')
>>> # Define component parameters
>>> parameters = {'L': 0.01,   # Height at rest (m)
...               'F': 10.0,   # Elastic characteristic force (N)
...               'A': 100.0,  # Damping coefficient (N.s/m)
...               'B': 2.5,    # Hysteresis coefficient (d.u.)
...              }
>>> # Instanciate component
>>> component = mechanics_dual.Felt(label, nodes, **parameters)
>>> # Graph dimensions
>>> len(component.nodes)
3
>>> len(component.edges)
2

Reference
---------

.. [1] Antoine Falaize and Thomas Helie. Passive simulation of the nonlinear port-hamiltonian modeling of a rhodes piano. Journal of Sound and Vibration, 2016.



