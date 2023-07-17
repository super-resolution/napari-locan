"""
The data model

Serving as container for SMLM data.
Most parts of the model for a single SMLM dataset is already implemented
in locan as LocData.
"""
from __future__ import annotations

import logging
from pathlib import Path

import locan as lc
from qtpy.QtCore import QObject, Signal

logger = logging.getLogger(__name__)


class SmlmData(QObject):  # type: ignore
    """
    Container for one or more LocData objects.

    Attributes
    ----------
    locdatas
        Localization datasets
    locdata_names
        Localization string identifier
    index
        Current selection of of locdata
    locdata
        The selected LocData object
    locdata_name
        The selected LocData identifier
    """

    locdatas_signal = Signal(list)
    locdata_names_signal = Signal(list)
    index_signal = Signal(int)

    def __init__(self, locdatas: list[lc.LocData] | None = None):
        super().__init__()
        self._locdatas: list[lc.LocData] = []
        self._locdata_names: list[str] = []
        self._index: int = -1

        self.locdatas = locdatas  # type: ignore

    @property
    def locdatas(self) -> list[lc.LocData]:
        return self._locdatas

    @locdatas.setter
    def locdatas(self, value: list[lc.LocData] | None) -> None:
        if value is None:
            self._locdatas = []
        else:
            self._locdatas = value
        if self._locdatas:
            self._locdata_names = [
                item.meta.identifier + "-" + str(Path(item.meta.file.path).name)
                for item in self._locdatas
            ]
            self._index = 0
        else:
            self._locdata_names = []
            self._index = -1
        self.change_event()

    @property
    def locdata_names(self) -> list[str]:
        return self._locdata_names

    @property
    def index(self) -> int:
        return self._index

    @index.setter
    def index(self, value: int) -> None:
        self._index = value
        self.index_signal.emit(value)

    def set_index_slot(self, value: int) -> None:
        """QT slot for property self.index."""
        self.index = value

    @property
    def locdata(self) -> lc.LocData | None:
        if self._index == -1:
            return None
        else:
            return self._locdatas[self._index]

    @property
    def locdata_name(self) -> str:
        if self._index == -1:
            return ""
        else:
            return self._locdata_names[self._index]

    def change_event(self) -> None:
        """QT signal for any change"""
        self.locdatas_signal.emit(self._locdatas)
        self.locdata_names_signal.emit(self._locdata_names)
        self.index_signal.emit(self._index)
