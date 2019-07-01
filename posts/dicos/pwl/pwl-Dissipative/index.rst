
.. title: PWL Dissipation (Dissipative)
.. slug: pwl-Dissipative
.. date: 2019-04-28 12:31:26.772111
.. tags: pwl, mathjax
.. category: component
.. type: text

Piecewise-linear SISO dissipative component based on the PWL interpolation proposed in [1]_, (eq (2), known as the *Chua* interpolation). The file pointed by `file` argument should contains two lines, each blank separated list of floats for (x, y) values.

.. TEASER_END


===============================
 PWL Dissipation (Dissipative) 
===============================


Piecewise-linear SISO dissipative component based on the PWL interpolation proposed in [1]_, (eq (2), known as the *Chua* interpolation). The file pointed by `file` argument should contains two lines, each blank separated list of floats for (x, y) values.

Power variables
---------------

**flux**: Force :math:`f`   (N)

**effort**: Velocity :math:`v`   (m/s)

Arguments
---------

label : str
    Dissipative label.

nodes : ('N1', 'N2')
    Positive flux N1->N2.

parameters : keyword arguments
    Component parameter.

+-------+-------------------------------------+--------+-------------+
| Key   | Description                         | Unit   | Default     |
+=======+=====================================+========+=============+
| file  | Path to data file for (w, z) values | string | example.txt |
+-------+-------------------------------------+--------+-------------+
| start | Index of first value                | d.u.   | None        |
+-------+-------------------------------------+--------+-------------+
| stop  | Index of last value                 | d.u.   | None        |
+-------+-------------------------------------+--------+-------------+
| step  | step >= 1                           | d.u.   | None        |
+-------+-------------------------------------+--------+-------------+


Usage
-----

``diss = Dissipative('diss', ('N1', 'N2'), file='example.txt', start=None, stop=None, step=None)``

Netlist line
------------

``pwl.dissipative diss ('N1', 'N2'): file=example.txt; start=None; stop=None; step=None;``

Example
-------

>>> # Import dictionary
>>> from pyphs.dictionary import pwl
>>> # Define component label
>>> label = 'diss'
>>> # Define component nodes
>>> nodes = ('N1', 'N2')
>>> # Define component parameters
>>> parameters = {'file': 'example.txt',  # Path to data file for (w, z) values (string)
...               'start': None,          # Index of first value (d.u.)
...               'stop': None,           # Index of last value (d.u.)
...               'step': None,           # step >= 1 (d.u.)
...              }
>>> # Instanciate component
>>> component = pwl.Dissipative(label, nodes, **parameters)
>>> # Graph dimensions
>>> len(component.nodes)
2
>>> len(component.edges)
1

Reference
---------

.. [1] Chua, L., & Ying, R. (1983). Canonical piecewise-linear analysis. IEEE Transactions on Circuits and Systems, 30(3), 125-140.



