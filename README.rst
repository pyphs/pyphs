PyPHS
======
A python software dedicated to the simulation of multiphysical systems in the Port-Hamiltonian Systems (PHS) formalism. 

.. image:: https://badge.fury.io/py/pyphs.svg
    :target: https://badge.fury.io/py/pyphs

.. image:: https://img.shields.io/badge/licence-CeCILL--B-blue.svg
    :target: http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html

.. image:: https://img.shields.io/badge/python-2.7%2C%203.4%2C%203.5%2C%203.6-blue.svg
    :target: https://www.travis-ci.org/afalaize/pyphs
    
.. image:: https://img.shields.io/badge/documentation-website-blue.svg
    :target: https://afalaize.github.io/pyphs/

It is developped in the `project/team S3 <http://s3.ircam.fr/?lang=en>`__ (Sound Signals and Systems) at `STMS Research Lab <http://www.ircam.fr/recherche/lunite-mixte-de-recherche-stms/>`__ (CNRS UMR 9912), hosted by `IRCAM <http://www.ircam.fr/>`__. 

It was initially developed between 2012 and 2016 as a part of the PhD project of `Antoine Falaize <https://afalaize.github.io/>`__, under the direction of `Thomas Hélie <http://recherche.ircam.fr/anasyn/helie/>`__, through a funding from French doctoral school `EDITE <http://edite-de-paris.fr/spip/>`__ (UPMC ED-130), and in connection with the French National Research Agency project `HaMecMoPSys <https://hamecmopsys.ens2m.fr/>`__.

.. image:: https://www.travis-ci.org/afalaize/pyphs.svg?branch=master
    :target: https://www.travis-ci.org/afalaize/pyphs
 
.. image:: https://coveralls.io/repos/github/afalaize/pyphs/badge.svg?branch=master
    :target: https://coveralls.io/github/afalaize/pyphs?branch=master

.. image:: https://codecov.io/gh/afalaize/pyphs/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/afalaize/pyphs

.. image:: https://www.quantifiedcode.com/api/v1/project/0c1fbf5b44e94b4085a24c18a1895947/badge.svg?branch=master
  :target: https://www.quantifiedcode.com/app/project/0c1fbf5b44e94b4085a24c18a1895947
  :alt: issues   

.. image:: https://landscape.io/github/afalaize/pyphs/master/landscape.svg?style=flat
   :target: https://landscape.io/github/afalaize/pyphs/master
   :alt: Health
       
Installation
==============
It is possible to install ``pyphs`` from package (if you just want to use it) or source (if you plan to use it for development). Whichever method you choose, make sure that all prerequisites are installed.

Prerequisites
-------------

The ``pyphs`` package run on Python 2.7 and Python
3.4 or newer, with the following packages installed:

- `sympy <http://www.sympy.org/fr/>`_
- `numpy <http://www.numpy.org>`_
- `scipy <http://www.scipy.org>`_
- `matplotlib <http://matplotlib.org/>`_
- `networkx <http://networkx.github.io/>`_
- `stopit <https://pypi.python.org/pypi/stopit>`_
- `progressbar2 <https://pypi.python.org/pypi/progressbar2>`_
- `nose <https://github.com/nose-devs/nose>`_ (to run the tests)

Please refer to the `requirements.txt <requirements.txt>`_ file for the minimum
required versions and make sure that these modules are up to date.

Additionally, `theano <http://deeplearning.net/software/theano/>`_ is used if installed (for faster numerical evaluation of symbolic expressions).

Finally, the generated `C++` code rely on the `Eigen library <http://eigen.tuxfamily.org/index.php?title=Main_Page>`_ (see **Configuration** below). It is not needed for pure Python usage.

Install from package
--------------------

The instructions given here should be used if you just want to install the
package, e.g. to run the bundled programs or use some functionality for your
own project. If you intend to change anything within the `pyphs` package,
please follow the steps in the next section.

The easiest way to install the package is via ``pip`` from the `PyPI (Python
Package Index) <https://pypi.python.org/pypi>`_::

    pip install pyphs

This includes the latest code and should install all
dependencies automatically. If this is not the case, each dependency can be install the same way with ``pip``.

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

After installation, it is recommanded to configure the `config.py </pyphs/config.py>`_ to your needs. Particularily, this is where the local path to the `Eigen library <http://eigen.tuxfamily.org/index.php?title=Main_Page>`_ is specified (and then included in the generated C++ code).

Your local `config.py </pyphs/config.py>`_ file is located at the root of the `pyphs` package, which can be recovered with:
    
    >>> import pyphs
    >>> help(pyph)


Upgrade of existing installations
---------------------------------

To upgrade the package, please use the same mechanism (pip vs. source) as you
did for installation. In each case, it is recommanded to uninstall the package first.

Upgrade a package
~~~~~~~~~~~~~~~~~

Simply upgrade the package via pip::

    pip install --upgrade pyphs [--user]

Upgrade from source
~~~~~~~~~~~~~~~~~~~

Simply pull the latest sources::

    git pull

Package structure
-----------------

The package divided into the following folders:

`/docs <docs>`_
  package documentation
`/pyphs/tutorials </pyphs/tutorials>`_
  tutorials programs for the main `pyphs classes
`/pyphs/examples </pyphs/examples>`_
  additional examples (executable programs)
`/pyphs/core </pyphs/core>`_
    define the core PHS structure class `PHSCore`
`/pyphs/graphs </pyphs/graphs>`_
    define the classes `PHSNetlist` and `PHSGraph`
`/pyphs/dictionary </pyphs/dictionary>`_
  components (`PHSGraph`)
`/pyphs/numerics </pyphs/numerics>`_
    define the classes `PHSNumericalEval`, `PHSNumericalMethod` and `PHSNumericalCore` for the numerical evaluation of `PHSCore`
`/pyphs/simulations </pyphs/simulations>`_
    define the classes `PHSSimulation` and `PHSData` for simulation
`/pyphs/latex </pyphs/latex>`_
    LaTeX code generation
`/pyphs/cpp </pyphs/cpp>`_
    C++ code generation
`/pyphs/tests </pyphs/tests>`_
  test programs (withe `nose`)
`/pyphs/plots </pyphs/plots>`_
    Plot tools
`/pyphs/misc </pyphs/misc>`_
    Miscelaneous tools
  
Documentation
==============

Implemented methods
--------------------
The package began as an implementation of the methods proposed in the reference [1]_, in which the port-Hamiltonian formalism, the graph analaysis and the numerical method are exposed. This is worth to read before using the `pyphs` package. 

Tutorials and examples
-----------------------

The package comes with a serie of tutorials for the use of the main functionalities (`definition </pyphs/tutorials/phscore.py>`_, `evaluation </pyphs/tutorials/phsnumericaleval.py>`_, and `simulation </pyphs/tutorials/phssimulation.py>`_ of a core PHS structure). More tutorials are to come. Additionally, you can see the `examples </pyphs/examples>`_ scripts. Both the *tutorials* and the *examples* folders are located at your package root, which can be recovered in Python interpreter with:

    >>> import pyphs
    >>> help(pyphs)

The `website <https://afalaize.github.io/pyphs/>`_ contains additional materials.


Reference
=========
.. [1] Falaize, A., & Hélie, T. (2016). `Passive Guaranteed Simulation of Analog Audio Circuits: A Port-Hamiltonian Approach <https://hal.archives-ouvertes.fr/hal-01390501>`_. Applied Sciences, 6(10), 273.
