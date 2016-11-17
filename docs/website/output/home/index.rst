include .special.rst

.. title: Passive modeling and simulation in python
.. slug: index
.. date: 2016-11-13 20:05:17 UTC+01:00
.. tags: 
.. category: 
.. link: 
.. description: 
.. type: text

.. image:: /figures/examples.jpg
	:width: 500
	:align: center

This is a companion site for the python package `PyPHS <https://github.com/afalaize/pyphs/>`__, developped in the `project/team S3 <http://s3.ircam.fr/?lang=en>`__ (Sound Signals and Systems) at `STMS Research Lab <http://www.ircam.fr/recherche/lunite-mixte-de-recherche-stms/>`__ (CNRS UMR 9912), hosted by `IRCAM <http://www.ircam.fr/>`__. 

This software is dedicated to the treatment of passive multiphysical systems in the Port-Hamiltonian Systems (PHS) formalism. 

It was initially developed between 2012 and 2016 as a part of the PhD project of `Antoine Falaize <https://afalaize.github.io/>`__, under the direction of `Thomas Hélie <http://recherche.ircam.fr/anasyn/helie/>`__,  through a funding from French doctoral school `EDITE <http://edite-de-paris.fr/spip/>`__ (UPMC ED-130), and in connection with the French National Research Agency project `HaMecMoPSys <https://hamecmopsys.ens2m.fr/>`__.


Licence
--------------
`PyPHS <https://github.com/afalaize/pyphs/>`__ is distributed under the french `CeCILL-B <http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html>`__ licence.

Installation
--------------

* Using `pip <https://pypi.python.org/pypi/pip/>`__ (recommended):

	.. code:: 
		
		pip install pyphs
	
	
* See the `GitHub repository <https://github.com/afalaize/pyphs/>`__. 


* For `Anaconda <https://www.continuum.io/>`__ (**on Mac OSX only**):

	.. code:: 
		
		conda install -c afalaize pyphs


Introduction
--------------

The Port-Hamiltonian Systems (PHS) formalism structures physical systems into

* :blues:`energy conserving parts`,
* :blues:`power dissipating parts` and
* :blues:`source parts`.

This guarantees a power balance is fulfilled, including for simulations based on an adapted numerical method.

.. image:: /figures/examples.jpg
	:width: 500
	:align: center

.. image:: /figures/examples2.jpg
	:width: 400
	:align: center

1. Systems are described by directed multi-graphs.

2. The time-continuous port-Hamiltonian structure is build from an automated graph analysis.

3. The discrete-time port-Hamiltonian structure is derived from a structure preserving numerical method.

4. **LaTeX** description code and **C++** simulation code are automatically generated.

.. image:: /galleries/intro/intro1.jpg
	:width: 650
	:align: center

.. image:: /galleries/intro/intro2.jpg
	:width: 650
	:align: center

Example
--------------

Consider the following serial resistor-inductor-capacitor (RLC) electronic circuit:

.. image:: /figures/RLC.jpg
	:width: 400
	:align: center

1. Define the Netlist
~~~~~~~~~~~~~~~~~~~~~~

Put the following content in a text file with **.net** extension, (here *rlc_netlist.net*):

.. line-block::

	electronics.source out ('ref', 'A'): type='voltage';
	electronics.resistor R1 ('A', 'B'): R=1e3;
	electronics.inductor L1 ('B', 'C'): L=0.05;
	electronics.capacitor C1 ('C', 'ref'): C=2e-06;

2. Perform graph analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run the following python code from the netlist file directory:

.. code:: python

  import pyphs
  rlc = pyphs.PortHamiltonianObject(label='rlc', path='label')
  rlc.build_from_netlist('rlc_netlist.net')

3. Export **LaTeX**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

	rlc.texwrite()

This yields the following **tex** file:
	
* `rlc.tex </pyphs_outputs/RLC/tex/rlc.tex>`__

which is compiled to produce the following **pdf** file:
	
* `rlc.pdf </pyphs_outputs/RLC/tex/rlc.pdf>`__


4. Export **C++**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

	rlc.simu.init(nt=10)
	rlc.cppbuild()
	rlc.cppwrite()
	
This yields the following **cpp** files:

* `phobj.cpp </pyphs_outputs/RLC/cpp/phobj.cpp>`__
* `phobj.h </pyphs_outputs/RLC/cpp/phobj.h>`__
* `data.cpp </pyphs_outputs/RLC/cpp/data.cpp>`__
* `data.h </pyphs_outputs/RLC/cpp/data.h>`__
* `main.cpp </pyphs_outputs/RLC/cpp/main.cpp>`__

The compilation and execution of **main.cpp** run the passive simulation (no input here).
