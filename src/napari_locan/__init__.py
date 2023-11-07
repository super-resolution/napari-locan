"""
.. currentmodule:: napari_locan

napari-locan consists of the following modules:

.. autosummary::
   :toctree: generated/

   data_model
   sample_data
   scripts
   widgets
"""
from __future__ import annotations

import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())

try:
    from ._version import version as __version__  # type: ignore
except ImportError:
    __version__ = "unknown"


__all__: list[str] = [
    "smlm_data",
    "filter_specifications",
    "make_image_npc",
    "make_image_tubulin",
    "make_points_npc",
    "make_points_tubulin",
    "ClusteringQWidget",
    "FilterSpecificationsQWidget",
    "LoadQWidget",
    "NapariLocanProjectQWidget",
    "PropertyDistributionQWidget",
    "RenderCollection2dQWidget",
    "RenderCollectionFeaturesQWidget",
    "RenderFeaturesQWidget",
    "RenderImage2dQWidget",
    "RenderImage3dQWidget",
    "RenderPoints2dQWidget",
    "RenderPoints3dQWidget",
    "RegionSpecifications",
    "RoiQWidget",
    "RunScriptQWidget",
    "SelectQWidget",
    "ShowDataQWidget",
    "ShowMetadataQWidget",
    "ShowPropertiesQWidget",
    "SmlmDataQWidget",
]

from napari_locan.data_model.smlm_data import SmlmData

smlm_data: SmlmData = SmlmData()

from napari_locan.data_model.filter import FilterSpecifications

filter_specifications: FilterSpecifications = FilterSpecifications()

from napari_locan.data_model.region_specifications import RegionSpecifications

region_specifications: RegionSpecifications = RegionSpecifications()

from napari_locan.sample_data.sample_data import (
    make_image_npc,
    make_image_tubulin,
    make_points_npc,
    make_points_tubulin,
)
from napari_locan.widgets.widget_clustering import (
    ClusteringQWidget,
)
from napari_locan.widgets.widget_filter_specifications import (
    FilterSpecificationsQWidget,
)
from napari_locan.widgets.widget_load import (
    LoadQWidget,
)
from napari_locan.widgets.widget_napari_locan_project import (
    NapariLocanProjectQWidget,
)
from napari_locan.widgets.widget_property_distribution import (
    PropertyDistributionQWidget,
)
from napari_locan.widgets.widget_render_collection_2d import (
    RenderCollection2dQWidget,
)
from napari_locan.widgets.widget_render_collection_features import (
    RenderCollectionFeaturesQWidget,
)
from napari_locan.widgets.widget_render_features import (
    RenderFeaturesQWidget,
)
from napari_locan.widgets.widget_render_image_2d import (
    RenderImage2dQWidget,
)
from napari_locan.widgets.widget_render_image_3d import (
    RenderImage3dQWidget,
)
from napari_locan.widgets.widget_render_points_2d import (
    RenderPoints2dQWidget,
)
from napari_locan.widgets.widget_render_points_3d import (
    RenderPoints3dQWidget,
)
from napari_locan.widgets.widget_roi import (
    RoiQWidget,
)
from napari_locan.widgets.widget_run_script import (
    RunScriptQWidget,
)
from napari_locan.widgets.widget_select import (
    SelectQWidget,
)
from napari_locan.widgets.widget_show_data import (
    ShowDataQWidget,
)
from napari_locan.widgets.widget_show_metadata import (
    ShowMetadataQWidget,
)
from napari_locan.widgets.widget_show_properties import (
    ShowPropertiesQWidget,
)
from napari_locan.widgets.widget_smlm_data import (
    SmlmDataQWidget,
)
