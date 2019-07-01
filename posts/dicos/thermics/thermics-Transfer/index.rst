
.. title: Thermal transfer (Transfer)
.. slug: thermics-Transfer
.. date: 2019-04-28 12:31:26.763470
.. tags: thermics, mathjax
.. category: component
.. type: text

Irreversible heat transfer between two thermal nodes. It is made from two dissipative edges. The dissipation variables are temperatures (:math:`w_1=T_1` and :math:`w_2=T_2`). The dissipation functions are:

.. math::

    \begin{array}{rcl} \dot \sigma _1 = z_1(w_1, w_2) & = & R\frac{w_1-w_2}{w_1}, \\ \dot \sigma _2 = z_2(w_1, w_2) & = & R\frac{w_2-w_1}{w_2}.  \end{array}



.. TEASER_END


=============================
 Thermal transfer (Transfer) 
=============================


Irreversible heat transfer between two thermal nodes. It is made from two dissipative edges. The dissipation variables are temperatures (:math:`w_1=T_1` and :math:`w_2=T_2`). The dissipation functions are:

.. math::

    \begin{array}{rcl} \dot \sigma _1 = z_1(w_1, w_2) & = & R\frac{w_1-w_2}{w_1}, \\ \dot \sigma _2 = z_2(w_1, w_2) & = & R\frac{w_2-w_1}{w_2}.  \end{array}



Power variables
---------------

**flux**: Entropy variation :math:`\frac{d\sigma}{dt}`   (W/K)

**effort**: Temperature :math:`\theta`   (K)

Arguments
---------

label : str
    Transfer label.

nodes : ('T1', 'T2')
    The thermal transfer occurs between thermal points 'T1' and 'T2'.

parameters : keyword arguments
    Component parameter.

+-----+------------------------------+------+---------+
| Key | Description                  | Unit | Default |
+=====+==============================+======+=========+
| R   | Thermal transfer coefficient | W/K  | 1000.0  |
+-----+------------------------------+------+---------+


Usage
-----

``trans = Transfer('trans', ('T1', 'T2'), R=1000.0)``

Netlist line
------------

``thermics.transfer trans ('T1', 'T2'): R=1000.0;``

Example
-------

>>> # Import dictionary
>>> from pyphs.dictionary import thermics
>>> # Define component label
>>> label = 'trans'
>>> # Define component nodes
>>> nodes = ('T1', 'T2')
>>> # Define component parameters
>>> parameters = {'R': 1000.0,  # Thermal transfer coefficient (W/K)
...              }
>>> # Instanciate component
>>> component = thermics.Transfer(label, nodes, **parameters)
>>> # Graph dimensions
>>> len(component.nodes)
3
>>> len(component.edges)
2




