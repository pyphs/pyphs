
.. title: Triode
.. slug: electronics-Triode
.. date: 2019-04-28 12:31:26.755068
.. tags: electronics, mathjax
.. category: component
.. type: text

Triode model from [1]_ which includes Norman Koren modeling of plate to cathode current Ipk and grid effect for grid to cathod current Igk.

.. TEASER_END


========
 Triode 
========


Triode model from [1]_ which includes Norman Koren modeling of plate to cathode current Ipk and grid effect for grid to cathod current Igk.

Power variables
---------------

**flux**: Electrical current :math:`i`   (A)

**effort**: Electrical Voltage :math:`v`   (V)

Arguments
---------

label : str
    Triode label.

nodes : ('Nk', 'Np', 'Ng')
    Cathode 'K', Plate 'P' and Grid 'G'

parameters : keyword arguments
    Parameters description and default value.

+-----+----------------------------------+------+---------+
| Key | Description                      | Unit | Default |
+=====+==================================+======+=========+
| mu  | Norman Koren's parameters        | d.u. | 88.0    |
+-----+----------------------------------+------+---------+
| Ex  | Norman Koren's parameters        | d.u. | 1.4     |
+-----+----------------------------------+------+---------+
| Kg  | Norman Koren's parameters        | d.u. | 1060.0  |
+-----+----------------------------------+------+---------+
| Kp  | Norman Koren's parameters        | d.u. | 600.0   |
+-----+----------------------------------+------+---------+
| Kvb | Norman Koren's parameters        | d.u. | 300.0   |
+-----+----------------------------------+------+---------+
| Vct | Norman Koren's parameters        | V    | 0.5     |
+-----+----------------------------------+------+---------+
| Va  | Voltage threshold                | V    | 0.33    |
+-----+----------------------------------+------+---------+
| Rgk | Grid current resistive behaviour | Ohms | 3000.0  |
+-----+----------------------------------+------+---------+


Usage
-----

``tri = Triode('tri', ('Nk', 'Np', 'Ng'), mu=88.0, Ex=1.4, Kg=1060.0, Kp=600.0, Kvb=300.0, Vct=0.5, Va=0.33, Rgk=3000.0)``

Netlist line
------------

``electronics.triode tri ('Nk', 'Np', 'Ng'): mu=88.0; Ex=1.4; Kg=1060.0; Kp=600.0; Kvb=300.0; Vct=0.5; Va=0.33; Rgk=3000.0;``

Example
-------

>>> # Import dictionary
>>> from pyphs.dictionary import electronics
>>> # Define component label
>>> label = 'tri'
>>> # Define component nodes
>>> nodes = ('Nk', 'Np', 'Ng')
>>> # Define component parameters
>>> parameters = {'mu': 88.0,     # Norman Koren's parameters (d.u.)
...               'Ex': 1.4,      # Norman Koren's parameters (d.u.)
...               'Kg': 1060.0,   # Norman Koren's parameters (d.u.)
...               'Kp': 600.0,    # Norman Koren's parameters (d.u.)
...               'Kvb': 300.0,   # Norman Koren's parameters (d.u.)
...               'Vct': 0.5,     # Norman Koren's parameters (V)
...               'Va': 0.33,     # Voltage threshold (V)
...               'Rgk': 3000.0,  # Grid current resistive behaviour (Ohms)
...              }
>>> # Instanciate component
>>> component = electronics.Triode(label, nodes, **parameters)
>>> # Graph dimensions
>>> len(component.nodes)
3
>>> len(component.edges)
2

Reference
---------

.. [1] I. Cohen and T. Helie, Measures and parameter estimation of triodes for the real-time simulation of a multi-stage guitar preamplifier. 129th Convention of the AES, SF USA, 2009.



