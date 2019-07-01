
.. title: Thermal transfer (Transfer)
.. slug: transducers-Pickup
.. date: 2018-08-12 19:07:47.646667
.. tags: transducers, mathjax
.. category: component
.. type: text

Electro-mecanique pickup as found in electric instruments (guitars and piano). See [1]_ for details.

.. TEASER_END


=============================
 Thermal transfer (Transfer) 
=============================


Electro-mecanique pickup as found in electric instruments (guitars and piano). See [1]_ for details.

Power variables
---------------

**flux**: Not defined :math:`f`   (None)

**effort**: Not defined :math:`e`   (None)

Arguments
---------

label : str
    Transfer label.

nodes : ('MEC', 'EL1', 'EL2')
    MEC is a mechanical node, EL1, EL2 are electrical nodes.

parameters : keyword arguments
    Component parameter.

+-------+----------------------------------+------+---------+
| Key   | Description                      | Unit | Default |
+=======+==================================+======+=========+
| Ncoil | Number of pickup coil wire turns | d.u. | 100.0   |
+-------+----------------------------------+------+---------+
| Ccoil | Pickup coil inductance           | W/K2 | 3e-05   |
+-------+----------------------------------+------+---------+
| Rb    | Moving ball radius               | m    | 0.001   |
+-------+----------------------------------+------+---------+
| Rp    | Pickup coil radius               | m    | 0.001   |
+-------+----------------------------------+------+---------+
| H0    | Constant mmf of pickup magnet    | A    | 1.0     |
+-------+----------------------------------+------+---------+
| Lv    | Thermal transfer coefficient     | W/K2 | 0.001   |
+-------+----------------------------------+------+---------+
| Lh    | Horizontal distance              | m    | 0.0005  |
+-------+----------------------------------+------+---------+


Usage
-----

``trans = thermics.Transfer('trans', ('MEC', 'EL1', 'EL2'), Ncoil=100.0, Ccoil=3e-05, Rb=0.001, Rp=0.001, H0=1.0, Lv=0.001, Lh=0.0005)``

Netlist line
------------

``thermics.transfer trans ('MEC', 'EL1', 'EL2'): Ncoil=100.0; Ccoil=3e-05; Rb=0.001; Rp=0.001; H0=1.0; Lv=0.001; Lh=0.0005;``

Example
-------

>>> # Import dictionary
>>> from pyphs.dictionary import thermics
>>> # Define component label
>>> label = 'trans'
>>> # Define component nodes
>>> nodes = ('MEC', 'EL1', 'EL2')
>>> # Define component parameters
>>> parameters = {
        'Ncoil': 100.0,  # Number of pickup coil wire turns (d.u.)
        'Ccoil': 3e-05,  # Pickup coil inductance (W/K2)
        'Rb': 0.001,     # Moving ball radius (m)
        'Rp': 0.001,     # Pickup coil radius (m)
        'H0': 1.0,       # Constant mmf of pickup magnet (A)
        'Lv': 0.001,     # Thermal transfer coefficient (W/K2)
        'Lh': 0.0005,    # Horizontal distance (m)
        }
>>> # Instanciate component
>>> component = thermics.Transfer(label, nodes, **parameters)
>>> # Graph dimensions
>>> len(component.nodes)
2
>>> len(component.edges)
1

Reference
---------

.. [1] Antoine Falaize and Thomas Helie. Passive simulation of the nonlinear port-hamiltonian modeling of a rhodes piano. Journal of Sound and Vibration, 2016.



