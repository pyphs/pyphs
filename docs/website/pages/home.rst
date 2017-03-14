.. title: PyPHS: Passive modeling and simulation in python
.. slug: index
.. date: 2016-11-13 20:05:17 UTC+01:00
.. tags: mathjax
.. category: 
.. link: 
.. description: 
.. type: text

Welcome to PyPHS!
------------------
PyPHS is a Python (2.7-3.5) package that implements a set of numerical methods for the simulation of multi-physical systems with the *Port-Hamiltonian Systems* approach.

.. image:: /figures/home2.png
	:width: 650
	:align: center

It provides:

1. A python class `pyphs.PHSCore` that encodes the core **Port-Hamiltonian structure**. 
2. An automated generation of PHS cores from **netlists** through 

(i) the implementation of a specially designed **graph analysis** (see [GraphAnalysis2016]_), and 
(ii) a set of elementary **components** compiled in a **dictionary**.

3. A python class `pyphs.PHSSimulation` that runs the simulation of a discrete-time port-Hamiltonian structure, derived from a structure preserving numerical method (see [NumericalMethod2015]_). 
4. An automated C++ and $\LaTeX$ code generation.

.. image:: /figures/home1.png
	:width: 580
	:align: center

Installation
--------------

* From sources with `pip <https://pypi.python.org/pypi/pip/>`_:

.. code:: 
	
	pip install pyphs
	
	
* From a download of the `PyPHS <https://github.com/afalaize/pyphs/>`_ package from the `GitHub repository <https://github.com/afalaize/pyphs/>`_, execute in the package folder (that contains a `setup.py` file):

- with `setuptools <https://setuptools.readthedocs.io/en/latest/>`_
	
.. code:: 
	
	python setup.py install

- with `pip <https://pypi.python.org/pypi/pip/>`_

.. code:: 
	
	pip install .


Typical use
--------------

Consider the following serial diode-inductor-capacitor (DLC) electronic circuit:

.. image:: /figures/DLC.jpg
	:width: 300
	:align: center

with the following physical parameters:

+------------+------------------------------------------+----------------+
| Parameter  | Description (SI unit)                    | Typical value  |
+------------+------------------------------------------+----------------+
| $I_s$      | Diode saturation current (A)             | 2e-9           |
+------------+------------------------------------------+----------------+
| $v_0$      |  Diode thermal voltage (V)               | 26e-3          |
+------------+------------------------------------------+----------------+
| $\\mu$     |  Diode ideality factor (dimensionless)   | 1.7            |
+------------+------------------------------------------+----------------+
| $R$        |  Diode connectors resistance ($\\Omega$) | 0.5            |
+------------+------------------------------------------+----------------+
| $L$        |  Inductance value (H)                    | 0.05           |
+------------+------------------------------------------+----------------+
| $C$        |  Capacitance value (F)                   | 2e-06          |
+------------+------------------------------------------+----------------+



1. Define the Netlist
~~~~~~~~~~~~~~~~~~~~~~

Put the following content in a text file with **.net** extension, (here *dlc.net*):

.. line-block::

	electronics.source in ('#', 'n1'): type='voltage';
	electronics.diode D ('n1', 'n2'): Is=('Is', 2e-9); v0=('v0', 26e-3); mu=('mu', 1.7); R=('Rd', 0.5);
	electronics.inductor L ('n2', 'n3'): L=('L', 0.05);
	electronics.capacitor C ('n3', '#'): C=('C', 2e-06);

2. Perform graph analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run the following python code from the netlist file directory:

.. code:: python

	import pyphs
	
	# Read the 'dlc_netlist.net'
	netlist = pyphs.PHSNetlist('dlc.net')
	
	# Construct the graph associated with 'netlist'
	graph = pyphs.PHSGraph(netlist)
	
	# Construct the core Port-Hamiltonian System from 'graph'
	core = graph.buildCore()
	
3. Export $\\LaTeX$
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

	content = pyphs.netlist2tex(netlist)
	content += pyphs.core2tex(core)
	pyphs.texdocument(content, title='DLC', filename='dlc.tex')

This yields the following **tex** file:
	
* `dlc.tex </pyphs_outputs/dlc/tex/dlc.tex>`__

which is compiled to produce the following **pdf** file:
	
* `dlc.pdf </pyphs_outputs/dlc/tex/dlc.pdf>`__


4. Export $\\mathrm{C_{++}}$
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

	
	# Numerical method for time discretization of 'core'
	method = pyphs.PHSNumericalMethod(core)
	
	# Numerical evaluation of 'method'
	numcore = pyphs.PHSNumericalCore(method)
	
	# Export the set of C++ file for simulation
	pyphs.numcore2cpp(numcore)
	
This yields the following **cpp** files:

* `phobj.cpp </pyphs_outputs/dlc/cpp/phobj.cpp>`__
* `phobj.h </pyphs_outputs/dlc/cpp/phobj.h>`__
* `data.cpp </pyphs_outputs/dlc/cpp/data.cpp>`__
* `data.h </pyphs_outputs/dlc/cpp/data.h>`__

The `phobj.h` defines a class of `DLC` systems with passive update method for simulations.

Licence
--------------
`PyPHS <https://github.com/afalaize/pyphs/>`__ is distributed under the french `CeCILL-B <http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html>`__ licence.

Acknowledgement
-----------------
This software is currently developped by `Antoine Falaize <https://afalaize.github.io/>`__ (LaSIE, CNRS UMR 7356, ULR) in association with the `project/team S3 <http://s3.ircam.fr/?lang=en>`__ (Sound Signals and Systems) at `STMS Research Lab <http://www.ircam.fr/recherche/lunite-mixte-de-recherche-stms/>`__ (CNRS UMR 9912), hosted by `IRCAM <http://www.ircam.fr/>`__. 

The developpement of PyPHS began as a part of the PhD project of `Antoine Falaize <https://afalaize.github.io/>`__, under the direction of `Thomas Hélie <http://recherche.ircam.fr/anasyn/helie/>`__,  through a funding from French doctoral school `EDITE <http://edite-de-paris.fr/spip/>`__ (UPMC ED-130), and in connection with the French National Research Agency project `HaMecMoPSys <https://hamecmopsys.ens2m.fr/>`__ between 2012 and 2016.

References
-----------
.. [GraphAnalysis2016] Falaize, A., & Hélie, T. (2016). Passive Guaranteed Simulation of Analog Audio Circuits: A Port-Hamiltonian Approach. Applied Sciences, 6(10), 273.

.. [NumericalMethod2015] Lopes, N., Hélie, T., & Falaize, A. (2015). Explicit second-order accurate method for the passive guaranteed simulation of port-Hamiltonian systems. IFAC-PapersOnLine, 48(13), 223-228.


