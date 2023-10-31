.. _guide_on_rois:

==============================
Region and Region of interest
==============================

There are regions, regions of interest (ROI) and SMLM datasets.

Regions are geometrical objects like Rectangle, Ellipse or Polygon.

A ROI connects a region with a selected SMLM dataset for
selected coordinates (or, more general, for localization properties).

ROI specifications can be saved as yaml file.

Regions
--------------

The napari shapes layer provides geometrical objects we call regions (e.g. Rectangle).
These shapes can be transformed into corresponding
locan regions (e.g. locan.Rectangle). They are independent of any image or SMLM dataset.

To get regions for use in napari-locan:

1) Select a napari shapes layer with shapes.
2) Transform napari shapes into regions by `Get regions`.
3) Make sure the scale parameter of that shapes layer is 1.
   Depending on layer creation history it might be set to the shapes value of
   another layer. If so, press `Reset scale` and repeat (2).

ROIs
--------------

When dealing with ROIs we have to distinguish two workflows:

1) Select localizations within a region: for this, define a ROI
   with reference to a SMLM dataset and press `Apply` to create a new SmlmData
   with the selection.
2) Save ROI specifications: for this, define a ROI with reference to a localization file
   and press `Save` to save ROI specifications.

Every ROI specification contains a reference to data, a region definition and
a selection of localization properties. It is kept as instance of
`locan.Roi(reference, region, loc_properties)`.
Before creating a ROI in the Roi widget you have to specify the kind of reference.
For `SmlmData` the currently selected SMLM dataset is taken.
For `File reference`, a file path and type is extracted from the currently
selected SMLM dataset.
For `Open dialog` an existing localization file can be selected.
