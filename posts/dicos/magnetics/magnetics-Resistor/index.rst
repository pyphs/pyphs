
.. title: Magnetic resistor (Resistor)
.. slug: magnetics-Resistor
.. date: 2019-04-28 12:31:26.757333
.. tags: magnetics, mathjax
.. category: component
.. type: text

Magnetic resistance from [1]_ (chap 7). In Laplace domain with :math:`s\in\mathbb C`:

.. math::

    e(s) = R \, f(s).



.. TEASER_END


==============================
 Magnetic resistor (Resistor) 
==============================


Magnetic resistance from [1]_ (chap 7). In Laplace domain with :math:`s\in\mathbb C`:

.. math::

    e(s) = R \, f(s).



Power variables
---------------

**flux**: Magnetic flux variation (mfv) :math:`\frac{d\,\phi}{dt}`   (V)

**effort**: Magnetomotive force (mmf) :math:`\psi`   (A)

Arguments
---------

label : str
    Resistor label.

nodes : ('N1', 'N2')
    Component terminals with positive flux N1->N2.

parameters : keyword arguments
    Component parameters

+-----+---------------------+-------+---------+
| Key | Description         | Unit  | Default |
+=====+=====================+=======+=========+
| R   | Magnetic resistance | 1/Ohm | 0.001   |
+-----+---------------------+-------+---------+


Usage
-----

``res = Resistor('res', ('N1', 'N2'), R=0.001)``

Netlist line
------------

``magnetics.resistor res ('N1', 'N2'): R=0.001;``

Example
-------

>>> # Import dictionary
>>> from pyphs.dictionary import magnetics
>>> # Define component label
>>> label = 'res'
>>> # Define component nodes
>>> nodes = ('N1', 'N2')
>>> # Define component parameters
>>> parameters = {'R': 0.001,  # Magnetic resistance (1/Ohm)
...              }
>>> # Instanciate component
>>> component = magnetics.Resistor(label, nodes, **parameters)
>>> # Graph dimensions
>>> len(component.nodes)
2
>>> len(component.edges)
1

Reference
---------

.. [1] Antoine Falaize. Modelisation, simulation, generation de code et correction de systemes multi-physiques audios: Approche par reseau de composants et formulation hamiltonienne a ports. PhD thesis, ecole Doctorale d'Informatique, Telecommunication et electronique de Paris, Universite Pierre et Marie Curie, Paris 6, EDITE UPMC ED130, july 2016.



