.. _installation:

===========================
Installation
===========================

Dependencies
------------

* python 3
* napari, locan and its dependencies on standard scipy
  and other open source libraries


A list with all hard and optional dependencies is given in `pyproject.toml`.

Install from pypi
------------------------------

Install napari-locan directly from the Python Package Index::

    pip install napari-locan

Extra dependencies can be included::

    pip install napari-locan[test,dev,docs]

Install from distribution or sources
-------------------------------------

In order to get the latest changes install from the GitHub repository
main branch::

    pip install git+https://github.com/super-resolution/napari-locan.git@main

or download distribution or wheel archive and install with pip::

    pip install <distribution_file>

Install from local sources::

    pip install <napari-locan_directory>

Run tests
-----------------------

Use pytest to run the tests from the source directory::

    pytest
