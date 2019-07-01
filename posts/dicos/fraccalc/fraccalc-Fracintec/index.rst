
.. title: Effort-controlled fractional integrator (Fracintec)
.. slug: fraccalc-Fracintec
.. date: 2019-04-28 12:31:26.770585
.. tags: fraccalc, mathjax
.. category: component
.. type: text

Effort-controlled fractional integrator from [1]_ (chap 7):

.. math::

    f(s) = g \, s^{-beta}  \, e(s).



.. TEASER_END


=====================================================
 Effort-controlled fractional integrator (Fracintec) 
=====================================================


Effort-controlled fractional integrator from [1]_ (chap 7):

.. math::

    f(s) = g \, s^{-beta}  \, e(s).



Power variables
---------------

**flux**: Not defined :math:`f`   (None)

**effort**: Not defined :math:`e`   (None)

Arguments
---------

label : str
    Fracintec label.

nodes : ('N1', 'N2')
    Component terminals with positive flux N1->N2.

parameters : keyword arguments
    Component parameters

+--------------+-----------------------------------------------+---------+--------------+
| Key          | Description                                   | Unit    | Default      |
+==============+===============================================+=========+==============+
| g            | Gain                                          | unknown | 1.0          |
+--------------+-----------------------------------------------+---------+--------------+
| beta         | Integration order in (0, 1)                   | d.u.    | 0.5          |
+--------------+-----------------------------------------------+---------+--------------+
| NbPoles      | Approximation order                           | d.u.    | 20           |
+--------------+-----------------------------------------------+---------+--------------+
| PolesMinMax  | Poles modules in :math:`(10^{min}, 10^{max})` | Hz      | (-5, 10)     |
+--------------+-----------------------------------------------+---------+--------------+
| NbFreqPoints | Number of optimization points                 | d.u.    | 200          |
+--------------+-----------------------------------------------+---------+--------------+
| FreqsMinMax  | Optimization interval                         | Hz      | (1, 48000.0) |
+--------------+-----------------------------------------------+---------+--------------+
| DoPlot       | Plot transfer function                        | bool    | False        |
+--------------+-----------------------------------------------+---------+--------------+


Usage
-----

``fracint = Fracintec('fracint', ('N1', 'N2'), g=1.0, beta=0.5, NbPoles=20, PolesMinMax=(-5, 10), NbFreqPoints=200, FreqsMinMax=(1, 48000.0), DoPlot=False)``

Netlist line
------------

``fraccalc.fracintec fracint ('N1', 'N2'): g=1.0; beta=0.5; NbPoles=20; PolesMinMax=(-5, 10); NbFreqPoints=200; FreqsMinMax=(1, 48000.0); DoPlot=False;``

Example
-------

>>> # Import dictionary
>>> from pyphs.dictionary import fraccalc
>>> # Define component label
>>> label = 'fracint'
>>> # Define component nodes
>>> nodes = ('N1', 'N2')
>>> # Define component parameters
>>> parameters = {'g': 1.0,                     # Gain (unknown)
...               'beta': 0.5,                  # Integration order in (0, 1) (d.u.)
...               'NbPoles': 20,                # Approximation order (d.u.)
...               'PolesMinMax': (-5, 10),      # Poles modules in :math:`(10^{min}, 10^{max})` (Hz)
...               'NbFreqPoints': 200,          # Number of optimization points (d.u.)
...               'FreqsMinMax': (1, 48000.0),  # Optimization interval (Hz)
...               'DoPlot': False,              # Plot transfer function (bool)
...              }
>>> # Instanciate component
>>> component = fraccalc.Fracintec(label, nodes, **parameters)
>>> # Graph dimensions
>>> len(component.nodes)
19
>>> len(component.edges)
34

Reference
---------

.. [1] Antoine Falaize. Modelisation, simulation, generation de code et correction de systemes multi-physiques audios: Approche par reseau de composants et formulation hamiltonienne a ports. PhD thesis, ecole Doctorale d'Informatique, Telecommunication et electronique de Paris, Universite Pierre et Marie Curie, Paris 6, EDITE UPMC ED130, july 2016.



