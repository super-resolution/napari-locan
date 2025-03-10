"""
Show data statistics for a SMLM dataset.

A QWidget plugin for showing locdata data statistics (locdata.data.describe()).
"""

from __future__ import annotations

import logging
from typing import Any

from napari.viewer import Viewer
from qtpy.QtCore import QAbstractTableModel, Qt  # type: ignore[attr-defined]
from qtpy.QtWidgets import (
    QHBoxLayout,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from napari_locan import smlm_data
from napari_locan.data_model.smlm_data import SmlmData

logger = logging.getLogger(__name__)


class TableModel(QAbstractTableModel):  # type: ignore
    def __init__(self, data: Any) -> None:
        super().__init__()
        self._data = data

    def data(self, index, role) -> str:  # type: ignore
        if role == Qt.DisplayRole:  # type: ignore[attr-defined]
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, parent=None) -> int:  # type: ignore
        return self._data.shape[0]  # type: ignore

    def columnCount(self, parent=None) -> int:  # type: ignore
        return self._data.shape[1]  # type: ignore

    def headerData(self, section, orientation: Qt.Horizontal | Qt.Vertical, role) -> str:  # type: ignore
        # section is the index of the column/row.
        if role == Qt.DisplayRole:  # type: ignore[attr-defined]
            if orientation == Qt.Horizontal:  # type: ignore[attr-defined]
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:  # type: ignore[attr-defined]
                return str(self._data.index[section])


class ShowDataQWidget(QWidget):  # type: ignore
    def __init__(self, napari_viewer: Viewer, smlm_data: SmlmData = smlm_data):
        super().__init__()
        self.viewer = napari_viewer
        self.smlm_data = smlm_data

        self._add_table_view()
        self._set_layout()

    def _add_table_view(self) -> None:
        self._table_view = QTableView()
        self.smlm_data.index_changed_signal.connect(self._update_table_view)

        self._table_view_layout = QHBoxLayout()
        self._table_view_layout.addWidget(self._table_view)

        self.smlm_data.index_changed_signal.emit(self.smlm_data.index)

    def _update_table_view(self) -> None:
        if self.smlm_data.index != -1:
            self.model: TableModel | None = TableModel(
                data=self.smlm_data.locdata.data.describe()  # type: ignore
            )
        else:
            self.model = None
        self._table_view.setModel(self.model)

    def _set_layout(self) -> None:
        layout = QVBoxLayout()
        layout.addLayout(self._table_view_layout)
        self.setLayout(layout)
