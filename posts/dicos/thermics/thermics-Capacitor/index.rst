
.. title: Thermal Capacitor (Capacitor)
.. slug: thermics-Capacitor
.. date: 2019-04-28 12:31:26.762610
.. tags: thermics, mathjax
.. category: component
.. type: text

Heat capacity (or mass) with entropy :math:`\sigma\in\mathbb R`, energy (exponential law):

.. math::

    H(\sigma)= C\,T_0\,\exp{\left(\frac{\sigma}{C}\right)},

and temperature:

.. math::

    \theta(\sigma) = \frac{d H}{d \sigma}(\sigma) = T_0\,\exp{\left(\frac{\sigma}{C}\right)}.



.. TEASER_END


===============================
 Thermal Capacitor (Capacitor) 
===============================


Heat capacity (or mass) with entropy :math:`\sigma\in\mathbb R`, energy (exponential law):

.. math::

    H(\sigma)= C\,T_0\,\exp{\left(\frac{\sigma}{C}\right)},

and temperature:

.. math::

    \theta(\sigma) = \frac{d H}{d \sigma}(\sigma) = T_0\,\exp{\left(\frac{\sigma}{C}\right)}.



Power variables
---------------

**flux**: Entropy variation :math:`\frac{d\sigma}{dt}`   (W/K)

**effort**: Temperature :math:`\theta`   (K)

Arguments
---------

label : str
    Capacitor label.

nodes : ('T',)
    Thermal point associated with the heat mass. The node label must be the same as the component label. The capacity temperature is measured from the reference node (datum).

parameters : keyword arguments
    Component parameter.

+-----+---------------------+------+---------+
| Key | Description         | Unit | Default |
+=====+=====================+======+=========+
| C   | Thermal capacity    | J/K  | 1000.0  |
+-----+---------------------+------+---------+
| T0  | Initial temperature | K    | 273.16  |
+-----+---------------------+------+---------+


Usage
-----

``T = Capacitor('T', ('T',), C=1000.0, T0=273.16)``

Netlist line
------------

``thermics.capacitor T ('T',): C=1000.0; T0=273.16;``

Example
-------

>>> # Import dictionary
>>> from pyphs.dictionary import thermics
>>> # Define component label
>>> label = 'T'
>>> # Define component nodes
>>> nodes = ('T',)
>>> # Define component parameters
>>> parameters = {'C': 1000.0,   # Thermal capacity (J/K)
...               'T0': 273.16,  # Initial temperature (K)
...              }
>>> # Instanciate component
>>> component = thermics.Capacitor(label, nodes, **parameters)
>>> # Graph dimensions
>>> len(component.nodes)
2
>>> len(component.edges)
1




