
.. title: Magnetic capacitor (Capacitor)
.. slug: magnetics-Capacitor
.. date: 2019-04-28 12:31:26.756282
.. tags: magnetics, mathjax
.. category: component
.. type: text

Magnetic capacity from [1]_ (chap 7). In Laplace domain with :math:`s\in\mathbb C`:

.. math::

    e(s) = \frac{1}{C s} \, f(s).



.. TEASER_END


================================
 Magnetic capacitor (Capacitor) 
================================


Magnetic capacity from [1]_ (chap 7). In Laplace domain with :math:`s\in\mathbb C`:

.. math::

    e(s) = \frac{1}{C s} \, f(s).



Power variables
---------------

**flux**: Magnetic flux variation (mfv) :math:`\frac{d\,\phi}{dt}`   (V)

**effort**: Magnetomotive force (mmf) :math:`\psi`   (A)

Arguments
---------

label : str
    Capacitor label.

nodes : ('N1', 'N2')
    Component terminals with positive flux N1->N2.

parameters : keyword arguments
    Component parameters

+-----+----------------------+------+---------+
| Key | Description          | Unit | Default |
+=====+======================+======+=========+
| C   | Magnetic capacitance | H    | 1e-09   |
+-----+----------------------+------+---------+


Usage
-----

``capa = Capacitor('capa', ('N1', 'N2'), C=1e-09)``

Netlist line
------------

``magnetics.capacitor capa ('N1', 'N2'): C=1e-09;``

Example
-------

>>> # Import dictionary
>>> from pyphs.dictionary import magnetics
>>> # Define component label
>>> label = 'capa'
>>> # Define component nodes
>>> nodes = ('N1', 'N2')
>>> # Define component parameters
>>> parameters = {'C': 1e-09,  # Magnetic capacitance (H)
...              }
>>> # Instanciate component
>>> component = magnetics.Capacitor(label, nodes, **parameters)
>>> # Graph dimensions
>>> len(component.nodes)
2
>>> len(component.edges)
1

Reference
---------

.. [1] Antoine Falaize. Modelisation, simulation, generation de code et correction de systemes multi-physiques audios: Approche par reseau de composants et formulation hamiltonienne a ports. PhD thesis, ecole Doctorale d'Informatique, Telecommunication et electronique de Paris, Universite Pierre et Marie Curie, Paris 6, EDITE UPMC ED130, july 2016.



