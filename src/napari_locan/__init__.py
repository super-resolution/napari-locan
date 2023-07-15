"""
napari-locan should be used as napari plugin.
"""
from __future__ import annotations

from napari_locan.sample_data._sample_data import (
    make_image_npc,
    make_image_tubulin,
    make_points_npc,
    make_points_tubulin,
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

try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"

__all__: list[str] = [
    "make_image_npc",
    "make_image_tubulin",
    "make_points_npc",
    "make_points_tubulin",
    "LoadQWidget",
    "RenderQWidget",
    "RunScriptQWidget",
]
