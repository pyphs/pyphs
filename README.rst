PyPHS
======
|pypi version| |Licence| |Python| |Website|

.. |pypi version| image:: https://badge.fury.io/py/pyphs.svg
    :target: https://badge.fury.io/py/pyphs
.. |Licence| image:: https://img.shields.io/badge/licence-CeCILL--B-blue.svg
    :target: http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
.. |Python| image:: https://img.shields.io/badge/python-2.7%2C%203.5%2C%203.6-blue.svg
    :target: https://www.travis-ci.org/pyphs/pyphs
   :target: https://gitter.im/sympy/sympy?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
.. |Website| image:: https://img.shields.io/badge/documentation-website-blue.svg
    :target: https://pyphs.github.io/pyphs/

A Python software (Py) dedicated to the simulation of multiphysical Port-Hamiltonian Systems (PHS) described by graph structures.

1. Inputs are netlist description of network systems (very similar to SPICE netlists).
2. The associated graphs are analyzed to produce the system's dynamics equations in the PHS formalism.
3. Simulations (i.e. numerical solving of DAE equations) are performed based on a variety of numerical methods (can be extended with new ones).
4. The corresponding C++ simulation code is automatically generated and called from python (can also be used in bigger applications).
5. LaTeX description files can be generated (for documentation, publication, etc.).

.. image:: https://pyphs.github.io/pyphs/figures/synopsys.png
    :width: 800
    :align: center

Affiliations
=============

PyPHS is developed by `Antoine Falaize <https://afalaize.github.io/>`_ in the `Team M2N <http://lasie.univ-larochelle.fr/Axe-AB-17>`_ (Mathematical and Numerical Methods) at the `LaSIE Research Lab <http://lasie.univ-larochelle.fr>`_ (CNRS UMR 7356), hosted by `Université de La Rochelle <http://www.univ-larochelle.fr/>`_, and `Thomas Hélie <http://recherche.ircam.fr/anasyn/helie/>`_, `Project/team S3 <http://s3.ircam.fr/?lang=en>`_ (Sound Signals and Systems) at `STMS Research Lab <http://www.ircam.fr/recherche/lunite-mixte-de-recherche-stms/>`_ (CNRS UMR 9912), hosted by `IRCAM <http://www.ircam.fr/>`_, Paris.

See the AUTHORS file for the complete list of authors.

Short History
==============
PyPHS was initially developed between 2012 and 2016 through a funding from French doctoral school `EDITE <http://edite-de-paris.fr/spip/>`_ (UPMC ED-130) and in connection with the French National Research Agency project `HaMecMoPSys <https://hamecmopsys.ens2m.fr/>`_, as a part of the PhD thesis of `Antoine Falaize <https://afalaize.github.io/>`_ under the direction of `Thomas Hélie <http://recherche.ircam.fr/anasyn/helie/>`_.

Status
=======
This package is in development status Beta. The continuous integration is checked with Travis for Unix systems and AppVeyor for Windows systems (see build status below).

.. image:: https://www.travis-ci.org/pyphs/pyphs.svg?branch=master
    :target: https://www.travis-ci.org/pyphs/pyphs

.. image:: https://ci.appveyor.com/api/projects/status/lmj2m2hfbo0bdqku/branch/master?svg=true
	:target: https://ci.appveyor.com/project/pyphs/pyphs

.. image:: https://codecov.io/gh/pyphs/pyphs/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/pyphs/pyphs

.. image:: https://landscape.io/github/pyphs/pyphs/master/landscape.svg?style=flat
   :target: https://landscape.io/github/pyphs/pyphs/master
   :alt: Health

Installation
==============
It is possible to install ``PyPHS`` from package (if you just want to use it) or source (if you plan to use it for development). Whichever method you choose, make sure that all prerequisites are installed.

Python prerequisites
--------------------

The ``PyPHS`` package run on Python 2.7 and Python
3.5 or newer (3.4 is no longer tested), with the following packages installed:

- `sympy <http://www.sympy.org/fr/>`_
- `numpy <http://www.numpy.org>`_
- `scipy <http://www.scipy.org>`_
- `matplotlib <http://matplotlib.org/>`_
- `networkx <http://networkx.github.io/>`_
- `stopit <https://pypi.python.org/pypi/stopit>`_
- `progressbar2 <https://pypi.python.org/pypi/progressbar2>`_
- `nose <https://github.com/nose-devs/nose>`_ (to run the tests)

Please refer to the `requirements.txt <requirements.txt>`_ file for the required
versions and make sure that these modules are up to date.

Additionally, `theano <http://deeplearning.net/software/theano/>`_ is used if it can be found on the system, for faster numerical evaluation of symbolic expressions.

C++ prerequisites
------------------

The generated C++ sources build with `CMake <https://cmake.org/>`_ >= 3.1 (see **Configuration** below). The code relies on the `Eigen library <http://eigen.tuxfamily.org/index.php?title=Main_Page>`_ (not needed for pure Python usage).

Install from package
--------------------

The easiest way to install the package is via ``pip`` from the `PyPI (Python
Package Index) <https://pypi.python.org/pypi>`_::

    pip install pyphs

This includes the latest code and should install all dependencies automatically. If it complains about some missing dependencies, install them the same way with ``pip`` beforehand.

You might need higher privileges (use su or sudo) to install the package globally. Alternatively you can install the package locally
(i.e. only for you) by adding the ``--user`` argument::

    pip install --user pyphs

Install from source
-------------------

If you plan to use the package as a developer, clone the Git repository::

    git clone --recursive https://github.com/afalaize/pyphs.git

Then you can simply install the package in development mode::

    python setup.py develop --user

To run the included tests::

    python setup.py test

Configuration
--------------

After installation, it is recommended to configure the `config.py <https://github.com/pyphs/pyphs/tree/master/pyphs/config.py>`_ to your needs. Particularly, this is where the local path to the CMake binary and `Eigen library <http://eigen.tuxfamily.org/index.php?title=Main_Page>`_ is specified.

Your local `config.py <https://github.com/pyphs/pyphs/tree/master/pyphs/config.py>`_ file is located at the root of the `PyPHS` package, which can be recovered in a Python interpreter with::

    >>> from pyphs import path_to_configuration_file
    >>>  print(path_to_configuration_file)


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
-----------------

The package is divided into the following folders:

`/pyphs/tutorials <https://github.com/pyphs/pyphs/tree/master/pyphs/tutorials>`_
    Tutorials for the main `PyPHS` classes (executable programs).
`/pyphs/examples <https://github.com/pyphs/pyphs/tree/master/pyphs/examples>`_
    Various real-life applications (executable programs).
`/pyphs/core <https://github.com/pyphs/pyphs/tree/master/pyphs/core>`_
    `PHSCore` class :
        This is the central object of the `PyPHS` package. It implements the core PHS structure and provides several methods for its manipulation (reorganization, connection, simplification, etc.).
`/pyphs/graphs <https://github.com/pyphs/pyphs/tree/master/pyphs/graphs>`_
    `Netlist` class :
        Management of netlist description files.
    `Graph` class :
        (1) Construction and manipulation of network systems,
        (2) Analysis of network realizability,
        (3) Generation of PHS equations (`Core`).
`/pyphs/dictionary <https://github.com/pyphs/pyphs/tree/master/pyphs/dictionary>`_
    - The dictionary is organized in thematic sub-packages (*electronics*, *thermics*, *fractional calculus*, etc.).
    - Each theme is organized in component sub-packages (`electronics.resistor`, `thermics.transfer`, `fraccalc.fracderec`, etc.).
    - Components are `Graph` objects.
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

Theoretical overview
--------------------

The development of `PyPHS` started as an implementation of the methods proposed in the reference [1]_, in which the port-Hamiltonian formalism, the graph analysis and the numerical method are exposed. This is worth to read before using the package.

Q&A Mailing list
-----------------

The package mailing list is at https://groups.google.com/forum/#!forum/pyphs.

Tutorials and examples
-----------------------

The package comes with a set of tutorials for the use of the main functionalities (`definition <https://github.com/pyphs/pyphs/tree/master/pyphs/tutorials/core.py>`_, `evaluation <https://github.com/pyphs/pyphs/tree/master/pyphs/tutorials/evaluation.py>`_, and `simulation <https://github.com/pyphs/pyphs/tree/master/pyphs/tutorials/simulation.py>`_ of a core PHS structure). More tutorials are to come. Additionally, you can see the `examples <https://github.com/pyphs/pyphs/tree/master/pyphs/examples>`_ scripts. Both the *tutorials* and the *examples* folders are located at your package root, which can be recovered in Python interpreter with::

    >>> from pyphs import path_to_examples, path_to_tutorials
    >>> print(path_to_examples)
    >>> print(path_to_tutorials)

Reference
=========
.. [1] Falaize, A., & Hélie, T. (2016). `Passive Guaranteed Simulation of Analog Audio Circuits: A Port-Hamiltonian Approach <https://hal.archives-ouvertes.fr/hal-01390501>`_. Applied Sciences, 6(10), 273.
