.. title: Welcome!
.. slug: index
.. date: 2016-11-13 20:05:17 UTC+01:00
.. tags: 
.. category: 
.. link: 
.. description: 
.. type: text


This is a companion site for the python package **pyphs**, which is dedicated to the treatment of passive multiphysical systems in the Port-Hamiltonian Systems (PHS) formalism. This formalism structures physical systems into
— energy conserving parts,
— power dissipating parts and
— source parts.
This guarantees a power balance is fulfilled, including for numerical simulations based on an adapted numerical method.

1. Systems are described by directed multi-graphs (networkx.MultiDiGraph).
2. The time-continuous port-Hamiltonian structure is build from an automated graph analysis.
3. The discrete-time port-Hamiltonian structure is derived from a structure preserving numerical method.
4. **LaTeX** description code and **C++** simulation code are automatically generated.

Installation
--------------
It is recommanded to use `pip <https://pypi.python.org/pypi/pip/>`__. In terminal:
	``pip install pyphs``

An installation for `Anaconda <https://www.continuum.io/>`__ users **on Mac OSX** is also available:
	``conda install -c afalaize pyphs``

See also the `GitHub repository <https://github.com/afalaize/pyphs/>`__. 
