
.. title: PN Diode (Diode)
.. slug: electronics-Diode
.. date: 2019-04-28 12:31:26.752740
.. tags: electronics, mathjax
.. category: component
.. type: text

PN Diode governed by the Shockley diode equation [1]_.

.. TEASER_END


==================
 PN Diode (Diode) 
==================


PN Diode governed by the Shockley diode equation [1]_.

Power variables
---------------

**flux**: Electrical current :math:`i`   (A)

**effort**: Electrical Voltage :math:`v`   (V)

Arguments
---------

label : str
    Diode label.

nodes : ('N1', 'N2')
    The current is directed from 'N1' to 'N2'.

parameters : keyword arguments
    Parameters description and default value.

+-----+-----------------------+------+---------+
| Key | Description           | Unit | Default |
+=====+=======================+======+=========+
| Is  | Saturation current    | A    | 2e-09   |
+-----+-----------------------+------+---------+
| mu  | Quality factor        | d.u. | 1.7     |
+-----+-----------------------+------+---------+
| R   | Connectors resistance | Ohms | 0.5     |
+-----+-----------------------+------+---------+
| v0  | Thermal voltage       | V    | 0.026   |
+-----+-----------------------+------+---------+


Usage
-----

``D = Diode('D', ('N1', 'N2'), Is=2e-09, mu=1.7, R=0.5, v0=0.026)``

Netlist line
------------

``electronics.diode D ('N1', 'N2'): Is=2e-09; mu=1.7; R=0.5; v0=0.026;``

Example
-------

>>> # Import dictionary
>>> from pyphs.dictionary import electronics
>>> # Define component label
>>> label = 'D'
>>> # Define component nodes
>>> nodes = ('N1', 'N2')
>>> # Define component parameters
>>> parameters = {'Is': 2e-09,  # Saturation current (A)
...               'mu': 1.7,    # Quality factor (d.u.)
...               'R': 0.5,     # Connectors resistance (Ohms)
...               'v0': 0.026,  # Thermal voltage (V)
...              }
>>> # Instanciate component
>>> component = electronics.Diode(label, nodes, **parameters)
>>> # Graph dimensions
>>> len(component.nodes)
3
>>> len(component.edges)
3

Reference
---------

.. [1] https://en.wikipedia.org/wiki/Shockley_diode_equation



