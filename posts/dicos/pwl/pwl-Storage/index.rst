
.. title: PWL Storage (Storage)
.. slug: pwl-Storage
.. date: 2019-04-28 12:31:26.772490
.. tags: pwl, mathjax
.. category: component
.. type: text

Piecewise-linear SISO storage component based on the PWL interpolation proposed in [1]_, (eq (2), known as the *Chua* interpolation). The file pointed by `file` argument should contains two lines, each blank separated list of floats for (x, H) or (x, dxH) values. If (x, dxH) values are provided, the resulting interpolation must be integrated to yield a (x, H) mapping  (see `integrate` parameter below).

.. TEASER_END


=======================
 PWL Storage (Storage) 
=======================


Piecewise-linear SISO storage component based on the PWL interpolation proposed in [1]_, (eq (2), known as the *Chua* interpolation). The file pointed by `file` argument should contains two lines, each blank separated list of floats for (x, H) or (x, dxH) values. If (x, dxH) values are provided, the resulting interpolation must be integrated to yield a (x, H) mapping  (see `integrate` parameter below).

Power variables
---------------

**flux**: Force :math:`f`   (N)

**effort**: Velocity :math:`v`   (m/s)

Arguments
---------

label : str
    Storage label.

nodes : ('N1', 'N2')
    Positive flux N1->N2.

parameters : keyword arguments
    Component parameter.

+-----------+---------------------------------------------------+--------+-------------+
| Key       | Description                                       | Unit   | Default     |
+===========+===================================================+========+=============+
| file      | Path to data file for (x, H) or (x, dxH) values   | string | example.txt |
+-----------+---------------------------------------------------+--------+-------------+
| integrate | If True, data is (x, dxH) and integrate to (x, H) | bool   | False       |
+-----------+---------------------------------------------------+--------+-------------+
| start     | Index of first value                              | d.u.   | None        |
+-----------+---------------------------------------------------+--------+-------------+
| stop      | Index of last value                               | d.u.   | None        |
+-----------+---------------------------------------------------+--------+-------------+
| step      | step >= 1                                         | d.u.   | None        |
+-----------+---------------------------------------------------+--------+-------------+


Usage
-----

``stor = Storage('stor', ('N1', 'N2'), file='example.txt', integrate=False, start=None, stop=None, step=None)``

Netlist line
------------

``pwl.storage stor ('N1', 'N2'): file=example.txt; integrate=False; start=None; stop=None; step=None;``

Example
-------

>>> # Import dictionary
>>> from pyphs.dictionary import pwl
>>> # Define component label
>>> label = 'stor'
>>> # Define component nodes
>>> nodes = ('N1', 'N2')
>>> # Define component parameters
>>> parameters = {'file': 'example.txt',  # Path to data file for (x, H) or (x, dxH) values (string)
...               'integrate': False,     # If True, data is (x, dxH) and integrate to (x, H) (bool)
...               'start': None,          # Index of first value (d.u.)
...               'stop': None,           # Index of last value (d.u.)
...               'step': None,           # step >= 1 (d.u.)
...              }
>>> # Instanciate component
>>> component = pwl.Storage(label, nodes, **parameters)
>>> # Graph dimensions
>>> len(component.nodes)
2
>>> len(component.edges)
1

Reference
---------

.. [1] Chua, L., & Ying, R. (1983). Canonical piecewise-linear analysis. IEEE Transactions on Circuits and Systems, 30(3), 125-140.



