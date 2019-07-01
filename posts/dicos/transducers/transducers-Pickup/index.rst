
.. title: Electro-magnetic Pickup (Pickup)
.. slug: transducers-Pickup
.. date: 2019-04-28 12:31:26.774328
.. tags: transducers, mathjax
.. category: component
.. type: text

Electro-magnetic pickup as found in electric instruments (guitars and piano). See [1]_ for details.

.. TEASER_END


==================================
 Electro-magnetic Pickup (Pickup) 
==================================


Electro-magnetic pickup as found in electric instruments (guitars and piano). See [1]_ for details.

Power variables
---------------

**flux**: Not defined :math:`f`   (None)

**effort**: Not defined :math:`e`   (None)

Arguments
---------

label : str
    Pickup label.

nodes : ('MEC', 'EL1', 'EL2')
    MEC is a mechanical node. EL1, EL2 are electrical nodes with positive output current EL1->EL2.

parameters : keyword arguments
    Component parameter.

+-------+----------------------------------+------+---------+
| Key   | Description                      | Unit | Default |
+=======+==================================+======+=========+
| Lv    | Vertical distance                | m    | 0.001   |
+-------+----------------------------------+------+---------+
| Lh    | Horizontal distance              | m    | 0.0005  |
+-------+----------------------------------+------+---------+
| Ccoil | Pickup coil inductance           | W/K2 | 3e-05   |
+-------+----------------------------------+------+---------+
| Ncoil | Number of pickup coil wire turns | d.u. | 100.0   |
+-------+----------------------------------+------+---------+
| Rb    | Moving ball radius               | m    | 0.001   |
+-------+----------------------------------+------+---------+
| Rp    | Pickup coil radius               | m    | 0.001   |
+-------+----------------------------------+------+---------+
| H0    | Constant mmf of pickup magnet    | A    | 1.0     |
+-------+----------------------------------+------+---------+


Usage
-----

``pick = Pickup('pick', ('MEC', 'EL1', 'EL2'), Lv=0.001, Lh=0.0005, Ccoil=3e-05, Ncoil=100.0, Rb=0.001, Rp=0.001, H0=1.0)``

Netlist line
------------

``transducers.pickup pick ('MEC', 'EL1', 'EL2'): Lv=0.001; Lh=0.0005; Ccoil=3e-05; Ncoil=100.0; Rb=0.001; Rp=0.001; H0=1.0;``

Example
-------

>>> # Import dictionary
>>> from pyphs.dictionary import transducers
>>> # Define component label
>>> label = 'pick'
>>> # Define component nodes
>>> nodes = ('MEC', 'EL1', 'EL2')
>>> # Define component parameters
>>> parameters = {'Lv': 0.001,     # Vertical distance (m)
...               'Lh': 0.0005,    # Horizontal distance (m)
...               'Ccoil': 3e-05,  # Pickup coil inductance (W/K2)
...               'Ncoil': 100.0,  # Number of pickup coil wire turns (d.u.)
...               'Rb': 0.001,     # Moving ball radius (m)
...               'Rp': 0.001,     # Pickup coil radius (m)
...               'H0': 1.0,       # Constant mmf of pickup magnet (A)
...              }
>>> # Instanciate component
>>> component = transducers.Pickup(label, nodes, **parameters)
>>> # Graph dimensions
>>> len(component.nodes)
6
>>> len(component.edges)
7

Reference
---------

.. [1] Antoine Falaize and Thomas Helie. Passive simulation of the nonlinear port-hamiltonian modeling of a rhodes piano. Journal of Sound and Vibration, 2016.



