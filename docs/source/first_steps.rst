.. _first_steps:

===========================
First steps
===========================

If napari is up and running with napari-locan installed you can process
SMLM data by either opening sample data or loading SMLM data from a file.

SMLM data
--------------

When working with napari-locan you deal with SMLM data containing localizations
with coordinates and other localization properties.

These datasets are stored as SMLM data model that can be accessed through the
SMLM data widget.

It is important to note that the SMLM data model is completely independent
from napari layers.

Sample data
----------------

When opening the sample data, two things happen:
(i) Localization data is loaded and stored as a SMLM dataset.
(ii) The SMLM dataset is rendered as point cloud or image.

The SMLM dataset can be accessed through the SMLM data widget and further
processed through other widgets.

SMLM data procedures
-------------------------

Some widgets process SMLM datasets without modifying the SMLM data storage.
For instance, rendering SMLM data as image creates a new napari layer that is then
independent from the SMLM data.

Other widgets compute new SMLM datasets, e.g. by selecting data or
computing clusters, that are stored as addition to the SMLM data.
The new SMLM dataset is then accessible through the SMLM data widget.

Typically, widgets process the current selection in the SMLM data widget.
