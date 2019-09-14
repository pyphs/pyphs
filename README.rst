PyPHS
======

|pypi version| |Licence badge| |python versions| |Website badge|

.. |pypi version| image:: https://badge.fury.io/py/pyphs.svg
    :target: https://badge.fury.io/py/pyphs
.. |Licence badge| image:: https://img.shields.io/badge/licence-CeCILL--B-blue.svg
    :target: http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
.. |python versions| image:: https://img.shields.io/badge/python-2.7%2C%203.5%2C%203.6%2C%203.7-blue.svg
    :target: https://github.com/pyphs/pyphs
.. |Website badge| image:: https://img.shields.io/badge/documentation-website-blue.svg
    :target: https://pyphs.github.io/pyphs/

A Python software (Py) dedicated to the simulation of multi-physical Port-Hamiltonian Systems (PHS) described by graph structures.

The PHS formalism decomposes network systems into **conservative** parts, **dissipative** parts and **source** parts, which are combined according to an **energy conserving interconnection**. This approach permits to formulate the dynamics of multi-physical systems as a **set of differential-algebraic equations** structured according to energy flows. This **structure** proves the **passivity** of the system, including the nonlinear cases. Moreover, it guarantees the **stability** of the numerical simulations for an adapted structure preserving numerical method.

.. image:: https://pyphs.github.io/pyphs/figures/home2.png
	:width: 650
	:align: center

The main objects of the library are introduced in `this presentation <https://pyphs.github.io/pyphs/PyPHS_IRCAM_seminar_041217.pdf>`_.
The standard workflow is as follows.

1. Inputs are **netlist descriptions** of network systems (very similar to SPICE netlists).
2. The associated **graphs** are analyzed to produce the **core system's dynamics equations** in the PHS formalism.
3. **Simulations** (i.e. numerical solving of DAE equations) are performed based on a variety of **numerical methods** (can be extended with new ones).
4. The corresponding **C++** simulation code is automatically generated and called from python (can also be used in bigger applications).
5. **LaTeX** description files can be generated (for documentation, publication, etc.).

.. image:: https://pyphs.github.io/pyphs/figures/synopsys.png
    :width: 800
    :align: center

- The Python class **Core** defines symbolically a *continuous-time Port-Hamiltonian structure*.
- The Python class **Method** defines symbolically a *discrete-time port-Hamiltonian structure* derived from a given `Core` object and for several numerical schemes. It includes a structure preserving numerical method (see [NumericalMethod2015]_).
- The Python class **Netlist** reads and writes the descriptions of network systems.
- The Python class **Graph** defines a network structure for the automated generation of `Core` from `Netlist`, based on (i) the implementation of a specially designed **graph analysis** (see [GraphAnalysis2016]_), and (ii) a set of elementary **components** compiled in the **Dictionary**.
- The Python class **Simulation** evaluates iteratively a given `Method` object to produce the data result in text files. The evaluation can run in pure Python code with the **Numerical** object, or can run in C++ through the generated C++ files.

Status
======

This package is in development status Beta. The continuous integration is checked with Travis for Unix systems and AppVeyor for Windows systems (see build status below).

|Travis|  |Appveyor|  |Codecov|


.. |Travis| image:: https://www.travis-ci.org/pyphs/pyphs.svg?branch=master
    :target: https://www.travis-ci.org/pyphs/pyphs


.. |Appveyor| image:: https://ci.appveyor.com/api/projects/status/53d7phhgksrd4fvn?svg=true
    :target: https://ci.appveyor.com/project/pyphsadmin/pyphs


.. |Codecov| image:: https://codecov.io/gh/pyphs/pyphs/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/pyphs/pyphs


Licence
=======
`PyPHS <https://github.com/pyphs/pyphs/>`_ is distributed under the GNU General Public License v3.0. In short, permissions of this strong copyleft license are conditioned on making available complete source code of licensed works and modifications, which include larger works using a licensed work, under the same license. Copyright and license notices must be preserved. Contributors provide an express grant of patent rights.



Installation
==============
It is possible to install `PyPHS <https://github.com/pyphs/pyphs/>`_ from package (if you just want to use it) or source (if you plan to use it for development). Whichever method you choose, make sure that all prerequisites are installed.

Python prerequisites
--------------------

The `PyPHS <https://github.com/pyphs/pyphs/>`_ package run on Python 2.7 and Python
3.5 or newer (3.4 is no longer tested), with the following packages installed:

- `sympy <http://www.sympy.org/fr/>`_
- `numpy <http://www.numpy.org>`_
- `scipy <http://www.scipy.org>`_
- `matplotlib <http://matplotlib.org/>`_
- `networkx <http://networkx.github.io/>`_
- `h5py <http://docs.h5py.org/en/latest/index.html>`_
- `stopit <https://pypi.python.org/pypi/stopit>`_
- `progressbar2 <https://pypi.python.org/pypi/progressbar2>`_
- `nose <https://github.com/nose-devs/nose>`_ (optional to run the tests)

Please refer to the `requirements.txt <requirements.txt>`_ file for the required
versions and make sure that these modules are up to date.

Additionally, `theano <http://deeplearning.net/software/theano/>`_ is used if it can be found on the system, for faster numerical evaluation of symbolic expressions.

C++ prerequisites
------------------

The generated C++ sources build with `CMake <https://cmake.org/>`_ >= 3.1 (see **Configuration** below). The code relies on the `Eigen library <http://eigen.tuxfamily.org/index.php?title=Main_Page>`_ (not needed for pure Python usage).

Install from package
--------------------

The easiest way to install the package is via `pip` from the `PyPI (Python
Package Index) <https://pypi.python.org/pypi>`_::

    pip install pyphs

This includes the latest code and should install all dependencies automatically. If it complains about some missing dependencies, install them the same way with `pip` beforehand.

You might need higher privileges (use su or sudo) to install the package globally. Alternatively you can install the package locally
(i.e. only for you) by adding the `--user` argument::

    pip install --user pyphs

Install from source
-------------------

If you plan to use the package as a developer, clone the Git repository::

    git clone --recursive https://github.com/pyphs/pyphs.git

Then you can simply install the package in development mode::

    python setup.py develop --user

To run the included tests::

    python setup.py test

Configuration
--------------

After installation, it is recommended to configure the `config.py <https://github.com/pyphs/pyphs/tree/master/pyphs/config.py>`_ to your needs. Particularly, this is where the local path to the CMake binary is specified.

Your local `config.py <https://github.com/pyphs/pyphs/tree/master/pyphs/config.py>`_ file is located at the root of the `PyPHS <https://github.com/pyphs/pyphs/>`_ package, which can be recovered in a Python interpreter with


.. code:: python

    from pyphs import path_to_configuration_file
    print(path_to_configuration_file)


Upgrade of existing installations
---------------------------------

To upgrade the package, please use the same mechanism (pip vs. source) as you did for installation.

Upgrade a package
~~~~~~~~~~~~~~~~~

First, manually uninstall the package::

    pip uninstall pyphs

and reinstall as explained above.


Upgrade from source
~~~~~~~~~~~~~~~~~~~

Pull the latest sources::

    git pull

Package structure
=================

The package is divided into the following folders:

`/pyphs/tutorials <https://github.com/pyphs/pyphs/tree/master/pyphs/tutorials>`_
    Tutorials for the main `PyPHS <https://github.com/pyphs/pyphs/>`_ classes (executable programs).
`/pyphs/examples <https://github.com/pyphs/pyphs/tree/master/pyphs/examples>`_
    Various real-life applications (executable programs).
`/pyphs/core <https://github.com/pyphs/pyphs/tree/master/pyphs/core>`_
    `Core` class :
        This is the central object of the `PyPHS <https://github.com/pyphs/pyphs/>`_ package. It implements the core PHS structure and provides several methods for its manipulation (reorganization, connection, simplification, etc.).
`/pyphs/graphs <https://github.com/pyphs/pyphs/tree/master/pyphs/graphs>`_
    `Netlist` class :
        Management of netlist description files.
    `Graph` class :
        (1) Construction and manipulation of network systems,
        (2) Analysis of network realizability,
        (3) Generation of PHS equations (`Core`).
`/pyphs/dictionary <https://github.com/pyphs/pyphs/tree/master/pyphs/dictionary>`_
    - Components are `Graph` objects.
    - The dictionary is organized in thematic sub-packages (*electronics*, *thermics*, *fractional calculus*, etc.).
    - Each theme is organized in component sub-packages (`electronics.resistor`, `thermics.transfer`, `fraccalc.fracderec`, etc.).
`/pyphs/numerics <https://github.com/pyphs/pyphs/tree/master/pyphs/numerics>`_
    `Evaluation` class :
        Numerical evaluation of a given `Core`.
    `Method` object :
        Construction of the *symbolic* expressions associated with several numerical methods (theta-schemes, trapezoidal rule, discret gradient, etc.).
    `Simulation` object :
        Manage the iterative evaluation and associated results data for a given `Method`.
    `Numeric` object :
        Python evaluation of a given `Method`.
    `Data` object :
        Methods for writing, reading and rendering `Simulation` file results.
`/pyphs/tests <https://github.com/pyphs/pyphs/tree/master/pyphs/tests>`_
    Test programs executed by `nose` (see above).
`/pyphs/misc <https://github.com/pyphs/pyphs/tree/master/pyphs/misc>`_
    Miscellaneous tools (plots, LaTeX code generation, signal processing, files I/O).

Documentation
==============

Most of the documentation can be found in the `website <https://pyphs.github.io/pyphs/>`_.
In particular, you can see the two following resources:

- The `slides <https://pyphs.github.io/pyphs/PyPHS_IRCAM_seminar_041217.pdf>`_ from a talk given at IRCAM that introduces most the scientific background.
- The `tutorial <https://pyphs.github.io/pyphs/PyPHS_TUTORIAL.zip>`_ that shows practical usage of most PyPHS objects (3Mb).



Theoretical overview
--------------------

The development of `PyPHS <https://github.com/pyphs/pyphs/>`_ started as an implementation of the methods proposed in the reference [GraphAnalysis2016], in which the port-Hamiltonian formalism, the graph analysis and the structure preserving numerical method are exposed. This is worth to read before using the package.

Q&A Mailing list
-----------------

The package mailing list is at https://groups.google.com/forum/#!forum/pyphs.

Tutorials and examples
-----------------------

The package comes with a set of tutorials for the use of the main functionalities (`definition <https://github.com/pyphs/pyphs/tree/master/pyphs/tutorials/core.py>`_, `evaluation <https://github.com/pyphs/pyphs/tree/master/pyphs/tutorials/evaluation.py>`_, and `simulation <https://github.com/pyphs/pyphs/tree/master/pyphs/tutorials/simulation.py>`_ of a core PHS structure). More tutorials are to come. Additionally, you can see the `examples <https://github.com/pyphs/pyphs/tree/master/pyphs/examples>`_ scripts. Both the *tutorials* and the *examples* folders are located at your package root, which can be recovered in Python interpreter with


.. code:: python

    from pyphs import path_to_examples, path_to_tutorials
    print(path_to_examples)
    print(path_to_tutorials)

Typical use
===========

Consider the following serial diode-inductor-capacitor (DLC) electronic circuit:

.. image:: https://pyphs.github.io/pyphs/figures/DLC.jpg
    :width: 300
    :align: center

with the following physical parameters:

+------------+------------------------------------------+----------------+
| Parameter  | Description (SI unit)                    | Typical value  |
+------------+------------------------------------------+----------------+
| Is         | Diode saturation current (A)             | 2e-9           |
+------------+------------------------------------------+----------------+
| v0         |  Diode thermal voltage (V)               | 26e-3          |
+------------+------------------------------------------+----------------+
| mu         |  Diode ideality factor (dimensionless)   | 1.7            |
+------------+------------------------------------------+----------------+
| R          |  Diode connectors resistance (Ohms)      | 0.5            |
+------------+------------------------------------------+----------------+
| L          |  Inductance value (H)                    | 0.05           |
+------------+------------------------------------------+----------------+
| C          |  Capacitance value (F)                   | 2e-06          |
+------------+------------------------------------------+----------------+


1. Define the Netlist
---------------------

Put the following content in a text file with **.net** extension, (here *dlc.net*):

.. line-block::
    electronics.source in ('#', 'n1'): type='voltage';
    electronics.diode D ('n1', 'n2'): Is=('Is', 2e-9); v0=('v0', 26e-3); mu=('mu', 1.7); R=('Rd', 0.5);
    electronics.inductor L ('n2', 'n3'): L=('L', 0.05);
    electronics.capacitor C ('n3', '#'): C=('C', 2e-06);


2. Perform graph analysis
-------------------------

Run the following in a Python interpreter in the netlist file directory:

.. code:: python

    import pyphs as phs

    # Read the 'dlc_netlist.net'
    netlist = phs.Netlist('dlc.net')

    # Construct the graph associated with 'netlist'
    graph = netlist.to_graph()

    # Construct the core Port-Hamiltonian System from 'graph'
    core = graph.to_core()


3. Export LaTeX
----------------------------

.. code:: python

    # Add netlist to LaTeX content
    content = phs.netlist2tex(netlist)

    # Add PHS core to LaTeX content
    content += phs.core2tex(core)

    # Write ready-to-use .tex document
    phs.texdocument(content,
                    title='DLC',
                    path='dlc.tex')


This yields the following **tex** file:

* `dlc.tex <https://pyphs.github.io/pyphs/pyphs_outputs/dlc/tex/dlc.tex>`_

which is compiled to produce the following **pdf** file:

* `dlc.pdf <https://pyphs.github.io/pyphs/pyphs_outputs/dlc/tex/dlc.pdf>`_


4. Export C++ code
----------------------------

.. code:: python

    # Numerical method for time discretization of 'core'
    # with default configuration
    method = core.to_method()

    # Export the set of C++ file for simulation
    method.to_cpp()


This yields the following **cpp** files:

* `core.cpp <https://pyphs.github.io/pyphs/pyphs_outputs/dlc/cpp/core.cpp>`_
* `core.h <https://pyphs.github.io/pyphs/pyphs_outputs/dlc/cpp/core.h>`_
* `parameters.cpp <https://pyphs.github.io/pyphs/pyphs_outputs/dlc/cpp/parameters.cpp>`_
* `parameters.h <https://pyphs.github.io/pyphs/pyphs_outputs/dlc/cpp/parameters.h>`_

The `core.h` defines a class of `DLC` systems with an update method to be called at each iteration for the simulations.


Authors and Affiliations
========================

PyPHS is mainly developed by `Antoine Falaize <https://afalaize.github.io/>`_ and `Thomas Hélie <http://recherche.ircam.fr/anasyn/helie/>`_, respectively in

- the `Team M2N <http://lasie.univ-larochelle.fr/Axe-AB-17>`_ (Mathematical and Numerical Methods), `LaSIE Research Lab <http://lasie.univ-larochelle.fr>`_ (CNRS UMR 7356), hosted by the `University of La Rochelle <http://www.univ-larochelle.fr/>`_,
- the `Team S3AM <http://s3.ircam.fr/?lang=en>`_ (Sound Systems and Signals: Audio/Acoustics, InstruMents) at `STMS Research Lab <http://www.ircam.fr/recherche/lunite-mixte-de-recherche-stms/>`_ (CNRS UMR 9912), hosted by `IRCAM <http://www.ircam.fr/>`_ in Paris.

See the `AUTHORS <https://github.com/pyphs/pyphs/blob/master/AUTHORS>`_ file for the complete list of authors.


Short History
==============

The ideas behind PyPHS where developed between 2012 and 2016 as a part of the PhD thesis of `Antoine Falaize <https://afalaize.github.io/>`_ under the direction of `Thomas Hélie <http://recherche.ircam.fr/anasyn/helie/>`_, through a funding from  the French doctoral school `EDITE <http://edite-de-paris.fr/spip/>`_ (UPMC ED-130) and in connection with the French National Research Agency project `HaMecMoPSys <https://hamecmopsys.ens2m.fr/>`_.


References
==========

.. [NumericalMethod2015] Lopes, N., Hélie, T., & Falaize, A. (2015). Explicit second-order accurate method for the passive guaranteed simulation of port-Hamiltonian systems. IFAC-PapersOnLine, 48(13), 223-228.

.. [GraphAnalysis2016] Falaize, A., & Hélie, T. (2016). Passive Guaranteed Simulation of Analog Audio Circuits: A Port-Hamiltonian Approach. Applied Sciences, 6(10), 273.
