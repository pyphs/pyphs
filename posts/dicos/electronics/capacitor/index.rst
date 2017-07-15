.. title: Capacitor
.. slug: capacitor
.. date: 2016-11-16 18:12:20 UTC+01:00
.. tags: mathjax, components, storages
.. category: electronics
.. link: 
.. description: 
.. type: text


.. image:: /dico/elec/capacitor.jpg
	:width: 150
	:align: center

.. TEASER_END

Description
-------------

Linear flux-controlled capacitor with electric charge $q$, capacitance $C$, voltage $v$ and current $i$:
$$
\\left\\{
\\begin{array}{rcl}
\\frac{\\mathrm{d} q(t)}{\\mathrm{d} t} & = & i(t),  \\\\
v(t) & = &  \\frac{q(t)}{C}.
\\end{array}\\right.
$$

Usage
------

.. line-block::
	
	electronics.capacitor label ('N1', 'N2'): C=('Csymb', Cval);

Parameters
-----------

label: 
	string, capacitor label.

N1, N2: 
	strings, nodes labels. Positive direction of current is "N1 -> N2".

Csymb: 
	string, capacitance parameter symbol.

Cval: 
	float, capacitance parameter value.

Example
--------

For a capacitor named *myC* with electric capacitance $C_1=2\\mu$F between nodes *A* and *B*:

* In netlist.net

.. line-block::
	
	electronics.capacitor myC ('A', 'B'): C=('C1', 2e-6);

* In script.py

.. code:: python

	# capacitor
	capacitor = {'dictionary': 'electronics',
	             'component': 'capacitor',
	             'label': 'myC',
	             'nodes': ('A', 'B'),
	             'arguments': {'C': ('C1', 2e-6)}}
	phs.graph.netlist.add_line(capacitor)
