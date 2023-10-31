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

napari, locan and napari-locan require a Qt library like pyqt5 or pyside2,
which is not specified as hard requirement.
Make sure to have one (and only one) installed directly or through napari[pyqt5]
or locan[pyqt5].

Install from PyPI
------------------------------

Install napari-locan directly from the Python Package Index::

    pip install napari-locan

Extra dependencies can be included::

    pip install napari-locan[test,dev,docs]

Install from conda-forge
------------------------------

Install locan with the conda package manager (use mamba for better performance)::

    mamba install -c conda-forge napari-locan


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
