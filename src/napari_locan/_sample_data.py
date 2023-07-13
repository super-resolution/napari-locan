"""
SMLM sample data

This module provides SMLM sample data
as could be generated with napari-locan.

It implements the "sample data" specification.
see: https://napari.org/stable/plugins/guides.html?#sample-data
"""
from __future__ import annotations

import locan as lc


def make_image_tubulin() -> list[tuple]:
    """
    Generate a sample image from `locan.datasets.load_tubulin`.
    """
    locdata = lc.datasets.load_tubulin()
    data, bins, labels = lc.histogram(locdata, bin_size=10)
    data = lc.adjust_contrast(data, rescale=lc.Trafo.EQUALIZE_0P3)
    return [(data, {"name": "tubulin", "colormap": "gray"}, "image")]


def make_image_npc() -> list[tuple]:
    """
    Generate a sample image from `locan.datasets.load_npc`.
    """
    locdata = lc.datasets.load_npc()
    data, bins, labels = lc.histogram(locdata, bin_size=10)
    data = lc.adjust_contrast(data, rescale=lc.Trafo.EQUALIZE_0P3)
    return [(data, {"name": "npc", "colormap": "gray"}, "image")]


def make_points_npc() -> list[tuple]:
    """
    Generate localizations from `locan.datasets.load_npc`.
    """
    locdata = lc.datasets.load_npc()
    condition = "4350 < position_x < 6350 and 6200 < position_y < 8200"
    locdata = lc.select_by_condition(locdata, condition)
    data = locdata.coordinates
    return [(data, {"name": "tubulin"}, "points")]


def make_points_tubulin() -> list[tuple]:
    """
    Generate localizations from `locan.datasets.load_tubulin`.
    """
    locdata = lc.datasets.load_tubulin()
    condition = "2800 < position_x < 5400 and 4800 < position_y < 6400"
    locdata = lc.select_by_condition(locdata, condition)
    data = locdata.coordinates
    return [(data, {"name": "tubulin"}, "points")]
