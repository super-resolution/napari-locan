"""
The data model for localization data

This module contains a data model to serve as container for SMLM data.
The individual SMLM datasets are provided as :class:`locan.LocData` instances.

SMLM data serves as data model for other napari-locan widgets to process or
render the localization data. It is entirely independent of napari layers.
Upon rendering a SMLM dataset a new image is created in a new napari layer.
"""

from __future__ import annotations

import logging
from typing import Any

import locan as lc
from qtpy.QtCore import QObject, Signal  # type: ignore[attr-defined]

logger = logging.getLogger(__name__)


class SmlmData(QObject):  # type: ignore
    """
    Container for one or more LocData objects.

    Attributes
    ----------
    index_changed_signal
        A Qt signal for index
    locdata_names_changed_signal
        A Qt signal for locdata_names
    locdatas
        Localization datasets
    locdata_names
        Localization string identifier
    index
        Current selection of locdatas
    locdata
        The selected LocData object
    locdata_name
        The selected LocData identifier
    """

    index_changed_signal: Signal = Signal(int)
    locdata_names_changed_signal: Signal = Signal(list)

    def __init__(
        self,
        locdatas: list[lc.LocData] | None = None,
        locdata_names: list[str] | None = None,
    ) -> None:
        super().__init__()
        if locdatas is None and locdata_names is None:
            self._locdatas: list[lc.LocData] = []
            self._locdata_names: list[str] = []
            self._index: int = -1
        elif locdata_names is None:
            assert locdatas is not None  # type narrowing # noqa: S101
            self._locdatas = locdatas
            self._locdata_names = [item.meta.identifier for item in self._locdatas]
            self._index = len(locdatas) - 1
        elif locdatas is not None and (len(locdatas) != len(locdata_names)):
            raise ValueError(
                "locdata and locdata_names must correspond and be of same length."
            )
        else:
            assert locdatas is not None  # type narrowing # noqa: S101
            self._locdatas = locdatas
            self._locdata_names = locdata_names
            self._index = len(locdatas) - 1

    def __getstate__(self) -> dict[str, Any]:
        """Modify pickling behavior."""
        state: dict[str, Any] = {}
        state["_locdatas"] = self._locdatas
        state["_locdata_names"] = self._locdata_names
        state["_index"] = self._index
        return state

    def __setstate__(self, state: dict[str, Any]) -> None:
        """Modify pickling behavior."""
        # Restore instance attributes.
        self.__dict__.update(state)
        super().__init__()

    @property
    def locdatas(self) -> list[lc.LocData]:
        return self._locdatas

    @property
    def locdata_names(self) -> list[str]:
        return self._locdata_names

    @property
    def index(self) -> int:
        return self._index

    @index.setter
    def index(self, value: int) -> None:
        if value > len(self.locdatas) - 1:
            raise IndexError(
                f"Index is larger than n_locdatas - 1: {len(self.locdatas) - 1}"
            )
        elif value < 0:
            self._index = -1
        else:
            self._index = value
        self.index_changed_signal.emit(self._index)

    def set_index_slot(self, value: int) -> None:
        """QT slot for property self.index."""
        self.index = value

    @property
    def locdata(self) -> lc.LocData | None:
        if self._index == -1:
            return None
        else:
            return self._locdatas[self._index]

    @locdata.setter
    def locdata(self, item: lc.LocData) -> None:
        if self._index == -1:
            raise ValueError(
                "Locdatas is empty. "
                "There is no item available to be replaced."
                "Use self.append_item instead."
            )
        else:
            self._locdatas[self._index] = item
            self.index_changed_signal.emit(self._index)

    @property
    def locdata_name(self) -> str:
        if self._index == -1:
            return ""
        else:
            return self._locdata_names[self._index]

    @locdata_name.setter
    def locdata_name(self, text: str) -> None:
        if self._index == -1:
            raise ValueError(
                "Locdata_names is empty. "
                "There is no item available to be replaced."
                "Use self.append_item instead."
            )
        else:
            self._locdata_names[self._index] = text
            self.locdata_names_changed_signal.emit(self._locdata_names)

    def append_item(
        self,
        locdata: lc.LocData | None,
        locdata_name: str | None = None,
        set_index: bool = True,
    ) -> None:
        current_index = self.index
        if locdata is None and locdata_name is None:
            return
        elif locdata_name is None:
            assert locdata is not None  # type narrowing # noqa: S101
            self._locdatas.append(locdata)
            self._locdata_names.append(locdata.meta.identifier)
        else:
            assert locdata is not None  # type narrowing # noqa: S101
            assert locdata_name is not None  # type narrowing # noqa: S101
            self._locdatas.append(locdata)
            self._locdata_names.append(locdata_name)
        if set_index:
            self._index = len(self.locdatas) - 1
        else:
            self._index = current_index

        self.locdata_names_changed_signal.emit(self.locdata_names)
        self.index_changed_signal.emit(self.index)

    def delete_item(self) -> None:
        current_index = self.index
        try:
            self._locdatas.pop(current_index)
            self._locdata_names.pop(current_index)
        except IndexError as exception:
            raise IndexError(
                "Index is out of range. No item available to be deleted."
            ) from exception

        if len(self._locdatas) == 0:
            self._index = -1
        elif current_index == 0:
            self._index = 0
        else:
            self._index = current_index - 1

        self.locdata_names_changed_signal.emit(self.locdata_names)
        self.index_changed_signal.emit(self.index)

    def delete_all(self) -> None:
        self._locdatas = []
        self._locdata_names = []
        self._index = -1
        self.locdata_names_changed_signal.emit(self.locdata_names)
        self.index_changed_signal.emit(self.index)
