"""
The data model for region specifications.

This module contains a data model to serve as container for region
specifications.

The data model is used by other napari-locan widgets to process
localization data.
It is entirely independent of napari layers.
"""

from __future__ import annotations

import logging

import locan as lc

from napari_locan.data_model.data_model_base import DataModel

logger = logging.getLogger(__name__)


class RegionSpecifications(DataModel):
    """
    Container for one or more region specifications.

    Attributes
    ----------
    datasets_changed_signal
        A Qt signal for index
    names_changed_signal
        A Qt signal for names
    index_changed_signal
        A Qt signal for index
    datasets
        Data structures
    names
        Data structure string identifier
    index
        Current selection of data structure
    dataset
        The selected data object
    name
        The selected data identifier
    """

    def __init__(
        self,
        datasets: list[lc.Region] | None = None,
        names: list[str] | None = None,
    ) -> None:
        super().__init__(datasets=datasets, names=names)
