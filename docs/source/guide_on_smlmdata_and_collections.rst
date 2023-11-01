.. _guide_on_smlmdata_and_collections:

==============================
SmlmData and collections
==============================

**Localization data** in napari-locan is made of point-clouds with attributes.

All localization data is kept in the **napari_locan.SmlmData model**
as **locan.LocData objects**.

LocData objects can also contain a **collection** of several localization datasets.

Localization data
------------------

Localization data consists of a list of localizations with various localization
properties.
The dataset is represented by a dataframe together with general properties,
metadata and other attributes.
In napari-locan a dataset is kept as `locan.LocData` object that is inserted
in the `napari_locan.SmlmData` model and can be accessed by the attribute
`smlm_data.locdata`.

For details on `locan.LocData` and data structures in locan please see the
`locan documentation on data structures`_

.. _locan documentation on data structures: https://locan.readthedocs.io/en/latest/source/datastructures.html

Collections
------------------
Collections contain the individual LocData objects together with aggregated
properties that make up a new LocData object. Think of it as localization clusters
where each cluster can be represented as a single "localization" with a center position
and other localization attributes.

In napari-locan, widgets typically access the current selection of the SmlmData model.
Some widgets deal with collections. In that case, the current selection of the
SmlmData model must be a collection.
