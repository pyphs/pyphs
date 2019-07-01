
.. title: Cantilever beam (Cantilever)
.. slug: beams-Cantilever
.. date: 2019-04-28 12:31:26.773441
.. tags: beams, mathjax
.. category: component
.. type: text

Euler-Bernouilli cantilever beam as presented in [1]_ (section 4.2).

.. TEASER_END


==============================
 Cantilever beam (Cantilever) 
==============================


Euler-Bernouilli cantilever beam as presented in [1]_ (section 4.2).

Power variables
---------------

**flux**: Force :math:`f`   (N)

**effort**: Velocity :math:`v`   (m.s)

Arguments
---------

label : str
    Cantilever label.

nodes : ('N1', 'N2')
    Any number of nodes associated with contact points. An effort-controlled port (u=force, y=velocity) is created for each node in the list. Two parameters (position 'w#' and width 'z#') must be provided for each contact point #.

parameters : keyword arguments
    The default values are taken from [1]_ (table 4) with two contact point N1 and N2.

+-----+--------------------------------+--------+----------------+
| Key | Description                    | Unit   | Default        |
+=====+================================+========+================+
| F   | Fondamental frequency          | Hz     | 440.0          |
+-----+--------------------------------+--------+----------------+
| N   | Number of eigen-modes          | d.u    | 5              |
+-----+--------------------------------+--------+----------------+
| R   | Radius                         | m      | 0.001          |
+-----+--------------------------------+--------+----------------+
| E   | Young modulus                  | N/m2   | 180000000000.0 |
+-----+--------------------------------+--------+----------------+
| M   | Mass density                   | kg/m3  | 7750           |
+-----+--------------------------------+--------+----------------+
| A   | Damping coefficient            | N/s    | 0.05           |
+-----+--------------------------------+--------+----------------+
| D   | Modes damping progression      | d.u    | 6.0            |
+-----+--------------------------------+--------+----------------+
| z1  | Relative position of contact 1 | [0, 1] | 0.15           |
+-----+--------------------------------+--------+----------------+
| w1  | width of contact 1             | m      | 0.015          |
+-----+--------------------------------+--------+----------------+
| z2  | Relative position of contact 2 | [0, 1] | 1.0            |
+-----+--------------------------------+--------+----------------+
| w2  | width of contact 2             | m      | 0.0            |
+-----+--------------------------------+--------+----------------+


Usage
-----

``beam = Cantilever('beam', ('N1', 'N2'), F=440.0, N=5, R=0.001, E=180000000000.0, M=7750, A=0.05, D=6.0, z1=0.15, w1=0.015, z2=1.0, w2=0.0)``

Netlist line
------------

``beams.cantilever beam ('N1', 'N2'): F=440.0; N=5; R=0.001; E=180000000000.0; M=7750; A=0.05; D=6.0; z1=0.15; w1=0.015; z2=1.0; w2=0.0;``

Example
-------

>>> # Import dictionary
>>> from pyphs.dictionary import beams
>>> # Define component label
>>> label = 'beam'
>>> # Define component nodes
>>> nodes = ('N1', 'N2')
>>> # Define component parameters
>>> parameters = {'F': 440.0,           # Fondamental frequency (Hz)
...               'N': 5,               # Number of eigen-modes (d.u)
...               'R': 0.001,           # Radius (m)
...               'E': 180000000000.0,  # Young modulus (N/m2)
...               'M': 7750,            # Mass density (kg/m3)
...               'A': 0.05,            # Damping coefficient (N/s)
...               'D': 6.0,             # Modes damping progression (d.u)
...               'z1': 0.15,           # Relative position of contact 1 ([0, 1])
...               'w1': 0.015,          # width of contact 1 (m)
...               'z2': 1.0,            # Relative position of contact 2 ([0, 1])
...               'w2': 0.0,            # width of contact 2 (m)
...              }
>>> # Instanciate component
>>> component = beams.Cantilever(label, nodes, **parameters)
>>> # Graph dimensions
>>> len(component.nodes)
16
>>> len(component.edges)
35

Reference
---------

.. [1] Antoine Falaize and Thomas Helie. Passive simulation of the nonlinear port-hamiltonian modeling of a Rhodes piano. Journal of Sound and Vibration, 2016.



