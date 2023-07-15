"""
napari-locan should be used as napari plugin.
"""
from __future__ import annotations

from ._sample_data import (
    make_image_npc,
    make_image_tubulin,
    make_points_npc,
    make_points_tubulin,
)
from ._widget import (
    LoadDataQWidget,
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
    "LoadDataQWidget",
    "RunScriptQWidget",
]
