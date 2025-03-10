"""
Show metadata for a SMLM dataset.

QWidget plugin for showing metadata
for a single SMLM dataset (locdata.meta).
"""

import logging

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


class ShowMetadataQWidget(QWidget):  # type: ignore
    def __init__(self, napari_viewer: Viewer, smlm_data: SmlmData = smlm_data):
        super().__init__()
        self.viewer = napari_viewer
        self.smlm_data = smlm_data

        self._add_metadata_text()
        self._set_layout()

    def _add_metadata_text(self) -> None:
        self._metadata_text_edit = QPlainTextEdit()
        self.smlm_data.index_changed_signal.connect(self._update_metadata_text)

        self._metadata_layout = QHBoxLayout()
        self._metadata_layout.addWidget(self._metadata_text_edit)
        self.smlm_data.index_changed_signal.emit(self.smlm_data.index)

    def _update_metadata_text(self) -> None:
        if self.smlm_data.index != -1:
            text = str(self.smlm_data.locdata.meta)  # type: ignore
            self._metadata_text_edit.setPlainText(text)
        else:
            self._metadata_text_edit.setPlainText("")

    def _set_layout(self) -> None:
        layout = QVBoxLayout()
        layout.addLayout(self._metadata_layout)
        self.setLayout(layout)
