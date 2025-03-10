"""
Show locdata properties for a SMLM dataset.

QWidget plugin for showing the aggregated properties
for a single SMLM dataset (locdata.properties).
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
from napari_locan.data_model.smlm_data import SmlmData

logger = logging.getLogger(__name__)


class ShowPropertiesQWidget(QWidget):  # type: ignore
    def __init__(self, napari_viewer: Viewer, smlm_data: SmlmData = smlm_data):
        super().__init__()
        self.viewer = napari_viewer
        self.smlm_data = smlm_data

        self._add_properties_text()
        self._set_layout()

    def _add_properties_text(self) -> None:
        self._properties_text_edit = QPlainTextEdit()
        self.smlm_data.index_changed_signal.connect(self._update_properties_text)

        self._properties_layout = QHBoxLayout()
        self._properties_layout.addWidget(self._properties_text_edit)
        self.smlm_data.index_changed_signal.emit(self.smlm_data.index)

    def _update_properties_text(self) -> None:
        if self.smlm_data.index != -1:
            text = pprint.pformat(self.smlm_data.locdata.properties)  # type: ignore
            self._properties_text_edit.setPlainText(text)
        else:
            self._properties_text_edit.setPlainText("")

    def _set_layout(self) -> None:
        layout = QVBoxLayout()
        layout.addLayout(self._properties_layout)
        self.setLayout(layout)
