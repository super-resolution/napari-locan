.. _development:

===========================
Development
===========================

We welcome any contributions for improving or further developing this package.

However, please excuse that we are limited in time for development and support.

Some things to keep in mind when adding code...

Install
========

A few extra libraries are needed for development::

        pip install .[test,dev,docs]

Import Conventions
====================

The following import conventions are used throughout Locan source code and
documentation::

    import locan as lc
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import numpy as np
    import scipy as sp
    import pandas as pd

This is enforced through ruff following specifications in pyproject.toml.

Unit tests
===========

For testing we use pytest_.

.. _pytest: https://docs.pytest.org/en/latest/index.html

A minimal test suite is provided in `src/napari_locan/tests`.
The extended test suite is provided in `tests`.

For unit testing we supply test data as data files located in `tests/test_data`.

Tests can also be run with tox_.

.. _tox: https://tox.readthedocs.io/en/latest/

Coverage
===========

For measuring code coverage in testing we use coverage.py_.

.. _coverage.py: https://coverage.readthedocs.io

Configurations are kept in pyproject.toml.

Code checks
============

We use black_ for formating and ruff_ for code linting.

.. _black: https://pypi.org/project/black/
.. _ruff: https://pypi.org/project/ruff

Configurations are kept in pyproject.toml.

Versioning
===========

We use `SemVer`_ for versioning. For all versions available, see the
`releases in this repository`_.

.. _SemVer: http://semver.org/
.. _releases in this repository: https://github.com/super-resolution/Locan/releases

Documentation
==============

Documentation is provided as restructured text, myst markdown,
and as docstrings within the code.
HTML pages and other documentation formats are build using Sphinx_.

.. _Sphinx: http://www.sphinx-doc.org

We follow standard recommendations for `python documentation`_
and the `numpy conventions`_.

.. _python documentation: https://www.python.org/dev/peps/pep-0008/
.. _numpy conventions: https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard

To update the documentation from sources delete ``/docs/sources/generated`` and run::

    sphinx-build -b html -E YOUR_PATH\napari-locan\docs YOUR_PATH\napari-locan\docs\_build

Type hints
==============

We try to make use of type checking using mypy_ as much as possible.

.. _mypy: https://pypi.org/project/mypy

Configurations are kept in pyproject.toml.

To remember
============

* The plugin is strongly linked to locan_ and its development procedures.

.. _locan: https://github.com/super-resolution/Locan/
