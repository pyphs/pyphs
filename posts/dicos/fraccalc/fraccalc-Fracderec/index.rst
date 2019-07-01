
.. title: Effort-controlled fractional derivator (Fracderec)
.. slug: fraccalc-Fracderec
.. date: 2019-04-28 12:31:26.769662
.. tags: fraccalc, mathjax
.. category: component
.. type: text

Effort-controlled fractional derivator from [1]_ (chap 7):

.. math::

    f(s) = g \, s^{alpha}  \, e(s).



.. TEASER_END


====================================================
 Effort-controlled fractional derivator (Fracderec) 
====================================================


Effort-controlled fractional derivator from [1]_ (chap 7):

.. math::

    f(s) = g \, s^{alpha}  \, e(s).



Power variables
---------------

**flux**: Not defined :math:`f`   (None)

**effort**: Not defined :math:`e`   (None)

Arguments
---------

label : str
    Fracderec label.

nodes : ('N1', 'N2')
    Component terminals with positive flux N1->N2.

parameters : keyword arguments
    Component parameters

+--------------+-----------------------------------------------+---------+--------------+
| Key          | Description                                   | Unit    | Default      |
+==============+===============================================+=========+==============+
| g            | Gain                                          | unknown | 1.0          |
+--------------+-----------------------------------------------+---------+--------------+
| alpha        | Derivation order in (0, 1)                    | d.u.    | 0.5          |
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

``fracder = Fracderec('fracder', ('N1', 'N2'), g=1.0, alpha=0.5, NbPoles=20, PolesMinMax=(-5, 10), NbFreqPoints=200, FreqsMinMax=(1, 48000.0), DoPlot=False)``

Netlist line
------------

``fraccalc.fracderec fracder ('N1', 'N2'): g=1.0; alpha=0.5; NbPoles=20; PolesMinMax=(-5, 10); NbFreqPoints=200; FreqsMinMax=(1, 48000.0); DoPlot=False;``

Example
-------

>>> # Import dictionary
>>> from pyphs.dictionary import fraccalc
>>> # Define component label
>>> label = 'fracder'
>>> # Define component nodes
>>> nodes = ('N1', 'N2')
>>> # Define component parameters
>>> parameters = {'g': 1.0,                     # Gain (unknown)
...               'alpha': 0.5,                 # Derivation order in (0, 1) (d.u.)
...               'NbPoles': 20,                # Approximation order (d.u.)
...               'PolesMinMax': (-5, 10),      # Poles modules in :math:`(10^{min}, 10^{max})` (Hz)
...               'NbFreqPoints': 200,          # Number of optimization points (d.u.)
...               'FreqsMinMax': (1, 48000.0),  # Optimization interval (Hz)
...               'DoPlot': False,              # Plot transfer function (bool)
...              }
>>> # Instanciate component
>>> component = fraccalc.Fracderec(label, nodes, **parameters)
>>> # Graph dimensions
>>> len(component.nodes)
37
>>> len(component.edges)
68

Reference
---------

.. [1] Antoine Falaize. Modelisation, simulation, generation de code et correction de systemes multi-physiques audios: Approche par reseau de composants et formulation hamiltonienne a ports. PhD thesis, ecole Doctorale d'Informatique, Telecommunication et electronique de Paris, Universite Pierre et Marie Curie, Paris 6, EDITE UPMC ED130, july 2016.



