.. _widgets:

===========================
Widgets
===========================

The plugin napari-locan contains the following widgets:

* SMLM data

    The data model for localization-based SMLM data.
    From this data images are rendered and localization-based analysis
    procedures are computed.
    Each dataset is kept as locdata, i.e. a locan.LocData object with metadata,
    aggregated properties, and localization properties for all localizations.

* Show metadata

    The metadata for a single SMLM dataset (locdata.meta) is shown.

* Show properties

    The aggregated properties (locdata.properties) for a single SMLM dataset
    are shown.

* Show localization data

    The dataframe with all localization properties (locdata.data) is shown.

* Load

    A widget to load SMLM data files into the SMLM data model.

* Filter specifications

    A data model for filter specifications that can be applied to select
    localizations.

* Select

    Select localizations in current SMLM dataset based on a filter
    specification.
    A new SMLM dataset will be created.

* Render points 2D / 3D

    Render SMLM data as point cloud.

* Render image 2D / 3D

    Render SMLM data as image by binning localization properties into
    pixels / voxels.

* Render features

    Render selected features of a SMLM dataset.

* Region of interest

    Create and regions of interest

* Cluster

    Compute localization cluster.
    More advanced clustering routines are available through locan-based scripts.

* Collection series

    Render a collection of SMLM data (e.g. a cluster collection)
    as series of point clouds.

* Run script

    A simple interface to handle scripts for localization analysis.
