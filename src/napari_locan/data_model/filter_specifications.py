"""
The data model for filter specifications.

This module contains a data model to serve as container for filter
specifications to select localization property values.

The data model is used by other napari-locan widgets to process
localization data and yield new SMLM datasets.
It is entirely independent of napari layers.
"""

from __future__ import annotations

import logging

import locan as lc

from napari_locan.data_model.data_model_base import DataModel

logger = logging.getLogger(__name__)


class FilterSpecifications(DataModel):
    """
    Container for one or more filter specifications.

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
        datasets: list[dict[str, lc.Selector]] | None = None,
        names: list[str] | None = None,
    ) -> None:
        super().__init__(datasets=datasets, names=names)

    @property
    def filter_condition(self) -> str:
        if self._index == -1:
            return ""
        else:
            return_value: str = lc.filter_condition(
                selectors=self.dataset.values()  # type: ignore[union-attr]
            )
            return return_value
