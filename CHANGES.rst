========================
Changelog
========================

0.6 - 2025-03-11
=================

New Features
------------
- add dependency-groups

Bug Fixes
---------
- fix dependence on locan test_data
- fix documentation

Other Changes and Additions
---------------------------
- refactor: update to python 3.12
- lint for numpy=2.0 and fix new ruff issues
- refactor tests layout
- add npc_gp210.asdf test data to scripts directory
- fix mypy issues


0.5 - 2023-12-07
========================

Bug Fixes
---------
- fix version readout with readthedocs
- fix use of new locan.colormaps module

Other Changes and Additions
---------------------------
- add GitHub action for deploying to PyPI and TestPyPI
- configure setuptools_scm for branching model
- bump version requirements for dependencies

0.4.0 - 2023-11-08
========================

New Features
------------
- add widget to save and load project
- add button to get regions from locdata hulls

Other Changes and Additions
---------------------------
- add abstract base class for DataModels
- add data model for region specifications
- add data model for roi specifications
- add data model for filter specifications
- minor modifications like button rearrangement

0.3.0 - 2023-11-01
========================

Bug Fixes
---------
- add dependency for matplotlip<3.8.0

Other Changes and Additions
---------------------------
- additions to the documentation

0.2.0 - 2023-10-31
========================

Bug Fixes
---------
- correct requirements
- always open dialog with load button
- remove unknown_file_format from load options
- fix dockerfile
- fix readthedocs

Other Changes and Additions
---------------------------
- add to documentation

0.1.0 - 2023-10-29
========================

New Features
------------
- sample data for 2d
- data models from SmlmData and FilterSpecifications
- widgets for
    * SMLM data
    * Show metadata
    * Show properties
    * Show localization data
    * Show localization property distributions
    * Load
    * Filter specifications
    * Select
    * Region of interest
    * Render points 2D / 3D
    * Render image 2D / 3D
    * Render features of a SMLM dataset
    * Cluster
    * Render collection as 2D / 3D point cloud
    * Render collection features
    * Run script
- documentation via readthedocs
