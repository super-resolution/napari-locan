.. _introduction:

This plugin allows loading, visualizing and analyzing
single-molecule localization microscopy (SMLM) data.
napari-locan is well suited for exploratory data analysis.

It implements a subset of methods from Locan_, a python-based library with
code for analyzing SMLM data.
Such data is typically generated in fluorescence-based super-resolution
microscopy methods.
SMLM techniques rely on finding the
position of single-molecule emitters in time and space and reconstructing a
super-resolved image or movie.
The generated localizations are analyzed point-by-point for statistical and
structural insight.

.. _Locan: https://github.com/super-resolution/Locan

Locan provides extended functionality that is better suited for script- or
notebook-based analysis procedures.
