
.. title: Saturating magnetic capacitor (Capacitorsat)
.. slug: magnetics-Capacitorsat
.. date: 2019-04-28 12:31:26.756891
.. tags: magnetics, mathjax
.. category: component
.. type: text

Saturating magnetic capacity from [1]_ (chap 7) with state :math:`\phi\in [-\phi_{sat}, \phi_{sat}]` and parameters described below. The energy is

.. math::

    H(\phi) = \frac{1}{C_{0}} \, \left( \frac{\phi^2}{2} +  C_{sat} H_{sat}(\phi)\right),

with

.. math::

    H_{sat}(\phi) = -  \frac{8 \phi_{sat}}{\pi \left(4-\pi\right)} \, \left(\frac{\pi^{2} \phi^{2}}{8\phi_{sat}^{2}} + \log{\left (\cos{\left (\frac{\pi \phi}{2 \phi_{sat}} \right)} \right)}\right).

The resulting magnetomotive force is:

.. math::

    \psi(\phi)= \frac{d\,H(\phi)}{d \phi} = \frac{ 1}{C_{0}} \left(\phi + C_{sat} \frac{d\,H_{sat}(\phi)}{d \phi}\right),

with

.. math::

    \frac{d\,H_{sat}(\phi)}{d \phi}= \frac{4}{4- \pi} \left(\tan{\left (\frac{\pi \phi}{2 \phi_{sat}} \right )} - \frac{\pi \phi}{2\phi_{sat}} \right).



.. TEASER_END


==============================================
 Saturating magnetic capacitor (Capacitorsat) 
==============================================


Saturating magnetic capacity from [1]_ (chap 7) with state :math:`\phi\in [-\phi_{sat}, \phi_{sat}]` and parameters described below. The energy is

.. math::

    H(\phi) = \frac{1}{C_{0}} \, \left( \frac{\phi^2}{2} +  C_{sat} H_{sat}(\phi)\right),

with

.. math::

    H_{sat}(\phi) = -  \frac{8 \phi_{sat}}{\pi \left(4-\pi\right)} \, \left(\frac{\pi^{2} \phi^{2}}{8\phi_{sat}^{2}} + \log{\left (\cos{\left (\frac{\pi \phi}{2 \phi_{sat}} \right)} \right)}\right).

The resulting magnetomotive force is:

.. math::

    \psi(\phi)= \frac{d\,H(\phi)}{d \phi} = \frac{ 1}{C_{0}} \left(\phi + C_{sat} \frac{d\,H_{sat}(\phi)}{d \phi}\right),

with

.. math::

    \frac{d\,H_{sat}(\phi)}{d \phi}= \frac{4}{4- \pi} \left(\tan{\left (\frac{\pi \phi}{2 \phi_{sat}} \right )} - \frac{\pi \phi}{2\phi_{sat}} \right).



Power variables
---------------

**flux**: Magnetic flux variation (mfv) :math:`\frac{d\,\phi}{dt}`   (V)

**effort**: Magnetomotive force (mmf) :math:`\psi`   (A)

Arguments
---------

label : str
    Capacitorsat label.

nodes : ('N1', 'N2')
    Component terminals with positive flux N1->N2.

parameters : keyword arguments
    Component parameters

+--------+----------------------------------+------+---------+
| Key    | Description                      | Unit | Default |
+========+==================================+======+=========+
| C0     | Magnetic capacitance around zero | H    | 1000.0  |
+--------+----------------------------------+------+---------+
| Csat   | Nonlinearity parameter           | d.u. | 1000.0  |
+--------+----------------------------------+------+---------+
| phisat | Magnetic capacitance             | Wb   | 0.1     |
+--------+----------------------------------+------+---------+


Usage
-----

``capa = Capacitorsat('capa', ('N1', 'N2'), C0=1000.0, Csat=1000.0, phisat=0.1)``

Netlist line
------------

``magnetics.capacitorsat capa ('N1', 'N2'): C0=1000.0; Csat=1000.0; phisat=0.1;``

Example
-------

>>> # Import dictionary
>>> from pyphs.dictionary import magnetics
>>> # Define component label
>>> label = 'capa'
>>> # Define component nodes
>>> nodes = ('N1', 'N2')
>>> # Define component parameters
>>> parameters = {'C0': 1000.0,    # Magnetic capacitance around zero (H)
...               'Csat': 1000.0,  # Nonlinearity parameter (d.u.)
...               'phisat': 0.1,   # Magnetic capacitance (Wb)
...              }
>>> # Instanciate component
>>> component = magnetics.Capacitorsat(label, nodes, **parameters)
>>> # Graph dimensions
>>> len(component.nodes)
2
>>> len(component.edges)
1

Reference
---------

.. [1] Antoine Falaize. Modelisation, simulation, generation de code et correction de systemes multi-physiques audios: Approche par reseau de composants et formulation hamiltonienne a ports. PhD thesis, ecole Doctorale d'Informatique, Telecommunication et electronique de Paris, Universite Pierre et Marie Curie, Paris 6, EDITE UPMC ED130, july 2016.



