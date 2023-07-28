"""
The data model for filter settings

Serving as container for filter specifications
to select localization property values.
"""
from __future__ import annotations

import logging

import locan as lc
from qtpy.QtCore import QObject, Signal

logger = logging.getLogger(__name__)


class FilterSpecifications(QObject):  # type: ignore
    """
    Container for one or more filter specifications.

    Attributes
    ----------
    filters
        Collection of selectors for certain loc_properties
    filter_names
        Filter string identifier
    index
        Current selection of filters
    filter
        The selected filter object
    filter_name
        The selected filter identifier
    """

    filters_signal = Signal(list)
    filter_names_signal = Signal(list)
    index_signal = Signal(int)

    def __init__(self, filters: list[list[lc.Selector]] | None = None):
        super().__init__()
        self._filters: list[list[lc.Selector]] = []
        self._filter_names: list[str] = []
        self._index: int = -1

        self.filters = filters  # type: ignore

    @property
    def filters(self) -> list[list[lc.Selector]]:
        return self._filters

    @filters.setter
    def filters(self, value: list[list[lc.Selector]] | None) -> None:
        if value is None:
            self._filters = []
        else:
            self._filters = value
        if self._filters:
            self._filter_names = [str(i) for i in range(len(self._filters))]
            self._index = 0
        else:
            self._filter_names = []
            self._index = -1
        self.change_event()

    @property
    def filter_names(self) -> list[str]:
        return self._filter_names

    @property
    def index(self) -> int:
        return self._index

    @index.setter
    def index(self, value: int) -> None:
        if value > len(self.filters) - 1:
            raise IndexError(
                f"Index is larger than n_filters - 1: {len(self.filters) - 1}"
            )
        self._index = value
        self.index_signal.emit(value)

    def set_index_slot(self, value: int) -> None:
        """QT slot for property self.index."""
        self.index = value

    @property
    def filter(self) -> list[lc.Selector] | None:  # noqa: A003
        if self._index == -1:
            return None
        else:
            return self._filters[self._index]

    @property
    def filter_name(self) -> str:
        if self._index == -1:
            return ""
        else:
            return self._filter_names[self._index]

    def change_event(self) -> None:
        """QT signal for any change"""
        self.filters_signal.emit(self._filters)
        self.filter_names_signal.emit(self._filter_names)
        self.index_signal.emit(self._index)

    def append_filter(self, filter: list[lc.Selector] | None) -> None:  # noqa: A002
        if filter is not None:
            self._filters.append(filter)
            self.filters = self._filters
            self.index = len(self.filters) - 1
