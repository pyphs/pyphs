.. title: Passive modeling and simulation in python
.. slug: index
.. date: 2016-11-13 20:05:17 UTC+01:00
.. tags: mathjax
.. category: 
.. link: 
.. description: 
.. type: text

.. image:: /figures/examples.jpg
	:width: 500
	:align: center

This is a companion site for the python package `PyPHS <https://github.com/afalaize/pyphs/>`__, developped in the `project/team S3 <http://s3.ircam.fr/?lang=en>`__ (Sound Signals and Systems) at `STMS Research Lab <http://www.ircam.fr/recherche/lunite-mixte-de-recherche-stms/>`__ (CNRS UMR 9912), hosted by `IRCAM <http://www.ircam.fr/>`__. 

This software is dedicated to the treatment of passive multiphysical systems in the Port-Hamiltonian Systems (PHS) formalism. 

.. image:: /galleries/intro/intro2.jpg
	:width: 650
	:align: center

It was initially developed between 2012 and 2016 as a part of the PhD project of `Antoine Falaize <https://afalaize.github.io/>`__, under the direction of `Thomas Hélie <http://recherche.ircam.fr/anasyn/helie/>`__,  through a funding from French doctoral school `EDITE <http://edite-de-paris.fr/spip/>`__ (UPMC ED-130), and in connection with the French National Research Agency project `HaMecMoPSys <https://hamecmopsys.ens2m.fr/>`__.

Licence
--------------
`PyPHS <https://github.com/afalaize/pyphs/>`__ is distributed under the french `CeCILL-B <http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html>`__ licence.

Installation
--------------

Using `pip <https://pypi.python.org/pypi/pip/>`__ (recommended): 
	.. code:: 
		
		pip install pyphs	
	
For `Anaconda <https://www.continuum.io/>`__ (**on Mac OSX only**):
	.. code:: 
		
		conda install -c afalaize pyphs

See also the `GitHub repository <https://github.com/afalaize/pyphs/>`__. 


Introduction
--------------

The Port-Hamiltonian Systems (PHS) formalism structures physical systems into

* energy conserving parts,
* power dissipating parts and
* source parts.

.. image:: /galleries/intro/intro1.jpg
	:width: 650
	:align: center

This guarantees a power balance is fulfilled, including for simulations based on an adapted numerical method.

1. Systems are described by directed multi-graphs: 

* use of `Networkx MultiDiGraph <https://networkx.github.io/>`__ for graph structure,
* use of `Sympy <http://www.sympy.org/>`__ for symbolic computations.

2. The time-continuous port-Hamiltonian structure is build from an automated graph analysis (see [GraphAnalysis2016]_).

3. The discrete-time port-Hamiltonian structure is derived from a structure preserving numerical method (see [NumericalMethod2015]_).

4. **LaTeX** description code and **C++** simulation code are automatically generated:
	
* Use of `Sympy <http://www.sympy.org/>`__ `Latex <http://docs.sympy.org/latest/modules/printing.html#module-sympy.printing.ccode>`__ and `CCode <http://docs.sympy.org/latest/modules/printing.html#module-sympy.printing.ccode>`__ printers.

Example
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
	electronics.diodepn D ('n1', 'n2'): Is=('Is', 2e-9); v0=('v0', 26e-3); mu=('mu', 1.7); R=('Rd', 0.5);
	electronics.inductor L ('n2', 'n3'): L=('L', 0.05);
	electronics.capacitor C ('n3', '#'): C=('C', 2e-06);

2. Perform graph analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run the following python code from the netlist file directory:

.. code:: python

  import pyphs
  netlist = pyphs.PHSNetlist('dlc.net')
  graph = pyphs.PHSGraph(netlist=netlist)
  core = graph.buildCore()

3. Export **LaTeX**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

	dlc.texwrite()

This yields the following **tex** file:
	
* `dlc.tex </pyphs_outputs/dlc/tex/dlc.tex>`__

which is compiled to produce the following **pdf** file:
	
* `dlc.pdf </pyphs_outputs/dlc/tex/dlc.pdf>`__


4. Export **C++**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

	dlc.simu.init(nt=10)
	dlc.cppbuild()
	dlc.cppwrite()
	
This yields the following **cpp** files:

* `phobj.cpp </pyphs_outputs/dlc/cpp/phobj.cpp>`__
* `phobj.h </pyphs_outputs/dlc/cpp/phobj.h>`__
* `data.cpp </pyphs_outputs/dlc/cpp/data.cpp>`__
* `data.h </pyphs_outputs/dlc/cpp/data.h>`__
* `main.cpp </pyphs_outputs/dlc/cpp/main.cpp>`__

The compilation and execution of **main.cpp** run the passive simulation (but, first, you must specify a sequence of input values).

References
-----------
.. [GraphAnalysis2016] Falaize, A., & Hélie, T. (2016). Passive Guaranteed Simulation of Analog Audio Circuits: A Port-Hamiltonian Approach. Applied Sciences, 6(10), 273.

.. [NumericalMethod2015] Lopes, N., Hélie, T., & Falaize, A. (2015). Explicit second-order accurate method for the passive guaranteed simulation of port-Hamiltonian systems. IFAC-PapersOnLine, 48(13), 223-228.


