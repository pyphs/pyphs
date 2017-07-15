.. title: Resistor
.. slug: resistor
.. date: 2016-11-16 18:12:37 UTC+01:00
.. tags: mathjax, components, dissipatives
.. category: electronics
.. link: 
.. description: 
.. type: text


.. image:: /dico/elec/inductor.jpg
	:width: 150
	:align: center

.. TEASER_END

Description
-------------

Linear free-controlled resistor with electric resistance $R$, voltage $v$ and current $i$:
$$
\\left\\{
\\begin{array}{rcl}
w(t) & = & i(t),  \\\\
v(t) & = &  R\\,w(t),
\\end{array}\\right.
$$

or

$$
\\left\\{
\\begin{array}{rcl}
w(t) & = & v(t),  \\\\
i(t) & = &  \\frac{w(t)}{R}.
\\end{array}\\right.
$$

Usage
------

.. line-block::
	
	electronics.resistor label ('N1', 'N2'): R=('Rsymb', Rval);

Parameters
-----------

label: 
	string, resistor label.

N1, N2: 
	strings, nodes labels. Positive direction of current is "N1 -> N2".

Rsymb: 
	string, resistance parameter symbol.

Rval: 
	strictly positive float, resistance parameter value.

Example
--------

For a resistor named *myR* with resistance $R_1=1$k$\\Omega$ between nodes *A* and *B*:

* In netlist.net

.. line-block::
	
	electronics.resistor myR ('A', 'B'): R=('R1', 1e3);

* In script.py

.. code:: python

	# resistor
	resistor = {'dictionary': 'electronics',
	            'component': 'resistor',
	            'label': 'myR',
	            'nodes': ('A', 'B'),
	            'arguments': {'R': ('R1', 1e3)}}
	phs.graph.netlist.add_line(resistor)
