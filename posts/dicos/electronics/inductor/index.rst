.. title: Inductor
.. slug: inductor
.. date: 2016-11-16 18:12:27 UTC+01:00
.. tags: mathjax, components, storages
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

Linear voltage-controlled iductor with total magnetic flux $p$, inductance $L$, voltage $v$ and current $i$:
$$
\\left\\{
\\begin{array}{rcl}
\\frac{\\mathrm{d} p(t)}{\\mathrm{d} t} & = & v(t),  \\\\
i(t) & = &  \\frac{p(t)}{L}.
\\end{array}\\right.
$$

Usage
------

.. line-block::
	
	electronics.inductor label ('N1', 'N2'): L=('Lsymb', Lval);

Parameters
-----------

label: 
	string, inductor label.

N1, N2: 
	strings, nodes labels. Positive direction of current is "N1 -> N2".

Lsymb: 
	string, inductance parameter symbol.

Lval: 
	strictly positive float, inductance parameter value.

Example
--------

For an inductor named *myL* with inductance $L_1=50$mH between nodes *A* and *B*:

* In netlist.net

.. line-block::
	
	electronics.inductor myL ('A', 'B'): C=('L1', 5e-2);

* In script.py

.. code:: python

	# inductor
	inductor = {'dictionary': 'electronics',
	            'component': 'inductor',
	            'label': 'myL',
	            'nodes': ('A', 'B'),
	            'arguments': {'L': ('L1', 5e-2)}}
	phs.graph.netlist.add_line(inductor)
