
.. title: Transformer
.. slug: connectors-Transformer
.. date: 2019-04-28 12:31:26.768515
.. tags: connectors, mathjax
.. category: component
.. type: text

Quadripole connector of transformer type with:

.. math::

    \left\{\begin{array}{rcl} f_A &=& -\alpha\, f_B, \\ e_B &=& + \alpha\,e_A. \end{array}\right.



.. TEASER_END


=============
 Transformer 
=============


Quadripole connector of transformer type with:

.. math::

    \left\{\begin{array}{rcl} f_A &=& -\alpha\, f_B, \\ e_B &=& + \alpha\,e_A. \end{array}\right.



Power variables
---------------

**flux**: Not defined :math:`f`   (None)

**effort**: Not defined :math:`e`   (None)

Arguments
---------

label : str
    Transformer label.

nodes : ('A1', 'A2', 'B1', 'B2')
    Connected edges are A1->A2 and B1->B2.

parameters : keyword arguments
    Parameters description and default value.

+-------+-------------+---------+---------+
| Key   | Description | Unit    | Default |
+=======+=============+=========+=========+
| alpha | Ratio       | unknown | 1.0     |
+-------+-------------+---------+---------+


Usage
-----

``trans = Transformer('trans', ('A1', 'A2', 'B1', 'B2'), alpha=1.0)``

Netlist line
------------

``connectors.transformer trans ('A1', 'A2', 'B1', 'B2'): alpha=1.0;``

Example
-------

>>> # Import dictionary
>>> from pyphs.dictionary import connectors
>>> # Define component label
>>> label = 'trans'
>>> # Define component nodes
>>> nodes = ('A1', 'A2', 'B1', 'B2')
>>> # Define component parameters
>>> parameters = {'alpha': 1.0,  # Ratio (unknown)
...              }
>>> # Instanciate component
>>> component = connectors.Transformer(label, nodes, **parameters)
>>> # Graph dimensions
>>> len(component.nodes)
4
>>> len(component.edges)
2




