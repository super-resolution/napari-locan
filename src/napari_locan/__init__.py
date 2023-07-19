"""
napari-locan should be used as napari plugin.
"""
from __future__ import annotations

import logging


logging.getLogger(__name__).addHandler(logging.NullHandler())


try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"


__all__: list[str] = [
    "smlm_data",
    "make_image_npc",
    "make_image_tubulin",
    "make_points_npc",
    "make_points_tubulin",
    "LocdatasQWidget",
    "LoadQWidget",
    "RenderQWidget",
    "RunScriptQWidget",
    "ShowFeaturesQWidget",
]

from napari_locan.data_model._locdata import SmlmData

smlm_data: SmlmData = SmlmData()

from napari_locan.sample_data._sample_data import (
    make_image_npc,
    make_image_tubulin,
    make_points_npc,
    make_points_tubulin,
)
from napari_locan.widgets._widget_locdatas import (
    LocdatasQWidget,
)
from napari_locan.widgets._widget_load import (
    LoadQWidget,
)
from napari_locan.widgets._widget_render import (
    RenderQWidget,
)
from napari_locan.widgets._widget_run_script import (
    RunScriptQWidget,
)
from napari_locan.widgets._widget_locdata_features import (
    ShowFeaturesQWidget,
)
