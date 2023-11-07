"""
The data model for filter settings

This module contains a data model to serve as container for filter
specifications to select localization property values.

The data model is used by other napari-locan widgets to process
localization data and yield new SMLM datasets.
It is entirely independent of napari layers.
"""
from __future__ import annotations

import logging
from typing import Any

import locan as lc
from qtpy.QtCore import QObject, Signal  # type: ignore[attr-defined]

logger = logging.getLogger(__name__)


class FilterSpecifications(QObject):  # type: ignore
    """
    Container for one or more filter specifications.

    Attributes
    ----------
    filters_changed_signal
        A Qt signal for filters
    filter_names_changed_signal
        A Qt signal for filter_names
    index_changed_signal
        A Qt signal for index
    filters
        Collection of mapping between certain loc_properties and selectors
    filter_names
        Filter string identifier
    index
        Current selection of filters
    filter
        The selected filter object
    filter_name
        The selected filter identifier
    """

    filters_changed_signal: Signal = Signal(list)
    filter_names_changed_signal: Signal = Signal(list)
    index_changed_signal: Signal = Signal(int)

    def __init__(self, filters: list[dict[str, lc.Selector]] | None = None) -> None:
        super().__init__()
        self._filters: list[dict[str, lc.Selector]] = []
        self._filter_names: list[str] = []
        self._index: int = -1

        self.filters = filters  # type: ignore

    def __getstate__(self) -> dict[str, Any]:
        """Modify pickling behavior."""
        state: dict[str, Any] = {}
        state["_filters"] = self._filters
        state["_filter_names"] = self._filter_names
        state["_index"] = self._index
        return state

    def __setstate__(self, state: dict[str, Any]) -> None:
        """Modify pickling behavior."""
        # Restore instance attributes.
        self.__dict__.update(state)
        super().__init__()

    @property
    def filters(self) -> list[dict[str, lc.Selector]]:
        return self._filters

    @filters.setter
    def filters(self, value: list[dict[str, lc.Selector]] | None) -> None:
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
        self.index_changed_signal.emit(value)

    def set_index_slot(self, value: int) -> None:
        """QT slot for property self.index."""
        self.index = value

    @property
    def filter(self) -> dict[str, lc.Selector] | None:  # noqa: A003
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

    @property
    def filter_condition(self) -> str:
        if self._index == -1:
            return ""
        else:
            return_value: str = lc.filter_condition(
                selectors=self.filter.values()  # type: ignore[union-attr]
            )
            return return_value

    def change_event(self) -> None:
        """QT signal for any change"""
        self.filters_changed_signal.emit(self._filters)
        self.filter_names_changed_signal.emit(self._filter_names)
        self.index_changed_signal.emit(self._index)

    def append_item(self, filter: dict[str, lc.Selector] | None) -> None:  # noqa: A002
        if filter is not None:
            self._filters.append(filter)
            self.filters = self._filters
            self.index = len(self.filters) - 1

    def delete_item(self) -> None:
        current_index = self.index
        try:
            self._filters.pop(current_index)
            self._filter_names.pop(current_index)
        except IndexError as exception:
            raise IndexError(
                "Index is out of range. No item available to be deleted."
            ) from exception
        self._index = current_index - 1
        self.filter_names_changed_signal.emit(self._filter_names)
        self.index_changed_signal.emit(self._index)

    def delete_all(self) -> None:
        self._filters = []
        self._filter_names = []
        self._index = -1
        self.filter_names_changed_signal.emit(self._filter_names)
        self.index_changed_signal.emit(self._index)
