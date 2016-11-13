======
pyphs
======

The python package **pyphs** is dedicated to the treatment of passive multiphy- sical systems in the Port-Hamiltonian Systems (PHS) formalism.
This formalism structures physical systems into
— energy conserving parts,
— power dissipating parts and
— source parts.
This guarantees a power balance is fulfilled, including for numerical simulations based on an adapted numerical method.

1. Systems are described by directed multi-graphs (networkx.MultiDiGraph).
2. The time-continuous port-Hamiltonian structure is build from an automated graph analysis.
3. The discrete-time port-Hamiltonian structure is derived from a structure preserving numerical method.
4. **LaTeX** description code and **C++** simulation code are automatically generated.

.. image:: docs/figures/pyphs_mindmap.png
   :height: 100
   :width: 200
   :scale: 50
   :alt: Package mindmap

Installation
--------------
It is recommanded to install **pyphs** using pip. In terminal:
``pip install pyphs``
An installation for *Anaconda* users **on Mac OSX** is also available (can be temporarily outdated, prefer pip install):
``conda install -c afalaize pyphs``

Documentation
--------------
Documentation and tutorials are hosted at the Python Package Index https://pypi.python.org/pypi/pyphs
