"""
napari-locan should be used as napari plugin.
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
    "LocdatasQWidget",
    "PropertyDistributionQWidget",
    "RenderCollectionSeries2dQWidget",
    "RenderFeaturesQWidget",
    "RenderImage2dQWidget",
    "RenderPoints2dQWidget",
    "RenderPoints3dQWidget",
    "RoiQWidget",
    "RunScriptQWidget",
    "SelectQWidget",
    "ShowDataQWidget",
    "ShowMetadataQWidget",
    "ShowPropertiesQWidget",
]

from napari_locan.data_model._locdata import SmlmData

smlm_data: SmlmData = SmlmData()

from napari_locan.data_model._filter import FilterSpecifications

filter_specifications: FilterSpecifications = FilterSpecifications()

from napari_locan.sample_data._sample_data import (
    make_image_npc,
    make_image_tubulin,
    make_points_npc,
    make_points_tubulin,
)
from napari_locan.widgets._widget_clustering import (
    ClusteringQWidget,
)
from napari_locan.widgets._widget_filter_specifications import (
    FilterSpecificationsQWidget,
)
from napari_locan.widgets._widget_load import (
    LoadQWidget,
)
from napari_locan.widgets._widget_locdatas import (
    LocdatasQWidget,
)
from napari_locan.widgets._widget_property_distribution import (
    PropertyDistributionQWidget,
)
from napari_locan.widgets._widget_render_collection_series_2d import (
    RenderCollectionSeries2dQWidget,
)
from napari_locan.widgets._widget_render_features import (
    RenderFeaturesQWidget,
)
from napari_locan.widgets._widget_render_image_2d import (
    RenderImage2dQWidget,
)
from napari_locan.widgets._widget_render_points_2d import (
    RenderPoints2dQWidget,
)
from napari_locan.widgets._widget_render_points_3d import (
    RenderPoints3dQWidget,
)
from napari_locan.widgets._widget_roi import (
    RoiQWidget,
)
from napari_locan.widgets._widget_run_script import (
    RunScriptQWidget,
)
from napari_locan.widgets._widget_select import (
    SelectQWidget,
)
from napari_locan.widgets._widget_show_data import (
    ShowDataQWidget,
)
from napari_locan.widgets._widget_show_metadata import (
    ShowMetadataQWidget,
)
from napari_locan.widgets._widget_show_properties import (
    ShowPropertiesQWidget,
)
