
.. title: Magnetic source (Source)
.. slug: magnetics-Source
.. date: 2019-04-28 12:31:26.757624
.. tags: magnetics, mathjax
.. category: component
.. type: text

Magnetic source from [1]_ (chap 7). Could be a source a magnetomotive force (mmf, e.g. a magnet) or a source of magnetic flux variation (mfv).

.. TEASER_END


==========================
 Magnetic source (Source) 
==========================


Magnetic source from [1]_ (chap 7). Could be a source a magnetomotive force (mmf, e.g. a magnet) or a source of magnetic flux variation (mfv).

Power variables
---------------

**flux**: Magnetic flux variation (mfv) :math:`\frac{d\,\phi}{dt}`   (V)

**effort**: Magnetomotive force (mmf) :math:`\psi`   (A)

Arguments
---------

label : str
    Source label.

nodes : ('N1', 'N2')
    Component terminals with positive flux N1->N2.

parameters : keyword arguments
    Component parameters

+------+-------------------------------+--------+---------+
| Key  | Description                   | Unit   | Default |
+======+===============================+========+=========+
| type | Source type in {'mmf', 'mfv'} | string | mmf     |
+------+-------------------------------+--------+---------+


Usage
-----

``sourc = Source('sourc', ('N1', 'N2'), type='mmf')``

Netlist line
------------

``magnetics.source sourc ('N1', 'N2'): type=mmf;``

Example
-------

>>> # Import dictionary
>>> from pyphs.dictionary import magnetics
>>> # Define component label
>>> label = 'sourc'
>>> # Define component nodes
>>> nodes = ('N1', 'N2')
>>> # Define component parameters
>>> parameters = {'type': 'mmf',  # Source type in {'mmf', 'mfv'} (string)
...              }
>>> # Instanciate component
>>> component = magnetics.Source(label, nodes, **parameters)
>>> # Graph dimensions
>>> len(component.nodes)
2
>>> len(component.edges)
1

Reference
---------

.. [1] Antoine Falaize. Modelisation, simulation, generation de code et correction de systemes multi-physiques audios: Approche par reseau de composants et formulation hamiltonienne a ports. PhD thesis, ecole Doctorale d'Informatique, Telecommunication et electronique de Paris, Universite Pierre et Marie Curie, Paris 6, EDITE UPMC ED130, july 2016.



