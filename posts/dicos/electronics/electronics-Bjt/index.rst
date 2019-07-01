
.. title: Bipolar junction transistor (Bjt)
.. slug: electronics-Bjt
.. date: 2019-04-28 12:31:26.751728
.. tags: electronics, mathjax
.. category: component
.. type: text

Bipolar junction transistor of NPN type according to the Ebers-Moll model [1]_.

.. TEASER_END


===================================
 Bipolar junction transistor (Bjt) 
===================================


Bipolar junction transistor of NPN type according to the Ebers-Moll model [1]_.

Power variables
---------------

**flux**: Electrical current :math:`i`   (A)

**effort**: Electrical Voltage :math:`v`   (V)

Arguments
---------

label : str
    Bjt label.

nodes : ('Nb', 'Nc', 'Ne')
    base 'Nb', collector 'Nc', emitter 'Ne'.

parameters : keyword arguments
    Parameters description and default value.

+-------+--------------------------------------------------+------+---------+
| Key   | Description                                      | Unit | Default |
+=======+==================================================+======+=========+
| Is    | Reverse saturation current                       | A    | 1e-12   |
+-------+--------------------------------------------------+------+---------+
| betaR | Reverse common emitter current gain in [0, 20]   | d.u. | 10.0    |
+-------+--------------------------------------------------+------+---------+
| betaF | Forward common emitter current gain in [20, 500] | d.u. | 200.0   |
+-------+--------------------------------------------------+------+---------+
| Vt    | Thermal voltage at room temperature              | V    | 0.026   |
+-------+--------------------------------------------------+------+---------+
| mu    | Ideality factor in [1, 2]                        | d.u. | 1.0     |
+-------+--------------------------------------------------+------+---------+
| Rb    | Zero bias base resistance                        | Ohms | 20.0    |
+-------+--------------------------------------------------+------+---------+
| Rc    | Collector resistance                             | Ohms | 0.1     |
+-------+--------------------------------------------------+------+---------+
| Re    | Emitter resistance                               | Ohms | 0.1     |
+-------+--------------------------------------------------+------+---------+


Usage
-----

``bjt = Bjt('bjt', ('Nb', 'Nc', 'Ne'), Is=1e-12, betaR=10.0, betaF=200.0, Vt=0.026, mu=1.0, Rb=20.0, Rc=0.1, Re=0.1)``

Netlist line
------------

``electronics.bjt bjt ('Nb', 'Nc', 'Ne'): Is=1e-12; betaR=10.0; betaF=200.0; Vt=0.026; mu=1.0; Rb=20.0; Rc=0.1; Re=0.1;``

Example
-------

>>> # Import dictionary
>>> from pyphs.dictionary import electronics
>>> # Define component label
>>> label = 'bjt'
>>> # Define component nodes
>>> nodes = ('Nb', 'Nc', 'Ne')
>>> # Define component parameters
>>> parameters = {'Is': 1e-12,     # Reverse saturation current (A)
...               'betaR': 10.0,   # Reverse common emitter current gain in [0, 20] (d.u.)
...               'betaF': 200.0,  # Forward common emitter current gain in [20, 500] (d.u.)
...               'Vt': 0.026,     # Thermal voltage at room temperature (V)
...               'mu': 1.0,       # Ideality factor in [1, 2] (d.u.)
...               'Rb': 20.0,      # Zero bias base resistance (Ohms)
...               'Rc': 0.1,       # Collector resistance (Ohms)
...               'Re': 0.1,       # Emitter resistance (Ohms)
...              }
>>> # Instanciate component
>>> component = electronics.Bjt(label, nodes, **parameters)
>>> # Graph dimensions
>>> len(component.nodes)
6
>>> len(component.edges)
5

Reference
---------

.. [1] https://en.wikipedia.org/wiki/Bipolar_junction_transistor#Ebers.E2.80.93Moll_model



