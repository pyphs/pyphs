
.. title: Saturating spring (Springsat)
.. slug: mechanics-Springsat
.. date: 2019-04-28 12:31:26.760913
.. tags: mechanics, mathjax
.. category: component
.. type: text

Saturating spring from [1]_ (chap 7) with state :math:`q\in [-q_{sat}, q_{sat}]` and parameters described below. The energy is

.. math::

    H(q) = K_0 \, \left( \frac{q^2}{2} +  K_{sat} H_{sat}(q)\right),

with

.. math::

    H_{sat}(q) = -  \frac{8 q_{sat}}{\pi \left(4-\pi\right)} \, \left(\frac{\pi^{2} q^{2}}{8q_{sat}^{2}} + \log{\left (\cos{\left (\frac{\pi q}{2 q_{sat}} \right)} \right)}\right).

The resulting force is:

.. math::

    f(q)= \frac{d\,H(q)}{d q} = K_{0} \left(q + K_{sat} \frac{d\,H_{sat}(q)}{d q}\right),

with

.. math::

    \frac{d\,H_{sat}(q)}{d q}= \frac{4}{4- \pi} \left(\tan{\left (\frac{\pi q}{2 q_{sat}} \right )} - \frac{\pi q}{2q_{sat}} \right).



.. TEASER_END


===============================
 Saturating spring (Springsat) 
===============================


Saturating spring from [1]_ (chap 7) with state :math:`q\in [-q_{sat}, q_{sat}]` and parameters described below. The energy is

.. math::

    H(q) = K_0 \, \left( \frac{q^2}{2} +  K_{sat} H_{sat}(q)\right),

with

.. math::

    H_{sat}(q) = -  \frac{8 q_{sat}}{\pi \left(4-\pi\right)} \, \left(\frac{\pi^{2} q^{2}}{8q_{sat}^{2}} + \log{\left (\cos{\left (\frac{\pi q}{2 q_{sat}} \right)} \right)}\right).

The resulting force is:

.. math::

    f(q)= \frac{d\,H(q)}{d q} = K_{0} \left(q + K_{sat} \frac{d\,H_{sat}(q)}{d q}\right),

with

.. math::

    \frac{d\,H_{sat}(q)}{d q}= \frac{4}{4- \pi} \left(\tan{\left (\frac{\pi q}{2 q_{sat}} \right )} - \frac{\pi q}{2q_{sat}} \right).



Power variables
---------------

**flux**: Force :math:`f`   (N)

**effort**: Velocity :math:`v`   (m/s)

Arguments
---------

label : str
    Springsat label.

nodes : ('P1', 'P2')
    Mechanical points associated with component endpoints (positive flux P1->P2).

parameters : keyword arguments
    Component parameters

+------+------------------------+------+---------+
| Key  | Description            | Unit | Default |
+======+========================+======+=========+
| K0   | Stiffness around zero  | H    | 1000.0  |
+------+------------------------+------+---------+
| Ksat | Nonlinearity parameter | d.u. | 1000.0  |
+------+------------------------+------+---------+
| xsat | Saturating position    | m    | 0.01    |
+------+------------------------+------+---------+


Usage
-----

``spring = Springsat('spring', ('P1', 'P2'), K0=1000.0, Ksat=1000.0, xsat=0.01)``

Netlist line
------------

``mechanics.springsat spring ('P1', 'P2'): K0=1000.0; Ksat=1000.0; xsat=0.01;``

Example
-------

>>> # Import dictionary
>>> from pyphs.dictionary import mechanics
>>> # Define component label
>>> label = 'spring'
>>> # Define component nodes
>>> nodes = ('P1', 'P2')
>>> # Define component parameters
>>> parameters = {'K0': 1000.0,    # Stiffness around zero (H)
...               'Ksat': 1000.0,  # Nonlinearity parameter (d.u.)
...               'xsat': 0.01,    # Saturating position (m)
...              }
>>> # Instanciate component
>>> component = mechanics.Springsat(label, nodes, **parameters)
>>> # Graph dimensions
>>> len(component.nodes)
2
>>> len(component.edges)
1

Reference
---------

.. [1] Antoine Falaize. Modelisation, simulation, generation de code et correction de systemes multi-physiques audios: Approche par reseau de composants et formulation hamiltonienne a ports. PhD thesis, ecole Doctorale d'Informatique, Telecommunication et electronique de Paris, Universite Pierre et Marie Curie, Paris 6, EDITE UPMC ED130, july 2016.



