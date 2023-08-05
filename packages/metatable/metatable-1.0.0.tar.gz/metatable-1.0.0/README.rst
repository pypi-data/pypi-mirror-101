=========
metatable
=========

Extensible table data structure that supports the introduction of user-defined workflow combinators and the use of these combinators in concise workflow descriptions.

|pypi| |travis| |coveralls|

.. |pypi| image:: https://badge.fury.io/py/metatable.svg
   :target: https://badge.fury.io/py/metatable
   :alt: PyPI version and link.

.. |travis| image:: https://travis-ci.com/reity/metatable.svg?branch=main
   :target: https://travis-ci.com/reity/metatable

.. |coveralls| image:: https://coveralls.io/repos/github/reity/metatable/badge.svg?branch=main
   :target: https://coveralls.io/github/reity/metatable?branch=main

Package Installation and Usage
------------------------------
The package is available on PyPI::

    python -m pip install metatable

The library can be imported in the usual ways::

    import metatable
    from metatable import *

Testing and Conventions
-----------------------
All unit tests are executed and their coverage is measured when using `nose <https://nose.readthedocs.io/>`_ (see ``setup.cfg`` for configution details)::

    nosetests

Alternatively, all unit tests are included in the module itself and can be executed using `doctest <https://docs.python.org/3/library/doctest.html>`_::

    python metatable/metatable.py -v

Style conventions are enforced using `Pylint <https://www.pylint.org/>`_::

    pylint metatable

Contributions
-------------
In order to contribute to the source code, open an issue or submit a pull request on the GitHub page for this library.

Versioning
----------
The version number format for this library and the changes to the library associated with version number increments conform with `Semantic Versioning 2.0.0 <https://semver.org/#semantic-versioning-200>`_.
