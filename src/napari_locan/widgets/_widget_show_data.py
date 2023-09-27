"""
QWidget plugin for showing locdata properties
"""
import logging
import pprint

from napari.viewer import Viewer
from qtpy.QtWidgets import (
    QHBoxLayout,
    QPlainTextEdit,
    QVBoxLayout,
    QWidget,
)

from napari_locan import smlm_data
from napari_locan.data_model._locdata import SmlmData

logger = logging.getLogger(__name__)


class ShowDataQWidget(QWidget):  # type: ignore
    def __init__(self, napari_viewer: Viewer, smlm_data: SmlmData = smlm_data):
        super().__init__()
        self.viewer = napari_viewer
        self.smlm_data = smlm_data

        self._add_data_text()
        self._set_layout()

    def _add_data_text(self) -> None:
        # QTableView
        self._data_text_edit = QPlainTextEdit()
        self.smlm_data.index_signal.connect(self._update_data_text)

        self._data_layout = QHBoxLayout()
        self._data_layout.addWidget(self._data_text_edit)
        self.smlm_data.index_signal.emit(self.smlm_data.index)

    def _update_data_text(self) -> None:
        if self.smlm_data.index != -1:
            text = pprint.pformat(self.smlm_data.locdata.data)  # type: ignore
            self._data_text_edit.setPlainText(text)
        else:
            self._data_text_edit.setPlainText("")

    def _set_layout(self) -> None:
        layout = QVBoxLayout()
        layout.addLayout(self._data_layout)
        self.setLayout(layout)
