
.. title: Gyrator
.. slug: connectors-Gyrator
.. date: 2019-04-28 12:31:26.768062
.. tags: connectors, mathjax
.. category: component
.. type: text

Quadripole connector of gyrator type with:

.. math::

    \left\{\begin{array}{rcl} e_A &=& -\alpha\,f_B, \\ e_B &=& + \alpha\,f_A. \end{array}\right.



.. TEASER_END


=========
 Gyrator 
=========


Quadripole connector of gyrator type with:

.. math::

    \left\{\begin{array}{rcl} e_A &=& -\alpha\,f_B, \\ e_B &=& + \alpha\,f_A. \end{array}\right.



Power variables
---------------

**flux**: Not defined :math:`f`   (None)

**effort**: Not defined :math:`e`   (None)

Arguments
---------

label : str
    Gyrator label.

nodes : ('A1', 'A2', 'B1', 'B2')
    Connected edges are edge A = A1->A2 and edge B = B1->B2.

parameters : keyword arguments
    Parameters description and default value.

+-------+-------------+---------+---------+
| Key   | Description | Unit    | Default |
+=======+=============+=========+=========+
| alpha | Ratio       | unknown | 1.0     |
+-------+-------------+---------+---------+


Usage
-----

``gyr = Gyrator('gyr', ('A1', 'A2', 'B1', 'B2'), alpha=1.0)``

Netlist line
------------

``connectors.gyrator gyr ('A1', 'A2', 'B1', 'B2'): alpha=1.0;``

Example
-------

>>> # Import dictionary
>>> from pyphs.dictionary import connectors
>>> # Define component label
>>> label = 'gyr'
>>> # Define component nodes
>>> nodes = ('A1', 'A2', 'B1', 'B2')
>>> # Define component parameters
>>> parameters = {'alpha': 1.0,  # Ratio (unknown)
...              }
>>> # Instanciate component
>>> component = connectors.Gyrator(label, nodes, **parameters)
>>> # Graph dimensions
>>> len(component.nodes)
4
>>> len(component.edges)
2




