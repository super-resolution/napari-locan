"""
SMLM sample data

This module provides SMLM sample data
as could be generated with napari-locan.

It implements the "sample data" specification.
see information here_("https://napari.org/stable/plugins/building_a_plugin/guides.html#sample-data").
"""

from __future__ import annotations

import locan as lc
import napari
from napari.types import LayerData

from napari_locan import smlm_data
from napari_locan.data_model.smlm_data import SmlmData


def make_image_tubulin(smlm_data: SmlmData = smlm_data) -> list[LayerData]:
    """
    Generate a sample image from `locan.datasets.load_tubulin`.
    """
    with napari.utils.progress() as progress_bar:
        progress_bar.set_description("Loading data")
        locdata = lc.datasets.load_tubulin()
        smlm_data.append_item(locdata=locdata)
        data, image_kwargs, layer_type = lc.render_2d_napari_image(
            locdata,
            bin_size=10,
            bin_range="zero",
            rescale=lc.Trafo.EQUALIZE_0P3,
        )
    napari.utils.notifications.show_info(
        "tubulin: bin_size=10, rescale=lc.Trafo.EQUALIZE_0P3"
    )
    return [
        (
            data,
            dict(image_kwargs, name="tubulin", colormap="gray"),
            layer_type,
        )
    ]


def make_image_npc(smlm_data: SmlmData = smlm_data) -> list[LayerData]:
    """
    Generate a sample image from `locan.datasets.load_npc`.
    """
    with napari.utils.progress() as progress_bar:
        progress_bar.set_description("Loading data")
        locdata = lc.datasets.load_npc()
        smlm_data.append_item(locdata=locdata)
        data, image_kwargs, layer_type = lc.render_2d_napari_image(
            locdata,
            bin_size=10,
            bin_range="zero",
            rescale=lc.Trafo.EQUALIZE_0P3,
        )
    napari.utils.notifications.show_info(
        "npc: bin_size=10, rescale=lc.Trafo.EQUALIZE_0P3"
    )
    return [(data, dict(image_kwargs, name="npc", colormap="gray"), layer_type)]


def make_points_npc(smlm_data: SmlmData = smlm_data) -> list[LayerData]:
    """
    Generate localizations from `locan.datasets.load_npc`.
    """
    with napari.utils.progress() as progress_bar:
        progress_bar.set_description("Loading data")
        locdata = lc.datasets.load_npc()
        condition = "4350 < position_x < 6350 and 6200 < position_y < 8200"
        locdata = lc.select_by_condition(locdata, condition)
        smlm_data.append_item(locdata=locdata)
        data = locdata.coordinates
    return [(data, {"name": "npc"}, "points")]


def make_points_tubulin(smlm_data: SmlmData = smlm_data) -> list[LayerData]:
    """
    Generate localizations from `locan.datasets.load_tubulin`.
    """
    with napari.utils.progress() as progress_bar:
        progress_bar.set_description("Loading data")
        locdata = lc.datasets.load_tubulin()
        condition = "2800 < position_x < 5400 and 4800 < position_y < 6400"
        locdata = lc.select_by_condition(locdata, condition)
        smlm_data.append_item(locdata=locdata)
        data = locdata.coordinates
    return [(data, {"name": "tubulin"}, "points")]
